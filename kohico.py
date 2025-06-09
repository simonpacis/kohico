#!/usr/bin/env python3
import sys
import os
from fuzzywuzzy import fuzz
import re
import json
import base64
import PyPDF2
import hashlib
import random
import string
import pdfminer.pdfparser
import pdfminer.pdfdocument
from lupa import LuaRuntime
from datetime import datetime, timezone
import fitz
import argparse
import subprocess
import time
from thefuzz import fuzz

# This script simply opens the metadata.pdf.lua file, converts it to json and spits it out. Easiest way to convert the lua data structure to json.
encoded_lua_script = 'bG9jYWwgZGtqc29uID0gcmVxdWlyZSAiZGtqc29uIgoKbG9jYWwgc3RhdHVzLCBkYXRhID0gcGNhbGwoZG9maWxlLCBhcmd1bWVudCkKaWYgc3RhdHVzIHRoZW4KCWxvY2FsIGpzb25fc3RyaW5nID0gZGtqc29uLmVuY29kZShkYXRhLCB7IGluZGVudCA9IHRydWUgfSkKCXJldHVybiBqc29uX3N0cmluZwplbmQK'
DEBUG = False

def generate_readest_uid(length=7):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

class Document:
    def __init__(self, title, author):
        self.title = title
        self.author = author

class Annotation:
    def __init__(self, fingerprint, title, vault_path, text, notes, pdf_path, page_number, context, chapter):
        characters = string.ascii_lowercase + string.digits
        self.unique_id = ''.join(random.choice(characters) for _ in range(10))
        self.title = title
        self.notes = notes
        self.text = text
        self.page_number = page_number
        self.chapter = chapter
        self.context = context
        self.data = {
                "text": text,
                "created": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4]+"7Z",
                "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-4]+"7Z",
                "document": {
                    "title": title ,
                    "link": [
                        {"href": "urn:x-pdf:"+fingerprint},
                        {"href": vault_path}
                        ],
                    "documentFingerprint": fingerprint
                    },
                "uri": vault_path,
                "target": [
                    {
                        "source": vault_path,
                        "selector": [
                            {
                                "type": "TextPositionSelector",
                                "start": context['start_pos'],
                                "end": context['end_pos'] 
                                },
                            {
                                "type": "TextQuoteSelector",
                                "exact": notes,
                                "prefix": context['preceding'],
                                "suffix": context['succeeding'] 
                                }
                            ]
                        }
                    ]
                }

    
    def hypothesis_data(self):
        return json.dumps(self.data)

    def nonewlines(self, string):
        return string.replace('\r\n', '').replace('\n', '')

    def get_selection_offsets(self):
        pages = self.context['text_contents']
        text_contents = page_data = next((page for page in pages if page['page'] == self.page_number), None)
        result = find_string(text_contents, self.text)
        if result:
            return {
                'id': result['start_text_content_id'],
                'start': result['start_text_offset'],
                'end_id': result['end_text_content_id'],
                'end': result['end_text_offset']
            }
        else:
            return None


    def pdfplus(self):
        selection = self.get_selection_offsets()
        return_string = f"""> [!PDF|] [[{raw_vault_path}#page={self.page_number}&selection={selection['id']},{selection['start']},{selection['end_id']},{selection['end']}|Hanley2004, p. ({self.page_number})]]
> > {self.text}
> 
> {self.notes}

        """
        return return_string + '\n'

    def hypothesis(self):
        return_string = f"""
>%%
>```annotation-json
>{self.hypothesis_data()}
>```
>%%
>*%%PREFIX%%{self.nonewlines(self.context['preceding'])}%%HIGHLIGHT%% =={self.nonewlines(self.notes)}== %%POSTFIX%%{self.nonewlines(self.context['succeeding'])}*
>%%LINK%%[[#^{self.unique_id}|show annotation]]
>%%COMMENT%%
>{self.nonewlines(self.text)}
>%%TAGS%%
>
^{self.unique_id}"""
        return return_string + '\n'



    def markdown(self, annotation_template, iteration):
        markdown = annotation_template.format(text=self.notes, page_number=self.page_number, highlight=self.text, context=self.context, unique_id=self.unique_id, data=self.data, iteration=iteration, title=self.title, author=document.author, vault_path=vault_path, chapter=self.chapter)
        return markdown


class CFIGenerator:
    def __init__(self, cfi_data, page_count):
        """
        Initialize with the complete CFI data structure

        Args:
            cfi_data: The full document structure with idref, href, and content arrays
        """
        self.cfi_data = cfi_data
        self.page_count = page_count

    def _find_text_node(self, global_pos):
        """Find which text node contains the given global position"""
        idx = bisect_right(self.cumulative_lengths, global_pos) - 1
        if 0 <= idx < len(self.text_nodes):
            return idx, global_pos - self.cumulative_lengths[idx]
        return None, None

    def find_text_position(self, target_text, context_xpath=None):
        """
        Find best fuzzy match of target_text across all text nodes,
        return the exact CFI start and end of the match.
        """

        target_text = normalize_text(target_text)
        if not target_text:
            return None

        target_len = len(target_text)
        best_score = 0
        best_start = None
        best_end = None

        # Build normalized flat text for global search
        flat_text = ''.join(node['text'] for node in self.text_nodes)
        flat_text_norm = normalize_text(flat_text)

        # Sliding window over flat_text to find best fuzzy match
        step = max(1, target_len // 4)
        window_range = range(0, len(flat_text_norm) - target_len + 1, step)

        for i in window_range:
            window = flat_text_norm[i:i + target_len]
            score = fuzz.ratio(target_text, window)
            if score > best_score:
                best_score = score
                best_start = i
                best_end = i + target_len
                if score >= 95:
                    break  # early exit on near-perfect match

        if best_score < 85:
            return None  # reject low-confidence match

        start_idx, offset_start = self._find_text_node(best_start)
        end_idx, offset_end = self._find_text_node(best_end)

        if start_idx is None or end_idx is None:
            return None

        return (
            self.text_nodes[start_idx]['cfi'],
            offset_start,
            self.text_nodes[end_idx]['cfi'],
            offset_end
        )

    def _filter_nodes_by_xpath(self, xpath):
        """
        Filter text nodes based on xpath hint

        Args:
            xpath: The xpath to use as a filter

        Returns:
            List of indices of text nodes that likely match the xpath
        """
        # Extract key components from xpath
        # Example: "/body/DocFragment[10]/body/div/p[6]/text().820"
        pattern = r"/body/DocFragment\[(\d+)\]/body/div/p\[(\d+)\]"
        match = re.search(pattern, xpath)
        if not match:
            return range(len(self.text_nodes))  # Fallback to all nodes

        doc_fragment_num = int(match.group(1))
        paragraph_num = int(match.group(2))

        # In a real implementation, you'd use these to filter nodes
        # For now, we'll return all nodes as we don't have xpath-CFI mapping
        return range(len(self.text_nodes))

    def find_nodes_for_match(self, start, end):
        if DEBUG:
            print(start, end)
        matching_nodes = []
        for spine in self.cfi_data["spines"]:
            for item in spine.get("content", []):
                node_start = item["offset"]
                node_end = node_start + item["length"]
                # Check for overlap between matched text and node
                if (start < node_end) and (end > node_start):
                    matching_nodes.append({
                        "node": item["node"],
                        "cfi": item["cfi"],
                        "href": spine["href"],
                        "offset": item["offset"],
                        "idref": spine["idref"]
                    })
        return matching_nodes

    def generate_cfi_range(self, annotation):
        if DEBUG:
            print(f"Looking for: {annotation['text']}")
        page = annotation['pageno']
        annotation_text = annotation['text']
        text_len = len(annotation_text)
        full_text = self.cfi_data['full_text']  # Move this outside the loop
        text_length = len(full_text)

        # Precompute these once
        page_percentage = (page / self.page_count) * 100
        values = [0.05, 0.15, 0.3, 0.6, 0.9, 1.0]

        match_start = None
        match_end = None

        for percentage in values:
            # Calculate ranges
            start_percentage = max(0, ((page - (self.page_count * percentage)) / self.page_count) * 100)
            end_percentage = min(100, ((page + (self.page_count * percentage)) / self.page_count) * 100)

            # Convert to character offsets
            start_char = int((start_percentage / 100) * text_length)
            end_char = int((end_percentage / 100) * text_length)

            # Extract substring
            extracted_text = full_text[start_char:end_char]

            # Optimized fuzzy search
            best_match_pos = None
            highest_score = 0

            # Slide through the extracted text with a larger step to reduce iterations
            step = max(1, len(annotation_text) // 4)  # Adjust step size as needed
            for i in range(0, len(extracted_text) - text_len + 1, step):
                candidate = extracted_text[i:i + text_len]
                score = fuzz.partial_ratio(annotation_text, candidate)
                if score > highest_score:
                    highest_score = score
                    best_match_pos = i
                    if highest_score > 90:  # Early exit if we find a very good match
                        break

            if highest_score > 80:
                match_start = start_char + best_match_pos
                match_end = match_start + text_len
                break

        if match_start is None:
            # Fallback to full text search if nothing found in ranges
            best_match_pos = None
            highest_score = 0
            for i in range(0, len(full_text) - text_len + 1, text_len // 2):
                candidate = full_text[i:i + text_len]
                score = fuzz.partial_ratio(annotation_text, candidate)
                if score > highest_score:
                    highest_score = score
                    best_match_pos = i
                    if highest_score > 90:
                        break

            if highest_score > 80:
                match_start = best_match_pos + 3
                match_end = match_start + text_len

        if DEBUG:
            print(f"Match start: {match_start}, Match end: {match_end}")

        matching_nodes = self.find_nodes_for_match(match_start, match_end)
        return self.calculate_range(annotation_text, matching_nodes, match_start, match_end)

    def calculate_range(self, annotation_text, matching_nodes, match_start, match_end):
        if not matching_nodes:
            return None

        first_node = matching_nodes[0]
        last_node = matching_nodes[-1]

        # Calculate relative offsets
        start_offset = max(0, match_start - first_node["offset"])
        end_offset = max(0, match_end - last_node["offset"] - 1)

        def parse_cfi_components(cfi):
            """Extracts components from CFI string with precise parsing"""
            if '!' not in cfi:
                return None, None, None, None

            base, path = cfi.split('!', 1)

            # Extract long identifier (up to closing bracket)
            long_id_end = path.find(']')
            if long_id_end == -1:
                return base, None, None, None

            long_id = path[:long_id_end+1]
            remaining_path = path[long_id_end+1:]

            # Extract node and subnode identifiers
            parts = [p for p in remaining_path.split('/') if p]
            if len(parts) < 1:
                return base, long_id, None, None

            node_id = parts[0]
            subnode_id = None

            if len(parts) > 1:
                subnode_part = parts[1].split(':')[0]
                if subnode_part:
                    subnode_id = subnode_part

            return base, long_id, node_id, subnode_id

        # Parse components
        first_base, first_long_id, first_node_id, first_subnode_id = parse_cfi_components(first_node["cfi"])
        last_base, last_long_id, last_node_id, last_subnode_id = parse_cfi_components(last_node["cfi"])

        # Verify we're in the same content
        if first_long_id != last_long_id:
            raise ValueError("Annotation spans multiple content documents")

        # Build position strings
        def build_position(node_id, subnode_id, offset):
            parts = []
            if node_id:
                parts.append(node_id)
            if subnode_id:
                parts.append(subnode_id)
            return f"/{'/'.join(parts)}:{offset}" if parts else f":{offset}"

        start_pos = build_position(first_node_id, first_subnode_id, start_offset)
        end_pos = build_position(last_node_id, last_subnode_id, end_offset)

        return f"epubcfi({first_base}!{first_long_id},{start_pos},{end_pos})"



def get_readest_bookkey(file_path):
    abs_path = os.path.abspath(file_path)

    js_code = f"""
    const {{ createHash }} = require('crypto');
    const fs = require('fs');

    async function partialMD5(filePath) {{
        const step = 1024;
        const size = 1024;
        const hasher = createHash('md5');
        const stats = fs.statSync(filePath);
        const fileSize = stats.size;

        for (let i = -1; i <= 10; i++) {{
            const start = Math.min(fileSize, step << (2 * i));
            const end = Math.min(start + size, fileSize);

            if (start >= fileSize) break;

            const fd = fs.openSync(filePath, 'r');
            const buffer = Buffer.alloc(end - start);
            fs.readSync(fd, buffer, 0, buffer.length, start);
            fs.closeSync(fd);
            
            hasher.update(buffer);
        }}

        return hasher.digest('hex');
    }}

    // Get file path from command line and run
    partialMD5("{abs_path}").then(console.log);
    """


    try:
        result = subprocess.run(
            ["node", "--eval", js_code],
            capture_output=True,
            text=True,
            check=True
        )
        
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Execution failed: {e.stderr or 'No stderr'}")
    except Exception as e:
        raise RuntimeError(f"Execution failed: {e}")

def get_pdfjs_text_content(pdf_path, page_spec=None):
    """
    Extract text from PDF using PDF.js
    
    Args:
        pdf_path: Path to PDF file
        page_spec: None for all pages, 
                   "3" for single page,
                   "1-6" for page range (inclusive)
    """
    abs_path = os.path.abspath(pdf_path)
    escaped_path = json.dumps(abs_path)

    # Parse page specification
    if page_spec is None or page_spec == "":
        page_logic = """
            for (let i = 1; i <= numPages; i++) {
                const page = await doc.getPage(i);
                const content = await page.getTextContent();
                allPagesContent.push({
                    page: i,
                    content: content
                });
            }
        """
    elif "-" in page_spec:
        start, end = map(int, page_spec.split("-"))
        page_logic = f"""
            const startPage = Math.max(1, {start});
            const endPage = Math.min(numPages, {end});
            for (let i = startPage; i <= endPage; i++) {{
                const page = await doc.getPage(i);
                const content = await page.getTextContent();
                allPagesContent.push({{
                    page: i,
                    content: content
                }});
            }}
        """
    else:  # Single page
        page_num = int(page_spec)
        page_logic = f"""
            const pageNum = Math.min(numPages, Math.max(1, {page_num}));
            const page = await doc.getPage(pageNum);
            const content = await page.getTextContent();
            allPagesContent.push({{
                page: pageNum,
                content: content
            }});
        """

    js_code = f"""
    import {{ readFileSync }} from 'fs';
    import {{ JSDOM }} from 'jsdom';
    import * as pdfjsLib from 'pdfjs-dist/legacy/build/pdf.mjs';
    import {{ fileURLToPath }} from 'url';
    import path from 'path';

    // Store the original stdout write function
    const originalStdoutWrite = process.stdout.write;
    const originalStderrWrite = process.stderr.write;

    // Temporarily suppress all output
    process.stdout.write = function() {{}};
    process.stderr.write = function() {{}};

    const dom = new JSDOM('<!DOCTYPE html>', {{
        runScripts: "dangerously",
        resources: "usable"
    }});

    globalThis.window = dom.window;
    globalThis.document = dom.window.document;
    globalThis.DOMMatrix = dom.window.DOMMatrix;
    globalThis.DOMParser = dom.window.DOMParser;

    const workerPath = path.resolve(
        path.dirname(fileURLToPath(import.meta.url)),
        'node_modules/pdfjs-dist/legacy/build/pdf.worker.mjs'
    );
    pdfjsLib.GlobalWorkerOptions.workerSrc = new URL('file://' + workerPath).href;

    async function extractPages() {{
        try {{
            const data = new Uint8Array(readFileSync({escaped_path}));
            pdfjsLib.GlobalWorkerOptions.standardFontDataUrl = new URL(
              'file://' + path.resolve(
                path.dirname(fileURLToPath(import.meta.url)),
                'node_modules/pdfjs-dist/standard_fonts/'
              )
            ).href;
            
            const doc = await pdfjsLib.getDocument({{ data }}).promise;
            const numPages = doc.numPages;
            const allPagesContent = [];
            
            {page_logic}
            
            // Restore stdout just for our JSON output
            process.stdout.write = originalStdoutWrite;
            process.stdout.write(JSON.stringify(allPagesContent));
        }} catch (err) {{
            // Restore stderr for error output
            process.stderr.write = originalStderrWrite;
            process.stderr.write("PDF.js Error: " + err.stack);
            process.exit(1);
        }}
    }}

    extractPages().catch(e => {{
        process.stderr.write = originalStderrWrite;
        process.stderr.write("Unhandled Error: " + e.stack);
        process.exit(1);
    }});
    """

    try:
        result = subprocess.run(
            ["node", "--input-type=module", "--eval", js_code],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Extract JSON from stdout
        json_match = re.search(r'\[.*\]', result.stdout, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
        else:
            raise RuntimeError("No JSON found in output")
            
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Execution failed: {e.stderr or 'No stderr'}")
    except json.JSONDecodeError:
        print("Raw stdout:", result.stdout)  # For debugging
        raise RuntimeError("Invalid JSON returned from PDF.js")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {str(e)}")

def remove_whitespace(text):
    return re.sub(r'\s+', '', text)

def get_page_offset(reader, page_index):
    if page_index >= len(reader.pages):
        raise ValueError('Invalid page index')

    offset = 0
    for i in range(page_index):
        page_text = reader.pages[i].extract_text()
        offset += len(page_text)

    return offset

def calculate_page_offsets(pdf_path):
    global page_offsets
    page_offsets = [0]  # Initialize with 0 for the first page

    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        cumulative_length = 0

        for page in reader.pages:
            text = page.extract_text()
            cumulative_length += len(text)
            page_offsets.append(cumulative_length)

def find_closest_match(haystack, needle):
    needle_length = len(needle)
    best_match = None
    best_score = 0
    best_index = -1

    for i in range(len(haystack) - needle_length + 1):
        segment = haystack[i:i + needle_length]
        score = fuzz.ratio(segment, needle)

        if score > best_score:
            best_score = score
            best_match = segment
            best_index = i

    return best_match, best_index

def find_context(pdf_path, page_number, search_string, pdfjs_text_content):
    if not page_offsets:
        calculate_page_offsets(pdf_path)

    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)

        # Ensure page number is within range
        if page_number < 1 or page_number > len(reader.pages):
            raise ValueError("Page number out of range")

        page = reader.pages[page_number - 1]
        original_text = page.extract_text()

        # Find the closest match in the text of the specified page
        _, match_index = find_closest_match(original_text, search_string)

        # Calculate global start and end positions in the entire document
        page_start_offset = page_offsets[page_number - 1]
        global_start_pos = page_start_offset + match_index
        global_end_pos = page_start_offset + match_index + len(search_string)

        # Calculate local start and end positions for preceding and succeeding text on the page
        local_start_pos = max(0, match_index - 31)
        local_end_pos = min(len(original_text), match_index + len(search_string) + 31)

        # Extract preceding and succeeding text
        preceding_text = original_text[local_start_pos:match_index]
        succeeding_text = original_text[match_index + len(search_string):local_end_pos]

        if pdfjs_text_content:
            text_contents = get_pdfjs_text_content(pdf_path)
        else:
            text_contents = []

        return {
                "preceding": preceding_text,
                "succeeding": succeeding_text,
                "start_pos": global_start_pos,
                "end_pos": global_end_pos,
                "text_contents": text_contents
                }

def find_string(text_contents, target_string):
    items = text_contents['content']['items']
    full_text = ''.join(item['str'] for item in items)
    
    # Fuzzy-match to find the best substring (variable length)
    best_match = None
    best_ratio = 0
    target_norm = target_string.lower()
    
    # Search with a sliding window (±25% of target length)
    min_len = max(1, int(len(target_string) * 0.75))
    max_len = int(len(target_string) * 1.25)
    
    for window_len in range(min_len, max_len + 1):
        for i in range(len(full_text) - window_len + 1):
            window = full_text[i:i + window_len]
            ratio = fuzz.ratio(target_norm, window.lower())
            if ratio > best_ratio:
                best_ratio = ratio
                best_match = (i, i + window_len)  # (start_global, end_global)
    
    if not best_match or best_ratio < 70:  # Threshold adjustable
        return None
    
    start_global, end_global = best_match
    
    # Map global positions to item indices and relative offsets
    start_item_idx, start_offset = None, None
    end_item_idx, end_offset = None, None
    current_pos = 0
    
    for idx, item in enumerate(items):
        item_start = current_pos
        item_end = current_pos + len(item['str'])
        
        # Check if match starts in this item
        if start_item_idx is None and item_start <= start_global < item_end:
            start_item_idx = idx
            start_offset = start_global - item_start  # Relative to item start
        
        # Check if match ends in this item
        if end_item_idx is None and item_start < end_global <= item_end:
            end_item_idx = idx
            end_offset = end_global - item_start  # Relative to item end
        
        current_pos = item_end
    
    return {
        'start_text_content_id': start_item_idx,  # Index of the starting item
        'start_text_offset': start_offset,         # Offset within starting item
        'end_text_content_id': end_item_idx,      # Index of the ending item
        'end_text_offset': end_offset             # Offset within ending item
    }

def lua_to_json(file_type):
    print('Converting metadata to JSON.')
    lua_script = base64.b64decode(encoded_lua_script).decode('utf-8')
    lua = LuaRuntime(unpack_returned_tuples=True)
    if needs_context == False:
        lua.globals().argument = file_path 
    else:
        if file_type == "pdf":
            sdr_directory = file_path.replace('.pdf', '', 1) + '.sdr'
            lua_path = os.path.dirname(file_path) + '/' + os.path.basename(sdr_directory) + '/metadata.pdf.lua'
        elif file_type == "epub":
            sdr_directory = file_path.replace('.epub', '', 1) + '.sdr'
            lua_path = os.path.dirname(file_path) + '/' + os.path.basename(sdr_directory) + '/metadata.epub.lua'
        lua.globals().argument = lua_path 
    return json.loads(lua.execute(lua_script))

def process_annotations(json_data):
    global annotations, document, page_offsets, fingerprint, needs_context
    print('Processing annotations.')
    # Process annotations
    if 'author' not in json_data['doc_props'] and 'authors' not in json_data['doc_props']:
        author = 'Unknown'
    elif 'author' in json_data['doc_props']:
        author = json_data['doc_props']['author']
    elif 'authors' in json_data['doc_props']:
        author = json_data['doc_props']['authors']
    document = Document(json_data['doc_props']['title'], author)
    if "bookmarks" in json_data:
        for bookmark in json_data["bookmarks"]:
            page_no = bookmark.get("page", 1)
            text = bookmark.get("text", "")
            notes = bookmark.get("notes", "No notes available")
            title = json_data['doc_props']['title']
            if needs_context:
                context = find_context(file_path, page_no, notes, True)
            else:
                context = {"preceding": 'na', 'succeeding': 'na', 'start_pos': 'na', 'end_pos': 'na'}
            annotations.append(Annotation(fingerprint, title, vault_path, text, notes, file_path, page_no, context))
    if "annotations" in json_data:
        for bookmark in json_data["annotations"]:
            page_no = bookmark.get("page", 1)
            text = bookmark.get("text", "")
            notes = bookmark.get("note", " ")
            chapter = bookmark.get("chapter", " ")
            title = json_data['doc_props']['title']
            if needs_context:
                context = find_context(file_path, page_no, notes, True)
            else:
                context = {"preceding": 'na', 'succeeding': 'na', 'start_pos': 'na', 'end_pos': 'na'}
            annotations.append(Annotation(fingerprint, title, vault_path, text, notes, file_path, page_no, context, chapter))

def is_cfi_in_booknotes(book_json_data, target_cfi):
    """Check if a CFI exists in the booknotes."""
    return any(annotation.get("cfi") == target_cfi 
              for annotation in book_json_data.get("booknotes", []))

def get_annotation_by_cfi(book_json_data, target_cfi):
    """Return the annotation matching the CFI, or None if not found."""
    return next(
        (annotation for annotation in book_json_data.get("booknotes", []) 
         if annotation.get("cfi") == target_cfi),
        None
    )


def convert_annotations_obsidian_annotator():
    global annotations
    print('Converting annotations (obsidian-annotator).')
    final_output = f"annotation-target::[[{vault_path.replace('vault:/', '', 1)}]]\n"
    for annotation in annotations:
        final_output = final_output + annotation.hypothesis()
    final_output = final_output + '\n'
    output_file_name = file_path.replace('.pdf', '', 1) + '_obs-anno.md'
    with open(output_file_name, 'w') as file:
        file.write(final_output)
    print(f"Annotation file saved as {output_file_name}.")
    return True

def convert_annotations_readest(json_data):
    global file_path, file_hash
    print('Converting annotations (readest).')
    cfi_job = subprocess.run(['epub-cfi-generator', file_path, 'output.json'], capture_output=True)
    cfi_data = json.loads(cfi_job.stdout.decode('utf-8'))

    annotations = json_data['annotations']
    generator = CFIGenerator(cfi_data, json_data['stats']['pages'])

    # TODO: Make this multi-platform. macOS only atm.
    readest_dir = os.path.expanduser("~/Library/Application Support/com.bilingify.readest/Readest/Books")
    readest_lib = os.path.join(readest_dir, "library.json")

    book_dir = os.path.join(readest_dir, file_hash)
    book_json = os.path.join(book_dir, "config.json")
    ps_aux = subprocess.run(['ps', 'aux'], capture_output=True)

    if "/Applications/Readest.app" in ps_aux.stdout.decode('utf-8'):
        quit_readest = ""
        while quit_readest.lower() != "y" and quit_readest.lower() != "n":
            quit_readest = input("Writing to Readest-files must be done with Readest closed, otherwise, any changes are overwritten when the app is later closed. Quit Readest? (y/n) ")

        if quit_readest.lower() == "y":
            app_name = "Readest"  # Exact name as seen in the Dock
            script = f'tell application "{app_name}" to quit'
            subprocess.run(["osascript", "-e", script])

    if not os.path.exists(book_dir):
        os.makedirs(book_dir)
    if not os.path.exists(book_json):
        initial_book_json = {"viewSettings":{},"searchConfig":{},"updatedAt":int(time.time())}
        with open(book_json, 'w') as f:
            f.write(json.dumps(initial_book_json))

    with open(readest_lib, 'r') as f:
        readest_lib_data = json.load(f)

    in_library = False
    for book in readest_lib_data:
        if book['hash'] == file_hash:
            in_library = True
            break

    if not in_library:
        readest_lib_data.append({"hash": file_hash, "format": "EPUB", "title": json_data['doc_props']['title'], "author": json_data['doc_props']['author'], "primaryLanguage": "en", "createdAt": int(time.time()), "uploadedAt": None, "deletedAt": int(time.time()), "downloadedAt": int(time.time()), "updatedAt": int(time.time()), "filePath": file_path})

        with open(readest_lib, 'w') as f:
            f.write(json.dumps(readest_lib_data))


    with open(book_json, 'r') as f:
        book_json_data = json.load(f)

    book_json_data['booknotes'] = []


    for annotation in annotations:
        cfi = generator.generate_cfi_range(annotation)


        if is_cfi_in_booknotes(book_json_data, cfi):
            existing_annotation = get_annotation_by_cfi(book_json_data, target_cfi)
            existing_annotation['text'] = annotation['text']
            existing_annotation['note'] = annotation.get('note', '')
            existing_annotation['updatedAt'] = int(time.time())
        else:
            book_json_data['booknotes'].append(
                    {"id": generate_readest_uid(),
                     "type": "annotation",
                     "cfi": cfi,
                     "style": "highlight",
                     "color": "yellow",
                     "text": annotation['text'],
                     "note": annotation.get('note', ''),
                     "createdAt": int(time.time()),
                     "updatedAt": int(time.time())
                    }
                    )

    with open(book_json, 'w') as f:
        f.write(json.dumps(book_json_data))


    print("Readest done.")
    return True

def convert_annotations_pdf_plus():
    global annotations
    print('Converting annotations (pdfplus).')

    # Generate new annotations markdown
    new_output = ""
    new_selections = set()
    for annotation in annotations:
        new_output += annotation.pdfplus()
        # Extract selection number (the part after "selection=" and before "|")
        start = new_output.find("selection=") + len("selection=")
        end = new_output.find("|", start)
        selection = new_output[start:end]
        new_selections.add(selection)

    output_file_name = file_path.replace('.pdf', '', 1) + ' annotations.md'

    # Check if file exists and read existing content
    existing_content = ""
    existing_selections = set()

    try:
        with open(output_file_name, 'r') as file:
            existing_content = file.read()

            # Find all existing selections in the file
            import re
            existing_selections = set(re.findall(r"selection=([^\|]+)", existing_content))
    except FileNotFoundError:
        pass  # File doesn't exist yet, we'll create it

    # Find which new annotations aren't already in the file
    unique_new_annotations = []
    current_annotations = annotations.copy()
    annotations.clear()  # Clear to rebuild with only new ones

    for i, annotation in enumerate(current_annotations):
        # Get the selection for this annotation
        temp_md = annotation.pdfplus()
        start = temp_md.find("selection=") + len("selection=")
        end = temp_md.find("|", start)
        selection = temp_md[start:end]

        if selection not in existing_selections:
            unique_new_annotations.append(temp_md)
            annotations.append(annotation)  # Add back to global annotations if it's new

    # Combine existing content with new unique annotations
    if unique_new_annotations:
        final_output = existing_content
        if final_output and not final_output.endswith('\n\n'):
            final_output += '\n\n'
        final_output += '\n\n'.join(unique_new_annotations)

        with open(output_file_name, 'w') as file:
            file.write(final_output)
        print(f"Annotation file updated with {len(unique_new_annotations)} new annotations. Total file: {output_file_name}.")
    else:
        print("No new annotations to add. File remains unchanged.")

    return True

def default_markdown_template():
    return_string = """# {title} annotations
{author}
{filename}
%annotation
---
> [!quote] &nbsp;
> =={highlight}== (p. {page_number})

> [!note] &nbsp;
> {text}
"""
    return return_string

def default_epub_markdown_template():
    return_string = """# {title} annotations
{author}
{filename}
%annotation
---
> [!quote] &nbsp;
> =={highlight}== (chp. {chapter})

> [!note] &nbsp;
> {text}
"""
    return return_string

def convert_annotations_markdown():
    global annotations, document
    print('Converting annotations (markdown).')
    sorted_annotations = sorted(annotations, key=lambda x: x.page_number)

    if args.template is None:
        if file_type() == 'epub':
            template = default_epub_markdown_template()
        else:
            template = default_markdown_template()
    else:
        with open(args.template, 'r') as file:
            template = file.read()

    template_parts = template.split('%annotation')

    if len(template_parts) < 2:
        print('A Markdown template must include a line containing just "%annotation". Everything before this line will be the global template, everything after will be repeated for each annotation. Exiting.')
        sys.exit(0)

    global_template = template_parts[0]

    markdown_output = global_template.format(filename=os.path.basename(file_path), title=document.title, author=document.author)

    annotation_template = template_parts[1]

    for iteration, annotation in enumerate(sorted_annotations):
        markdown_output = markdown_output + annotation.markdown(annotation_template, (iteration+1))
    markdown_output = markdown_output + '\n'
    last_slash_index = file_path.rfind('/')
    if file_type() == "pdf":
        output_file_name = file_path.replace('.pdf', '', 1) + '_anno.md'
    elif file_type() == "epub":
        output_file_name = file_path.replace('.epub', '', 1) + ' annotations.md'
    with open(output_file_name, 'w') as file:
        file.write(markdown_output)
    print(f"Annotation file saved as {output_file_name}.")
    return True

def convert_annotations_bake(pdf_path):
    print('Converting annotations (bake).')
    doc = fitz.open(pdf_path)
    for annotation in annotations:
        page = doc[annotation.page_number - 1]
        text_instances = page.search_for(annotation.notes)

        if text_instances:
            # Add highlight for each instance
            for inst in text_instances:
                highlight = page.add_highlight_annot(inst)

            # Calculate note position to be in the right margin but aligned with the first highlight
            first_instance = text_instances[0]
            y_position = first_instance[1]  # Y-coordinate of the first highlight's top edge
            x_position = page.rect.width - 60  # Assuming the note should be 60 units from the right edge
            note_position = (x_position, y_position)

            # Add one clickable note in the right margin for the highlight
            note = page.add_text_annot(note_position, annotation.text, icon="Comment")
            note.set_info(content=annotation.text, title="kohico")
            note.update()
    new_pdf_path = args.file_path.replace('.pdf', '_anno.pdf')
    doc.save(new_pdf_path)
    print(f"Annotated PDF saved as {new_pdf_path}.")


def hexify(byte_string):
    return byte_string.hex()


def hash_of_first_kilobyte(path):
    with open(path, 'rb') as f:
        h = hashlib.md5()
        h.update(f.read(1024))
        return h.hexdigest()


def file_id_from(path):
    """
    Return the PDF file identifier from the given file as a hex string.

    Returns None if the document doesn't contain a file identifier.

    """
    try:
        with open(path, 'rb') as f:
            parser = pdfminer.pdfparser.PDFParser(f)
            document = pdfminer.pdfdocument.PDFDocument(parser)

            for xref in document.xrefs:
                if xref.trailer:
                    trailer = xref.trailer

                    try:
                        id_array = trailer["ID"]
                    except KeyError:
                        continue

                    # Resolve indirect object references.
                    try:
                        id_array = id_array.resolve()
                    except AttributeError:
                        pass

                    try:
                        file_id = id_array[0]
                    except TypeError:
                        continue

                    return hexify(file_id)
    except FileNotFoundError:
        print('PDF not found. Abort.')
        sys.exit(0)


def get_fingerprint(path):
    print('Fingerprinting.')
    return file_id_from(path) or hash_of_first_kilobyte(path)

def find_relative_path_to_pdf(absolute_pdf_path):
    # Split the path into parts
    path_parts = absolute_pdf_path.split(os.sep)

    for i in range(len(path_parts) - 1, 0, -1):
        # Reconstruct the path up to the current part
        current_path = os.sep.join(path_parts[:i])

        # Check if the '.obsidian' or '.obsidian.nosync' directory exists in the current path
        if os.path.exists(os.path.join(current_path, '.obsidian')) or os.path.exists(os.path.join(current_path, '.obsidian.nosync')):
            # Return the relative path from the next directory after this one to the PDF
            return os.sep.join(path_parts[i:])

    return None

def parse_choices(choice_str = 'obs,md'):
    choices = choice_str.split(',')
    valid_choices = ['obsidian-annotator', 'obs', 'bake', 'markdown', 'md', 'pdfplus', 'pdf++', 'readest']
    for choice in choices:
        if choice not in valid_choices:
            raise argparse.ArgumentTypeError(f"{choice} is not a valid choice.")
    return choices

def file_type():
    global file_path
    if file_path[-7:] == 'pdf.lua':
        return 'pdf'
    elif file_path[-3:] == 'pdf':
        return 'pdf'
    elif file_path[-8:] == 'epub.lua':
        return 'epub'
    elif file_path[-4:] == 'epub':
        return 'epub'
    else:
        return 'pdf'

page_offsets = None
annotations = None
needs_context = None
file_path = None
vault_path = None
raw_vault_path = None
fingerprint = None
file_hash = None
args = None
document = None

def main():
    global page_offsets, annotations, needs_context, file_path, vault_path, fingerprint, raw_vault_path, file_hash, args
    parser = argparse.ArgumentParser(description="Convert KOReader highlights, either by baking them into the PDF, converting for use with the Annotator plugin for Obsidian, or exporting to Markdown.")
    parser.add_argument("file_path", help="Path to the PDF file. You can also give the path directly to a metadata.pdf.lua file, in which case not all output formats will be available.")
    parser.add_argument("output_format", type=parse_choices, nargs='?', default='obsidian-annotator',
                        help="Comma-separated types of output format(s) ('obsidian-annotator'/'obs' for Obsidian Annotator, 'bake' for baking into the PDF, 'markdown'/'md' for markdown output.). Default is 'obsidian-annotator,markdown'.")
    parser.add_argument('--template', type=str, help='Path to an optional Markdown template file.', default=None)
    args = parser.parse_args()
    print('Initiating.')

    file_path = args.file_path
    needs_context = True 

    if file_path[-3:] == 'lua':
        print("You have passed the metadata file directly instead of a PDF or epub. The only available output formats are: 'markdown'/'md'.")
        if not all(item in ['md', 'markdown'] for item in args.output_format):
            print('One of the selected conversion types is not available. Exiting.')
            sys.exit(0)
        needs_context = False


    raw_vault_path = find_relative_path_to_pdf(file_path)
    vault_path = 'vault:/' + find_relative_path_to_pdf(file_path)
    page_offsets = []
    annotations = []

    if 'obs' in args.output_format or 'obsidian-annotator' in args.output_format:
        fingerprint = get_fingerprint(file_path)
    else:
        fingerprint = 'na'
        
    if 'readest' in args.output_format:
        file_hash = get_readest_bookkey(file_path)

    json_data = lua_to_json(file_type())
    if file_type() == "epub":
        needs_context = False
    process_annotations(json_data)

    conversion_types = args.output_format

    for conversion_type in conversion_types:
        if conversion_type == 'obsidian-annotator' or conversion_type == 'obs':
            convert_annotations_obsidian_annotator()
        elif conversion_type == 'bake':
            convert_annotations_bake(file_path)
        elif conversion_type == 'pdfplus' or conversion_type == 'pdf++':
            convert_annotations_pdf_plus()
        elif conversion_type == 'markdown' or conversion_type == 'md':
            convert_annotations_markdown()
        elif conversion_type == 'readest':
            convert_annotations_readest(json_data)

    print('All done.')


if __name__ == "__main__":
    main()





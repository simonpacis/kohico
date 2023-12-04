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

# This script converts KOReader highlights into Hypothes.is annotations for use with the Obsidian plugin obsidian-annotator by elias-sundqvist.
# First, find the PDF in your KOReader-directory. Next to it there will be a directory called "PDFNAME.sdr". In it will be a file called "metadata.pdf.lua". Move this file next to the *same* PDF, but located somewhere in your Obsidian vault. This script needs access to the PDF to succesfully convert the highlights into annotations.
# The script will now generate a file called "PDFNAME_anno.md" next to the PDF. Open this in Obsidian with obsidian-annotator installed, click the three dots in top-right corner and click "Annotate". 
# Watch as the highlights you made on your Kindle are now in Obsidian.
#
# Hope it works for you.
#
#
# Important installation note: You need lua installed with the dkjson-package. And then install pip packages for all the imports you see up top.


# This script simply opens the metadata.pdf.lua file, converts it to json and spits it out. Easiest way to convert the lua data structure to json.
encoded_lua_script = 'bG9jYWwgZGtqc29uID0gcmVxdWlyZSAiZGtqc29uIgoKbG9jYWwgc3RhdHVzLCBkYXRhID0gcGNhbGwoZG9maWxlLCBhcmd1bWVudCkKaWYgc3RhdHVzIHRoZW4KCWxvY2FsIGpzb25fc3RyaW5nID0gZGtqc29uLmVuY29kZShkYXRhLCB7IGluZGVudCA9IHRydWUgfSkKCXJldHVybiBqc29uX3N0cmluZwplbmQK'

class Text:
    def __init__(self, text, highlight):
        self.highlight = highlight
        self.text = text

    def print(self):
        return f"**Highlight**: =={self.highlight}==\n**Notes**: {self.text}\n"

class Annotation:
    def __init__(self, fingerprint, title, vault_path, text, notes, pdf_path, page_number, context):
        characters = string.ascii_lowercase + string.digits
        self.unique_id = ''.join(random.choice(characters) for _ in range(10))
        self.notes = notes
        self.text = text
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

    def json(self):
        return json.dumps(self.data)

    def nonewlines(self, string):
        return string.replace('\r\n', '').replace('\n', '')

    def markdown(self):
        return_string = f"""
>%%
>```annotation-json
>{self.json()}
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

def find_context(pdf_path, page_number, search_string):
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

        return {
                "preceding": preceding_text,
                "succeeding": succeeding_text,
                "start_pos": global_start_pos,
                "end_pos": global_end_pos
                }

def format_annotations_as_markdown(json_data):
    global annotations
    used_texts = []
    markdown_output = ["# Annotations and Highlights\n"]

    # Process "highlight" annotations
    if "bookmarks" in json_data:
        for bookmark in json_data["bookmarks"]:
            page_no = bookmark.get("page", 1)
            text = bookmark.get("text", "")
            notes = bookmark.get("notes", "No notes available")
            title = json_data['doc_props']['title']
            context = find_context(file_path, page_no, notes)
            annotations.append(Annotation(fingerprint, title, vault_path, text, notes, file_path, page_no, context))
#    if "highlight" in json_data:
#        for page, highlights in json_data["highlight"].items():
#            markdown_output.append(f"## Page {page}\n")
#            for highlight in highlights:
#                text = highlight.get("text", "No text available")
#                text_class = next((p for p in used_texts if p.highlight == text), None)
#                if text_class is not None:
#                    markdown_output.append(text_class.print())

    return True


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


def fingerprint(path):
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

# Check if at least one argument is provided
if len(sys.argv) > 1:
    file_path = sys.argv[1]
else:
    print("No filename provided. First argument should be absolute path to the pdf-file in your Obsidian vault.")
    sys.exit(0)

raw_vault_path = find_relative_path_to_pdf(file_path)
vault_path = 'vault:/' + find_relative_path_to_pdf(file_path)

fingerprint = fingerprint(file_path)

page_offsets = []
annotations = []

lua_script = base64.b64decode(encoded_lua_script).decode('utf-8')
lua = LuaRuntime(unpack_returned_tuples=True)
lua.globals().argument = os.path.dirname(file_path) + '/metadata.pdf.lua' 
json_data = json.loads(lua.execute(lua_script))

markdown_output = format_annotations_as_markdown(json_data)
final_output = f"annotation-target::[[{vault_path.replace('vault:/', '', 1)}]]\n"
for annotation in annotations:
    final_output = final_output + annotation.markdown()
final_output = final_output + '\n'
last_slash_index = file_path.rfind('/')
output_file_name = file_path.replace('.pdf', '', 1) + '_anno.md'
with open(output_file_name, 'w') as file:
    file.write(final_output)
print('All done.')

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

# This script simply opens the metadata.pdf.lua file, converts it to json and spits it out. Easiest way to convert the lua data structure to json.
encoded_lua_script = 'bG9jYWwgZGtqc29uID0gcmVxdWlyZSAiZGtqc29uIgoKbG9jYWwgc3RhdHVzLCBkYXRhID0gcGNhbGwoZG9maWxlLCBhcmd1bWVudCkKaWYgc3RhdHVzIHRoZW4KCWxvY2FsIGpzb25fc3RyaW5nID0gZGtqc29uLmVuY29kZShkYXRhLCB7IGluZGVudCA9IHRydWUgfSkKCXJldHVybiBqc29uX3N0cmluZwplbmQK'

class Annotation:
    def __init__(self, fingerprint, title, vault_path, text, notes, pdf_path, page_number, context):
        characters = string.ascii_lowercase + string.digits
        self.unique_id = ''.join(random.choice(characters) for _ in range(10))
        self.notes = notes
        self.text = text
        self.page_number = page_number
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

    def default_markdown_template(self):
        return_string = """
---
Page {page_number}
=={highlight}==

{text}
"""
        return return_string

    def markdown(self, iteration):
        if args.template is None:
            template = self.default_markdown_template()
        else:
            with open(args.template, 'r') as file:
                template = file.read()
        return template.format(text=self.text, page_number=self.page_number, highlight=self.notes, context=self.context, unique_id=self.unique_id, data=self.data, iteration=iteration)

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

def lua_to_json():
    print('Converting metadata to JSON.')
    lua_script = base64.b64decode(encoded_lua_script).decode('utf-8')
    lua = LuaRuntime(unpack_returned_tuples=True)
    if needs_context == False:
        lua.globals().argument = file_path 
    else:
        lua.globals().argument = os.path.dirname(file_path) + '/metadata.pdf.lua' 
    return json.loads(lua.execute(lua_script))

def process_annotations(json_data, needs_context):
    global annotations
    print('Processing annotations.')
    # Process annotations
    if "bookmarks" in json_data:
        for bookmark in json_data["bookmarks"]:
            page_no = bookmark.get("page", 1)
            text = bookmark.get("text", "")
            notes = bookmark.get("notes", "No notes available")
            title = json_data['doc_props']['title']
            if needs_context:
                context = find_context(file_path, page_no, notes)
            else:
                context = {"preceding": 'na', 'succeeding': 'na', 'start_pos': 'na', 'end_pos': 'na'}
            annotations.append(Annotation(fingerprint, title, vault_path, text, notes, file_path, page_no, context))

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

def convert_annotations_markdown():
    global annotations
    print('Converting annotations (markdown).')
    markdown_output = "# Annotations and Highlights\nDocument: " + os.path.basename(file_path) + '\n'
    sorted_annotations = sorted(annotations, key=lambda x: x.page_number)
    for iteration, annotation in enumerate(sorted_annotations):
        markdown_output = markdown_output + annotation.markdown((iteration+1))
    markdown_output = markdown_output + '\n'
    last_slash_index = file_path.rfind('/')
    output_file_name = file_path.replace('.pdf', '', 1) + '_anno.md'
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


def fingerprint(path):
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
    valid_choices = ['obsidian-annotator', 'obs', 'bake', 'markdown', 'md']
    for choice in choices:
        if choice not in valid_choices:
            raise argparse.ArgumentTypeError(f"{choice} is not a valid choice.")
    return choices

parser = argparse.ArgumentParser(description="Convert KOReader highlights, either by baking them into the PDF, converting for use with the Annotator plugin for Obsidian, or exporting to Markdown.")
parser.add_argument("file_path", help="Path to the PDF file. You can also give the path directly to a metadata.pdf.lua file, in which case not all conversion types will be available.")
parser.add_argument("output_format", type=parse_choices, nargs='?', default='obsidian-annotator',
                    help="Comma-separated types of output format(s) ('obsidian-annotator'/'obs' for Obsidian Annotator, 'bake' for baking into the PDF, 'markdown'/'md' for markdown output.). Default is 'obsidian-annotator,markdown'.")
parser.add_argument('--template', type=str, help='Path to an optional Markdown template file.', default=None)
args = parser.parse_args()
print('Initiating.')

file_path = args.file_path
needs_context = True 

if file_path[-3:] == 'lua':
    print("You have passed the metadata file directly instead of a PDF. The only available conversion options are: 'markdown'/'md'.")
    if not all(item in ['md', 'markdown'] for item in args.output_format):
        print('One of the selected conversion types is not available. Exiting.')
        sys.exit(0)
    needs_context = False


raw_vault_path = find_relative_path_to_pdf(file_path)
vault_path = 'vault:/' + find_relative_path_to_pdf(file_path)
page_offsets = []
annotations = []

if 'obs' in args.output_format or 'obsidian-annotator' in args.output_format:
    fingerprint = fingerprint(file_path)
else:
    fingerprint = 'na'

json_data = lua_to_json()
process_annotations(json_data, needs_context)

conversion_types = args.output_format

for conversion_type in conversion_types:
    if conversion_type == 'obsidian-annotator' or conversion_type == 'obs':
        convert_annotations_obsidian_annotator()
    elif conversion_type == 'bake':
        convert_annotations_bake(file_path)
    elif conversion_type == 'markdown' or conversion_type == 'md':
        convert_annotations_markdown()

print('All done.')

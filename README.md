# kohico (KOReader Highlights Converter)
Convert PDF KOReader Highlights, so that the highlights and annotations can be used in different software.

Supported formats:
- Markdown
- [obsidian-annotator](https://github.com/elias-sundqvist/obsidian-annotator)
- baked in (embedded directly in PDF file)

Feel free to request other formats!

## Prerequisites

Before running this script, ensure you have the following prerequisites installed:

1. **Lua**: The script requires Lua with the `dkjson` package (install using [luarocks](https://luarocks.org)).
   ```bash
   luarocks install dkjson
   ```
2. **Python Dependencies**: Install all the Python packages mentioned in the script. You can use pip to install these packages:
   ```bash
   pip3 install -r requirements.txt
   ```

### For specific output formats
There are certain output formats which require more exotic installations.

#### Pdf++
This converts the KOReader annotations for .pdf-files, for use with the Obsidian plugin [PDF++](https://github.com/RyotaUshio/obsidian-pdf-plus).

Requirements for this output format include:
- [node](https://nodejs.org)

##### Setting up
To use this output format, you must first go to the `kohico/nodescripts` directory and run `npm install`.

#### Readest
Currently only supported on macOS.

This converts the KOReader annotations for .epub-files, for use in [Readest](https://readest.com).

Requirements for this output format include:
- [node](https://nodejs.org)

This output format does not currently work on Linux or Windows.

##### Setting up
To use this output format, you must first go to the `kohico/nodescripts/epub-cfi-generator` directory and run `npm install`.


## Usage

```bash
usage: python3 kohico.py [-h] [--template TEMPLATE] file_path [output_format]

Convert KOReader highlights, either by baking them into the PDF, converting for use with the Annotator plugin for Obsidian, or exporting to Markdown.

positional arguments:
  file_path            Path to the PDF file. You can also give the path directly to a metadata.pdf.lua file, in which case not all conversion types will be available.
  output_format        Comma-separated types of output format(s) ('obsidian-annotator'/'obs' for Obsidian Annotator, 'bake' for baking into the PDF, 'markdown'/'md' for markdown output.). Default is 'obsidian-annotator,markdown'.

options:
  -h, --help           show this help message and exit
  --template TEMPLATE  Path to an optional Markdown template file.
```

1. **Locate Your PDF**: Find the PDF in your KOReader directory. You should see a directory named `<PDFNAME>.sdr` next to it.

2. **Move Metadata File**: Move the `metadata.pdf.lua` file from the `.sdr` directory to the same location as the corresponding PDF (if converting for obsidian-annotator, the PDF must also be in your Obsidian vault).

3. **Run the Script**: Execute the script, passing the path to the PDF (or alternatively the metadata.pdf.lua file, in which case only `markdown` is available as output format), and your desired output as the second (You can do multiple outputs by separating with commas). It will generate a file named `<PDFNAME>_anno.md`, `<PDFNAME>_obs-anno.md` or `<PDFNAME>_anno.pdf` next to the original PDF.

5. **View Your Highlights**: Your kohiconverted highlights can now be viewed.

## Markdown Template?
Understanding that not everyone wants their outputted Markdown annotations to be formatted like me, it is possible to change it using a template.

There are two parts to a template, a `global` part, and an `annotation` part. The `global` part will only be outputted once, at the beginning of the resulting Markdown-document. The `annotation` part will be repeated for each annotation. They are separated by `%annotation`.

Here's how to do it:

1. Create a markdown file, you could call it `template.md`.
2. Populate it how you wish, separating the `global` part from the `annotation` part by a line containing `%annotation`. Wrap available variables in curly brackets (`{}`), as such (the following is the default template):

```markdown
# {title} annotations
File: {filename}
%annotation
---
Page {page_number}
=={highlight}==

{text}
```

3. Pass the template file along to kohico using `--template <PATH_TO_TEMPLATE_FILE>`. Remember, this only works with conversion type `markdown` (or `md`).

### Available variables
The following variables are available for use in the template:

#### Global
- **filename**: The file name.
- **title**: The title of the PDF document.
- **author**: The author of the PDF document.

#### Annotation
- **highlight**: The actual highlit text.
- **text**: Any written comment to the highlight.
- **page_number**: The page on which the highlight is found.
- **unique_id**: A unique ID (meant for use by obsidian-annotator) if you need it.
- **iteration**: Starting from 1, it represents the index of the current annotation.
- **title**: The title of the PDF document.

## How it Works
The script acceses the highlights metadata from KOReader, and converts it to JSON. It then iterates through every highlight, goes into the PDF and finds the highlight there, so that it can extract the surrounding textual content.

It then outputs these processed highlights and annotations into your desired format. 


## Important Notes

- The script needs access to both the PDF and the Lua metadata file to successfully convert the highlights.
- Ensure that the Lua environment and all Python dependencies are correctly installed before running the script.

## Feedback and Contributions

Feel free to open an issue for any bugs or feature requests, or submit a pull request if you've made improvements to the script.

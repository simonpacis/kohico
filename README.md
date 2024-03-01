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
   pip3 install fuzzywuzzy PyPDF2 pdfminer lupa PyMuPDF
   ```
   Note: You might need additional dependencies depending on your system setup. Run the script and see what it says.

## Usage

```bash
python3 kohico.py [-h] [--template MARKDOWN_TEMPLATE_FILE] file_path conversion_types

positional arguments:
  file_path            Path to the PDF file
  conversion_type      Comma-separated types of conversion ('obsidian-annotator'/'obs' for Obsidian Annotator, 'bake' for baking into the PDF, 'markdown'/'md' for markdown output.). Default is 'obsidian-annotator'

options:
  -h, --help           show this help message and exit
  --template MARKDOWN_TEMPLATE_FILE Path to an optional Markdown template file

```


1. **Locate Your PDF**: Find the PDF in your KOReader directory. You should see a directory named `<PDFNAME>.sdr` next to it.

2. **Move Metadata File**: Move the `metadata.pdf.lua` file from the `.sdr` directory to the same location as the corresponding PDF (if converting for obsidian-annotator, the PDF must be in your Obsidian vault).

3. **Run the Script**: Execute the script (`python3 kohico.py [...]`), passing the path to the PDF, and your desired output as the second (`obsidian-annotator` or `obs` for obsidian-annotator, `bake` for baked in, `markdown` or `md` for export to Markdown.). It will generate a file named `<PDFNAME>_anno.md`, `<PDFNAME>_obs-anno.md` or `<PDFNAME>_anno.pdf` next to the original PDF.

5. **View Your Highlights**: Your kohiconverted highlights can now be viewed.

## Markdown Template?
Understanding that not everyone wants their outputted Markdown annotations to be formatted like me, it is possible to change it using a template. Here's how:

1. Create a markdown file, you could call it `template.md`.
2. Populate it how you wish, wrapping available variables in curly brackets (`{}`), as such:

```markdown
## Annotation no. {iteration}
Page number: {page_number}
Highlighted text: {highlight}
```

3. Pass the template file along to kohico using `--template <PATH_TO_TEMPLATE_FILE>`. Remember, this only works with conversion type `markdown` (or `md`).

### Available variables
The following variables are available for use in the template:

- **highlight**: The actual highlit text.
- **text**: Any written comment to the highlight.
- **page_number**: The page on which the highlight is found.
- **unique_id**: A unique ID (meant for use by obsidian-annotator) if you need it.
- **iteration**: Starting from 1, it represents the index of the current annotation.

## How it Works
The script acceses the highlights metadata from KOReader, and converts it to JSON. It then iterates through every highlight, goes into the PDF and finds the highlight there, so that it can extract the surrounding textual content.

It then outputs these processed highlights and annotations into your desired format. 


## Important Notes

- The script needs access to both the PDF and the Lua metadata file to successfully convert the highlights.
- Ensure that the Lua environment and all Python dependencies are correctly installed before running the script.

## Feedback and Contributions

Feel free to open an issue for any bugs or feature requests, or submit a pull request if you've made improvements to the script.

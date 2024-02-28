# kohico (KOReader Highlights Converter)
Convert PDF KOReader Highlights, so that the highlights and annotations can be used in different software.

Supported formats:
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

1. **Locate Your PDF**: Find the PDF in your KOReader directory. You should see a directory named `<PDFNAME>.sdr` next to it.

2. **Move Metadata File**: Move the `metadata.pdf.lua` file from the `.sdr` directory to the same location as the corresponding PDF (if converting for obsidian-annotator, the PDF must be in your Obsidian vault).

3. **Run the Script**: Execute the script (`python3 kohico.py [...]`), passing the path to the PDF, and your desired output as the second (`obsidian-annotator` or `obs` for obsidian-annotator, `bake` for baked in). It will generate a file named `<PDFNAME>_anno.md` or `<PDFNAME>_anno.pdf` next to the original PDF.

5. **View Your Highlights**: Your KOReader highlights can now be viewed.

## How it Works
The script acceses the highlights metadata from KOReader, and converts it to JSON. It then iterates through every highlight, goes into the PDF and finds the highlight there, so that it can extract the surrounding textual content.

It then outputs these processed highlights and annotations into your desired format. 


## Important Notes

- The script needs access to both the PDF and the Lua metadata file to successfully convert the highlights.
- Ensure that the Lua environment and all Python dependencies are correctly installed before running the script.

## Feedback and Contributions

Feel free to open an issue for any bugs or feature requests, or submit a pull request if you've made improvements to the script.

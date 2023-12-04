# ko2hyp
Convert KOReader Highlights to Obsidian Annotations

This Python script is designed to convert KOReader highlights into Hypothes.is annotations, which can be used with the Obsidian plugin [obsidian-annotator](https://github.com/elias-sundqvist/obsidian-annotator).

## How it Works
```TL;DR```  
Script converts KOReader highlights into Obsidian Annotator (which is [hypothes.is](https://web.hypothes.is) in Obsidian) annotations.

The script acceses the highlights-metadata from KOReader, and converts it to JSON. It then iterates through every highlight, goes into the PDF and finds the highlight there, so that it can extract the surrounding textual content. This is done because the hypothes.is client needs it to succesfully locate where it should render the highlight.

It then generates a Markdown-file which corresponds to the format used by obsidian-annotator to store annotations.

## Prerequisites

Before running this script, ensure you have the following prerequisites installed:

1. **Lua**: The script requires Lua with the `dkjson` package.
2. **Python Dependencies**: Install all the Python packages mentioned in the script. You can use pip to install these packages:
   ```bash
   pip3 install fuzzywuzzy PyPDF2 pdfminer lupa
   ```
   Note: You might need additional dependencies depending on your system setup. Run the script and see what it says.

## Usage

1. **Locate Your PDF**: Find the PDF in your KOReader directory. You should see a directory named `<PDFNAME>.sdr` next to it.

2. **Move Metadata File**: Move the `metadata.pdf.lua` file from the `.sdr` directory to the same location as the corresponding PDF in your Obsidian vault.

3. **Run the Script**: Execute the script, passing the absolute path to the PDF in your Obsidian vault as the only system argument. It will generate a file named `<PDFNAME>_anno.md` next to the PDF.

4. **Annotate in Obsidian**: Open the generated markdown file in Obsidian (with obsidian-annotator installed). Click the three dots in the top-right corner and select "Annotate".

5. **View Your Highlights**: Your KOReader highlights should now appear as annotations in Obsidian.

## Important Notes

- The script needs access to both the PDF and the Lua metadata file to successfully convert the highlights.
- Ensure that the Lua environment and all Python dependencies are correctly installed before running the script.

## Feedback and Contributions

Feel free to open an issue for any bugs or feature requests, or submit a pull request if you've made improvements to the script.

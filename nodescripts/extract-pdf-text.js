import { readFileSync } from 'fs';
import { JSDOM } from 'jsdom';
import * as pdfjsLib from 'pdfjs-dist/legacy/build/pdf.mjs';
import { fileURLToPath } from 'url';
import path from 'path';

// Store the original stdout write function
const originalStdoutWrite = process.stdout.write;
const originalStderrWrite = process.stderr.write;

// Temporarily suppress all output
process.stderr.write = function() {};
process.stdout.write = function() {};

const dom = new JSDOM('<!DOCTYPE html>', {
		runScripts: "dangerously",
		resources: "usable"
});

globalThis.window = dom.window;
globalThis.document = dom.window.document;
globalThis.DOMMatrix = dom.window.DOMMatrix;
globalThis.DOMParser = dom.window.DOMParser;

const workerPath = path.resolve(
		path.dirname(fileURLToPath(import.meta.url)),
		'node_modules/pdfjs-dist/legacy/build/pdf.worker.mjs'
);
pdfjsLib.GlobalWorkerOptions.workerSrc = new URL('file://' + workerPath).href;


// Parse CLI args
const [,, pdfPath, pageSpec] = process.argv;
if (!pdfPath) {
  console.error('Usage: node extract-pdf-text.js <pdfPath> [pageSpec]');
  process.exit(1);
}

async function extractTextFromPdf(pathToPdf, pageSpec) {
  const data = new Uint8Array(readFileSync(pathToPdf));
  const doc = await pdfjsLib.getDocument({ data }).promise;
  const numPages = doc.numPages;
  const allPagesContent = [];

  let startPage = 1;
  let endPage = numPages;

  if (pageSpec && /^\d+$/.test(pageSpec)) {
    startPage = endPage = Math.max(1, Math.min(numPages, parseInt(pageSpec)));
  } else if (pageSpec && /^\d+-\d+$/.test(pageSpec)) {
    const [start, end] = pageSpec.split("-").map(x => parseInt(x));
    startPage = Math.max(1, start);
    endPage = Math.min(numPages, end);
  }

  for (let i = startPage; i <= endPage; i++) {
    const page = await doc.getPage(i);
    const content = await page.getTextContent();
    allPagesContent.push({ page: i, content });
  }

  return allPagesContent;
}

extractTextFromPdf(pdfPath, pageSpec)
  .then(content => {
		// Restore the original stdout write function
		process.stdout.write = originalStdoutWrite;
    console.log(JSON.stringify(content));
  })
  .catch(err => {
    console.error("Error extracting PDF text:", err.stack || err);
    process.exit(1);
  });


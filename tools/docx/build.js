// Build a Word document from the AST written by tools/docx/parse.py.
//
// Usage: node tools/docx/build.js
//
// Every document-specific value comes from the AST, which carries the
// tools/docx/documents.json entry that parse.py was run for. Run parse.py with
// the same document key first.
const fs = require('fs');
const docx = require('docx');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, TableOfContents, HeadingLevel,
  BorderStyle, WidthType, ShadingType, VerticalAlign, PageNumber,
  PageBreak, LevelFormat, ExternalHyperlink,
} = docx;

const path = require('path');
const REPO = path.resolve(__dirname, '..', '..');
const ast = JSON.parse(fs.readFileSync(path.join(REPO, 'ast.json'), 'utf8'));
const DOC = ast.doc;
const OUT = path.join(REPO, DOC.output);

const TITLE = DOC.title;
const VERSION = DOC.version;
const USABLE = 9360;           // US Letter minus 1in margins
const BODY = 22;               // 11pt
const MONO = 17;               // 8.5pt
const INK = '000000';
const MUTED = '4A4A4A';
const RULE = 'B0B0B0';
const HEADFILL = 'EAEFF0';
const CODEFILL = 'F4F3EF';

const thin = { style: BorderStyle.SINGLE, size: 1, color: RULE };
const allBorders = { top: thin, bottom: thin, left: thin, right: thin };
const noBorders = {
  top: { style: BorderStyle.NONE }, bottom: { style: BorderStyle.NONE },
  left: { style: BorderStyle.NONE }, right: { style: BorderStyle.NONE },
};

// ---- inline runs -----------------------------------------------------------
function runs(rs, opts = {}) {
  return rs.map((r) => new TextRun({
    text: r.t,
    bold: !!r.b || !!opts.bold,
    italics: !!r.i,
    font: r.c ? 'Consolas' : 'Arial',
    size: r.c ? Math.round((opts.size || BODY) * 0.95) : (opts.size || BODY),
    color: opts.color || INK,
  }));
}

// ---- column widths --------------------------------------------------------
function widths(ncol, rows) {
  const PAD = 240;        // cell margins, left + right
  const CHAR = 122;       // DXA per character at 10pt Arial, deliberately generous
  const len = [];
  const need = [];        // width required so no single word is broken mid-word
  for (let c = 0; c < ncol; c++) {
    let longest = 0;
    let longestWord = 0;
    rows.forEach((r) => {
      const txt = r[c].map((x) => x.t).join('');
      longest = Math.max(longest, txt.length);
      // Word only breaks a line at whitespace or after a hyphen. It will not
      // break at a dot or a slash, so identifiers and paths count in full.
      txt.split(/\s+/).forEach((w) => {
        w.split(/(?<=-)/).forEach((seg) => {
          longestWord = Math.max(longestWord, seg.length);
        });
      });
    });
    len.push(Math.max(longest, 6));
    need.push(PAD + longestWord * CHAR);
  }
  const minNeed = need.reduce((a, b) => a + b, 0);
  let w;
  if (minNeed >= USABLE) {
    // Cannot honour every minimum; share proportionally to the requirement.
    w = need.map((n) => Math.round((USABLE * n) / minNeed));
  } else {
    const spare = USABLE - minNeed;
    const total = len.reduce((a, b) => a + b, 0);
    w = need.map((n, ix) => n + Math.round((spare * len[ix]) / total));
  }
  // Correct rounding drift so the sum matches the table width exactly.
  w[ncol - 1] += USABLE - w.reduce((a, b) => a + b, 0);
  return w;
}

function buildTable(b) {
  const cw = widths(b.ncol, b.rows);
  const rows = b.rows.map((cells, ri) => new TableRow({
    tableHeader: ri === 0,
    cantSplit: true,
    children: cells.map((cell, ci) => new TableCell({
      borders: allBorders,
      width: { size: cw[ci], type: WidthType.DXA },
      shading: ri === 0 ? { fill: HEADFILL, type: ShadingType.CLEAR } : undefined,
      margins: { top: 70, bottom: 70, left: 110, right: 110 },
      verticalAlign: VerticalAlign.TOP,
      children: [new Paragraph({
        spacing: { before: 0, after: 0, line: 260 },
        children: runs(cell, { bold: ri === 0, size: 20 }),
      })],
    })),
  }));
  return new Table({
    width: { size: USABLE, type: WidthType.DXA },
    columnWidths: cw,
    rows,
  });
}

// ---- block rendering ------------------------------------------------------
const HL = [null, HeadingLevel.HEADING_1, HeadingLevel.HEADING_2,
  HeadingLevel.HEADING_3, HeadingLevel.HEADING_4];

// Each ordered list gets its own numbering instance, so a new numbered list
// restarts at 1 instead of continuing the previous list's count.
let orderedInstance = 0;

function render(blocks) {
  const out = [];
  blocks.forEach((b, bx) => {
    if (b.k === 'li' && b.ord) {
      const prev = blocks[bx - 1];
      if (!prev || prev.k !== 'li' || !prev.ord) orderedInstance += 1;
    }
    if (b.k === 'h') {
      out.push(new Paragraph({
        heading: HL[b.level],
        keepNext: true,
        children: runs(b.runs, { size: b.level === 1 ? 30 : b.level === 2 ? 25 : 23, bold: true }),
      }));
    } else if (b.k === 'p') {
      out.push(new Paragraph({
        spacing: { before: 0, after: 160, line: 300 },
        children: runs(b.runs),
      }));
    } else if (b.k === 'li') {
      out.push(new Paragraph({
        numbering: b.ord
          ? { reference: 'steps', level: 0, instance: orderedInstance }
          : { reference: 'bullets', level: 0 },
        spacing: { before: 0, after: 120, line: 300 },
        children: runs(b.runs),
      }));
    } else if (b.k === 'table') {
      out.push(buildTable(b));
      out.push(new Paragraph({ spacing: { before: 0, after: 200 }, children: [new TextRun('')] }));
    } else if (b.k === 'code') {
      b.lines.forEach((ln, ix) => out.push(new Paragraph({
        keepLines: true,
        keepNext: ix < b.lines.length - 1,
        shading: { fill: CODEFILL, type: ShadingType.CLEAR },
        indent: { left: 200, right: 200 },
        spacing: { before: ix === 0 ? 60 : 0, after: ix === b.lines.length - 1 ? 60 : 0, line: 240 },
        children: [new TextRun({ text: ln || ' ', font: 'Consolas', size: MONO, color: INK })],
      })));
      if (b.wrapped) {
        out.push(new Paragraph({
          spacing: { before: 80, after: 200 },
          children: [new TextRun({
            text: 'Note: one line in the example above is wrapped to fit the page width. '
              + 'In the source file it is a single line.',
            italics: true, font: 'Arial', size: 19, color: MUTED,
          })],
        }));
      } else {
        out.push(new Paragraph({ spacing: { before: 0, after: 200 }, children: [new TextRun('')] }));
      }
    }
  });
  return out;
}

// ---- front matter ---------------------------------------------------------
function statusRow(label, value) {
  return new TableRow({
    cantSplit: true,
    children: [label, value].map((txt, ci) => new TableCell({
      borders: allBorders,
      width: { size: ci === 0 ? 2600 : 6760, type: WidthType.DXA },
      shading: ci === 0 ? { fill: HEADFILL, type: ShadingType.CLEAR } : undefined,
      margins: { top: 80, bottom: 80, left: 110, right: 110 },
      verticalAlign: VerticalAlign.TOP,
      children: [new Paragraph({
        spacing: { before: 0, after: 0, line: 270 },
        children: [new TextRun({ text: txt, bold: ci === 0, font: 'Arial', size: 20 })],
      })],
    })),
  });
}

const statusTable = new Table({
  width: { size: USABLE, type: WidthType.DXA },
  columnWidths: [2600, 6760],
  rows: [
    new TableRow({ // header row
      tableHeader: true,
      cantSplit: true,
      children: ['Field', 'Value'].map((txt, ci) => new TableCell({
        borders: allBorders,
        width: { size: ci === 0 ? 2600 : 6760, type: WidthType.DXA },
        shading: { fill: HEADFILL, type: ShadingType.CLEAR },
        margins: { top: 80, bottom: 80, left: 110, right: 110 },
        children: [new Paragraph({
          spacing: { before: 0, after: 0 },
          children: [new TextRun({ text: txt, bold: true, font: 'Arial', size: 20 })],
        })],
      })),
    }),
    ...ast.status.map(([label, value]) => statusRow(label, value)),
  ],
});

const title = [
  new Paragraph({
    spacing: { before: 1200, after: 60 },
    children: [new TextRun({ text: TITLE, bold: true, font: 'Arial', size: 56, color: INK })],
  }),
  new Paragraph({
    spacing: { before: 0, after: 240 },
    children: [new TextRun({
      text: `Version ${VERSION}`, font: 'Arial', size: 30, color: MUTED,
    })],
  }),
  new Paragraph({
    spacing: { before: 0, after: 480 },
    border: { top: { style: BorderStyle.SINGLE, size: 6, color: '01696F', space: 8 } },
    children: [new TextRun({
      text: DOC.subtitle,
      font: 'Arial', size: 24, color: INK,
    })],
  }),
  new Paragraph({
    heading: HeadingLevel.HEADING_1,
    keepNext: true,
    children: [new TextRun({ text: DOC.abstractHeading, bold: true, font: 'Arial', size: 30 })],
  }),
  ...render(ast.intro),
  new Paragraph({
    heading: HeadingLevel.HEADING_1,
    keepNext: true,
    children: [new TextRun({ text: 'Document status', bold: true, font: 'Arial', size: 30 })],
  }),
  new Paragraph({
    spacing: { before: 0, after: 160, line: 300 },
    children: [new TextRun({
      text: 'This document is generated from the project Markdown sources named below. '
        + 'Where this document and those sources disagree, the Markdown sources are '
        + 'authoritative and the disagreement is a defect in this document.',
      font: 'Arial', size: BODY,
    })],
  }),
  statusTable,
  new Paragraph({ children: [new PageBreak()] }),
  new Paragraph({
    heading: HeadingLevel.HEADING_1,
    keepNext: true,
    children: [new TextRun({ text: 'Contents', bold: true, font: 'Arial', size: 30 })],
  }),
  new Paragraph({
    spacing: { before: 0, after: 200 },
    children: [new TextRun({
      text: 'This list is generated from the document headings. Word populates it when the '
        + 'document is opened; press F9 to refresh it after editing.',
      italics: true, font: 'Arial', size: 19, color: MUTED,
    })],
  }),
  new TableOfContents('Contents', { hyperlink: true, headingStyleRange: '1-3' }),
  new Paragraph({ children: [new PageBreak()] }),
];

// The annex is optional: a document with no annex entry renders nothing here.
const annexHead = DOC.annex ? [
  new Paragraph({
    pageBreakBefore: true,
    heading: HeadingLevel.HEADING_1,
    keepNext: true,
    children: [new TextRun({
      text: DOC.annex.heading, bold: true, font: 'Arial', size: 30,
    })],
  }),
  new Paragraph({
    spacing: { before: 0, after: 160, line: 300 },
    children: [new TextRun({
      text: DOC.annex.intro,
      font: 'Arial', size: BODY,
    })],
  }),
] : [];

// ---- document -------------------------------------------------------------
const heading = (id, name, size, before, after, outline) => ({
  id, name, basedOn: 'Normal', next: 'Normal', quickFormat: true,
  run: { size, bold: true, font: 'Arial', color: INK },
  paragraph: { spacing: { before, after }, outlineLevel: outline, keepNext: true },
});

const doc = new Document({
  title: `${TITLE} ${VERSION}`,
  description: DOC.description,
  creator: 'Bob Dodd — Accessible by Design',
  subject: DOC.subject,
  keywords: DOC.keywords,
  styles: {
    default: {
      document: { run: { font: 'Arial', size: BODY, color: INK, language: { value: 'en-GB' } } },
      hyperlink: { run: { color: '0C4E54', underline: {} } },
    },
    paragraphStyles: [
      heading('Heading1', 'Heading 1', 30, 400, 160, 0),
      heading('Heading2', 'Heading 2', 25, 300, 130, 1),
      heading('Heading3', 'Heading 3', 23, 260, 120, 2),
      heading('Heading4', 'Heading 4', 22, 240, 110, 3),
    ],
  },
  numbering: {
    config: [
      {
        reference: 'bullets',
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: '\u2022',
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 620, hanging: 300 } } },
        }],
      },
      {
        reference: 'steps',
        levels: [{
          level: 0, format: LevelFormat.DECIMAL, text: '%1.',
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 620, hanging: 300 } } },
        }],
      },
    ],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
      },
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [new TextRun({
            text: `${TITLE} ${VERSION} — ${DOC.headerSuffix}`,
            font: 'Arial', size: 17, color: MUTED,
          })],
        })],
      }),
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: 'Page ', font: 'Arial', size: 18, color: MUTED }),
            new TextRun({ children: [PageNumber.CURRENT], font: 'Arial', size: 18, color: MUTED }),
            new TextRun({ text: ' of ', font: 'Arial', size: 18, color: MUTED }),
            new TextRun({ children: [PageNumber.TOTAL_PAGES], font: 'Arial', size: 18, color: MUTED }),
          ],
        })],
      }),
    },
    children: [...title, ...render(ast.body), ...annexHead, ...render(ast.annex)],
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT, buf);
  console.log('written', buf.length, 'bytes');
});

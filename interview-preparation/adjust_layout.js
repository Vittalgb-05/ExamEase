const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const htmlPath = path.join(__dirname, 'guide_template.html');
let html = fs.readFileSync(htmlPath, 'utf8');

// Replace CSS styles with an ultra-compact print stylesheet where each of the 8 pages fits exactly on 1 printed page.
const printStyles = `
  @page {
    size: A4 portrait;
    margin: 8mm 9mm 8mm 9mm;
  }

  *, *::before, *::after {
    box-sizing: border-box;
  }

  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    color: #1e293b;
    background: #ffffff;
    font-size: 7.2pt;
    line-height: 1.25;
    margin: 0;
    padding: 0;
  }

  .page {
    page-break-after: always;
    break-after: page;
    height: 279mm;
    max-height: 279mm;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding-bottom: 1mm;
  }

  .page-header {
    border-bottom: 1.5px solid #2563eb;
    padding-bottom: 2px;
    margin-bottom: 4px;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
  }
  .page-header .doc-title {
    font-size: 10pt;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.02em;
  }
  .page-header .doc-title span { color: #2563eb; }
  .page-header .page-topic {
    font-size: 6.8pt;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }

  .page-footer {
    border-top: 1px solid #e2e8f0;
    padding-top: 2px;
    margin-top: 3px;
    display: flex;
    justify-content: space-between;
    font-size: 6.5pt;
    color: #94a3b8;
  }

  h1 { font-size: 12pt; font-weight: 800; color: #0f172a; margin: 0 0 3px 0; line-height: 1.15; }
  h2 { font-size: 8.8pt; font-weight: 700; color: #1e3a8a; margin: 4px 0 2px 0; border-bottom: 1px solid #e2e8f0; padding-bottom: 1px; }
  h3 { font-size: 7.8pt; font-weight: 700; color: #0f172a; margin: 3px 0 1px 0; }
  p { margin: 0 0 2.5px 0; }
  ul, ol { margin: 0 0 2.5px 0; padding-left: 13px; }
  li { margin-bottom: 1px; }

  .hero-banner {
    background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
    color: white;
    padding: 6px 10px;
    border-radius: 5px;
    margin-bottom: 4px;
  }
  .hero-banner h1 { color: white; margin-bottom: 1px; }
  .hero-banner .tagline { font-size: 7.8pt; opacity: 0.9; margin: 0; }
  .hero-banner .meta { font-size: 6.8pt; opacity: 0.8; margin-top: 2px; }

  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 5px; margin-bottom: 3px; }
  .grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 4px; margin-bottom: 3px; }

  .metric-card {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 4px;
    padding: 3px 6px;
    text-align: center;
  }
  .metric-val { font-size: 11pt; font-weight: 800; color: #2563eb; }
  .metric-lbl { font-size: 6.5pt; color: #64748b; font-weight: 600; text-transform: uppercase; }

  .callout {
    background: #f8fafc;
    border-left: 2.5px solid #3b82f6;
    padding: 3px 6px;
    border-radius: 0 4px 4px 0;
    margin: 2.5px 0;
    font-size: 7pt;
  }
  .callout-success { border-left-color: #10b981; background: #f0fdf4; }
  .callout-warning { border-left-color: #f59e0b; background: #fffbeb; }
  .callout-danger { border-left-color: #ef4444; background: #fef2f2; }
  .callout-title { font-weight: 700; color: #0f172a; margin-bottom: 1.5px; font-size: 7.4pt; }

  table { width: 100%; border-collapse: collapse; margin: 2.5px 0; font-size: 6.7pt; }
  th, td { border: 1px solid #cbd5e1; padding: 2px 4px; text-align: left; vertical-align: top; }
  th { background: #f1f5f9; font-weight: 700; color: #1e293b; }
  tr:nth-child(even) td { background: #f8fafc; }

  .diagram-box {
    background: #0f172a;
    color: #e2e8f0;
    padding: 4px 7px;
    border-radius: 4px;
    font-family: "Consolas", "Courier New", monospace;
    font-size: 6.4pt;
    line-height: 1.18;
    white-space: pre;
    margin: 2px 0;
    overflow-x: hidden;
  }

  code {
    font-family: "Consolas", monospace;
    background: #e2e8f0;
    padding: 0.5px 2.5px;
    border-radius: 2px;
    font-size: 6.8pt;
    color: #0f172a;
  }

  .badge {
    display: inline-block;
    padding: 0.5px 3.5px;
    border-radius: 2px;
    font-size: 6.4pt;
    font-weight: 700;
  }
  .badge-blue { background: #dbeafe; color: #1e40af; }
  .badge-green { background: #dcfce7; color: #166534; }
  .badge-amber { background: #fef3c7; color: #92400e; }

  .qa-block { margin-bottom: 3.5px; }
  .qa-q { font-weight: 700; color: #1e3a8a; font-size: 7.4pt; margin-bottom: 1px; }
  .qa-a { color: #334155; font-size: 7.1pt; margin-bottom: 1.5px; }
  .qa-followup { font-size: 6.6pt; color: #64748b; font-style: italic; background: #f1f5f9; padding: 1.5px 4px; border-radius: 2px; }
`;

html = html.replace(/<style>[\s\S]*?<\/style>/, '<style>' + printStyles + '</style>');
fs.writeFileSync(htmlPath, html, 'utf8');
console.log('guide_template.html successfully updated with compact single-page layout.');

# CMA Part 2 Practice Exam Simulator

Interactive practice exam simulator for **CMA (Certified Management Accountant) Part 2 – Strategic Financial Management**.

## 🚀 Quick Start

### 1. Generate the question bank from your PDF

```bash
pip install pypdf poppler-utils   # or: sudo apt install poppler-utils
python3 parse_pdf.py your_cma_pdf.pdf
```

This creates `questions.json` with all parsed questions.

### 2. Open in browser

Just open `index.html` in any browser. No server needed locally.

### 3. Host on GitHub Pages

1. Push this repo to GitHub
2. Go to **Settings → Pages → Source: main branch / root**
3. Your exam is live at `https://yourusername.github.io/repo-name`

> **Note:** `questions.json` must be committed to the repo alongside `index.html`.

---

## 📁 Files

| File | Description |
|------|-------------|
| `index.html` | The full interactive exam app |
| `parse_pdf.py` | PDF → JSON parser script |
| `questions.json` | Generated question bank (run parser first) |

---

## ✨ Features

- **Exam Mode** – Timed, no feedback until you submit. Mirrors real CMA conditions.
- **Practice Mode** – Instant answer feedback with detailed explanations.
- **Official CMA Timing** – 4-hour countdown for 100 questions, scales proportionally.
- **10 Mock Tests** – Select individual tests or mix all questions.
- **Question Navigator** – Visual grid showing answered/flagged/correct/wrong status.
- **Flag & Review** – Mark questions to revisit before submitting.
- **Retry Wrong** – After finishing, instantly retry only the questions you got wrong.
- **Full Keyboard Support** – A/B/C/D to select, ←→ to navigate, F to flag, Enter to submit.
- **Score Report** – Detailed breakdown with pass/fail indicator (≥72% = CMA passing threshold).

---

## 📊 CMA Part 2 Coverage

Questions cover all major Part 2 topics:
- Financial Statement Analysis
- Corporate Finance (Capital Structure, Cost of Capital)
- Capital Budgeting & Investment Decisions
- Risk Management & ERM
- Working Capital Management
- Ethics (IMA Standards)
- Decision Analysis (CVP, Make vs Buy, Pricing)
- International Finance

---

## 🔧 Troubleshooting

**"questions.json not found"** – Run `parse_pdf.py` with your PDF file path.

**Parsing issues** – The parser works best with text-based PDFs. Scanned PDFs may need OCR preprocessing.

**PDF tools missing** – Install `poppler-utils`:
- Ubuntu/Debian: `sudo apt install poppler-utils`
- macOS: `brew install poppler`
- Windows: Download from https://github.com/oschwartz10612/poppler-windows

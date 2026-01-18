# Receipt Parser

Parse grocery receipts from plain text or PDFs, map line items to canonical items,
and generate monthly summaries and reports.

## Quick start

1) Create the environment:

```sh
conda env create -f ica-env.yaml
conda activate ica
```

2) Configure inputs in `config.yaml`.

3) Run:

```sh
python ICA.py
```

## Inputs

- `receipts_<month>.txt`: plain text pasted receipt data for each month.
- `items.csv`: canonical items, aliases, and family allocation.
- `adjustments.txt` (optional): manual corrections.

## Configuration (`config.yaml`)

Key options:

- `month`: set to a month like `dec` or to `all` to run all `receipts_*.txt`.
- `text_file`: default input if `month` is not set.
- `out`: detailed CSV output (default `sammanfattning.csv`).
- `report`: categorized summary (default `kategoriserad.txt`).
- `report_text`: formatted Swedish report (default `kategoriserad_rapport.txt`).
- `report_xlsx`: formatted Swedish XLSX report (default `kategoriserad_rapport.xlsx`).

When `month` is set, outputs are written to `./<month>/` and suffixed
with `_<month>` (e.g., `kategoriserad_rapport_dec.txt`).

## Outputs

- `sammanfattning*.csv`: detailed per-line rows.
- `kategoriserad*.txt`: categorized summary (tab-separated).
- `kategoriserad_rapport*.txt`: formatted Swedish report (derived from categorized).
- `kategoriserad_rapport*.xlsx`: formatted spreadsheet (requires `openpyxl`).
- `familj_sammanfattning*.txt`: family allocation summary.

## Combine all months into one report

After generating month outputs, you can produce a combined report:

```sh
python kategoriserad_rapport_alla.py
```

This writes `kategoriserad_rapport_alla.txt` and, if `openpyxl` is installed,
`kategoriserad_rapport_alla.xlsx`.

## Notes

- PDFs require `pdfplumber`; OCR requires `pytesseract`, `pdf2image`, and `poppler`.
- XLSX output requires `openpyxl`.

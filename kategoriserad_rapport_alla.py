#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import pandas as pd  # type: ignore

from ICA import (
    OPENPYXL_AVAILABLE,
    build_swedish_report_df,
    read_categorized_report,
    write_categorized_text_report,
    write_categorized_xlsx_report,
)


def find_categorized_files(root: Path) -> list[Path]:
    files = sorted(root.glob("*/kategoriserad_*.txt"))
    return [p for p in files if "_rapport_" not in p.name]


def combine_categorized(files: list[Path]) -> pd.DataFrame:
    dfs = [read_categorized_report(str(path)) for path in files]
    if not dfs:
        return pd.DataFrame()
    df = pd.concat(dfs, ignore_index=True)

    for col in ["canonical", "qty", "total_price_sek", "family_alloc_sek", "personal_alloc_sek"]:
        if col not in df.columns:
            df[col] = "" if col == "canonical" else 0.0

    for col in ["qty", "total_price_sek", "family_alloc_sek", "personal_alloc_sek"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0.0)

    grouped = (
        df.groupby("canonical", as_index=False)
        .agg(
            qty=("qty", "sum"),
            total_price_sek=("total_price_sek", "sum"),
            family_alloc_sek=("family_alloc_sek", "sum"),
            personal_alloc_sek=("personal_alloc_sek", "sum"),
        )
    )

    grouped["avg_unit_price_sek"] = grouped.apply(
        lambda r: (r["total_price_sek"] / r["qty"]) if r["qty"] else 0.0,
        axis=1,
    )
    grouped["effective_family_pct"] = grouped.apply(
        lambda r: (r["family_alloc_sek"] / r["total_price_sek"]) if r["total_price_sek"] else 0.0,
        axis=1,
    )

    grouped = grouped[
        [
            "canonical",
            "qty",
            "avg_unit_price_sek",
            "total_price_sek",
            "family_alloc_sek",
            "personal_alloc_sek",
            "effective_family_pct",
        ]
    ]
    grouped.sort_values("family_alloc_sek", ascending=False, inplace=True, ignore_index=True)
    return grouped


def main() -> None:
    files = find_categorized_files(Path("."))
    if not files:
        raise SystemExit("No kategoriserad_*.txt files found under month folders.")

    combined = combine_categorized(files)
    report_df = build_swedish_report_df(combined)

    out_txt = Path("kategoriserad_rapport_alla.txt")
    write_categorized_text_report(report_df, str(out_txt))
    print(f"Wrote {out_txt}")

    if OPENPYXL_AVAILABLE:
        out_xlsx = Path("kategoriserad_rapport_alla.xlsx")
        write_categorized_xlsx_report(report_df, str(out_xlsx))
        print(f"Wrote {out_xlsx}")
    else:
        print("[INFO] Skipped XLSX report (openpyxl not installed).")


if __name__ == "__main__":
    main()

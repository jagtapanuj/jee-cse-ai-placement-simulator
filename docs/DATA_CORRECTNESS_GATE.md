# Data Correctness Gate v6

Rows are not public unless they pass all gates:

1. Official source URL exists.
2. Branch/program is explicit.
3. Placement year or cutoff year is explicit.
4. Denominator is available where placement percent is displayed, or a visible warning is attached.
5. Admission row is verified, not merely source-indexed or staged.
6. Salary field distinguishes median, average and highest.
7. Row has a confidence/status field.
8. Row is hidden by default unless `publish_default=yes`.

This pack intentionally exposes only a very small default dataset because most rows still need final verification.

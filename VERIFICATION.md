# Verification record

## Execution

The delivered notebook was executed from the first code cell to the last, in a fresh Python process, using `scripts/execute_notebook.py`. All seven code cells completed, with outputs retained and three charts embedded. Execution uses IPython in-process; a Jupyter server is not required by the supplied execution command.

## Data and calculations

- Raw file SHA-256: `6db5da70bf3d18db8ffaff30416118440859ab522e2b4305df3dd1f607c7656c`.
- The original attached file and the preserved raw copy have identical bytes.
- Processed data: 55 observations, 11 geographies, five years, complete grid, no duplicate keys, no missing or suppressed rates, and values within 0–100.
- `scripts/verify_project.py` independently compares all 55 processed rates with exact raw-row values using `Decimal`, without pandas.
- All provincial summary rates, net changes and rankings are independently checked, including the BC/Ontario tie.
- All five BC gaps and all 44 defined annual movements are independently checked. The 11 blank baseline changes are intentional.
- Source note references, geography exclusions, units and change definitions are documented.

## Charts and documentation

The three PNG charts were visually inspected for legible labels, source notes, scale consistency and clipping. Plotted series use the same validated rate, benchmark and net-change tables exported by the notebook. Chart values and endpoint labels agree with the tables. The notebook contains all three rendered charts.

README local links and referenced output files are checked by the verification script. The README provincial table is cross-checked against the summary CSV during final review. The package includes only the original input, required source code, documentation and final outputs; development scripts and temporary execution files are excluded. No credential, token, personal account configuration or existing repository content is included.

## Scope of verification

No GitHub repository or profile was created, changed or published. No causal, significance, forecasting or workplace-impact claims are made. The project is ready for publication review, subject to the author's approval. These checks verify the supplied snapshot and calculations, not future source revisions or survey precision.

## Final pre-publication audit — October 11, 2026

**Result: PASS — ready for publication approval.**

- Installed only `requirements.txt` into a new isolated virtual environment (Python 3.12). `pip check` reported no broken requirements.
- Copied the project into a differently named directory containing spaces; removed generated outputs and cleared saved notebook results before execution.
- Ran both supplied scripts from an unrelated working directory. All seven code cells executed, all three charts were embedded, and independent verification passed.
- Regenerated processed data, tables, quality report and PNG charts matched the delivered output files byte-for-byte.
- Independently confirmed every numerical result in the README and notebook against the processed rates, including the annual-path statements, endpoint changes, BC gaps, extrema, rankings and ties. Confirmed the README provincial table against the exported summary.
- Re-inspected all three figures and reviewed the actual notebook code, outputs, scripts, requirements and documentation. All local README links resolve. The Statistics Canada source page was accessible; the DOI matches the identifier published on that page. Direct DOI resolution was not independently confirmed by the browsing tool.
- No credentials, private environment paths, account configuration, temporary files or obsolete drafts are included. The author name is intentional public attribution; no additional personal details are included.
- Corrected one documentation issue: the README minimum Python version is now **3.11**, matching the pinned IPython dependency. Execution was tested on Python 3.12; other platforms and Python versions were not separately tested.
- The five direct dependencies are used by the analysis or supplied execution script. No SQL, Tableau, machine learning, causal inference, statistical significance or workplace-outcome claims are present.
- No GitHub write operation was performed. Existing repositories and the profile were not accessed for modification.

The final project contains 16 files. Audit environments and temporary audit copies remain outside the publication package. Survey uncertainty, rounding, the short annual window and source-snapshot limitations remain documented.

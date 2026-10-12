"""Execute every notebook cell in order, without opening kernel sockets.

Run from any directory: python /path/to/project/scripts/execute_notebook.py
"""
import os
from pathlib import Path
import nbformat
from IPython.core.interactiveshell import InteractiveShell
from IPython.utils.capture import capture_output

root = Path(__file__).resolve().parents[1]
path = root / 'notebooks/unemployment_analysis.ipynb'
notebook = nbformat.read(path, as_version=4)
os.chdir(root / 'notebooks')
shell = InteractiveShell.instance()
shell.run_cell("import matplotlib; matplotlib.use('module://matplotlib_inline.backend_inline')")
from matplotlib_inline.backend_inline import flush_figures
count = 0
for cell in notebook.cells:
    if cell.cell_type != 'code':
        continue
    count += 1
    with capture_output(stdout=True, stderr=True, display=True) as captured:
        result = shell.run_cell(cell.source, store_history=True)
        flush_figures()
    if result.error_before_exec or result.error_in_exec:
        raise RuntimeError(f'Notebook failed in code cell {count}: {captured.stderr}\n{captured.stdout}') from (result.error_before_exec or result.error_in_exec)
    cell.execution_count = count
    cell.outputs = []
    if captured.stdout:
        cell.outputs.append(nbformat.v4.new_output('stream', name='stdout', text=captured.stdout))
    if captured.stderr:
        cell.outputs.append(nbformat.v4.new_output('stream', name='stderr', text=captured.stderr))
    for output in captured.outputs:
        cell.outputs.append(nbformat.v4.new_output('display_data', data=output.data, metadata=output.metadata))
notebook.metadata.language_info = {'name': 'python', 'version': __import__('platform').python_version()}
nbformat.validate(notebook)
nbformat.write(notebook, path)
print(f'PASS: executed all {count} code cells in order; saved outputs to {path.name}.')

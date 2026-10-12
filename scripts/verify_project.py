"""Independent audit using the standard library and exact decimal arithmetic."""
from pathlib import Path
from decimal import Decimal
import csv
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
def require(condition, message):
    if not condition:
        raise ValueError(message)
def read_csv(path):
    with path.open(encoding='utf-8', newline='') as handle:
        return list(csv.DictReader(handle))
PROVINCES = ['Newfoundland and Labrador', 'Prince Edward Island', 'Nova Scotia',
             'New Brunswick', 'Quebec', 'Ontario', 'Manitoba', 'Saskatchewan',
             'Alberta', 'British Columbia']
YEARS = range(2021, 2026)
raw = ROOT / 'data/raw/1410046401-eng.csv'
require(hashlib.sha256(raw.read_bytes()).hexdigest() == '6db5da70bf3d18db8ffaff30416118440859ab522e2b4305df3dd1f607c7656c', 'Raw file changed.')
with raw.open(encoding='utf-8-sig', newline='') as handle:
    records = list(csv.reader(handle))
source = {}
for geography in ['Canada'] + PROVINCES:
    label = 'Canada 8' if geography == 'Canada' else geography
    rows = [row for row in records if len(row)==6 and row[0]==label]
    require(len(rows)==1, f'Source geography mismatch: {label}')
    for year, value in zip(YEARS, rows[0][1:]):
        source[(geography, year)] = Decimal(value)
clean_rows = read_csv(ROOT / 'data/processed/provincial_unemployment_2021_2025.csv')
require(len(clean_rows)==55, 'Clean row count mismatch.')
clean = {(row['geography'],int(row['year'])):Decimal(row['unemployment_rate']) for row in clean_rows}
require(len(clean)==55 and clean==source, 'Raw-to-clean mismatch or duplicate key.')
net = {g:clean[(g,2025)]-clean[(g,2021)] for g in PROVINCES}
summary = read_csv(ROOT / 'outputs/tables/provincial_summary.csv')
require(len(summary)==10 and {r['geography'] for r in summary}==set(PROVINCES), 'Summary scope mismatch.')
for row in summary:
    g=row['geography']
    for y in YEARS:
        require(Decimal(row[f'rate_{y}'])==clean[(g,y)], 'Summary annual rate mismatch.')
    require(Decimal(row['net_change_pp'])==net[g], 'Net change mismatch.')
    rank2025=1+sum(clean[(p,2025)]<clean[(g,2025)] for p in PROVINCES)
    ranknet=1+sum(net[p]>net[g] for p in PROVINCES)
    require(int(row['rank_2025_lowest_rate'])==rank2025, 'Rate rank mismatch.')
    require(int(row['rank_net_change_descending'])==ranknet, 'Net rank mismatch.')
bc = read_csv(ROOT / 'outputs/tables/bc_canada_comparison.csv')
require(len(bc)==5 and {int(r['year']) for r in bc}==set(YEARS), 'BC scope mismatch.')
for row in bc:
    y=int(row['year'])
    require(Decimal(row['bc_rate'])==clean[('British Columbia',y)], 'BC rate mismatch.')
    require(Decimal(row['canada_rate'])==clean[('Canada',y)], 'Canada rate mismatch.')
    require(Decimal(row['gap_pp'])==clean[('British Columbia',y)]-clean[('Canada',y)], 'BC gap mismatch.')
annual=read_csv(ROOT / 'outputs/tables/annual_changes.csv')
require(len(annual)==55 and {(r['geography'],int(r['year'])) for r in annual}==set(clean), 'Annual table scope mismatch.')
for row in annual:
    g,y=row['geography'],int(row['year'])
    require(Decimal(row['unemployment_rate'])==clean[(g,y)], 'Annual rate mismatch.')
    expected='' if y==2021 else clean[(g,y)]-clean[(g,y-1)]
    actual=row['year_over_year_change_pp']
    require(actual=='' if expected=='' else Decimal(actual)==expected, 'Annual movement mismatch.')
nb=json.loads((ROOT / 'notebooks/unemployment_analysis.ipynb').read_text())
codes=[c for c in nb['cells'] if c['cell_type']=='code']
require([c['execution_count'] for c in codes]==list(range(1,len(codes)+1)), 'Notebook not fully executed.')
require(not any(o['output_type']=='error' for c in codes for o in c['outputs']), 'Notebook error output.')
require(sum('image/png' in o.get('data',{}) for c in codes for o in c['outputs'])==3, 'Expected three embedded notebook charts.')
readme=(ROOT/'README.md').read_text()
for ref in re.findall(r'\]\(([^)]+)\)',readme):
    if not ref.startswith(('http://','https://','#')):
        require((ROOT/ref).is_file(),f'Broken README link: {ref}')
for image in (ROOT/'outputs/figures').glob('*.png'):
    require(image.read_bytes().startswith(b'\x89PNG\r\n\x1a\n'), 'Invalid chart file.')
require(len(list((ROOT/'outputs/figures').glob('*.png')))==3, 'Chart count mismatch.')
quality=json.loads((ROOT/'outputs/tables/data_quality_report.json').read_text())
require(quality['status']=='PASS' and quality['observations']==55, 'Quality report mismatch.')
print('PASS: 55 raw/processed matches; all summary rates, net changes, rankings, BC gaps and annual movements independently verified with Decimal.')
print(f'PASS: {len(codes)} executed code cells, three embedded charts, three PNG files, all README file links resolve.')
print('Net changes:', ', '.join(f'{g}: {v:+.1f} pp' for g,v in net.items()))

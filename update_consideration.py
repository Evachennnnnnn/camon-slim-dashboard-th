#!/usr/bin/env python3
"""Update dashboard with 11/15 Consideration data."""
import re
import json
import subprocess
import sys

HTML_PATH = 'index.html'

with open(HTML_PATH, 'r') as f:
    lines = f.readlines()

start_line = None
end_line = None
for i, line in enumerate(lines):
    if 'const D = {' in line:
        start_line = i
    if start_line and line.strip() == '}' and i > start_line + 100:
        for j in range(i+1, min(i+5, len(lines))):
            if lines[j].strip().startswith('//'):
                end_line = i
                break
        if end_line:
            break

d_lines = lines[start_line:end_line+1]
d_text = ''.join(d_lines).replace('const D = ', '', 1)
D = json.loads(d_text)

# ============================================================
# UPDATE: Consideration 11/15
# ============================================================
# Add 11/15 to consideration chart
D['consideration']['labels'].append('11/15')
D['consideration']['brandData'].append(2052898)
D['consideration']['industryData'].append(5355370)

# Calculate 11/15 rate: 2,052,898 / 13,596,202 = 15.10%
rate_1115 = round(2052898 / 13596202 * 100, 2)
D['consideration']['rateData'].append(rate_1115)
D['consideration']['rateLabels'].append('11/15')
D['consideration']['latestRate'] = rate_1115
D['consideration']['note'] = f'Brand Consideration latest 2.05M (11/15). / 本品牌 Consideration 最新 2.05M（11/15）。'
D['consideration']['rateNote'] = f'Consideration Rate = Consideration / TECNO总曝光，最新 {rate_1115}% (11/15)'

# Update KPI card
D['kpis'][4]['value'] = '2.05M'
D['kpis'][4]['sub'] = 'CAMON Slim KPI 目标 1.5M+ · As of / 截至 11/15'

D['kpis'][5]['value'] = f'{rate_1115}%'
D['kpis'][5]['sub'] = 'Consideration / TECNO曝光 · As of / 截至 11/15'

# Update hero
D['hero']['desc'] = f'Google Brand SOV 2.09% and Product SOV 11.76% (11/18); TT VV SOV 10.83% and Search SOV 1.30% (11/15); Meta impressions 5.18M (11/17); Consideration 2.05M (11/15), Rate {rate_1115}%.'
D['hero']['stats'][3]['value'] = '2.05M'

# Update overview
D['overview'][7]['current'] = '2.05M'
D['overview'][7]['date'] = '11/15'
D['overview'][8]['current'] = f'{rate_1115}%'
D['overview'][8]['date'] = '11/15'

# Update alert banner
D['alertBanner'] = f'数据更新至 11/18：Google Product SOV 11.76%（11/18），TT VV SOV 10.83%（11/15），Consideration 2.05M（11/15），Consideration Rate {rate_1115}%（11/15），挑战赛 12天 3,583 视频已超 POVA 8 Benchmark。'

# ============================================================
# VALIDATE
# ============================================================
print(f"Consideration: labels={len(D['consideration']['labels'])}, brand={len(D['consideration']['brandData'])}, industry={len(D['consideration']['industryData'])}")
print(f"Rate: labels={len(D['consideration']['rateLabels'])}, rate={len(D['consideration']['rateData'])}")
assert len(D['consideration']['labels']) == len(D['consideration']['brandData']) == len(D['consideration']['industryData']), "Consideration mismatch!"
assert len(D['consideration']['rateLabels']) == len(D['consideration']['rateData']), "Rate mismatch!"

print(f"\n✅ 11/15 Consideration: 2,052,898")
print(f"✅ 11/15 TT Exposure: 13,596,202")
print(f"✅ 11/15 Consideration Rate: {rate_1115}%")

# Write back
new_d_json = json.dumps(D, ensure_ascii=False, indent=2)
new_lines = lines[:start_line] + ['const D = ' + new_d_json + '\n'] + lines[end_line+1:]
with open(HTML_PATH, 'w') as f:
    f.writelines(new_lines)

# JS validate
validate_js = '''
const fs = require("fs");
const html = fs.readFileSync("index.html", "utf8");
const m = html.match(/const D = (\\{[\\s\\S]*?\\n\\})\\n/);
if(!m) { console.log("ERROR: no D match"); process.exit(1); }
try {
    const D = JSON.parse(m[1]);
    console.log("✅ JS parse OK");
    console.log("   consideration labels: " + D.consideration.labels.length);
    console.log("   rate labels: " + D.consideration.rateLabels.length);
    console.log("   latest rate: " + D.consideration.latestRate + "%");
    console.log("   kpi[4] value: " + D.kpis[4].value);
    console.log("   kpi[5] value: " + D.kpis[5].value);
} catch(e) {
    console.log("❌ PARSE ERROR: " + e.message);
    process.exit(1);
}
'''
result = subprocess.run(['node', '-e', validate_js], capture_output=True, text=True)
print(f"\n--- JS Validation ---")
print(result.stdout)
if result.returncode != 0:
    print("STDERR:", result.stderr)
    sys.exit(1)

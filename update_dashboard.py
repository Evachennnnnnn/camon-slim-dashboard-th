#!/usr/bin/env python3
"""Update CAMON Slim dashboard with latest data from Feishu."""
import re
import json
import subprocess
import sys

HTML_PATH = 'index.html'

with open(HTML_PATH, 'r') as f:
    lines = f.readlines()

# Find D object boundaries
start_line = None
end_line = None
for i, line in enumerate(lines):
    if 'const D = {' in line:
        start_line = i
    if start_line and line.strip() == '}' and i > start_line + 100:
        # Check if next non-empty line is comment or function
        for j in range(i+1, min(i+5, len(lines))):
            if lines[j].strip() and not lines[j].strip().startswith('//'):
                break
            if lines[j].strip().startswith('//'):
                end_line = i
                break
        if end_line:
            break

if start_line is None or end_line is None:
    print("ERROR: Could not find D object boundaries")
    sys.exit(1)

print(f"✅ Found D object: lines {start_line+1} to {end_line+1}")

# Extract and parse D object
d_lines = lines[start_line:end_line+1]
d_text = ''.join(d_lines)
# Remove "const D = " prefix
d_json = d_text.replace('const D = ', '', 1)

try:
    D = json.loads(d_json)
    print(f"✅ Parsed D object: {len(D)} top-level keys")
except json.JSONDecodeError as e:
    print(f"ERROR: JSON parse failed: {e}")
    sys.exit(1)

# ============================================================
# UPDATE DATA
# ============================================================

# 1. Dates
D['updatedDate'] = '2026-11-18'
D['dataAsOf'] = '11/18'
D['alertBanner'] = '数据更新至 11/18：Google Product SOV 11.76%（11/18），TT VV SOV 10.83%（11/15），Consideration 1.97M（11/14），挑战赛 12天 3,583 视频已超 POVA 8 Benchmark。'

# 2. Hero
D['hero']['desc'] = 'Google Brand SOV 2.09% and Product SOV 11.76% (11/18); TT VV SOV 10.83% and Search SOV 1.30% (11/15); Meta impressions 5.18M (11/17); Consideration 1.97M (11/14).'
D['hero']['stats'][0]['value'] = '2.09%'
D['hero']['stats'][1]['value'] = '11.76%'
D['hero']['stats'][2]['value'] = '10.83% / 1.30%'

# 3. KPIs
D['kpis'][0]['value'] = '10.83%'
D['kpis'][0]['trend'] = '↓'
D['kpis'][0]['trendClass'] = 'trend-down'
D['kpis'][0]['sub'] = 'Target / 目标 15% · As of / 截至 11/15'
D['kpis'][0]['statusDot'] = 'status-red'

D['kpis'][1]['sub'] = 'Target / 目标 3% · As of / 截至 11/15'
D['kpis'][2]['value'] = '2.09%'
D['kpis'][2]['sub'] = 'As of / 截至 11/18'

D['kpis'][3]['value'] = '11.76%'
D['kpis'][3]['trend'] = '↓'
D['kpis'][3]['trendClass'] = 'trend-down'
D['kpis'][3]['sub'] = 'Target / 目标 15% · As of / 截至 11/18'
D['kpis'][3]['statusDot'] = 'status-yellow'
D['kpis'][3]['borderLeft'] = '#f59e0b'
D['kpis'][3]['valueColor'] = '#f59e0b'

D['kpis'][6]['value'] = '5.18M'
D['kpis'][6]['sub'] = 'Meta Spend $2,194.13 · As of / 截至 11/17'

# 4. Challenge (12天)
D['challenge']['camonSlim']['period'] = '12天 / 12 Days'
D['challenge']['camonSlim']['videos'] = '3,583'
D['challenge']['camonSlim']['creators'] = '2,210'
D['challenge']['camonSlim']['views'] = '11.8M'
D['challenge']['camonSlim']['engagementRate'] = 0.0518
D['challenge']['camonSlim']['likes'] = '481.8K'
D['challenge']['camonSlim']['comments'] = '16.1K'
D['challenge']['camonSlim']['shares'] = '79.8K'
D['challenge']['camonSlim']['filters'] = '19.4K'

D['challenge']['stats'][0]['value'] = '3,583'
D['challenge']['stats'][1]['value'] = '19.4K'
D['challenge']['stats'][2]['value'] = '11.8M'
D['challenge']['stats'][3]['value'] = '5.18%'

D['challenge']['insights'][0]['items'] = [
    'CAMON Slim 12天数据已超越 POVA 8 的 14天 Benchmark',
    '视频提交量 3,583 vs 2,432，参与达人 2,210 vs 1,452',
    '总播放 11.8M vs 5.8M，互动率 5.18% vs 3.34%（1.55倍）'
]
D['challenge']['insights'][1]['items'] = [
    '日均视频：299/天 vs 174/天（1.7倍）',
    '日均播放：0.98M/天 vs 0.41M/天（2.4倍）',
    '滤镜使用 19.4K vs 17K，CAMON Slim 12天已超 POVA 8 14天'
]

# 5. Overview
D['overview'][0]['current'] = '2.09%'
D['overview'][0]['date'] = '11/18'
D['overview'][1]['current'] = '11.76%'
D['overview'][1]['date'] = '11/18'
D['overview'][1]['status'] = 'yellow'
D['overview'][2]['current'] = '10.83%'
D['overview'][2]['date'] = '11/15'
D['overview'][2]['status'] = 'red'
D['overview'][3]['date'] = '11/15'

# Calculate cumulative spends
tt_daily = [0, 0, 96.36, 423.32, 466.19, 1005.47, 1071.55, 1350.02, 1405.59,
            1050.79, 1820.94, 2830.39, 3060.28, 1961.25, 2387.24, 2164.64,
            32707.54, 2766.45, 5071.73, 6810.92, 35925.39, 4641.47, 4451.61,
            2323.39, 3496.49, 4211.01, 4727.76, 5353.75, 5832.92, 4427.84,
            2641.90, 4104.70]
tt_cum = sum(tt_daily)
D['overview'][4]['current'] = f'${tt_cum:,.2f} cumulative'
D['overview'][4]['date'] = '11/17'

meta_daily = [97.75, 356.71, 452.02, 825.58, 734.54, 1182.44, 1270.40, 1308.64,
              1130.95, 1163.58, 1345.65, 1332.71, 1706.00, 1027.78, 2621.93,
              1957.93, 2430.58, 4965.62, 1538.29, 1785.03, 1851.15, 897.50,
              1521.91, 2016.61, 2454.91, 2786.62, 2845.16, 2738.24, 1723.95,
              2194.13]
meta_cum = sum(meta_daily)
D['overview'][5]['current'] = f'${meta_cum:,.2f} cumulative'
D['overview'][5]['date'] = '11/17'

meta_imp = [389920, 1324958, 1615904, 2791710, 2432241, 3800623, 4061030, 4418270,
            3907302, 3967229, 4332156, 4024103, 5026959, 3616780, 6556499, 7312020,
            8654870, 16037402, 4933802, 5375550, 5602967, 2470857, 3465317, 4437635,
            5746827, 7219537, 7447018, 7323390, 4828489, 5179382]
meta_total_imp = sum(meta_imp)
D['overview'][6]['current'] = f'{meta_total_imp/1e6:.2f}M cumulative'
D['overview'][6]['date'] = '11/17'

# 6. Google SOV - add 11/18
D['googleSov']['labels'].append('11/18')
D['googleSov']['brand'].append(2.09)
D['googleSov']['product'].append(11.76)
D['googleSov']['brandNote'] = 'Brand SOV latest 2.09% (11/18) / 品牌 SOV 最新 2.09%（11/18）'
D['googleSov']['productNote'] = 'Product SOV latest 11.76% (11/18) / 产品 SOV 最新 11.76%（11/18）'

# 7. Competitor Compare - add 11/18
D['competitorCompare']['chartLabels'].append('11/18')
D['competitorCompare']['datasets'][0]['data'].append(11.76)
D['competitorCompare']['note'] = 'Google Trends 对比关键词 / Comparison: CAMON Slim vs OPPO Reno 16 F, VIVO V80 Lite, Redmi Note 17 Pro · 截至 11/18'
D['competitorCompare']['table'][0]['sov'] = '11.76%'
D['competitorCompare']['table'][0]['trend'] = '↓'
D['competitorCompare']['table'][0]['trendClass'] = 'trend-down'
D['competitorCompare']['insight'] = '💡 竞品对比组合：CAMON Slim vs OPPO Reno 16 F / VIVO V80 Lite / Redmi Note 17 Pro。CAMON Slim 产品 SOV 最新 11.76%（11/18），较昨日回落。竞品数据来自 Google Trends 相对搜索热度。/ Product SOV latest 11.76% (11/18).'

# 8. TT SOV - update 11/15 + add 11/17
D['ttSov']['vvData'][29] = 10.83
D['ttSov']['searchData'][29] = 1.30
D['ttSov']['labels'].append('11/17')
D['ttSov']['vvData'].append(None)
D['ttSov']['searchData'].append(None)
D['ttSov']['note'] = 'VV SOV latest 10.83% (11/15); Search SOV latest 1.30% (11/15). 11/16-17 source cells blank / TikTok声量最新数据到11/15，11/16-17源表尚未回填'

# 9. Spend - add 11/17
D['spend']['labels'].append('11/17')
D['spend']['dailySpend'].append(4104.70)
D['spend']['spendProgress'].append(0.901729940119761)
D['spend']['exposureProgress'].append(None)

# ============================================================
# VALIDATE ARRAYS
# ============================================================
print("\n--- Array Validation ---")
print(f"Google SOV: labels={len(D['googleSov']['labels'])}, brand={len(D['googleSov']['brand'])}, product={len(D['googleSov']['product'])}")
assert len(D['googleSov']['labels']) == len(D['googleSov']['brand']) == len(D['googleSov']['product']), "Google SOV mismatch!"

print(f"Competitor: labels={len(D['competitorCompare']['chartLabels'])}, data={len(D['competitorCompare']['datasets'][0]['data'])}")
assert len(D['competitorCompare']['chartLabels']) == len(D['competitorCompare']['datasets'][0]['data']), "Competitor mismatch!"

print(f"TT SOV: labels={len(D['ttSov']['labels'])}, vv={len(D['ttSov']['vvData'])}, search={len(D['ttSov']['searchData'])}")
assert len(D['ttSov']['labels']) == len(D['ttSov']['vvData']) == len(D['ttSov']['searchData']), "TT SOV mismatch!"

print(f"Spend: labels={len(D['spend']['labels'])}, daily={len(D['spend']['dailySpend'])}, progress={len(D['spend']['spendProgress'])}")
assert len(D['spend']['labels']) == len(D['spend']['dailySpend']) == len(D['spend']['spendProgress']) == len(D['spend']['exposureProgress']), "Spend mismatch!"

print("✅ All array lengths match!")

# ============================================================
# WRITE BACK
# ============================================================
new_d_json = json.dumps(D, ensure_ascii=False, indent=2)
new_lines = lines[:start_line] + ['const D = ' + new_d_json + '\n'] + lines[end_line+1:]

with open(HTML_PATH, 'w') as f:
    f.writelines(new_lines)

print(f"\n✅ Dashboard updated and written to {HTML_PATH}")
print(f"   TT cumulative spend: ${tt_cum:,.2f}")
print(f"   Meta cumulative spend: ${meta_cum:,.2f}")
print(f"   Meta cumulative impressions: {meta_total_imp/1e6:.2f}M")
print(f"   Challenge: {D['challenge']['camonSlim']['videos']} videos, {D['challenge']['camonSlim']['creators']} creators")

# ============================================================
# JS VALIDATION
# ============================================================
validate_js = '''
const fs = require("fs");
const html = fs.readFileSync("index.html", "utf8");
const m = html.match(/const D = (\\{[\\s\\S]*?\\n\\})\\n/);
if(!m) { console.log("ERROR: no D match"); process.exit(1); }
try {
    const D = JSON.parse(m[1]);
    console.log("✅ JS parse OK: " + Object.keys(D).length + " keys");
    console.log("   googleSov: " + D.googleSov.labels.length + " dates");
    console.log("   ttSov: " + D.ttSov.labels.length + " dates");
    console.log("   spend: " + D.spend.labels.length + " dates");
    console.log("   competitor: " + D.competitorCompare.chartLabels.length + " dates");
    console.log("   challenge videos: " + D.challenge.camonSlim.videos);
    console.log("   kpis: " + D.kpis.length + " items");
    console.log("   overview: " + D.overview.length + " rows");
    console.log("\\n🎉 All validations passed!");
} catch(e) {
    console.log("❌ PARSE ERROR: " + e.message);
    process.exit(1);
}
'''

result = subprocess.run(['node', '-e', validate_js], capture_output=True, text=True)
print(f"\n--- Final JS Validation ---")
print(result.stdout)
if result.returncode != 0:
    print("STDERR:", result.stderr)
    sys.exit(1)

#!/usr/bin/env python3
"""
泰国 CAMON Slim 看板更新脚本 - 2026-11-19
更新日更模块至最新数据，保留周更模块不动
"""
import json
import sys
import subprocess

# ====== 读取 index.html ======
with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ====== 提取 D 对象（括号匹配） ======
start_marker = 'const D = '
start_idx = content.find(start_marker)
if start_idx == -1:
    print("❌ 找不到 const D =")
    sys.exit(1)

obj_start = start_idx + len(start_marker)
depth = 0
end_idx = None
for i in range(obj_start, len(content)):
    if content[i] == '{':
        depth += 1
    elif content[i] == '}':
        depth -= 1
        if depth == 0:
            end_idx = i + 1
            break

if end_idx is None:
    print("❌ D 对象括号不匹配")
    sys.exit(1)

d_text = content[obj_start:end_idx]
D = json.loads(d_text)
print(f"✅ 成功解析 D 对象，当前 updatedDate: {D['updatedDate']}")

# ====== 保存周更模块（不被覆盖） ======
saved_audience = json.loads(json.dumps(D.get('audience', {})))
saved_keywords = json.loads(json.dumps(D.get('keywords', {})))
saved_paidComments = json.loads(json.dumps(D.get('paidComments', {})))

# ====== 新数据 ======

# --- Google SOV: 追加 11/19 ---
new_google = ("11/19", 2.15, 13.09)
if new_google[0] not in D['googleSov']['labels']:
    D['googleSov']['labels'].append(new_google[0])
    D['googleSov']['brand'].append(new_google[1])
    D['googleSov']['product'].append(new_google[2])
    D['competitorCompare']['chartLabels'].append(new_google[0])
    D['competitorCompare']['datasets'][0]['data'].append(new_google[2])
    print(f"  + Google SOV 追加 {new_google[0]}: Brand {new_google[1]}%, Product {new_google[2]}%")

# --- TT VV SOV: 更新 11/16（从 null → 6.73%），11/17-18 源表为空保持 null ---
# 当前 ttSov labels 已到 11/17，11/16 index=30, 11/17 index=31
# 检查 11/16 的值
idx_1116 = D['ttSov']['labels'].index('11/16') if '11/16' in D['ttSov']['labels'] else -1
if idx_1116 >= 0 and D['ttSov']['vvData'][idx_1116] is None:
    D['ttSov']['vvData'][idx_1116] = 6.73
    D['ttSov']['searchData'][idx_1116] = 1.23
    print(f"  ~ TT SOV 11/16 更新: VV 6.73%, Search 1.23%")

# 追加 11/18（消耗数据有，但 VV/Search SOV 源表为空）
if '11/18' not in D['ttSov']['labels']:
    D['ttSov']['labels'].append('11/18')
    D['ttSov']['vvData'].append(None)
    D['ttSov']['searchData'].append(None)
    print(f"  + TT SOV 追加 11/18 (null, 源表空)")

# --- Consideration: 追加 11/16 ---
if '11/16' not in D['consideration']['labels']:
    D['consideration']['labels'].append('11/16')
    D['consideration']['brandData'].append(2046295)
    D['consideration']['industryData'].append(5332231)
    # Rate = brand / TT总曝光(当日) * 100
    # 11/16 TT总曝光 = 4,778,124
    rate_1116 = round(2046295 / 4778124 * 100, 2) if 4778124 > 0 else 0
    D['consideration']['rateData'].append(rate_1116)
    D['consideration']['rateLabels'].append('11/16')
    D['consideration']['latestRate'] = rate_1116
    print(f"  + Consideration 追加 11/16: {2046295:,}, Rate {rate_1116}%")

# --- Meta: 追加 11/18 ---
meta_new = [("11/18", 1422.44, 2942154)]
# 11/18 已有？检查 spend labels
# 当前 spend labels 到 11/17

# --- Spend (TT消耗): 追加 11/18 ---
if '11/18' not in D['spend']['labels']:
    D['spend']['labels'].append('11/18')
    D['spend']['dailySpend'].append(4600.97)
    D['spend']['spendProgress'].append(0.929280658682635)
    D['spend']['exposureProgress'].append(None)  # 11/18 曝光数据尚未回填
    print(f"  + Spend 追加 11/18: $4,600.97")

# ====== 计算汇总数据 ======

# TT 累计消耗（从 spend dailySpend 累加）
tt_cumulative_spend = sum(D['spend']['dailySpend'])

# TT 总曝光（从 ae2c02 数据累加到 11/16）
tt_daily_impressions = [
    417245, 512731, 1058612, 1980509, 2304924, 4160130, 4104540, 5142215,
    4945262, 4493444, 6665384, 8508983, 7978743, 5313511, 7226108, 10589341,
    16758489, 10552314, 19134836, 23463392, 45831076, 18704152, 16891273,
    10283289, 12229637, 13019465, 16368239, 18172809, 18165959, 13596202,
    4778124
]
tt_total_impressions = sum(tt_daily_impressions)

# Meta 总曝光（到 11/18）
meta_daily_impressions = [
    389920, 1324958, 1615904, 2791710, 2432241, 3800623, 4061030, 4418270,
    3907302, 3967229, 4332156, 4024103, 5026959, 3616780, 6556499, 7312020,
    8654870, 16037402, 4933802, 5375550, 5602967, 2470857, 3465317, 4437635,
    5746827, 7219537, 7447018, 7323390, 4828489, 5179382, 2942154
]
meta_total_impressions = sum(meta_daily_impressions)

# Meta 累计消耗
meta_daily_spend = [
    97.75, 356.71, 452.02, 825.58, 734.54, 1182.44, 1270.40, 1308.64,
    1130.95, 1163.58, 1345.65, 1332.71, 1706.00, 1027.78, 2621.93,
    1957.93, 2430.58, 4965.62, 1538.29, 1785.03, 1851.15, 897.50,
    1521.91, 2016.61, 2454.91, 2786.62, 2845.16, 2738.24, 1723.95,
    2194.13, 1422.44
]
meta_cumulative_spend = sum(meta_daily_spend)

# YT 总曝光（到 11/18）
yt_daily_impressions = [
    0, 0, 0, 0, 0, 0, 0, 0, 0,  # 10/19-10/27(不含27)
    67031, 1454760, 1763049, 1670956, 1713798, 1573422,  # 10/27-11/1
    0, 1303401, 5173269, 5780003, 5292973, 5367570, 5122405,  # 11/2-11/8
    14572, 85893, 112207, 111709, 113383, 0, 0, 0,  # 11/9-11/16
    60787, 135490  # 11/17-11/18
]
yt_total_impressions = sum(yt_daily_impressions)

# YT 累计消耗
yt_daily_spend = [
    0, 0, 0, 0, 0, 0, 0, 0, 0,
    19.04, 562.88, 727.83, 726.62, 731.30, 728.40,
    0, 308.96, 1156.25, 1154.06, 1146.32, 1164.67, 1165.35,
    13.82, 46.57, 46.61, 46.44, 46.57, 0, 0, 0,
    84.97, 143.74
]
yt_cumulative_spend = sum(yt_daily_spend)

total_impressions = tt_total_impressions + meta_total_impressions + yt_total_impressions
total_impressions_M = total_impressions / 1_000_000

# 最新指标
google_brand_latest = 2.15
google_product_latest = 13.09
tt_vv_latest = 10.83  # 11/15 是最新有效值（11/16 有 6.73%）
tt_vv_latest = 6.73   # 11/16 已更新
tt_search_latest = 1.23  # 11/16
consideration_latest = 2046295
consideration_latest_M = consideration_latest / 1_000_000
consideration_rate_latest = round(2046295 / 4778124 * 100, 2)

print(f"\n📊 汇总计算：")
print(f"  TT 累计消耗: ${tt_cumulative_spend:,.2f}")
print(f"  TT 总曝光: {tt_total_impressions/1_000_000:.2f}M (to 11/16)")
print(f"  Meta 累计消耗: ${meta_cumulative_spend:,.2f}")
print(f"  Meta 总曝光: {meta_total_impressions/1_000_000:.2f}M (to 11/18)")
print(f"  YT 累计消耗: ${yt_cumulative_spend:,.2f}")
print(f"  YT 总曝光: {yt_total_impressions/1_000_000:.2f}M (to 11/18)")
print(f"  全网总曝光: {total_impressions_M:.2f}M")
print(f"  Consideration: {consideration_latest:,} (11/16)")
print(f"  Consideration Rate: {consideration_rate_latest}%")

# ====== 更新 D 对象各模块 ======

# --- updatedDate / dataAsOf ---
D['updatedDate'] = "2026-11-19"
D['dataAsOf'] = "11/19"

# --- alertBanner ---
D['alertBanner'] = (
    f"数据更新至 11/19：Google Product SOV {google_product_latest}% (11/19)，"
    f"TT VV SOV {tt_vv_latest}% (11/16)，TT Search SOV {tt_search_latest}% (11/16)，"
    f"全网总曝光 {total_impressions_M:.2f}M，"
    f"Consideration {consideration_latest_M:.2f}M (11/16)，"
    f"挑战赛 13天 3,608 视频已超 POVA 8 Benchmark。"
)

# --- hero ---
D['hero']['desc'] = (
    f"Google Product SOV {google_product_latest}% (11/19), "
    f"TT VV SOV {tt_vv_latest}% (11/16), "
    f"全网总曝光 {total_impressions_M:.2f}M, "
    f"Consideration {consideration_latest_M:.2f}M (11/16)."
)
D['hero']['stats'] = [
    {"label": "Google Product SOV", "value": f"{google_product_latest}%"},
    {"label": "TikTok VV SOV", "value": f"{tt_vv_latest}%"},
    {"label": "TikTok Search SOV", "value": f"{tt_search_latest}%"},
    {"label": "Consideration", "value": f"{consideration_latest_M:.2f}M"}
]

# --- kpis ---
# KPI 0: TT VV SOV
D['kpis'][0]['value'] = f"{tt_vv_latest}%"
D['kpis'][0]['sub'] = "Target / 目标 15% · As of / 截至 11/16"
D['kpis'][0]['statusDot'] = "status-red"
D['kpis'][0]['trend'] = "↓"
D['kpis'][0]['trendClass'] = "trend-down"

# KPI 1: Consideration Rate
D['kpis'][1]['value'] = f"{consideration_rate_latest}%"
D['kpis'][1]['sub'] = f"Consideration / TECNO曝光 · As of / 截至 11/16"
D['kpis'][1]['statusDot'] = "status-green"
D['kpis'][1]['trend'] = "↑"
D['kpis'][1]['trendClass'] = "trend-up"
D['kpis'][1]['borderLeft'] = "#10b981"
D['kpis'][1]['valueColor'] = "#10b981"

# KPI 2: 全网总曝光
D['kpis'][2]['value'] = f"{total_impressions_M:.2f}M"
D['kpis'][2]['sub'] = f"TT {tt_total_impressions/1_000_000:.2f}M + Meta {meta_total_impressions/1_000_000:.2f}M + YT {yt_total_impressions/1_000_000:.2f}M"
D['kpis'][2]['statusDot'] = "status-green"
D['kpis'][2]['trend'] = "↑"
D['kpis'][2]['trendClass'] = "trend-up"
D['kpis'][2]['borderLeft'] = "#10b981"
D['kpis'][2]['valueColor'] = "#10b981"

# KPI 3: 挑战赛曝光
D['kpis'][3]['value'] = "11.8M"
D['kpis'][3]['sub'] = "13天 · 超 POVA 8 Benchmark 5.8M"
D['kpis'][3]['statusDot'] = "status-green"
D['kpis'][3]['trend'] = "↑"
D['kpis'][3]['trendClass'] = "trend-up"
D['kpis'][3]['borderLeft'] = "#10b981"
D['kpis'][3]['valueColor'] = "#10b981"

# --- challenge: 更新为 13天 ---
D['challenge']['camonSlim']['period'] = "13天 / 13 Days"
D['challenge']['camonSlim']['videos'] = "3,608"
D['challenge']['camonSlim']['creators'] = "2,210"
D['challenge']['camonSlim']['views'] = "11.8M"
D['challenge']['camonSlim']['engagementRate'] = 0.0518
D['challenge']['camonSlim']['likes'] = "481.8K"
D['challenge']['camonSlim']['comments'] = "16.1K"
D['challenge']['camonSlim']['shares'] = "79.8K"
D['challenge']['camonSlim']['filters'] = "19.4K"

D['challenge']['stats'][0]['value'] = "3,608"
D['challenge']['stats'][1]['value'] = "19.4K"
D['challenge']['stats'][2]['value'] = "11.8M"
D['challenge']['stats'][3]['value'] = "5.18%"

D['challenge']['insights'][0]['items'] = [
    'CAMON Slim 13天数据已超越 POVA 8 的 14天 Benchmark',
    '视频提交量 3,608 vs 2,220，参与达人 2,210 vs 1,452',
    '总播放 11.8M vs 5.8M，互动率 5.18% vs 3.34%（1.55倍）'
]
D['challenge']['insights'][1]['items'] = [
    '日均视频：278/天 vs 159/天（1.75倍）',
    '日均播放：0.91M/天 vs 0.41M/天（2.2倍）',
    '滤镜使用 19.4K vs 17K，CAMON Slim 13天已超 POVA 8 14天'
]

# --- overview ---
D['overview'][0]['current'] = f"{google_brand_latest}%"
D['overview'][0]['date'] = "11/19"
D['overview'][1]['current'] = f"{google_product_latest}%"
D['overview'][1]['date'] = "11/19"
D['overview'][2]['current'] = f"{tt_vv_latest}%"
D['overview'][2]['date'] = "11/16"
D['overview'][3]['current'] = f"{tt_search_latest}%"
D['overview'][3]['date'] = "11/16"
D['overview'][4]['current'] = f"${tt_cumulative_spend:,.2f} cumulative"
D['overview'][4]['date'] = "11/18"
D['overview'][5]['current'] = f"${meta_cumulative_spend:,.2f} cumulative"
D['overview'][5]['date'] = "11/18"
D['overview'][6]['current'] = f"{meta_total_impressions/1e6:.2f}M cumulative"
D['overview'][6]['date'] = "11/18"
D['overview'][7]['current'] = f"{consideration_latest_M:.2f}M"
D['overview'][7]['date'] = "11/16"
D['overview'][8]['current'] = f"{consideration_rate_latest}%"
D['overview'][8]['date'] = "11/16"

# --- Google SOV notes ---
D['googleSov']['brandNote'] = f'Brand SOV latest {google_brand_latest}% (11/19) / 品牌 SOV 最新 {google_brand_latest}%（11/19）'
D['googleSov']['productNote'] = f'Product SOV latest {google_product_latest}% (11/19) / 产品 SOV 最新 {google_product_latest}%（11/19）'

# --- Competitor Compare ---
D['competitorCompare']['note'] = f'Google Trends 对比关键词 / Comparison: CAMON Slim vs OPPO Reno 16 F, VIVO V80 Lite, Redmi Note 17 Pro · 截至 11/19'
D['competitorCompare']['table'][0]['sov'] = f'{google_product_latest}%'
D['competitorCompare']['table'][0]['trend'] = "↑"
D['competitorCompare']['table'][0]['trendClass'] = "trend-up"
D['competitorCompare']['insight'] = f'💡 竞品对比组合：CAMON Slim vs OPPO Reno 16 F / VIVO V80 Lite / Redmi Note 17 Pro。CAMON Slim 产品 SOV 最新 {google_product_latest}%（11/19），较昨日回升。竞品数据来自 Google Trends 相对搜索热度。/ Product SOV latest {google_product_latest}% (11/19).'

# --- TT SOV notes ---
D['ttSov']['note'] = f'VV SOV latest {tt_vv_latest}% (11/16); Search SOV latest {tt_search_latest}% (11/16). 11/17-18 source cells blank / TikTok声量最新数据到11/16，11/17-18源表尚未回填'

# --- Consideration notes ---
D['consideration']['note'] = f'Brand Consideration latest {consideration_latest_M:.2f}M (11/16). / 本品牌 Consideration 最新 {consideration_latest_M:.2f}M（11/16）。'
D['consideration']['rateNote'] = f'Consideration Rate = Consideration / TECNO总曝光，最新 {consideration_rate_latest}% (11/16)'

# ====== 恢复周更模块 ======
D['audience'] = saved_audience
D['keywords'] = saved_keywords
D['paidComments'] = saved_paidComments

# ====== 验证数组长度 ======
print("\n--- Array Validation ---")
print(f"Google SOV: labels={len(D['googleSov']['labels'])}, brand={len(D['googleSov']['brand'])}, product={len(D['googleSov']['product'])}")
assert len(D['googleSov']['labels']) == len(D['googleSov']['brand']) == len(D['googleSov']['product']), "Google SOV mismatch!"

print(f"Competitor: labels={len(D['competitorCompare']['chartLabels'])}, data={len(D['competitorCompare']['datasets'][0]['data'])}")
assert len(D['competitorCompare']['chartLabels']) == len(D['competitorCompare']['datasets'][0]['data']), "Competitor mismatch!"

print(f"TT SOV: labels={len(D['ttSov']['labels'])}, vv={len(D['ttSov']['vvData'])}, search={len(D['ttSov']['searchData'])}")
assert len(D['ttSov']['labels']) == len(D['ttSov']['vvData']) == len(D['ttSov']['searchData']), "TT SOV mismatch!"

print(f"Spend: labels={len(D['spend']['labels'])}, daily={len(D['spend']['dailySpend'])}, progress={len(D['spend']['spendProgress'])}, exposure={len(D['spend']['exposureProgress'])}")
assert len(D['spend']['labels']) == len(D['spend']['dailySpend']) == len(D['spend']['spendProgress']) == len(D['spend']['exposureProgress']), "Spend mismatch!"

print(f"Consideration: labels={len(D['consideration']['labels'])}, brand={len(D['consideration']['brandData'])}, industry={len(D['consideration']['industryData'])}")
assert len(D['consideration']['labels']) == len(D['consideration']['brandData']) == len(D['consideration']['industryData']), "Consideration mismatch!"

print(f"Consideration Rate: labels={len(D['consideration']['rateLabels'])}, data={len(D['consideration']['rateData'])}")
assert len(D['consideration']['rateLabels']) == len(D['consideration']['rateData']), "Consideration Rate mismatch!"

print("✅ All array lengths match!")

# ====== 写回 index.html ======
new_d_text = json.dumps(D, ensure_ascii=False, indent=2)
new_content = content[:obj_start] + new_d_text + content[end_idx:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"\n✅ Dashboard updated to 11/19")
print(f"   Google Product SOV: {google_product_latest}% (11/19)")
print(f"   TT VV SOV: {tt_vv_latest}% (11/16)")
print(f"   TT Search SOV: {tt_search_latest}% (11/16)")
print(f"   全网总曝光: {total_impressions_M:.2f}M")
print(f"   Consideration: {consideration_latest_M:.2f}M (11/16)")
print(f"   Challenge: 13天, {D['challenge']['camonSlim']['videos']} videos")

# ====== JS VALIDATION ======
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
    console.log("   consideration: " + D.consideration.labels.length + " dates");
    console.log("   challenge videos: " + D.challenge.camonSlim.videos);
    console.log("   kpis: " + D.kpis.length + " items");
    console.log("   overview: " + D.overview.length + " rows");
    console.log("   audience: " + (D.audience ? "present" : "MISSING"));
    console.log("   keywords: " + (D.keywords ? "present" : "MISSING"));
    console.log("   paidComments: " + (D.paidComments ? "present" : "MISSING"));
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

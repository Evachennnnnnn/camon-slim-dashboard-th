const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const m = html.match(/const D = (\{[\s\S]*?\n\})\n/);
if (!m) { console.log('NO MATCH'); process.exit(1); }
const D = JSON.parse(m[1]);

// === DATES ===
D.updatedDate = '2026-11-24';
D.dataAsOf = '11/24';
D.alertBanner = '数据更新至 11/24：Google Product SOV 12.8%（11/24），TT VV SOV 5.54%（11/21），TT Search SOV 1.23%（11/22），全网总曝光 559.23M，Consideration 1.76M（11/21），TT 消耗进度 102.8%。';

// === HERO ===
D.hero.desc = 'Google Product SOV 12.8% (11/24), TT VV SOV 5.54% (11/21), 全网总曝光 559.23M, Consideration 1.76M (11/21).';
D.hero.stats[0].value = '12.8%';
D.hero.stats[1].value = '5.54%';
D.hero.stats[2].value = '1.23%';
D.hero.stats[3].value = '1.76M';

// === KPIs ===
// kpi[0]: TT VV SOV
D.kpis[0].value = '5.54%';
D.kpis[0].trend = '↓';
D.kpis[0].trendClass = 'trend-down';
D.kpis[0].sub = 'Target / 目标 15% · As of / 截至 11/21';
D.kpis[0].statusDot = 'status-red';
D.kpis[0].borderLeft = '#ef4444';
D.kpis[0].valueColor = '#ef4444';
// kpi[1]: Consideration Rate
D.kpis[1].value = '22.84%';
D.kpis[1].sub = 'Consideration / TECNO曝光 · As of / 截至 11/21';
// kpi[2]: 全网总曝光
D.kpis[2].value = '559.23M';
D.kpis[2].sub = 'TT 368.43M + Meta 150.74M + YT 40.06M';
// kpi[3]: 挑战赛 - no change

// === OVERVIEW ===
D.overview[0].current = '2.15%';
D.overview[0].date = '11/24';
D.overview[1].current = '12.8%';
D.overview[1].date = '11/24';
D.overview[1].status = 'red';
D.overview[2].current = '5.54%';
D.overview[2].date = '11/21';
D.overview[3].current = '1.23%';
D.overview[3].date = '11/22';
D.overview[4].current = '$170,714.67 cumulative';
D.overview[4].date = '11/21';
D.overview[5].current = '$59,222.75 cumulative';
D.overview[5].date = '11/23';
D.overview[6].current = '150.74M cumulative';
D.overview[6].date = '11/23';
D.overview[7].current = '1.76M';
D.overview[7].date = '11/21';
D.overview[8].current = '22.84%';
D.overview[8].date = '11/21';

// === GOOGLE SOV - add 11/24 ===
D.googleSov.labels.push('11/24');
D.googleSov.brand.push(2.15);
D.googleSov.product.push(12.8);
D.googleSov.brandNote = 'Brand SOV latest 2.15% (11/24) / 品牌 SOV 最新 2.15%（11/24）';
D.googleSov.productNote = 'Product SOV latest 12.8% (11/24) / 产品 SOV 最新 12.8%（11/24）';

// === COMPETITOR - add 11/24 ===
D.competitorCompare.chartLabels.push('11/24');
D.competitorCompare.datasets[0].data.push(12.8);
D.competitorCompare.note = 'Google Trends 对比关键词 / Comparison: CAMON Slim vs OPPO Reno 16 F, VIVO V80 Lite, Redmi Note 17 Pro · 截至 11/24';

// === TT SOV - add 11/22 ===
D.ttSov.labels.push('11/22');
D.ttSov.vvData.push(null); // 11/22 VV SOV 为空
D.ttSov.searchData.push(1.23);
D.ttSov.note = 'VV SOV latest 5.54% (11/21); Search SOV latest 1.23% (11/22). 11/22-23 VV source cells blank / TikTok VV声量最新数据到11/21，11/22-23源表尚未回填';

// === SPEND - add 11/22, 11/23 ===
D.spend.labels.push('11/22', '11/23');
D.spend.dailySpend.push(3067.44, 2058.51);
D.spend.spendProgress.push(1.01569023952096, 1.02801664670659);
D.spend.exposureProgress.push(null, null); // 11/22-23 曝光数据为空

// === CONSIDERATION - no new data (11/22-23 are empty) ===
// Keep as is

// === VALIDATE ===
console.log('--- Array Validation ---');
console.log(`Google SOV: labels=${D.googleSov.labels.length}, brand=${D.googleSov.brand.length}, product=${D.googleSov.product.length}`);
if (D.googleSov.labels.length !== D.googleSov.brand.length || D.googleSov.labels.length !== D.googleSov.product.length) {
    console.error('❌ Google SOV mismatch!'); process.exit(1);
}
console.log(`Competitor: labels=${D.competitorCompare.chartLabels.length}, data=${D.competitorCompare.datasets[0].data.length}`);
if (D.competitorCompare.chartLabels.length !== D.competitorCompare.datasets[0].data.length) {
    console.error('❌ Competitor mismatch!'); process.exit(1);
}
console.log(`TT SOV: labels=${D.ttSov.labels.length}, vv=${D.ttSov.vvData.length}, search=${D.ttSov.searchData.length}`);
if (D.ttSov.labels.length !== D.ttSov.vvData.length || D.ttSov.labels.length !== D.ttSov.searchData.length) {
    console.error('❌ TT SOV mismatch!'); process.exit(1);
}
console.log('✅ All array lengths match!');

// === WRITE ===
const newJson = JSON.stringify(D, null, 2);
const newHtml = html.replace(/const D = \{[\s\S]*?\n\}\n/, 'const D = ' + newJson + '\n');
fs.writeFileSync('index.html', newHtml);
console.log('✅ Dashboard updated to 11/24');
console.log(`   Google SOV: ${D.googleSov.labels.length} dates (to 11/24)`);
console.log(`   TT SOV: ${D.ttSov.labels.length} dates (to 11/22)`);
console.log(`   TT Spend: $170,714.67 cumulative (to 11/21)`);
console.log(`   Meta Spend: $59,222.75 cumulative (to 11/23)`);
console.log(`   YT Spend: $9,687.23 cumulative (to 11/23)`);
console.log(`   Total Impressions: 559.23M (TT 368.43M + Meta 150.74M + YT 40.06M)`);
console.log(`   Consideration: 1.76M (11/21)`);

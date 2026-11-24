const fs = require('fs');
const html = fs.readFileSync('index.html', 'utf8');
const m = html.match(/const D = (\{[\s\S]*?\n\})\n/);
if (!m) { console.log('NO MATCH'); process.exit(1); }
const D = JSON.parse(m[1]);

// === DATES ===
D.updatedDate = '2026-11-23';
D.dataAsOf = '11/23';
D.alertBanner = '数据更新至 11/23：Google Product SOV 9.09%（11/21-23），TT VV SOV 5.54%（11/21），TT Search SOV 1.38%（11/21），全网总曝光 555.05M，Consideration 1.76M（11/21），TT 消耗进度 101.6%。';

// === HERO ===
D.hero.desc = 'Google Product SOV 9.09% (11/21-23), TT VV SOV 5.54% (11/21), 全网总曝光 555.05M, Consideration 1.76M (11/21).';
D.hero.stats[0].value = '9.09%';
D.hero.stats[1].value = '5.54%';
D.hero.stats[2].value = '1.38%';
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
D.kpis[2].value = '555.05M';
D.kpis[2].sub = 'TT 368.43M + Meta 146.69M + YT 39.93M';
// kpi[3]: 挑战赛 - no change

// === OVERVIEW ===
D.overview[0].current = '2.11%';
D.overview[0].date = '11/23';
D.overview[1].current = '9.09%';
D.overview[1].date = '11/21';
D.overview[1].status = 'red';
D.overview[2].current = '5.54%';
D.overview[2].date = '11/21';
D.overview[3].current = '1.38%';
D.overview[3].date = '11/21';
D.overview[4].current = '$170,714.67 cumulative';
D.overview[4].date = '11/21';
D.overview[5].current = '$58,006.37 cumulative';
D.overview[5].date = '11/22';
D.overview[6].current = '146.69M cumulative';
D.overview[6].date = '11/22';
D.overview[7].current = '1.76M';
D.overview[7].date = '11/21';
D.overview[8].current = '22.84%';
D.overview[8].date = '11/21';

// === GOOGLE SOV - add 11/21, 11/22, 11/23 ===
D.googleSov.labels.push('11/21', '11/22', '11/23');
D.googleSov.brand.push(2.07, 2.08, 2.11);
D.googleSov.product.push(9.09, 9.09, 9.09);
D.googleSov.brandNote = 'Brand SOV latest 2.11% (11/23) / 品牌 SOV 最新 2.11%（11/23）';
D.googleSov.productNote = 'Product SOV latest 9.09% (11/21-23) / 产品 SOV 最新 9.09%（11/21-23）';

// === COMPETITOR - add 11/21, 11/22, 11/23 ===
D.competitorCompare.chartLabels.push('11/21', '11/22', '11/23');
D.competitorCompare.datasets[0].data.push(9.09, 9.09, 9.09);
D.competitorCompare.note = 'Google Trends 对比关键词 / Comparison: CAMON Slim vs OPPO Reno 16 F, VIVO V80 Lite, Redmi Note 17 Pro · 截至 11/23';

// === TT SOV - add 11/20, 11/21 ===
D.ttSov.labels.push('11/20', '11/21');
D.ttSov.vvData.push(6.43, 5.54);
D.ttSov.searchData.push(1.25, 1.38);
D.ttSov.note = 'VV SOV latest 5.54% (11/21); Search SOV latest 1.38% (11/21). 11/22 source cells blank / TikTok声量最新数据到11/21，11/22源表尚未回填';

// === SPEND - add 11/20, 11/21 ===
D.spend.labels.push('11/20', '11/21');
D.spend.dailySpend.push(3636.85, 3554.45);
D.spend.spendProgress.push(0.976038203592814, 0.997322335329341);
D.spend.exposureProgress.push(null, null);

// === CONSIDERATION - add 11/18, 11/19, 11/20, 11/21 ===
D.consideration.labels.push('11/18', '11/19', '11/20', '11/21');
D.consideration.brandData.push(2005412, 2010821, 1973770, 1762500);
D.consideration.industryData.push(5390632, 5437111, 5453325, 5504046);
D.consideration.note = 'Brand Consideration latest 1.76M (11/21). / 本品牌 Consideration 最新 1.76M（11/21）。';

// === TOP VIDEOS (update names from source) ===
D.topVideos = [
    { rank: 1, name: 'FB | Supe Zoom', url: 'https://www.tiktok.com/@tecnomobileth/video/7699071414929788181', value: '22.9M', gold: true },
    { rank: 2, name: 'Reveal | 4 BA', url: 'https://www.tiktok.com/@tecnomobileth/video/7699103279812185352', value: '18.1M', gold: false },
    { rank: 3, name: 'JMNK | Supe-Zoom', url: 'https://www.tiktok.com/@tecnomobileth/video/7699072176372059413', value: '7.1M', gold: false },
    { rank: 4, name: 'MagBadge | ForceBook', url: 'https://www.tiktok.com/@tecnomobileth/video/7701994721069010177', value: '6.9M', gold: false },
    { rank: 5, name: 'In-house | MagBadge Unbox', url: 'https://www.tiktok.com/@tecnomobileth/video/7699105143987408136', value: '6.4M', gold: false }
];

// === KOL VIDEOS (update from source) ===
D.kolVideos = [
    { rank: '#1', name: 'Teaser | CN6 | Unboxing | StepGeek', url: 'https://www.tiktok.com/@naduchstepgeek/video/7700943845537680648', value: '9.2M', gold: true },
    { rank: '#2', name: 'Teaser | CN6 | Unboxing | Driosan', url: 'https://www.tiktok.com/@droidsans/video/7701213212548631829', value: '9.1M', gold: false },
    { rank: '#3', name: 'KOL Launch Event | tonyon', url: 'https://www.tiktok.com/@tonyon__/video/7703799128647568658', value: '3.5M', gold: false },
    { rank: '#4', name: 'Teaser | CN6 | Unboxing | Guzapam', url: 'https://www.tiktok.com/@guzappam/video/7701207813594434834?_r=1&_t=ZS-9AtggtfCrI6', value: '3.6M', gold: false },
    { rank: '#5', name: 'Fashion KOL | konnenaruk', url: 'https://www.tiktok.com/@konnenaruk/video/7704163691582754068?_r=1&_t=ZS-9B7lqVD2EpY', value: '3.5M', gold: false }
];

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
console.log(`Spend: labels=${D.spend.labels.length}, daily=${D.spend.dailySpend.length}, progress=${D.spend.spendProgress.length}, exposure=${D.spend.exposureProgress.length}`);
if (D.spend.labels.length !== D.spend.dailySpend.length || D.spend.labels.length !== D.spend.spendProgress.length) {
    console.error('❌ Spend mismatch!'); process.exit(1);
}
console.log(`Consideration: labels=${D.consideration.labels.length}, brand=${D.consideration.brandData.length}, industry=${D.consideration.industryData.length}`);
if (D.consideration.labels.length !== D.consideration.brandData.length) {
    console.error('❌ Consideration mismatch!'); process.exit(1);
}
console.log('✅ All array lengths match!');

// === WRITE ===
const newJson = JSON.stringify(D, null, 2);
const newHtml = html.replace(/const D = \{[\s\S]*?\n\}\n/, 'const D = ' + newJson + '\n');
fs.writeFileSync('index.html', newHtml);
console.log('✅ Dashboard updated to 11/23');
console.log(`   Google SOV: ${D.googleSov.labels.length} dates (to 11/23)`);
console.log(`   TT SOV: ${D.ttSov.labels.length} dates (to 11/21)`);
console.log(`   TT Spend: $170,714.67 cumulative (to 11/21)`);
console.log(`   Meta Spend: $58,006.37 cumulative (to 11/22)`);
console.log(`   YT Spend: $9,543.53 cumulative (to 11/22)`);
console.log(`   Total Impressions: 555.05M (TT 368.43M + Meta 146.69M + YT 39.93M)`);
console.log(`   Consideration: 1.76M (11/21)`);

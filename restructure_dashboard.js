#!/usr/bin/env node
/**
 * Restructure dashboard: Hero = 4 KPIs, KPI cards = 4 metrics
 */
const fs = require('fs');

const html = fs.readFileSync('index.html', 'utf8');
const match = html.match(/const D = (\{[\s\S]*?\n\})\n/);
if (!match) {
    console.log('ERROR: Could not find D object');
    process.exit(1);
}

const D = JSON.parse(match[1]);

// ============================================================
// CALCULATE 全网总曝光
// ============================================================
const ttDaily = [417245, 512731, 1058612, 1980509, 2304924, 4160130, 4104540, 5142215,
    4945262, 4493444, 6665384, 8508983, 7978743, 5313511, 7226108,
    10589341, 16758489, 10552314, 19134836, 23463392, 45831076,
    18704152, 16891273, 10283289, 12229637, 13019465, 16368239,
    18172809, 18165959, 13596202];
const ttTotal = ttDaily.reduce((a, b) => a + b, 0);

const metaDaily = [389920, 1324958, 1615904, 2791710, 2432241, 3800623, 4061030, 4418270,
    3907302, 3967229, 4332156, 4024103, 5026959, 3616780, 6556499, 7312020,
    8654870, 16037402, 4933802, 5375550, 5602967, 2470857, 3465317, 4437635,
    5746827, 7219537, 7447018, 7323390, 4828489, 5179382];
const metaTotal = metaDaily.reduce((a, b) => a + b, 0);

const ytDaily = [67031, 1454760, 1763049, 1670956, 1713798, 1573422, 1303401, 5173269,
    5780003, 5292973, 5367570, 5122405, 14572, 85893, 112207, 111709, 113383, 60787];
const ytTotal = ytDaily.reduce((a, b) => a + b, 0);

const grandTotal = ttTotal + metaTotal + ytTotal;
console.log(`TT: ${(ttTotal/1e6).toFixed(2)}M, Meta: ${(metaTotal/1e6).toFixed(2)}M, YT: ${(ytTotal/1e6).toFixed(2)}M`);
console.log(`全网总曝光: ${(grandTotal/1e6).toFixed(2)}M`);

// ============================================================
// UPDATE HERO: 4 KPIs
// ============================================================
D.hero.stats = [
    {
        label: 'Google Product SOV',
        value: '11.76%'
    },
    {
        label: 'TikTok VV SOV',
        value: '10.83%'
    },
    {
        label: 'TikTok Search SOV',
        value: '1.30%'
    },
    {
        label: 'Consideration',
        value: '2.05M'
    }
];

D.hero.desc = 'Google Product SOV 11.76% (11/18); TikTok VV SOV 10.83% and Search SOV 1.30% (11/15); Consideration 2.05M (11/15), Rate 15.10%.';

// ============================================================
// UPDATE KPI CARDS: 4 metrics
// ============================================================
D.kpis = [
    {
        label: 'Google Brand SOV',
        statusDot: 'status-green',
        value: '2.09%',
        trend: '↑',
        trendClass: 'trend-up',
        sub: 'As of / 截至 11/18',
        borderLeft: '#10b981',
        valueColor: '#10b981'
    },
    {
        label: 'Consideration Rate',
        statusDot: 'status-green',
        value: '15.10%',
        trend: '↑',
        trendClass: 'trend-up',
        sub: 'Consideration / TECNO曝光 · As of / 截至 11/15',
        borderLeft: '#10b981',
        valueColor: '#10b981'
    },
    {
        label: '全网总曝光 / Total Impressions',
        statusDot: 'status-green',
        value: `${(grandTotal/1e6).toFixed(2)}M`,
        trend: '↑',
        trendClass: 'trend-up',
        sub: `TT ${(ttTotal/1e6).toFixed(2)}M + Meta ${(metaTotal/1e6).toFixed(2)}M + YT ${(ytTotal/1e6).toFixed(2)}M`,
        borderLeft: '#10b981',
        valueColor: '#10b981'
    },
    {
        label: '挑战赛曝光 / Challenge Views',
        statusDot: 'status-green',
        value: '11.8M',
        trend: '↑',
        trendClass: 'trend-up',
        sub: '12天 · 超 POVA 8 Benchmark 5.8M',
        borderLeft: '#10b981',
        valueColor: '#10b981'
    }
];

// ============================================================
// UPDATE ALERT BANNER
// ============================================================
D.alertBanner = '数据更新至 11/18：Google Product SOV 11.76%（11/18），TT VV SOV 10.83%（11/15），Consideration 2.05M（11/15），Consideration Rate 15.10%（11/15），挑战赛 12天 3,583 视频已超 POVA 8 Benchmark。';

// ============================================================
// VALIDATE & WRITE
// ============================================================
console.log(`\n✅ Hero stats: ${D.hero.stats.length} items`);
console.log(`✅ KPI cards: ${D.kpis.length} items`);
console.log(`   KPI 1: ${D.kpis[0].label} = ${D.kpis[0].value}`);
console.log(`   KPI 2: ${D.kpis[1].label} = ${D.kpis[1].value}`);
console.log(`   KPI 3: ${D.kpis[2].label} = ${D.kpis[2].value}`);
console.log(`   KPI 4: ${D.kpis[3].label} = ${D.kpis[3].value}`);

const newDJson = JSON.stringify(D, null, 2);
const newHtml = html.replace(/const D = \{[\s\S]*?\n\}\n/, `const D = ${newDJson}\n`);

fs.writeFileSync('index.html', newHtml);
console.log(`\n✅ Dashboard updated and written to index.html`);

// Final validation
try {
    const newMatch = newHtml.match(/const D = (\{[\s\S]*?\n\})\n/);
    const newD = JSON.parse(newMatch[1]);
    console.log(`✅ Final JS parse OK`);
    console.log(`   Hero stats: ${newD.hero.stats.length}`);
    console.log(`   KPI cards: ${newD.kpis.length}`);
    console.log(`\n🎉 All validations passed!`);
} catch(e) {
    console.log('❌ Final parse error:', e.message);
    process.exit(1);
}

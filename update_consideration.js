#!/usr/bin/env node
/**
 * Update dashboard with 11/15 Consideration data
 */
const fs = require('fs');

const html = fs.readFileSync('index.html', 'utf8');

// Extract D object
const match = html.match(/const D = (\{[\s\S]*?\n\})\n/);
if (!match) {
    console.log('ERROR: Could not find D object');
    process.exit(1);
}

let D;
try {
    D = JSON.parse(match[1]);
    console.log('✅ Parsed D object:', Object.keys(D).length, 'keys');
} catch(e) {
    console.log('❌ JSON parse error:', e.message);
    console.log('Around char:', match[1].substring(e.position - 100, e.position + 100));
    process.exit(1);
}

// ============================================================
// UPDATE: Consideration 11/15
// ============================================================
// Add 11/15 to consideration chart
D.consideration.labels.push('11/15');
D.consideration.brandData.push(2052898);
D.consideration.industryData.push(5355370);

// Calculate 11/15 rate: 2,052,898 / 13,596,202 = 15.10%
const rate_1115 = Math.round(2052898 / 13596202 * 10000) / 100;
D.consideration.rateData.push(rate_1115);
D.consideration.rateLabels.push('11/15');
D.consideration.latestRate = rate_1115;
D.consideration.note = `Brand Consideration latest 2.05M (11/15). / 本品牌 Consideration 最新 2.05M（11/15）。`;
D.consideration.rateNote = `Consideration Rate = Consideration / TECNO总曝光，最新 ${rate_1115}% (11/15)`;

// Update KPI card
D.kpis[4].value = '2.05M';
D.kpis[4].sub = 'CAMON Slim KPI 目标 1.5M+ · As of / 截至 11/15';

D.kpis[5].value = `${rate_1115}%`;
D.kpis[5].sub = 'Consideration / TECNO曝光 · As of / 截至 11/15';

// Update hero
D.hero.desc = `Google Brand SOV 2.09% and Product SOV 11.76% (11/18); TT VV SOV 10.83% and Search SOV 1.30% (11/15); Meta impressions 5.18M (11/17); Consideration 2.05M (11/15), Rate ${rate_1115}%.`;
D.hero.stats[3].value = '2.05M';

// Update overview
D.overview[7].current = '2.05M';
D.overview[7].date = '11/15';
D.overview[8].current = `${rate_1115}%`;
D.overview[8].date = '11/15';

// Update alert banner
D.alertBanner = `数据更新至 11/18：Google Product SOV 11.76%（11/18），TT VV SOV 10.83%（11/15），Consideration 2.05M（11/15），Consideration Rate ${rate_1115}%（11/15），挑战赛 12天 3,583 视频已超 POVA 8 Benchmark。`;

// ============================================================
// VALIDATE
// ============================================================
console.log(`\n--- Validation ---`);
console.log(`Consideration: labels=${D.consideration.labels.length}, brand=${D.consideration.brandData.length}, industry=${D.consideration.industryData.length}`);
console.log(`Rate: labels=${D.consideration.rateLabels.length}, rate=${D.consideration.rateData.length}`);

if (D.consideration.labels.length !== D.consideration.brandData.length || 
    D.consideration.labels.length !== D.consideration.industryData.length) {
    console.log('❌ Consideration array mismatch!');
    process.exit(1);
}
if (D.consideration.rateLabels.length !== D.consideration.rateData.length) {
    console.log('❌ Rate array mismatch!');
    process.exit(1);
}

console.log(`\n✅ 11/15 Consideration: 2,052,898`);
console.log(`✅ 11/15 TT Exposure: 13,596,202`);
console.log(`✅ 11/15 Consideration Rate: ${rate_1115}%`);

// ============================================================
// WRITE BACK
// ============================================================
const newDJson = JSON.stringify(D, null, 2);
const newHtml = html.replace(/const D = \{[\s\S]*?\n\}\n/, `const D = ${newDJson}\n`);

fs.writeFileSync('index.html', newHtml);
console.log(`\n✅ Dashboard updated and written to index.html`);

// Final validation
try {
    const newMatch = newHtml.match(/const D = (\{[\s\S]*?\n\})\n/);
    const newD = JSON.parse(newMatch[1]);
    console.log(`✅ Final JS parse OK`);
    console.log(`   consideration labels: ${newD.consideration.labels.length}`);
    console.log(`   rate labels: ${newD.consideration.rateLabels.length}`);
    console.log(`   latest rate: ${newD.consideration.latestRate}%`);
    console.log(`   kpi[4] value: ${newD.kpis[4].value}`);
    console.log(`   kpi[5] value: ${newD.kpis[5].value}`);
    console.log(`\n🎉 All validations passed!`);
} catch(e) {
    console.log('❌ Final parse error:', e.message);
    process.exit(1);
}

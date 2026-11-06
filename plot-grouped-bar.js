// plot-grouped-bar.js — Observable Plot grouped-bar starter
// Source: art_01M6MH8DFE1KD1GQA0A0VTGENT rev 2 (checklist, documented-not-tested)
// Run in an Observable notebook cell, or Node >=18 ESM after:
//   npm install @observablehq/plot d3

import * as Plot from "@observablehq/plot";

// --- RULE 1: coerce types at load time (checklist: "coerce numbers and dates") ---
// Strings → ordinal scale, numbers → linear, dates → utc. Wrong type = wrong scale.
const raw = [
  { year: 2021, region: "North", sales: 42 },
  { year: 2021, region: "South", sales: 38 },
  { year: 2022, region: "North", sales: 55 },
  { year: 2022, region: "South", sales: 61 },
  { year: 2023, region: "North", sales: 70 },
  { year: 2023, region: "South", sales: 48 },
];
// year is kept as a number here; to treat it as a category coerce to string:
const data = raw.map(d => ({ ...d, year: String(d.year) }));

// --- RULE 2: band scale on category axis (checklist: "bar mark needs a band scale") ---
// barY infers a band scale on x when x values are strings — confirmed by coercion above.
// BASELINE: remove the String() cast above and observe the scale type change.

// --- RULE 3: group transform for one value per category (checklist: "groupX most often") ---
// Here the data is already one row per (year, region); no group needed.
// To count rows instead, replace the marks block with:
//   Plot.barY(data, Plot.groupX({ y: "count" }, { x: "year", fill: "region" }))

// --- RULE 4: stack is implicit in barY when only one y value is given (checklist: "stack implicit") ---
// Providing both fx (facet) and fill avoids stacking; regions appear side-by-side.
// To see stacked form: remove fx and keep fill. The stack transform fires automatically.

const chart = Plot.plot({
  // --- RULE 5: axis label and tickFormat (checklist: "tickFormat, label") ---
  x: {
    label: "Year",
    // tickFormat omitted — string years print as-is; add tickFormat: d => `'${d.slice(2)}` to shorten
  },
  y: {
    label: "Sales (units)",
    // --- RULE 6: zero option extends domain to zero (checklist: "zero extends domain") ---
    zero: true,
  },
  // --- RULE 7: grid for readability (checklist: "grid") ---
  grid: true,
  color: { legend: true },

  marks: [
    // --- RULE 8: text mark labels bars directly (checklist: "text mark…label bars") ---
    Plot.barY(data, { x: "year", y: "sales", fill: "region", fx: "region" }),
    Plot.text(
      data,
      {
        x: "year",
        y: "sales",
        fx: "region",
        text: d => String(d.sales),
        dy: -6,           // lift label above bar top
        fontSize: 11,
        // --- RULE 9: check text at the sizes you ship (checklist: "Inspect the result") ---
        // Plot does not measure text exactly — verify visually at your target viewport.
      }
    ),
    // Default axes are added automatically; to remove y-axis: declare axisY(null) or set y.axis = null
  ],
});

// In a browser notebook: return chart;
// In Node: use plot's SVG string output
export { chart, data };
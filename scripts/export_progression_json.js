/* Exporte progression-data.js en JSON pour les scripts Python. */
const fs = require("fs");
const path = require("path");

const window = {};
const dataPath = path.join(__dirname, "..", "assets", "js", "progression-data.js");
eval(fs.readFileSync(dataPath, "utf-8"));

const outDir = path.join(__dirname, "..", "assets", "data");
if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

const outPath = path.join(outDir, "progression.json");
fs.writeFileSync(outPath, JSON.stringify(window.PROGRESSION_ANNUELLE, null, 2));
console.log(`✓ ${path.relative(path.join(__dirname, ".."), outPath)}`);

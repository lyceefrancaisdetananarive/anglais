/* ============================================================
   generate_pdf_library.js
   Génère pdf-imprimables/index.html à partir de progression.json,
   organisé par cycle/niveau, avec une carte par séquence.
   ============================================================ */

const fs = require("fs");
const path = require("path");

const PROG = JSON.parse(fs.readFileSync(
  path.join(__dirname, "..", "assets", "data", "progression.json"), "utf-8"
));

function slugify(s) {
  return String(s)
    .toLowerCase()
    .normalize("NFD").replace(/[̀-ͯ]/g, "")
    .replace(/['']/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

function esc(s) {
  if (s == null) return "";
  return String(s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

function ficheFilename(niveauKey, seqTitre) {
  const safeDir = niveauKey.replace(/-/g, "_");
  return `fiche_${safeDir}_${slugify(seqTitre).replace(/-/g, "_")}.pdf`;
}

function fileSizeKb(filename) {
  const p = path.join(__dirname, "..", "pdf-imprimables", filename);
  if (!fs.existsSync(p)) return null;
  return Math.round(fs.statSync(p).size / 1024);
}

const NIVEAU_LABELS = {
  "6e":         { label: "6ᵉ",          cecrl: "A1",   cycle: "college" },
  "4e":         { label: "4ᵉ LV1",      cecrl: "A2+",  cycle: "college" },
  "4e-non-si":  { label: "4ᵉ NON SI",   cecrl: "B1",   cycle: "college" },
  "4e-lce":     { label: "4ᵉ LCE",      cecrl: "A2+",  cycle: "college" },
  "3e":         { label: "3ᵉ LV1",      cecrl: "A2+/B1", cycle: "college" },
  "3e-non-si":  { label: "3ᵉ NON SI",   cecrl: "B1",   cycle: "college" },
  "1ere":       { label: "1ʳᵉ euro",    cecrl: "B2",   cycle: "lycee" },
  "terminale":  { label: "Tᵉ LVA",      cecrl: "B2/C1", cycle: "lycee" },
};

const CYCLE_ORDER = {
  "college": ["6e", "4e", "4e-non-si", "4e-lce", "3e", "3e-non-si"],
  "lycee":   ["1ere", "terminale"],
};

const NIVEAU_ICONS = {
  "6e": "ph-baby",
  "4e": "ph-student",
  "4e-non-si": "ph-globe",
  "4e-lce": "ph-flag",
  "3e": "ph-graduation-cap",
  "3e-non-si": "ph-globe",
  "1ere": "ph-book-open",
  "terminale": "ph-medal",
};

// --------------------------------------------------------------
//   Render
// --------------------------------------------------------------
function renderCard(niveauKey, seq) {
  const filename = ficheFilename(niveauKey, seq.titre);
  const sizeKb = fileSizeKb(filename) || 0;
  const lvl = NIVEAU_LABELS[niveauKey];
  const icon = NIVEAU_ICONS[niveauKey] || "ph-file-text";

  return `
        <article class="fiche-lib-card glass-card">
          <div class="fiche-lib-card__head">
            <span class="fiche-lib-card__niveau">
              <i class="ph ${icon}" aria-hidden="true"></i>
              ${esc(lvl.label)}
            </span>
            <span class="fiche-lib-card__cecrl">${esc(seq.cecrl || lvl.cecrl)}</span>
          </div>
          <h3 class="fiche-lib-card__title">${esc(seq.titre)}</h3>
          <p class="fiche-lib-card__theme">${esc(seq.theme || "")}</p>
          <div class="fiche-lib-card__meta">
            <span><i class="ph ph-file-pdf"></i> ${sizeKb} Ko</span>
            <span><i class="ph ph-calendar-blank"></i> ${esc(seq.periode || "")}</span>
          </div>
          <div class="fiche-lib-card__actions">
            <a href="${esc(filename)}" target="_blank" rel="noopener" class="btn btn--accent">
              <i class="ph ph-download-simple"></i> Télécharger
            </a>
            <a href="../sequences/${niveauKey}/${slugify(seq.titre)}.html" class="btn btn--secondary">
              <i class="ph ph-arrow-square-out"></i> Voir la séquence
            </a>
          </div>
        </article>`;
}

function renderNiveauSection(niveauKey) {
  const data = PROG[niveauKey];
  if (!data) return "";
  const lvl = NIVEAU_LABELS[niveauKey];
  const cards = data.sequences.map(seq => renderCard(niveauKey, seq)).join("");

  return `
      <section class="fiche-lib-niveau" id="niv-${niveauKey}" aria-labelledby="niv-${niveauKey}-title">
        <header class="fiche-lib-niveau__header">
          <h3 id="niv-${niveauKey}-title" class="fiche-lib-niveau__title">
            <i class="ph ${NIVEAU_ICONS[niveauKey]} ph-icon ph-icon--lg ph-icon--bf"></i>
            ${esc(lvl.label)}
            <span class="fiche-lib-niveau__count">${data.sequences.length} fiches</span>
          </h3>
          <p class="fiche-lib-niveau__intro">${esc(data.intro ? data.intro.replace(/<[^>]+>/g, "") : "")}</p>
        </header>
        <div class="cards-grid">${cards}</div>
      </section>`;
}

function renderCycle(cycleKey, label, icon, intro) {
  const niveaux = CYCLE_ORDER[cycleKey].map(renderNiveauSection).join("");
  return `
    <div class="fiche-lib-cycle">
      <header class="cycle-block__header">
        <h2 class="cycle-block__title">
          <i class="ph ${icon} ph-icon ph-icon--xl ph-icon--bf"></i> ${label}
        </h2>
        <p class="cycle-block__intro">${intro}</p>
      </header>
      ${niveaux}
    </div>`;
}

// Compteurs
let totalFiches = 0;
Object.values(PROG).forEach(d => { totalFiches += d.sequences.length; });

const html = `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Bibliothèque PDF — Espace Anglais — LFT</title>
  <meta name="description" content="Bibliothèque complète des ${totalFiches} fiches d'activité imprimables d'anglais : Cycle 4 (6e, 4e, 3e), Section Internationale, LCE et Lycée. Mise en page institutionnelle AEFE — Marque État." />
  <meta name="theme-color" content="#000091" />
  <link rel="icon" type="image/png" href="../assets/img/logo-lft.png" />
  <link rel="stylesheet" href="../assets/css/style.css" />
  <link rel="preload" href="../assets/fonts/Marianne-Regular.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="preload" href="../assets/fonts/Marianne-Bold.woff2" as="font" type="font/woff2" crossorigin />
</head>
<body>

  <a href="#main-content" class="skip-link">Aller au contenu principal</a>

  <header class="site-header" role="banner">
    <div class="site-header__top">
      <div class="container site-header__top-inner">
        <span>République française · AEFE · Établissement en gestion directe</span>
        <a href="../index.html">Retour à l'accueil</a>
      </div>
    </div>
    <div class="site-header__main">
      <div class="container site-header__main-inner">
        <a href="../index.html" class="brand">
          <img src="../assets/img/logo-lft.png" alt="" />
          <div class="brand-text">
            <div class="line1">Lycée Français de Tananarive</div>
            <div class="line2">Bibliothèque PDF — Mme FALIMANANA</div>
            <div class="line3">${totalFiches} fiches d'activité imprimables</div>
          </div>
        </a>
        <nav class="nav-main" aria-label="Navigation principale">
          <a href="../index.html">Accueil</a>
          <a href="../niveaux/6e.html">6<sup>e</sup></a>
          <a href="../niveaux/4e.html">4<sup>e</sup></a>
          <a href="../niveaux/3e.html">3<sup>e</sup></a>
          <a href="index.html" aria-current="page">Bibliothèque</a>
        </nav>
      </div>
    </div>
  </header>

  <main id="main-content">
    <section class="hero hero--compact">
      <div class="container">
        <h1 class="hero__title">Bibliothèque de fiches d'activité</h1>
        <p class="hero__subtitle">
          <strong>${totalFiches} fiches</strong> au format PDF, prêtes à imprimer
          ou à projeter. Mise en page institutionnelle <strong>AEFE — Marque
          État</strong> (logos officiels, police Marianne, palette tricolore),
          format <strong>manuel scolaire</strong> avec QR code vers
          l'activité d'entraînement en ligne.
        </p>
      </div>
    </section>

    <div class="container">
      ${renderCycle("college", "Collège", "ph-backpack",
        "Cycle 3 (6ᵉ) et Cycle 4 (5ᵉ-3ᵉ) · Niveaux A1 → B1 du CECRL.")}
      ${renderCycle("lycee", "Lycée", "ph-graduation-cap",
        "Voie générale · Section européenne · Niveaux B1 → C1 du CECRL.")}
    </div>
  </main>

  <footer class="site-footer" role="contentinfo">
    <div class="container">
      <div class="site-footer__bottom">
        <span class="tricolore-bar" aria-hidden="true"></span>
        <p>© 2026 Lycée Français de Tananarive · Mme Salamo FALIMANANA · <a href="mailto:salamo.falimanana@egd.mg" style="color: var(--lft-magenta-light);">salamo.falimanana@egd.mg</a></p>
      </div>
    </div>
  </footer>

  <script src="../assets/js/analytics.js" defer></script>
</body>
</html>
`;

const outPath = path.join(__dirname, "..", "pdf-imprimables", "index.html");
fs.writeFileSync(outPath, html, "utf-8");
console.log(`✓ ${path.relative(path.join(__dirname, ".."), outPath)} (${totalFiches} fiches)`);

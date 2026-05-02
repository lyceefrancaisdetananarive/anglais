/* ============================================================
   generate_sequence_pages.js
   Génère 1 page HTML par séquence à partir de progression-data.js.
   Sortie : sequences/{niveauSlug}/{seqSlug}.html
   ============================================================ */

const fs = require("fs");
const path = require("path");

// ---- Charger les données ---------------------------------
// progression-data.js définit window.PROGRESSION_ANNUELLE
const window = {};
const dataPath = path.join(__dirname, "..", "assets", "js", "progression-data.js");
const dataCode = fs.readFileSync(dataPath, "utf-8");
eval(dataCode);
const PROG = window.PROGRESSION_ANNUELLE;

// ---- Templates grammaticaux (exemples canoniques) -------
const GRAMMAR_TEMPLATES = JSON.parse(fs.readFileSync(
  path.join(__dirname, "..", "assets", "data", "grammar-templates.json"),
  "utf-8"
));

// ---- Lexique enrichi par séquence (titre → [en, ipa, fr]) ------
const LEXIQUE_SEQUENCES = JSON.parse(fs.readFileSync(
  path.join(__dirname, "..", "assets", "data", "lexique-sequences.json"),
  "utf-8"
));

// ---- Documents supports authentiques (texte / dialogue / extrait) ---
const DOCUMENTS_SUPPORTS = JSON.parse(fs.readFileSync(
  path.join(__dirname, "..", "assets", "data", "documents-supports.json"),
  "utf-8"
));

// ---- Repères culturels enrichis (contexte + faits + figures + lieux) ----
const REPERES_CULTURELS = JSON.parse(fs.readFileSync(
  path.join(__dirname, "..", "assets", "data", "reperes-culturels.json"),
  "utf-8"
));

function getLexiqueFor(seqTitre) {
  const rows = LEXIQUE_SEQUENCES[seqTitre];
  return Array.isArray(rows) ? rows : null;
}

function getSupportFor(seqTitre) {
  const s = DOCUMENTS_SUPPORTS[seqTitre];
  return (s && typeof s === "object" && s.content) ? s : null;
}

function getReperesFor(seqTitre) {
  const r = REPERES_CULTURELS[seqTitre];
  return (r && typeof r === "object" && r.context) ? r : null;
}

function matchGrammarTemplate(langueRaw) {
  const langue = String(langueRaw || "")
    .toLowerCase()
    .replace(/<[^>]+>/g, " ")
    .replace(/[^\p{L}\p{N}\s']/gu, " ");
  let bestKey = "_default";
  let bestScore = 0;
  for (const [key, tpl] of Object.entries(GRAMMAR_TEMPLATES)) {
    if (!tpl.keywords || key === "_default") continue;
    let score = 0;
    for (const kw of tpl.keywords) {
      // mot-clé entier ou substring case-insensitive
      const re = new RegExp(`\\b${kw.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\b`, "i");
      if (re.test(langue)) score += kw.length; // pondère par longueur
    }
    if (score > bestScore) {
      bestScore = score;
      bestKey = key;
    }
  }
  return GRAMMAR_TEMPLATES[bestKey];
}

// ---- Mapping niveau → dossier sequences ------------------
const NIVEAU_TO_DIR = {
  "6e": "6e",
  "4e": "4e",
  "4e-non-si": "4e-non-si",
  "4e-lce": "4e-lce",
  "3e": "3e",
  "3e-non-si": "3e-non-si",
  "1ere": "1ere",
  "terminale": "terminale",
};

// ---- Mapping niveau → libellé classe + page niveau --------
const NIVEAU_LABEL = {
  "6e":         { court: "6ᵉ", complet: "6ᵉ — Cycle 3",
                  pageHref: "../../niveaux/6e.html",       breadcrumb: "6ᵉ" },
  "4e":         { court: "4ᵉ LV1", complet: "4ᵉ — Cycle 4 · LV1",
                  pageHref: "../../niveaux/4e.html",       breadcrumb: "4ᵉ LVA" },
  "4e-non-si":  { court: "4ᵉ NON SI", complet: "4ᵉ Section Internationale",
                  pageHref: "../../niveaux/non-si.html",   breadcrumb: "Section Internationale" },
  "4e-lce":     { court: "4ᵉ LCE", complet: "4ᵉ Langues et Cultures Européennes",
                  pageHref: "../../niveaux/lce.html",      breadcrumb: "4ᵉ LCE" },
  "3e":         { court: "3ᵉ LV1", complet: "3ᵉ — Cycle 4 · Préparation au DNB",
                  pageHref: "../../niveaux/3e.html",       breadcrumb: "3ᵉ LVA" },
  "3e-non-si":  { court: "3ᵉ NON SI", complet: "3ᵉ Section Internationale",
                  pageHref: "../../niveaux/non-si.html",   breadcrumb: "Section Internationale" },
  "1ere":       { court: "1ʳᵉ euro", complet: "1ʳᵉ — Section européenne · APPROF LING + DNL SVT",
                  pageHref: "../../niveaux/1ere.html",     breadcrumb: "1ʳᵉ euro" },
  "terminale":  { court: "Tᵉ LVA", complet: "Terminale — 8 axes culturels du Bac",
                  pageHref: "../../niveaux/terminale.html", breadcrumb: "Terminale LVA" },
};

// ---- Construction automatique du nom de fiche PDF ---------
// Doit rester synchronisé avec generate_fiches_manuel.py (Python).
function autoFicheFilename(niveauKey, seqTitre) {
  const safeDir = niveauKey.replace(/-/g, "_");
  return `fiche_${safeDir}_${slugify(seqTitre).replace(/-/g, "_")}.pdf`;
}

// Overrides : fiches enrichies avec un contenu pédagogique riche
// (style manuel, contenu authentique). Pour les autres séquences,
// le nom est calculé automatiquement.
const PDF_OVERRIDES = {
  "Welcome to Big Ben Academy!":   "fiche_6e_welcome_big_ben.pdf",
  "Stuck at Big Bay School":       "fiche_4e_stuck_at_big_bay_school.pdf",
  "The Giver — Lois Lowry (1993)": "fiche_4e_non_si_the_giver.pdf",
};

// ============================================================
//   Helpers
// ============================================================
function slugify(str) {
  return String(str)
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

// stripHtml() : retire les balises HTML mais garde le texte.
// Utilisé pour les contenus de progression-data qui peuvent contenir
// <em>, <strong> etc. mais qui sont injectés dans des contextes texte.
function stripHtml(s) {
  if (s == null) return "";
  return String(s).replace(/<[^>]+>/g, "");
}

// escClean() : strip + escape — texte propre pour injection HTML
function escClean(s) {
  return esc(stripHtml(s));
}

// ============================================================
//   Trace écrite — leçon structurée à recopier dans le cahier
// ============================================================

// Découpe une string lexique en items individuels (split sur , ; ou ·)
function splitLexique(str) {
  if (!str) return [];
  return stripHtml(str)
    .split(/[,;·]/)
    .map(x => x.trim())
    .filter(Boolean);
}

// Construit un tableau de mémo lexical.
// Priorité au lexique enrichi (anglais + phonétique + français) ;
// fallback sur la liste basique extraite de seq.lexique.
function buildLexiqueMemo(seq) {
  const enriched = getLexiqueFor(seq.titre);
  if (enriched && enriched.length > 0) {
    const rows = enriched.map(([en, ipa, fr]) => `
        <tr>
          <td class="trace-lex__en">${esc(en)}</td>
          <td class="trace-lex__ipa">${esc(ipa)}</td>
          <td class="trace-lex__fr">${esc(fr)}</td>
        </tr>`).join("");
    return `
      <table class="trace-lex-table">
        <thead>
          <tr>
            <th>Anglais</th>
            <th>Phonétique</th>
            <th>Français</th>
          </tr>
        </thead>
        <tbody>${rows}</tbody>
      </table>`;
  }
  const items = splitLexique(seq.lexique);
  if (items.length === 0) {
    return `<p class="trace-empty">Lexique à compléter en classe avec l'enseignante.</p>`;
  }
  const cells = items.map(it => `<li>${esc(it)}</li>`).join("");
  return `<ul class="trace-lex-list">${cells}</ul>`;
}

// Construit la "règle" de grammaire avec :
// - libellé propre (sans HTML brut)
// - 3 exemples canoniques tirés de GRAMMAR_TEMPLATES selon seq.langue
function buildFaitsDeLangue(seq) {
  const langueClean = stripHtml(seq.langue || "structures grammaticales clés");
  const tpl = matchGrammarTemplate(seq.langue);
  return `
    <div class="trace-grammar">
      <p class="trace-grammar__rule">
        <strong>Structures à maîtriser :</strong> ${esc(langueClean)}.
      </p>
      <div class="trace-grammar__examples">
        <p class="trace-grammar__lead">
          <strong>${esc(tpl.label)}</strong> — exemples canoniques :
        </p>
        <ul>
          <li><span class="trace-grammar__type">Affirmative :</span> <em>${tpl.examples.affirmative}</em></li>
          <li><span class="trace-grammar__type">Négative :</span> <em>${tpl.examples.negative}</em></li>
          <li><span class="trace-grammar__type">Interrogative :</span> <em>${tpl.examples.interrogative}</em></li>
        </ul>
        <p class="trace-grammar__remark">
          <strong>Remarque :</strong> ${tpl.remark}
        </p>
      </div>
    </div>`;
}

// Construit la fiche culture enrichie : contexte + dates-clés +
// figures historiques + lieux. Si données enrichies absentes, fallback
// sur split du seq.culturel.
function buildReperesCulturels(seq) {
  const enriched = getReperesFor(seq.titre);
  if (enriched) {
    const facts = (enriched.key_facts || []).map(f =>
      `<li class="trace-fact">
        <span class="trace-fact__date">${esc(f.date)}</span>
        <span class="trace-fact__text">${esc(f.fact)}</span>
      </li>`).join("");
    const figures = (enriched.key_figures || []).map(p =>
      `<li class="trace-figure">
        <strong>${esc(p.name)}</strong> — <span>${esc(p.role)}</span>
      </li>`).join("");
    const places = (enriched.key_places || []).map(l =>
      `<li class="trace-place">
        <strong>${esc(l.place)}</strong> — <span>${esc(l.info)}</span>
      </li>`).join("");

    let html = `<p class="trace-culture__context">${esc(enriched.context)}</p>`;
    if (facts) {
      html += `<div class="trace-culture__block">
        <h4 class="trace-culture__bh"><i class="ph ph-calendar-blank"></i> Dates-clés à retenir</h4>
        <ul class="trace-culture__facts">${facts}</ul>
      </div>`;
    }
    if (figures) {
      html += `<div class="trace-culture__block">
        <h4 class="trace-culture__bh"><i class="ph ph-users"></i> Personnages-clés</h4>
        <ul class="trace-culture__people">${figures}</ul>
      </div>`;
    }
    if (places) {
      html += `<div class="trace-culture__block">
        <h4 class="trace-culture__bh"><i class="ph ph-map-pin"></i> Lieux à connaître</h4>
        <ul class="trace-culture__places">${places}</ul>
      </div>`;
    }
    return html;
  }

  // Fallback : si pas de données enrichies, split du seq.culturel
  const culturel = stripHtml(seq.culturel || "");
  if (!culturel) {
    return `<p class="trace-empty">Repères culturels à compléter en classe.</p>`;
  }
  const items = culturel.split(/[,;]/).map(x => x.trim()).filter(Boolean);
  if (items.length <= 1) {
    return `<p class="trace-culture__intro">${esc(culturel)}.</p>`;
  }
  const lis = items.map(it => `<li>${esc(it)}</li>`).join("");
  return `<p class="trace-culture__intro">Cette séquence aborde :</p>
    <ul class="trace-culture__list">${lis}</ul>`;
}

function renderDocumentSupport(seq) {
  const sup = getSupportFor(seq.titre);
  if (!sup) return ""; // section omise si pas de support

  const TYPE_LABEL = {
    text: "Document court",
    dialogue: "Dialogue",
    excerpt: "Extrait littéraire",
    article: "Article / document informatif",
  };
  const typeLabel = TYPE_LABEL[sup.type] || "Document support";

  const questions = (sup.questions || []).map((q, i) =>
    `<li class="doc-support__q"><span class="doc-support__qnum">${i + 1}.</span> ${q}</li>`
  ).join("");

  return `
    <section class="seq-section" id="document">
      <h2 class="seq-section__title"><i class="ph ph-text-aa" aria-hidden="true"></i> Document support</h2>
      <p class="seq-section__intro">
        <strong>Document à étudier en classe</strong> — texte court à
        lire en autonomie ou collectivement, suivi de questions de
        compréhension. Le document mobilise le lexique de la séquence
        et prépare aux faits de langue.
      </p>

      <article class="doc-support">
        <header class="doc-support__head">
          <span class="doc-support__type">${esc(typeLabel)}</span>
          <h3 class="doc-support__title">${esc(sup.title)}</h3>
        </header>
        <div class="doc-support__content">${sup.content}</div>
      </article>

      <div class="doc-support__questions">
        <h3 class="doc-support__qtitle">
          <i class="ph ph-question" aria-hidden="true"></i>
          Questions de compréhension
        </h3>
        <ol class="doc-support__qlist">${questions}</ol>
      </div>
    </section>`;
}

function renderTraceEcrite(seq) {
  return `
    <section class="seq-section" id="lecon">
      <h2 class="seq-section__title"><i class="ph ph-book-open" aria-hidden="true"></i> Cours / Leçon</h2>
      <p class="seq-section__intro">
        <strong>Trace écrite</strong> de la séquence — à recopier
        dans le cahier d'anglais et à mémoriser avant la tâche finale.
        Construite collectivement en classe à partir des documents
        supports, du lexique, des observations grammaticales et des
        repères culturels.
      </p>

      <div class="trace-grid">

        <article class="trace-card trace-card--lex">
          <header class="trace-card__head">
            <i class="ph ph-translate ph-icon ph-icon--bf" aria-hidden="true"></i>
            <h3 class="trace-card__title">Mémo lexical</h3>
          </header>
          <p class="trace-card__intro">
            <strong>Mots-clés à mémoriser</strong> pour cette séquence :
          </p>
          ${buildLexiqueMemo(seq)}
          <p class="trace-card__hint">
            Le lexique illustré complet (anglais · phonétique · français)
            figure dans la <a href="#fiches">fiche d'activité PDF</a>.
          </p>
        </article>

        <article class="trace-card trace-card--gram">
          <header class="trace-card__head">
            <i class="ph ph-ruler ph-icon ph-icon--bf" aria-hidden="true"></i>
            <h3 class="trace-card__title">Faits de langue — règle</h3>
          </header>
          ${buildFaitsDeLangue(seq)}
          <p class="trace-card__hint">
            Tableaux de conjugaison et exercices d'application
            dans la <a href="#fiches">fiche d'activité PDF</a>
            et l'<a href="#activite">activité d'entraînement</a>.
          </p>
        </article>

        <article class="trace-card trace-card--cult">
          <header class="trace-card__head">
            <i class="ph ph-globe ph-icon ph-icon--bf" aria-hidden="true"></i>
            <h3 class="trace-card__title">Repères culturels</h3>
          </header>
          ${buildReperesCulturels(seq)}
        </article>

      </div>

      <aside class="trace-tip">
        <i class="ph ph-lightbulb ph-icon ph-icon--accent" aria-hidden="true"></i>
        <p>
          <strong>Conseil de méthode :</strong> recopiez la trace écrite
          dans votre cahier le jour-même. Mémorisez le lexique sur
          plusieurs jours (5 mots par soir). Réinvestissez les structures
          dans l'<a href="#activite">activité d'entraînement</a> avant
          la tâche finale.
        </p>
      </aside>
    </section>`;
}

// Plan générique des séances en fonction des informations de séquence.
// Les élèves voient un fil pédagogique cohérent ; l'enseignante reste libre
// de l'adapter. Permet de respecter la structure « séquence → séances ».
function buildPlanSeances(seq) {
  const lex = stripHtml(seq.lexique || "lexique de la séquence");
  const langue = stripHtml(seq.langue || "structures grammaticales clés");
  const cult = stripHtml(seq.culturel || "repères culturels");
  return [
    { num: 1, titre: "Découverte (warm-up)",
      objectif: `Entrer dans le thème — ${escClean(seq.theme || seq.titre)}`,
      al: "CO · IO" },
    { num: 2, titre: "Lexique en contexte",
      objectif: `S'approprier le vocabulaire : ${esc(lex)}`,
      al: "CE · EOC" },
    { num: 3, titre: "Compréhension de l'écrit / oral",
      objectif: "Étudier un document support (texte, image, audio, vidéo)",
      al: "CE / CO" },
    { num: 4, titre: "Faits de langue",
      objectif: `Manipuler en contexte : ${esc(langue)}`,
      al: "EE · EOC" },
    { num: 5, titre: "Repères culturels",
      objectif: `Approfondir : ${esc(cult)}`,
      al: "CE · IO" },
    { num: 6, titre: "Préparation de la tâche finale",
      objectif: "Mobiliser les acquis pour produire",
      al: "EOC / EE" },
    { num: 7, titre: "Tâche finale (production)",
      objectif: escClean(seq.tache || "Production évaluée"),
      al: "EE / EOC" },
    { num: 8, titre: "Bilan et remédiation",
      objectif: "Auto-évaluation, retour collectif, remédiation",
      al: "IO" },
  ];
}

// ============================================================
//   Section ÉVALUATIONS — 3 PDF par séquence
// ============================================================
function evalFilename(type, niveauKey, seqTitre) {
  const safeDir = niveauKey.replace(/-/g, "_");
  return `eval_${type}_${safeDir}_${slugify(seqTitre).replace(/-/g, "_")}.pdf`;
}

function renderEvaluations(niveauKey, seq) {
  const diag = evalFilename("diagnostique", niveauKey, seq.titre);
  const form = evalFilename("formative",    niveauKey, seq.titre);
  const somm = evalFilename("sommative",    niveauKey, seq.titre);

  const card = (kind, title, color, intro, duree, moment, file) => `
        <article class="eval-card eval-card--${kind}">
          <header class="eval-card__head">
            <h3 class="eval-card__title">${esc(title)}</h3>
            <span class="eval-card__duree">${esc(duree)}</span>
          </header>
          <p class="eval-card__moment"><i class="ph ph-calendar-blank"></i> ${esc(moment)}</p>
          <p class="eval-card__intro">${intro}</p>
          <a href="../../pdf-imprimables/${esc(file)}" target="_blank" rel="noopener"
             class="btn btn--accent eval-card__btn">
            <i class="ph ph-download-simple"></i> Télécharger l'évaluation (PDF)
          </a>
        </article>`;

  return `
    <section class="seq-section" id="evaluation">
      <h2 class="seq-section__title"><i class="ph ph-chart-bar" aria-hidden="true"></i> Évaluations</h2>
      <p class="seq-section__intro">
        <strong>3 évaluations imprimables</strong> conçues pour cette séquence,
        en cohérence avec le <strong>CECRL</strong> et les programmes officiels :
        une évaluation diagnostique en début de parcours, une évaluation
        formative à mi-parcours et une évaluation sommative en fin de séquence
        avec grille de compétences.
      </p>
      <div class="eval-grid">
        ${card("diag", "Évaluation diagnostique", "bf",
          "<strong>Positionnement</strong> initial : repérer les acquis " +
          "et les besoins. Non notée. Vocabulaire, vrai/faux, amorce de production.",
          "10 minutes", "En début de séquence", diag)}
        ${card("form", "Évaluation formative", "magenta",
          "<strong>Vérification des progrès</strong> à mi-parcours : " +
          "lexique, faits de langue, mini-compréhension. Notée par compétences.",
          "20 minutes", "Au milieu de la séquence", form)}
        ${card("somm", "Évaluation sommative", "rouge",
          "<strong>Tâche finale</strong> de la séquence : grille " +
          "d'évaluation détaillée par compétences langagières (CO, CE, EOC, EE).",
          "40 à 60 minutes", "En fin de séquence", somm)}
      </div>

      <aside class="eval-tip">
        <i class="ph ph-info ph-icon ph-icon--bf"></i>
        <p>
          Les évaluations sont distribuées par l'enseignante en classe et
          notées selon une <strong>grille de compétences</strong>
          (recevabilité linguistique, cohérence, lexique, faits de langue).
          La <a href="#activite">activité d'entraînement en ligne</a>
          sert de support d'<em>auto-évaluation</em> à n'importe quel moment.
        </p>
      </aside>
    </section>`;
}

// ============================================================
//   Template HTML d'une page séquence
// ============================================================
function renderSequencePage(niveauKey, seq, prevNext) {
  const lvl = NIVEAU_LABEL[niveauKey];
  const seqSlug = slugify(seq.titre);
  const niveauSlug = NIVEAU_TO_DIR[niveauKey];
  // Toutes les séquences ont une fiche PDF (40/40 générées en Phase B+).
  // On préfère les overrides enrichis quand ils existent, sinon
  // on construit le nom automatiquement.
  const fiche = PDF_OVERRIDES[seq.titre] || autoFicheFilename(niveauKey, seq.titre);
  const quizUrl = seq.url ? seq.url.replace(/^\.\.\//, "../../") : null;
  const ficheUrl = `../../pdf-imprimables/${fiche}`;

  const tags = [];
  if (seq.cecrl)   tags.push(`<span class="seq-tag seq-tag--cecrl">${esc(seq.cecrl)}</span>`);
  if (seq.periode) tags.push(`<span class="seq-tag">${esc(seq.periode)}</span>`);

  const seances = buildPlanSeances(seq).map(s => `
        <li class="seance-item">
          <div class="seance-item__num">S${s.num}</div>
          <div class="seance-item__body">
            <div class="seance-item__title">${esc(s.titre)}</div>
            <p class="seance-item__obj">${s.objectif}</p>
            <span class="seance-item__al">${esc(s.al)}</span>
          </div>
        </li>`).join("");

  // Section DOCUMENT SUPPORT — texte authentique en anglais + questions
  const sectionSupport = renderDocumentSupport(seq);

  // Section LEÇON / COURS — trace écrite enrichie et structurée
  const sectionLecon = renderTraceEcrite(seq);

  // Section FICHES D'ACTIVITÉ — la fiche PDF existe systématiquement
  const sectionDocs = `
    <section class="seq-section" id="fiches">
      <h2 class="seq-section__title"><i class="ph ph-file-text" aria-hidden="true"></i> Fiches d'activité</h2>
      <p class="seq-section__intro">
        <strong>Document pédagogique</strong> à imprimer ou projeter
        en classe. Mise en page institutionnelle <strong>AEFE — Marque
        État</strong> (logos AEFE et LFT, police Marianne, palette tricolore).
        Format manuel scolaire avec QR code vers l'activité d'entraînement.
      </p>
      <div class="seq-doc-grid">
        <article class="seq-doc-card">
          <div class="seq-doc-card__icon" aria-hidden="true"><i class="ph ph-file-pdf"></i></div>
          <h3 class="seq-doc-card__title">Fiche élève — Séquence ${esc(seq.n)}</h3>
          <p class="seq-doc-card__desc">
            Document A4 (4 pages) : couverture éditoriale, lexique
            illustré, document support, faits de langue avec exemples,
            activité de production, tâche finale et critères de réussite.
          </p>
          <a href="${esc(ficheUrl)}" target="_blank" rel="noopener" class="btn btn--accent">
            <i class="ph ph-download-simple"></i> Télécharger la fiche (PDF)
          </a>
        </article>
      </div>
    </section>`;

  // Section ACTIVITÉS D'ENTRAÎNEMENT (quiz interactif)
  const sectionQuiz = quizUrl ? `
    <section class="seq-section" id="activite">
      <h2 class="seq-section__title"><i class="ph ph-cursor-click" aria-hidden="true"></i> Activités d'entraînement</h2>
      <p class="seq-section__intro">
        Activité interactive en ligne, synchronisée avec la séquence.
        À faire en classe ou en autonomie pour <strong>s'entraîner</strong>
        et <strong>s'auto-évaluer</strong> avant la tâche finale.
        Lien partageable, retour automatique par e-mail à l'élève
        et à l'enseignante.
      </p>
      <div class="seq-quiz-card">
        <div class="seq-quiz-card__head">
          <h3 class="seq-quiz-card__title">${esc(seq.titre)}</h3>
          <span class="seq-tag seq-tag--cecrl">${esc(seq.cecrl || "")}</span>
        </div>
        <div class="seq-quiz-card__actions">
          <a href="${esc(quizUrl)}" class="btn btn--accent btn--lg">▶ Lancer l'activité</a>
          <button type="button" class="btn btn--secondary btn--copy" data-share-url="${esc(quizUrl)}">
            🔗 Copier le lien à partager
          </button>
        </div>
        <p class="seq-quiz-card__notice">
          🔒 Conforme RGPD : pas de cookies, pas de mot de passe,
          pas d'IP collectée.
        </p>
      </div>
    </section>` : `
    <section class="seq-section" id="activite">
      <h2 class="seq-section__title"><i class="ph ph-cursor-click" aria-hidden="true"></i> Activités d'entraînement</h2>
      <p class="seq-section__intro">
        <em>L'activité interactive en ligne de cette séquence est en
        cours de finalisation.</em>
      </p>
    </section>`;

  // Navigation prev/next
  const navPrev = prevNext.prev ? `
        <a href="${esc(slugify(prevNext.prev.titre))}.html" class="seq-nav__prev">
          <span class="seq-nav__arrow">←</span>
          <span class="seq-nav__label">Séquence ${esc(prevNext.prev.n)}</span>
          <span class="seq-nav__title">${esc(prevNext.prev.titre)}</span>
        </a>` : `<div></div>`;

  const navNext = prevNext.next ? `
        <a href="${esc(slugify(prevNext.next.titre))}.html" class="seq-nav__next">
          <span class="seq-nav__label">Séquence ${esc(prevNext.next.n)}</span>
          <span class="seq-nav__title">${esc(prevNext.next.titre)}</span>
          <span class="seq-nav__arrow">→</span>
        </a>` : `<div></div>`;

  return `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>${esc(seq.titre)} — ${esc(lvl.complet)} — LFT</title>
  <meta name="description" content="Séquence pédagogique d'anglais : ${esc(seq.titre)} (${esc(lvl.complet)}, niveau ${esc(seq.cecrl)}). Plan des séances, fiche imprimable, activité en ligne, tâche finale." />
  <meta name="theme-color" content="#000091" />
  <link rel="icon" type="image/png" href="../../assets/img/logo-lft.png" />
  <link rel="stylesheet" href="../../assets/css/style.css" />
  <link rel="preload" href="../../assets/fonts/Marianne-Regular.woff2" as="font" type="font/woff2" crossorigin />
  <link rel="preload" href="../../assets/fonts/Marianne-Bold.woff2" as="font" type="font/woff2" crossorigin />
</head>
<body>

  <a href="#main-content" class="skip-link">Aller au contenu principal</a>

  <header class="site-header" role="banner">
    <div class="site-header__top">
      <div class="container site-header__top-inner">
        <span>République française · AEFE · Établissement en gestion directe</span>
        <a href="${esc(lvl.pageHref)}">Retour au niveau</a>
      </div>
    </div>
    <div class="site-header__main">
      <div class="container site-header__main-inner">
        <a href="../../index.html" class="brand">
          <img src="../../assets/img/logo-lft.png" alt="" />
          <div class="brand-text">
            <div class="line1">Lycée Français de Tananarive</div>
            <div class="line2">${esc(seq.titre)}</div>
            <div class="line3">${esc(lvl.court)} · ${esc(seq.cecrl || "")} · Mme FALIMANANA</div>
          </div>
        </a>
        <nav class="nav-main" aria-label="Navigation principale">
          <a href="../../index.html">Accueil</a>
          <a href="${esc(lvl.pageHref)}">${esc(lvl.breadcrumb)}</a>
          <a href="#" aria-current="page">Séquence ${esc(seq.n)}</a>
        </nav>
      </div>
    </div>
  </header>

  <main id="main-content">

    <!-- Fil d'Ariane -->
    <div class="container">
      <nav class="breadcrumb" aria-label="Fil d'Ariane">
        <a href="../../index.html">Accueil</a>
        <span aria-hidden="true">›</span>
        <a href="${esc(lvl.pageHref)}">${esc(lvl.breadcrumb)}</a>
        <span aria-hidden="true">›</span>
        <span aria-current="page">Séquence ${esc(seq.n)} — ${esc(seq.titre)}</span>
      </nav>
    </div>

    <!-- Hero de la séquence -->
    <section class="seq-hero">
      <div class="container">
        <div class="seq-hero__meta">
          <span class="seq-hero__num">Séquence ${esc(seq.n)}</span>
          <span class="seq-hero__niveau">${esc(lvl.complet)}</span>
        </div>
        <h1 class="seq-hero__title">${esc(seq.titre)}</h1>
        <p class="seq-hero__theme">${escClean(seq.theme || "")}</p>
        <div class="seq-hero__tags">${tags.join(" ")}</div>
      </div>
    </section>

    <div class="container">

      <!-- Présentation -->
      <section class="seq-section" id="presentation">
        <h2 class="seq-section__title"><i class="ph ph-info" aria-hidden="true"></i> Présentation de la séquence</h2>
        <div class="seq-info-grid">
          <div class="seq-info-card">
            <span class="seq-info-card__label">Axe culturel</span>
            <p class="seq-info-card__value">${esc(seq.axe || "—")}</p>
          </div>
          <div class="seq-info-card">
            <span class="seq-info-card__label">Période</span>
            <p class="seq-info-card__value">${esc(seq.periode || "—")}</p>
          </div>
          <div class="seq-info-card">
            <span class="seq-info-card__label">Niveau CECRL</span>
            <p class="seq-info-card__value">${esc(seq.cecrl || "—")}</p>
          </div>
          <div class="seq-info-card">
            <span class="seq-info-card__label">Tâche finale</span>
            <p class="seq-info-card__value">${escClean(seq.tache || "—")}</p>
          </div>
        </div>

        <div class="seq-detail-grid">
          <div class="seq-detail-card">
            <h3>Lexique</h3>
            <p>${escClean(seq.lexique || "—")}</p>
          </div>
          <div class="seq-detail-card">
            <h3>Faits de langue</h3>
            <p>${escClean(seq.langue || "—")}</p>
          </div>
          <div class="seq-detail-card">
            <h3>Repères culturels</h3>
            <p>${escClean(seq.culturel || "—")}</p>
          </div>
        </div>
      </section>

      <!-- Sommaire pédagogique -->
      <nav class="seq-toc" aria-label="Sommaire de la séquence">
        <h2 class="seq-toc__title">Au sommaire de cette séquence</h2>
        <ol class="seq-toc__list">
          <li><a href="#presentation"><i class="ph ph-info seq-toc__icon"></i> Présentation</a></li>
          <li><a href="#plan"><i class="ph ph-list-checks seq-toc__icon"></i> Plan des séances</a></li>
          <li><a href="#document"><i class="ph ph-text-aa seq-toc__icon"></i> Document support</a></li>
          <li><a href="#lecon"><i class="ph ph-book-open seq-toc__icon"></i> Cours / Leçon</a></li>
          <li><a href="#fiches"><i class="ph ph-file-text seq-toc__icon"></i> Fiches d'activité</a></li>
          <li><a href="#activite"><i class="ph ph-cursor-click seq-toc__icon"></i> Activités d'entraînement</a></li>
          <li><a href="#tache"><i class="ph ph-target seq-toc__icon"></i> Tâche finale</a></li>
          <li><a href="#evaluation"><i class="ph ph-chart-bar seq-toc__icon"></i> Évaluations</a></li>
        </ol>
      </nav>

      <!-- Plan des séances -->
      <section class="seq-section" id="plan">
        <h2 class="seq-section__title"><i class="ph ph-list-checks" aria-hidden="true"></i> Plan des séances</h2>
        <p class="seq-section__intro">
          Déroulé pédagogique sur 6 à 8 séances de 55 minutes. Chaque
          séance mobilise une ou deux <strong>activités langagières</strong>
          dominantes (CO, CE, EOC, IO, EE).
        </p>
        <ol class="seance-list">${seances}
        </ol>
      </section>

      ${sectionSupport}

      ${sectionLecon}

      ${sectionDocs}

      ${sectionQuiz}

      <!-- Tâche finale -->
      <section class="seq-section" id="tache">
        <h2 class="seq-section__title"><i class="ph ph-target" aria-hidden="true"></i> Tâche finale</h2>
        <div class="seq-task-card">
          <p class="seq-task-card__desc">${escClean(seq.tache || "—")}</p>
          <div class="seq-task-card__criteria">
            <h4>Critères d'évaluation par compétences</h4>
            <ul>
              <li><strong>Recevabilité linguistique</strong> — correction grammaticale, prononciation, fluidité</li>
              <li><strong>Cohérence de la production</strong> — structure, pertinence des idées, lien avec la tâche</li>
              <li><strong>Richesse lexicale</strong> — mobilisation du lexique de la séquence</li>
              <li><strong>Engagement / créativité</strong> — implication personnelle, originalité</li>
            </ul>
          </div>
        </div>
      </section>

      <!-- Évaluations — 3 PDF imprimables par séquence -->
      ${renderEvaluations(niveauKey, seq)}

      <!-- Navigation séquence précédente / suivante -->
      <nav class="seq-nav" aria-label="Navigation entre séquences">${navPrev}${navNext}
      </nav>

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

  <script>
  // Bouton « Copier le lien »
  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".btn--copy").forEach(btn => {
      btn.addEventListener("click", async () => {
        const path = btn.getAttribute("data-share-url");
        const absUrl = new URL(path, window.location.href).toString();
        const original = btn.innerHTML;
        try {
          await navigator.clipboard.writeText(absUrl);
          btn.innerHTML = "✓ Lien copié !";
          btn.classList.add("is-copied");
        } catch (e) {
          btn.innerHTML = "❌ Échec — copiez : " + absUrl;
        }
        setTimeout(() => {
          btn.innerHTML = original;
          btn.classList.remove("is-copied");
        }, 2200);
      });
    });
  });
  </script>
  <script src="../../assets/js/analytics.js" defer></script>
</body>
</html>`;
}

// ============================================================
//   Génération principale
// ============================================================
function main() {
  const outRoot = path.join(__dirname, "..", "sequences");
  if (!fs.existsSync(outRoot)) fs.mkdirSync(outRoot, { recursive: true });

  let total = 0;
  Object.entries(PROG).forEach(([niveauKey, niveauData]) => {
    const dir = NIVEAU_TO_DIR[niveauKey];
    if (!dir) return;

    const niveauOutDir = path.join(outRoot, dir);
    if (!fs.existsSync(niveauOutDir)) fs.mkdirSync(niveauOutDir, { recursive: true });

    const seqs = niveauData.sequences;
    seqs.forEach((seq, idx) => {
      const html = renderSequencePage(niveauKey, seq, {
        prev: idx > 0 ? seqs[idx - 1] : null,
        next: idx < seqs.length - 1 ? seqs[idx + 1] : null,
      });
      const filename = slugify(seq.titre) + ".html";
      const outPath = path.join(niveauOutDir, filename);
      fs.writeFileSync(outPath, html, "utf-8");
      total += 1;
      console.log(`  ✓ ${path.relative(path.join(__dirname, ".."), outPath)}`);
    });
  });

  console.log(`\n${total} pages séquence générées.`);
}

main();

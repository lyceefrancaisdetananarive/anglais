/* ============================================================
   niveau-page.js — Générateur de contenu pour les pages niveau
   ============================================================
   Philosophie pédagogique :
   La page niveau est une vue d'ensemble qui présente l'ANNÉE
   SCOLAIRE. Chaque séquence est cliquable et amène vers une page
   dédiée (sequences/{niveau}/{slug}.html) qui concentre :
   - Cours / Leçon (lexique, faits de langue, repères culturels)
   - Plan des séances
   - Fiche d'activité imprimable (PDF)
   - Activité d'entraînement (quiz interactif)
   - Tâche finale (évaluation sommative)
   - Évaluations diagnostique / formative / sommative

   Sections produites :
   1. Notice RGPD (suivi mail)
   2. Au programme cette année (table de progression cliquable)
   3. Accès rapide aux séquences (cartes cliquables)
   4. Évaluations (info pédagogique générale du niveau)

   Usage HTML :
   <main id="main-content" data-niveau="6e">
     <div id="niveau-content"></div>
   </main>
   <script src="../assets/js/progression-data.js"></script>
   <script src="../assets/js/niveau-page.js"></script>
   ============================================================ */

(function() {
  "use strict";

  // ============================================================
  //   Slug et helpers
  // ============================================================
  function slugify(s) {
    return String(s)
      .toLowerCase()
      .normalize("NFD").replace(/[̀-ͯ]/g, "")
      .replace(/['‘’]/g, "")
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

  // ============================================================
  //   Mapping niveauKey → dossier sequences/
  // ============================================================
  const NIVEAU_TO_DIR = {
    "6e": "6e", "4e": "4e", "4e-non-si": "4e-non-si",
    "4e-lce": "4e-lce", "3e": "3e", "3e-non-si": "3e-non-si",
    "1ere": "1ere", "terminale": "terminale",
  };

  function sequenceUrl(niveauKey, seq) {
    const dir = NIVEAU_TO_DIR[niveauKey];
    return `../sequences/${dir}/${slugify(seq.titre)}.html`;
  }

  // ============================================================
  //   Section — Notice de suivi automatique
  // ============================================================
  function renderRgpdNotice() {
    return `
      <aside class="niveau-notice">
        <strong>📬 Suivi pédagogique automatique :</strong>
        à la fin de chaque <strong>activité d'entraînement</strong> en
        ligne, l'élève reçoit un récapitulatif par e-mail et l'enseignante
        <a href="mailto:salamo.falimanana@egd.mg">Mme FALIMANANA</a>
        reçoit une copie. Les résultats sont également archivés dans un
        tableur sécurisé. Conforme RGPD : pas de cookies, pas de mot
        de passe, pas d'adresse IP collectée.
      </aside>
    `;
  }

  // ============================================================
  //   Section 1 — Au programme cette année (table cliquable)
  // ============================================================
  function renderProgramme(niveaux) {
    let rows = "";
    let totalSeq = 0;
    niveaux.forEach(key => {
      const data = window.PROGRESSION_ANNUELLE[key];
      if (!data) return;
      data.sequences.forEach(seq => {
        totalSeq += 1;
        const url = sequenceUrl(key, seq);
        const cecrl = seq.cecrl ? `<span class="seq-cecrl">${esc(seq.cecrl)}</span>` : "";
        const statutLabel = seq.statut === "live"
          ? '<span class="seq-statut seq-statut--live">✓ Activité disponible</span>'
          : '<span class="seq-statut seq-statut--todo">Au programme</span>';
        rows += `
          <tr>
            <td class="seq-num"><a href="${esc(url)}">${esc(seq.n)}</a></td>
            <td class="seq-period">${esc(seq.periode)}</td>
            <td class="seq-titre">
              <a href="${esc(url)}" class="seq-titre-link">${esc(seq.titre)}</a>
              <p class="seq-titre-theme">${esc(seq.theme || "")}</p>
            </td>
            <td>${cecrl}</td>
            <td>${statutLabel}</td>
            <td><a href="${esc(url)}" class="seq-row-cta" aria-label="Voir la séquence ${esc(seq.titre)}">Voir →</a></td>
          </tr>`;
      });
    });

    return `
      <section aria-labelledby="programme-title" class="niveau-section">
        <div class="niveau-section__header">
          <h2 id="programme-title" class="section-title">
            <span class="niveau-section__icon" aria-hidden="true">📅</span>
            Au programme cette année
          </h2>
          <p class="niveau-section__intro">
            <strong>${totalSeq} séquence${totalSeq > 1 ? "s" : ""}</strong> à
            mener sur l'année scolaire (septembre → juin). Programme
            officiel <a href="https://eduscol.education.fr/" target="_blank" rel="noopener">BO Eduscol</a>,
            adapté au contexte AEFE / Madagascar.
            <strong>Cliquez sur le titre d'une séquence</strong> pour
            accéder à son contenu complet : cours, fiche d'activité,
            activité d'entraînement, tâche finale et évaluations.
          </p>
        </div>
        <div class="niveau-table-wrap">
          <table class="progression-table progression-table--clickable">
            <thead>
              <tr>
                <th>N°</th>
                <th>Période</th>
                <th>Titre &amp; thème</th>
                <th>CECRL</th>
                <th>Statut</th>
                <th>Détails</th>
              </tr>
            </thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      </section>
    `;
  }

  // ============================================================
  //   Section 2 — Accès rapide aux séquences (cartes)
  // ============================================================
  function renderSequencesGrid(niveaux) {
    let cards = "";
    niveaux.forEach(key => {
      const data = window.PROGRESSION_ANNUELLE[key];
      if (!data) return;
      data.sequences.forEach(seq => {
        const url = sequenceUrl(key, seq);
        const piliers = [];
        piliers.push('<span class="seq-pillier">📖 Cours</span>');
        piliers.push('<span class="seq-pillier">📅 Plan</span>');
        piliers.push('<span class="seq-pillier">📄 Fiche</span>');
        if (seq.statut === "live" && seq.url) {
          piliers.push('<span class="seq-pillier seq-pillier--active">💻 Activité</span>');
        }
        piliers.push('<span class="seq-pillier">🎯 Tâche</span>');
        piliers.push('<span class="seq-pillier">📊 Éval</span>');

        cards += `
          <a href="${esc(url)}" class="sequence-card glass-card">
            <div class="sequence-card__head">
              <span class="sequence-card__num">Séquence ${esc(seq.n)}</span>
              <span class="sequence-card__cecrl">${esc(seq.cecrl || "")}</span>
            </div>
            <h3 class="sequence-card__title">${esc(seq.titre)}</h3>
            <p class="sequence-card__theme">${esc(seq.theme || "")}</p>
            <p class="sequence-card__period">${esc(seq.periode || "")}</p>
            <div class="sequence-card__piliers">${piliers.join("")}</div>
            <span class="sequence-card__cta">Ouvrir la séquence →</span>
          </a>
        `;
      });
    });

    if (!cards) return "";

    return `
      <section aria-labelledby="seqs-title" class="niveau-section">
        <div class="niveau-section__header">
          <h2 id="seqs-title" class="section-title">
            <span class="niveau-section__icon" aria-hidden="true">📚</span>
            Accès rapide aux séquences
          </h2>
          <p class="niveau-section__intro">
            Chaque séquence regroupe les <strong>4 piliers de
            l'apprentissage</strong> : <strong>cours/leçon</strong>
            (lexique, langue, repères culturels), <strong>fiche
            d'activité</strong> imprimable, <strong>activité d'entraînement</strong>
            en ligne et <strong>évaluations</strong> (formative + sommative).
          </p>
        </div>
        <div class="cards-grid">${cards}</div>
      </section>
    `;
  }

  // ============================================================
  //   Section 3 — Évaluations (info pédagogique du niveau)
  // ============================================================
  function renderEvaluations() {
    return `
      <section aria-labelledby="evaluations-title" class="niveau-section">
        <div class="niveau-section__header">
          <h2 id="evaluations-title" class="section-title">
            <span class="niveau-section__icon" aria-hidden="true">📊</span>
            Évaluations
          </h2>
          <p class="niveau-section__intro">
            Conformément au cadre européen commun de référence pour les
            langues (<strong>CECRL</strong>) et aux orientations du Ministère
            de l'Éducation nationale, l'évaluation est conçue comme un
            <strong>processus continu</strong>, articulant trois temps
            complémentaires.
          </p>
        </div>
        <div class="evaluation-grid">
          <article class="glass-card">
            <h3 class="card__title">📝 Évaluation diagnostique</h3>
            <p class="card__description">
              <strong>En début de séquence.</strong> Permet de situer
              les acquis initiaux des élèves sur les <em>activités
              langagières</em> mobilisées (CO, CE, EOC, IO, EE).
              Distribuée par l'enseignante en classe.
            </p>
          </article>
          <article class="glass-card">
            <h3 class="card__title">📈 Évaluation formative</h3>
            <p class="card__description">
              <strong>Pendant la séquence.</strong> Les
              <em>activités d'entraînement</em> en ligne (cf. table
              ci-dessus) servent de support d'<strong>auto-évaluation</strong>.
              Retour automatique par e-mail. L'enseignante dispose
              d'un suivi de classe consolidé.
            </p>
          </article>
          <article class="glass-card">
            <h3 class="card__title">🎯 Évaluation sommative</h3>
            <p class="card__description">
              <strong>En fin de séquence.</strong> La <em>tâche finale</em>
              (production écrite, expression orale en continu,
              médiation…) est notée selon une grille de
              <strong>compétences langagières</strong>. Évaluations
              communes ponctuelles également organisées par l'équipe
              pédagogique.
            </p>
          </article>
        </div>
      </section>
    `;
  }

  // ============================================================
  //   Render principal
  // ============================================================
  function renderNiveauPage(levelKeys) {
    if (!Array.isArray(levelKeys)) levelKeys = [levelKeys];
    const root = document.getElementById("niveau-content");
    if (!root) return;
    if (!window.PROGRESSION_ANNUELLE) {
      root.innerHTML = '<p>Chargement des données…</p>';
      return;
    }

    const html = [
      renderRgpdNotice(),
      renderSequencesGrid(levelKeys),
      renderProgramme(levelKeys),
      renderEvaluations(),
    ].join("");

    root.innerHTML = html;
  }

  // Auto-init
  document.addEventListener("DOMContentLoaded", () => {
    const main = document.getElementById("main-content");
    if (!main) return;
    const niveau = main.getAttribute("data-niveau");
    const niveaux = main.getAttribute("data-niveaux");
    if (niveaux) {
      renderNiveauPage(niveaux.split(",").map(s => s.trim()));
    } else if (niveau) {
      renderNiveauPage(niveau);
    }
  });

  window.renderNiveauPage = renderNiveauPage;
})();

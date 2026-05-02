/* ============================================================
   niveau-page.js — Générateur de contenu pour les pages niveau
   ============================================================
   Sections produites pour chaque niveau :
   1. Au programme cette année (progression septembre → juin)
   2. Activités en ligne (quiz interactifs, lien partageable, retour mail)
   3. Fiches d'activité imprimables (PDF)
   4. Évaluations (sur demande de l'enseignante)

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
  //   Mapping PDF par niveau (relatif à pdf-imprimables/)
  // ============================================================
  const PDF_PAR_NIVEAU = {
    "6e": [
      {
        titre: "Welcome to Big Ben Academy!",
        url: "fiche_6e_welcome_big_ben.pdf",
        pages: 4,
        desc: "Première séquence de l'année. Présentations, alphabet, nombres, verbe to be. Couverture institutionnelle, déroulement type, lexique, grille d'évaluation par compétences."
      }
    ],
    "4e": [
      {
        titre: "Stuck at Big Bay School",
        url: "fiche_4e_stuck_at_big_bay_school.pdf",
        pages: 4,
        desc: "Lecture cursive en Nouvelle-Zélande. Présent simple/continu, comparatifs, culture māorie. Déroulement de séance et grille d'évaluation par compétences."
      }
    ],
    "4e-non-si": [
      {
        titre: "The Giver — Lois Lowry",
        url: "fiche_4e_non_si_the_giver.pdf",
        pages: 4,
        desc: "Lecture suivie d'un classique de la littérature dystopique YA. Voix passive, conditional, lexique de la dystopie. Format magazine avec citation et QR vers l'activité en ligne."
      }
    ],
    "4e-lce": [
      {
        titre: "Britain & Europe",
        url: "fiche_4e_lce_britain_europe.pdf",
        pages: 4,
        desc: "Module culturel LCE. Des Romains au Brexit : 5 époques clés des relations RU-Continent. Frise chronologique + lexique civilisation."
      }
    ],
    "3e": [
      {
        titre: "Street Art — The Voice of the Wall",
        url: "fiche_3e_street_art_pilote.pdf",
        pages: 10,
        desc: "Fiche pilote magazine refondue : photos street art, infographies tricolores, QR code interactif. 10 activités, prépare au DNB."
      },
      {
        titre: "The Secret of Jatbula Trail",
        url: "fiche_3e_secret_jatbula_trail.pdf",
        pages: 4,
        desc: "Lecture cursive en Australie autochtone. Prétérit, modaux d'obligation, peuples premiers. Niveau pré-DNB."
      }
    ],
    "3e-non-si": [
      {
        titre: "The Curious Incident — Mark Haddon",
        url: "fiche_3e_non_si_curious_incident.pdf",
        pages: 4,
        desc: "Lecture suivie autour de la voix de Christopher Boone (neurodiversité). Past simple/present perfect, lexique de la narration. Format DNB-friendly."
      }
    ],
    "1ere": [
      {
        titre: "Madagascar's Biodiversity (DNL SVT)",
        url: "fiche_dnl_svt_1ere.pdf",
        pages: 10,
        desc: "Fiche DNL SVT — A Living Laboratory. 3 séances autour de la biodiversité malgache : endémisme, déforestation, conservation. Support APPROF LING."
      }
    ],
    "terminale": [
      {
        titre: "Identities & Exchanges",
        url: "fiche_terminale_identities_exchanges.pdf",
        pages: 4,
        desc: "Fiche Bac Terminale — Axe culturel n°1. Migration, diaspora malgache à Londres, multiculturalisme britannique. Préparation à l'épreuve écrite et orale."
      }
    ]
  };

  // Quiz qui correspondent à des évaluations finales (préparation à
  // l'évaluation sommative). Tous les autres sont des « activités
  // en ligne » d'entraînement classiques.
  const QUIZ_EVAL_FINALE = new Set([
    "My DNB Project",                                    // 3e
    "Towards Terminale: Reading Scientific Papers",      // 1ere
    "Music Through the Decades",                         // 4e (final 4e)
    "My Town, My Story",                                 // 4e (final 4e)
    "British Institutions",                              // 4e NON SI (final)
    "Territory and Memory",                              // Tale (axe 8 final)
  ]);

  // ============================================================
  //   Helpers HTML
  // ============================================================
  const esc = (s) => String(s == null ? "" : s)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  const slug = (s) => String(s).toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");

  // ============================================================
  //   Section 1 — Au programme cette année
  // ============================================================
  function renderProgramme(niveaux) {
    let rows = "";
    let totalSeq = 0;
    niveaux.forEach(key => {
      const data = window.PROGRESSION_ANNUELLE[key];
      if (!data) return;
      data.sequences.forEach(seq => {
        totalSeq += 1;
        const statutClass = seq.statut === "live" ? "seq-statut--live" : "seq-statut--todo";
        const statutLabel = seq.statut === "live" ? "✓ En ligne" : "Au programme";
        const cecrl = seq.cecrl ? `<span class="seq-cecrl">${esc(seq.cecrl)}</span>` : "";
        rows += `
          <tr>
            <td class="seq-num">${esc(seq.n)}</td>
            <td class="seq-period">${esc(seq.periode)}</td>
            <td class="seq-titre">${esc(seq.titre)}</td>
            <td class="seq-tache">${esc(seq.tache || "—")}</td>
            <td>${cecrl}</td>
            <td><span class="seq-statut ${statutClass}">${statutLabel}</span></td>
          </tr>
        `;
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
            <strong>${totalSeq} séquence${totalSeq > 1 ? "s" : ""}</strong> à aborder
            sur l'année scolaire (septembre → juin). Programme officiel
            <a href="https://eduscol.education.fr/" target="_blank" rel="noopener">BO Eduscol</a>,
            adapté au contexte AEFE / Madagascar.
          </p>
        </div>
        <div class="niveau-table-wrap">
          <table class="progression-table">
            <thead>
              <tr>
                <th>N°</th>
                <th>Période</th>
                <th>Titre de la séquence</th>
                <th>Tâche finale</th>
                <th>CECRL</th>
                <th>Statut</th>
              </tr>
            </thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      </section>
    `;
  }

  // ============================================================
  //   Section 2 — Activités en ligne (quiz interactifs)
  // ============================================================
  function renderActivitesEnLigne(niveaux) {
    let cardsClassiques = "";
    let cardsEvalFinale = "";
    let countOnline = 0;

    niveaux.forEach(key => {
      const data = window.PROGRESSION_ANNUELLE[key];
      if (!data) return;
      data.sequences.forEach(seq => {
        if (seq.statut !== "live" || !seq.url) return;
        countOnline += 1;

        const isEvalFinale = QUIZ_EVAL_FINALE.has(seq.titre);
        const cardHtml = `
          <article class="activite-card glass-card">
            <div class="activite-card__head">
              <span class="activite-card__num">Séq. ${esc(seq.n)}</span>
              <span class="activite-card__cecrl">${esc(seq.cecrl || "")}</span>
            </div>
            <h3 class="activite-card__title">${esc(seq.titre)}</h3>
            <p class="activite-card__theme">${esc(seq.theme || "")}</p>
            <ul class="activite-card__details">
              <li><strong>Activités langagières :</strong> CO, CE, EOC, EE</li>
              <li><strong>Tâche finale :</strong> ${esc(seq.tache || "—")}</li>
              ${seq.langue ? `<li><strong>Faits de langue :</strong> ${esc(seq.langue)}</li>` : ""}
            </ul>
            <div class="activite-card__footer">
              <a href="${esc(seq.url)}" class="btn btn--accent">▶ Lancer l'activité</a>
              <button type="button" class="btn btn--secondary btn--copy" data-share-url="${esc(seq.url)}">
                🔗 Copier le lien
              </button>
            </div>
          </article>
        `;

        if (isEvalFinale) cardsEvalFinale += cardHtml;
        else              cardsClassiques += cardHtml;
      });
    });

    if (countOnline === 0) {
      return "";
    }

    let html = `
      <section aria-labelledby="online-title" class="niveau-section">
        <div class="niveau-section__header">
          <h2 id="online-title" class="section-title">
            <span class="niveau-section__icon" aria-hidden="true">💻</span>
            Activités en ligne
          </h2>
          <p class="niveau-section__intro">
            Activités interactives à faire <strong>directement en ligne</strong>.
            Chaque activité génère un <strong>lien unique partageable</strong>
            (cliquez sur « Copier le lien »). Les résultats sont
            <strong>archivés automatiquement</strong> et envoyés par e-mail à
            l'élève et à l'enseignante.
          </p>
        </div>
        <div class="cards-grid">${cardsClassiques}</div>
    `;

    if (cardsEvalFinale) {
      html += `
        <div class="niveau-section__header niveau-section__header--mt">
          <h3 class="section-title section-title--sub">
            <span class="niveau-section__icon" aria-hidden="true">🎯</span>
            Quiz d'évaluation des acquis
          </h3>
          <p class="niveau-section__intro">
            Activités d'<strong>évaluation formative</strong> en fin de séquence.
            Servent à <strong>préparer l'évaluation sommative</strong>
            (DNB, Bac, contrôle de fin de séquence).
          </p>
        </div>
        <div class="cards-grid">${cardsEvalFinale}</div>
      `;
    }

    html += `</section>`;
    return html;
  }

  // ============================================================
  //   Section 3 — Fiches d'activité imprimables
  // ============================================================
  function renderFiches(niveaux) {
    let cards = "";
    niveaux.forEach(key => {
      const fiches = PDF_PAR_NIVEAU[key] || [];
      fiches.forEach(f => {
        cards += `
          <article class="fiche-card glass-card">
            <div class="fiche-card__icon" aria-hidden="true">📄</div>
            <h3 class="fiche-card__title">${esc(f.titre)}</h3>
            <p class="fiche-card__desc">${esc(f.desc)}</p>
            <div class="fiche-card__meta">
              <span><strong>${f.pages}</strong> pages</span>
              <span>PDF A4</span>
            </div>
            <a href="../pdf-imprimables/${esc(f.url)}" class="btn btn--secondary" target="_blank" rel="noopener">
              ⬇ Télécharger
            </a>
          </article>
        `;
      });
    });

    if (!cards) {
      cards = `
        <article class="glass-card">
          <p class="card__description">
            <em>Les fiches d'activité de ce niveau sont en cours de finalisation.</em>
            Toutes les fiches existantes sont accessibles dans la
            <a href="../pdf-imprimables/">bibliothèque PDF</a>.
          </p>
        </article>
      `;
    }

    return `
      <section aria-labelledby="fiches-title" class="niveau-section">
        <div class="niveau-section__header">
          <h2 id="fiches-title" class="section-title">
            <span class="niveau-section__icon" aria-hidden="true">📄</span>
            Fiches d'activité imprimables
          </h2>
          <p class="niveau-section__intro">
            Fiches pédagogiques au format PDF, prêtes à imprimer pour la classe.
            Mise en page institutionnelle <strong>AEFE — Marque État</strong> :
            police Marianne, palette officielle, en-tête tricolore,
            <strong>QR code</strong> vers l'activité en ligne synchronisée.
          </p>
        </div>
        <div class="cards-grid">${cards}</div>
      </section>
    `;
  }

  // ============================================================
  //   Section 4 — Évaluations sommatives
  // ============================================================
  function renderEvaluations(niveaux) {
    return `
      <section aria-labelledby="evaluations-title" class="niveau-section">
        <div class="niveau-section__header">
          <h2 id="evaluations-title" class="section-title">
            <span class="niveau-section__icon" aria-hidden="true">📊</span>
            Évaluations
          </h2>
          <p class="niveau-section__intro">
            Les <strong>évaluations sommatives</strong> (contrôles de fin de séquence,
            évaluations communes, devoirs surveillés) sont distribuées en classe
            par l'enseignante. Elles ne sont pas accessibles en libre service
            pour préserver leur valeur diagnostique.
          </p>
        </div>
        <div class="evaluation-grid">
          <article class="glass-card">
            <h3 class="card__title">📝 Évaluations diagnostiques</h3>
            <p class="card__description">
              En début d'année : positionnement initial sur les
              activités langagières (CO, CE, EOC, EE).
              Distribuées par l'enseignante en classe.
            </p>
          </article>
          <article class="glass-card">
            <h3 class="card__title">📈 Évaluations formatives</h3>
            <p class="card__description">
              Pendant la séquence : les <em>quiz d'évaluation des acquis</em>
              (ci-dessus) servent de support pour s'auto-évaluer
              et identifier les points à retravailler.
            </p>
          </article>
          <article class="glass-card">
            <h3 class="card__title">🎯 Évaluations sommatives</h3>
            <p class="card__description">
              En fin de séquence : la <strong>tâche finale</strong>
              (production écrite, oral en continu, médiation…).
              Notation par grille de compétences ou note chiffrée.
            </p>
          </article>
        </div>
      </section>
    `;
  }

  // ============================================================
  //   Notice retour par mail
  // ============================================================
  function renderRgpdNotice() {
    return `
      <aside class="niveau-notice">
        <strong>📬 Suivi automatique des activités en ligne :</strong>
        à la fin de chaque activité, l'élève reçoit un récapitulatif par e-mail
        et l'enseignante <a href="mailto:salamo.falimanana@egd.mg">Mme FALIMANANA</a>
        reçoit une copie. Les résultats sont également archivés dans un tableur
        sécurisé. Conforme RGPD : pas de cookies, pas de mot de passe,
        pas d'adresse IP collectée.
      </aside>
    `;
  }

  // ============================================================
  //   Copier le lien d'une activité dans le presse-papier
  // ============================================================
  function bindCopyButtons(root) {
    root.querySelectorAll(".btn--copy").forEach(btn => {
      btn.addEventListener("click", async () => {
        const path = btn.getAttribute("data-share-url");
        // Construire l'URL absolue à partir du domaine du site
        const absUrl = new URL(path, window.location.href).toString();
        const original = btn.innerHTML;
        try {
          await navigator.clipboard.writeText(absUrl);
          btn.innerHTML = "✓ Lien copié !";
          btn.classList.add("is-copied");
        } catch (e) {
          btn.innerHTML = "❌ Échec — copiez manuellement : " + absUrl;
        }
        setTimeout(() => {
          btn.innerHTML = original;
          btn.classList.remove("is-copied");
        }, 2200);
      });
    });
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
      renderProgramme(levelKeys),
      renderActivitesEnLigne(levelKeys),
      renderFiches(levelKeys),
      renderEvaluations(levelKeys),
    ].join("");

    root.innerHTML = html;
    bindCopyButtons(root);
  }

  // Auto-init si l'attribut data-niveau est présent sur <main>
  document.addEventListener("DOMContentLoaded", () => {
    const main = document.getElementById("main-content");
    if (!main) return;
    const niveau = main.getAttribute("data-niveau");
    const niveaux = main.getAttribute("data-niveaux"); // multi (csv)
    if (niveaux) {
      renderNiveauPage(niveaux.split(",").map(s => s.trim()));
    } else if (niveau) {
      renderNiveauPage(niveau);
    }
  });

  window.renderNiveauPage = renderNiveauPage;
})();

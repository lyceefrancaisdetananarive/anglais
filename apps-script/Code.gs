/**
 * APPS SCRIPT — Réception des résultats de quiz
 * Plateforme Anglais — Lycée Français de Tananarive
 * Mme Salamo FALIMANANA
 *
 * Rôle :
 *   1. Reçoit en POST le payload JSON envoyé par quiz-engine.js
 *   2. Archive une ligne dans une feuille Google Sheets
 *   3. Envoie un mail récapitulatif à l'enseignante (toujours)
 *   4. Envoie un mail à l'élève s'il a saisi son adresse
 *
 * Installation : voir README.md du repo, section « Configuration Apps Script »
 */

/* ================================================================
   PARAMÈTRES À ADAPTER LORS DU PREMIER DÉPLOIEMENT
   ================================================================ */

// E-mail de l'enseignante (destinataire principal de chaque résultat)
const TEACHER_EMAIL = "salamo.falimanana@egd.mg";

// === MODE PRODUCTION =======================================================
// Plateforme en production depuis 2026 — la copie (CC) admin est désactivée.
// Pour réactiver le suivi technique : passer DEV_MODE à true et redéployer
// (Apps Script > Déployer > Gérer les déploiements > Modifier la version).
const DEV_MODE = false;
const DEV_CC_EMAIL = "max.rafaliarison@egd.mg";
// ===========================================================================

// Nom de l'expéditeur affiché dans les mails
const SENDER_NAME = "Espace Anglais — LFT";

// ID de la feuille Google Sheets qui archive les résultats.
// Pour le récupérer : ouvrir la feuille, l'URL contient .../d/{ID}/edit
// Feuille partagée par Mme FALIMANANA :
// https://docs.google.com/spreadsheets/d/1wlyyG8mOdDCf807Wk6FFJ_Tj4aMWfzzuILsO_R9EfJs/edit
const SHEET_ID = "1wlyyG8mOdDCf807Wk6FFJ_Tj4aMWfzzuILsO_R9EfJs";

// Nom de l'onglet où s'écrivent les résultats de quiz
const SHEET_TAB = "Résultats quiz";

// Nom de l'onglet où s'écrivent les visites de la plateforme
const VISITS_TAB = "Visites";


/* ================================================================
   POINT D'ENTRÉE WEB (déclenché par fetch POST côté client)
   ================================================================ */

/**
 * Reçoit le POST du quiz, traite et renvoie un statut.
 * Le navigateur de l'élève appelle ce script en mode "no-cors", donc
 * il ne lira pas la réponse — mais on la renvoie quand même pour
 * faciliter le debug en environnement de test.
 */
function doPost(e) {
  try {
    if (!e || !e.postData || !e.postData.contents) {
      return jsonResponse({ ok: false, error: "no-payload" }, 400);
    }

    const payload = JSON.parse(e.postData.contents);

    // ===== PING DE VISITE (analytics anonyme) =====
    if (payload.type === "visit") {
      logVisit(payload);
      return jsonResponse({ ok: true, kind: "visit" });
    }

    // ===== SOUMISSION DE QUIZ =====
    if (!payload.quizId || !payload.student || !payload.score) {
      return jsonResponse({ ok: false, error: "invalid-payload" }, 400);
    }

    // 1) Archive
    appendToSheet(payload);

    // 2) Mail enseignante
    sendTeacherEmail(payload);

    // 3) Mail élève (si adresse fournie)
    if (payload.student.email && isValidEmail(payload.student.email)) {
      sendStudentEmail(payload);
    }

    return jsonResponse({ ok: true, kind: "quiz" });

  } catch (err) {
    Logger.log("Erreur doPost : " + err);
    return jsonResponse({ ok: false, error: String(err) }, 500);
  }
}


/* ================================================================
   ANALYTICS — feuille "Visites"
   ================================================================ */

function getVisitsSheet_() {
  const ss = SHEET_ID
    ? SpreadsheetApp.openById(SHEET_ID)
    : (function () {
        const fname = "Plateforme Anglais LFT — Résultats quiz";
        const files = DriveApp.getFilesByName(fname);
        return files.hasNext()
          ? SpreadsheetApp.open(files.next())
          : SpreadsheetApp.create(fname);
      })();

  let sh = ss.getSheetByName(VISITS_TAB);
  if (!sh) {
    sh = ss.insertSheet(VISITS_TAB);
    sh.appendRow([
      "Date",
      "Page",
      "Titre",
      "Appareil",
      "Marque / Modèle",
      "OS",
      "Navigateur",
      "Langue",
      "Fuseau horaire",
      "Résolution écran",
      "Provenance",
    ]);
    sh.getRange(1, 1, 1, 11)
      .setFontWeight("bold")
      .setBackground("#E6007E")  // magenta LFT (vs bleu pour la feuille quiz)
      .setFontColor("#ffffff");
    sh.setFrozenRows(1);
  }
  return sh;
}

function logVisit(p) {
  const sh = getVisitsSheet_();
  sh.appendRow([
    new Date(),
    p.page || "",
    p.title || "",
    p.deviceType || "",
    p.deviceBrand || "",
    p.osName || "",
    p.browser || "",
    p.language || "",
    p.timezone || "",
    p.screen || "",
    p.referrer || "",
  ]);
}


/* ================================================================
   ARCHIVAGE DANS GOOGLE SHEETS (Quiz)
   ================================================================ */

function getSheet_() {
  let ss;
  if (SHEET_ID) {
    ss = SpreadsheetApp.openById(SHEET_ID);
  } else {
    // Cherche un fichier portant le nom standard ou le crée
    const fname = "Plateforme Anglais LFT — Résultats quiz";
    const files = DriveApp.getFilesByName(fname);
    if (files.hasNext()) {
      ss = SpreadsheetApp.open(files.next());
    } else {
      ss = SpreadsheetApp.create(fname);
    }
  }

  let sh = ss.getSheetByName(SHEET_TAB);
  if (!sh) {
    sh = ss.insertSheet(SHEET_TAB);
    sh.appendRow([
      "Date soumission", "Quiz ID", "Quiz titre", "Séquence", "Niveau",
      "Prénom élève", "Classe", "E-mail élève",
      "Score brut", "Total questions", "Note /20",
      "Démarré à", "Soumis à",
      "Détail réponses (JSON)",
    ]);
    sh.getRange(1, 1, 1, 14).setFontWeight("bold").setBackground("#000091").setFontColor("#ffffff");
    sh.setFrozenRows(1);
  }
  return sh;
}

function appendToSheet(p) {
  const sh = getSheet_();
  sh.appendRow([
    new Date(),
    p.quizId,
    p.quizTitle,
    p.quizSequence || "",
    p.level || "",
    p.student.firstname,
    p.student.classGroup,
    p.student.email || "",
    p.score.correct,
    p.score.total,
    p.score.score20,
    p.startedAt,
    p.submittedAt,
    JSON.stringify(p.answers),
  ]);
}


/* ================================================================
   MAIL POUR L'ENSEIGNANTE
   ================================================================ */

function sendTeacherEmail(p) {
  const subject = `[Anglais LFT] ${p.student.firstname} (${p.student.classGroup}) — ${p.score.score20}/20 — ${p.quizTitle}`;
  const html = buildEmailHtml({
    title: "Résultat de quiz reçu",
    intro: `<strong>${escapeHtml(p.student.firstname)}</strong> (classe ${escapeHtml(p.student.classGroup)}) vient de terminer le quiz <em>${escapeHtml(p.quizTitle)}</em>.`,
    payload: p,
    audience: "teacher",
  });

  MailApp.sendEmail({
    to: TEACHER_EMAIL,
    cc: DEV_MODE ? DEV_CC_EMAIL : "",
    subject: subject,
    htmlBody: html,
    name: SENDER_NAME,
    replyTo: p.student.email || TEACHER_EMAIL,
  });
}


/* ================================================================
   MAIL POUR L'ÉLÈVE
   ================================================================ */

function sendStudentEmail(p) {
  const subject = `Tes résultats — ${p.quizTitle} — ${p.score.score20}/20`;
  const html = buildEmailHtml({
    title: "Tes résultats de quiz",
    intro: `Bonjour ${escapeHtml(p.student.firstname)},<br><br>Voici tes résultats au quiz <em>${escapeHtml(p.quizTitle)}</em>. Tu y as obtenu <strong>${p.score.score20}/20</strong>.`,
    payload: p,
    audience: "student",
  });

  MailApp.sendEmail({
    to: p.student.email,
    cc: DEV_MODE ? DEV_CC_EMAIL : "",
    subject: subject,
    htmlBody: html,
    name: SENDER_NAME,
    replyTo: TEACHER_EMAIL,
  });
}


/* ================================================================
   GÉNÉRATEUR HTML DES MAILS (mise en page LFT/AEFE)
   ================================================================ */

function buildEmailHtml({ title, intro, payload, audience }) {
  const p = payload;
  const correctRows = p.answers.map((a, i) => {
    const okIcon = a.correct
      ? '<span style="color:#18753c; font-weight:bold;">&#10004;</span>'
      : '<span style="color:#ce0500; font-weight:bold;">&#10008;</span>';
    return `
      <tr>
        <td style="padding:8px 12px; border-bottom:1px solid #eee; vertical-align:top; width:30px;">${okIcon}</td>
        <td style="padding:8px 12px; border-bottom:1px solid #eee; vertical-align:top;">
          <div style="font-weight:600; color:#000091; margin-bottom:4px;">Q${a.index}. ${escapeHtml(a.question)}</div>
          <div style="font-size:13px; color:#3a3a3a;">
            <strong>Réponse de l'élève :</strong> ${escapeHtml(a.studentAnswer)}<br>
            <strong>Réponse attendue :</strong> ${escapeHtml(a.expectedAnswer)}
          </div>
        </td>
      </tr>`;
  }).join("");

  const scoreColor = p.score.score20 >= 14 ? "#18753c"
                  : p.score.score20 >= 10 ? "#000091"
                  : "#b34000";

  return `
    <!DOCTYPE html>
    <html>
    <body style="margin:0; padding:0; font-family: 'Marianne', Arial, sans-serif; background:#f5f5fe; color:#161616;">
      <div style="max-width:640px; margin:0 auto; background:#ffffff;">

        <!-- En-tête -->
        <div style="background:#000091; color:#ffffff; padding:24px 32px;">
          <div style="font-size:14px; opacity:0.9; letter-spacing:1px; text-transform:uppercase;">
            Lycée Français de Tananarive · AEFE
          </div>
          <div style="font-size:20px; font-weight:700; margin-top:6px;">
            Espace Anglais — Mme FALIMANANA
          </div>
        </div>

        <!-- Filet doré tricolore -->
        <div style="height:4px; background: linear-gradient(to right, #000091 50%, #e1000f 50%);"></div>

        <!-- Titre -->
        <div style="padding:32px 32px 8px;">
          <h1 style="color:#000091; font-size:22px; margin:0 0 16px;">${escapeHtml(title)}</h1>
          <p style="font-size:15px; color:#3a3a3a; line-height:1.6; margin:0;">${intro}</p>
        </div>

        <!-- Score -->
        <div style="padding:24px 32px;">
          <div style="background: linear-gradient(135deg, rgba(0,0,145,0.06), rgba(230,0,126,0.06));
                      border-radius:12px; padding:24px; text-align:center;">
            <div style="font-size:48px; font-weight:800; color:${scoreColor}; line-height:1;">
              ${p.score.correct} / ${p.score.total}
            </div>
            <div style="font-size:18px; color:#3a3a3a; margin-top:8px;">
              Soit <strong style="color:${scoreColor};">${p.score.score20} / 20</strong>
            </div>
          </div>
        </div>

        <!-- Métadonnées -->
        <div style="padding:0 32px 16px; font-size:13px; color:#7a7a7a;">
          <div><strong>Quiz :</strong> ${escapeHtml(p.quizTitle)}</div>
          ${p.quizSequence ? `<div><strong>Séquence :</strong> ${escapeHtml(p.quizSequence)}</div>` : ""}
          ${p.level ? `<div><strong>Niveau :</strong> ${escapeHtml(p.level)}</div>` : ""}
          <div><strong>Élève :</strong> ${escapeHtml(p.student.firstname)} — Classe ${escapeHtml(p.student.classGroup)}</div>
          <div><strong>Date de soumission :</strong> ${new Date(p.submittedAt).toLocaleString("fr-FR")}</div>
        </div>

        <!-- Correction détaillée -->
        <div style="padding:8px 32px 24px;">
          <h2 style="color:#000091; font-size:18px; margin:24px 0 12px; padding-bottom:8px; border-bottom:2px solid #e6007e;">
            Correction détaillée
          </h2>
          <table style="width:100%; border-collapse:collapse; font-size:14px;">
            ${correctRows}
          </table>
        </div>

        ${audience === "student" ? `
        <div style="padding:0 32px 24px;">
          <div style="background:#ececfe; border-left:4px solid #000091; padding:16px; border-radius:4px; font-size:14px; color:#3a3a3a;">
            <strong>Pour progresser :</strong> relis les questions où tu as fait une erreur et reviens
            sur le cours correspondant. N'hésite pas à reposer la question à Mme FALIMANANA en classe.
          </div>
        </div>
        ` : `
        <div style="padding:0 32px 24px;">
          <div style="background:#fff5f5; border-left:4px solid #e6007e; padding:16px; border-radius:4px; font-size:14px; color:#3a3a3a;">
            <strong>Note enseignante :</strong> ce résultat a été archivé automatiquement dans la feuille Google Sheets
            «&nbsp;Plateforme Anglais LFT — Résultats quiz&nbsp;».
          </div>
        </div>
        `}

        <!-- Pied de page -->
        <div style="background:#000091; color:#ffffff; padding:20px 32px; font-size:12px; text-align:center;">
          <div style="display:inline-block; width:60px; height:3px;
                      background:linear-gradient(to right, #ffffff 50%, #e1000f 50%);
                      margin-bottom:12px;"></div>
          <div>© Lycée Français de Tananarive · Établissement AEFE</div>
          <div style="opacity:0.8; margin-top:4px;">Mme Salamo FALIMANANA — salamo.falimanana@egd.mg</div>
        </div>

      </div>
    </body>
    </html>
  `;
}


/* ================================================================
   UTILITAIRES
   ================================================================ */

function jsonResponse(obj, status) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function isValidEmail(s) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(String(s));
}

function escapeHtml(s) {
  return String(s == null ? "" : s)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}


/* ================================================================
   TEST MANUEL — exécutable depuis l'éditeur Apps Script
   pour vérifier que tout fonctionne sans avoir à passer un vrai quiz
   ================================================================ */

function testManuel() {
  const fakePayload = {
    quizId: "test-001",
    quizTitle: "Quiz de test",
    quizSequence: "Test interne",
    level: "3e",
    student: {
      firstname: "Élève Test",
      classGroup: "3M5",
      email: "",  // mettre votre adresse pour tester l'envoi élève
    },
    score: { correct: 8, total: 10, score20: 16 },
    startedAt: new Date(Date.now() - 5 * 60 * 1000).toISOString(),
    submittedAt: new Date().toISOString(),
    answers: [
      { index: 1, question: "Question test 1", type: "qcm",
        studentAnswer: "A stencil", expectedAnswer: "A stencil", correct: true },
      { index: 2, question: "Question test 2", type: "saisie",
        studentAnswer: "this mural was painted", expectedAnswer: "this mural was painted by banksy", correct: false },
    ],
    teacherEmail: TEACHER_EMAIL,
  };

  appendToSheet(fakePayload);
  sendTeacherEmail(fakePayload);
  Logger.log("Test exécuté — vérifier le mail enseignante et la feuille Sheets.");
}

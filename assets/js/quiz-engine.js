/* =========================================================
   MOTEUR DE QUIZ — Plateforme Anglais LFT
   Mme FALIMANANA · Statique, sans dépendance externe
   =========================================================
   Usage :
   <script src="../../assets/js/quiz-engine.js"></script>
   <script>
     QuizEngine.init({
       id: "3e-street-art",
       title: "Street Art — Vocabulaire & voix passive",
       level: "3e",
       sequence: "Street Art: The Voice of the Wall",
       questions: [ ... ]  // voir format ci-dessous
     });
   </script>
   ========================================================= */

(function (global) {
  "use strict";

  /* ----------- ENDPOINT APPS SCRIPT (à configurer une fois publié) ----------- */
  const APPS_SCRIPT_URL = "https://script.google.com/macros/s/REMPLACEZ_PAR_VOTRE_ID/exec";

  /* ----------- ÉTAT DU QUIZ ----------- */
  const state = {
    config: null,        // configuration du quiz courant
    student: null,       // { firstname, classGroup, email? }
    currentStep: 0,      // étape actuelle (0 = intro, 1..N = questions, N+1 = résultat)
    answers: [],         // tableau des réponses élève
    startedAt: null,
    submittedAt: null,
  };

  /* ----------- HELPERS DOM ----------- */
  const $ = (sel) => document.querySelector(sel);
  const el = (tag, cls, txt) => {
    const node = document.createElement(tag);
    if (cls) node.className = cls;
    if (txt !== undefined) node.textContent = txt;
    return node;
  };

  /* ----------- INITIALISATION ----------- */
  function init(config) {
    if (!config || !config.questions || !config.questions.length) {
      console.error("QuizEngine: configuration invalide");
      return;
    }
    state.config = config;
    state.answers = new Array(config.questions.length).fill(null);
    state.startedAt = new Date().toISOString();
    renderShell();
    showStep(0);
  }

  /* ----------- RENDU DE LA STRUCTURE ----------- */
  function renderShell() {
    const root = $("#quiz-root");
    if (!root) {
      console.error("QuizEngine: #quiz-root introuvable");
      return;
    }
    root.innerHTML = "";
    root.classList.add("quiz-shell");

    // barre de progression
    const progressWrap = el("div", "quiz-progress");
    progressWrap.setAttribute("role", "progressbar");
    progressWrap.setAttribute("aria-label", "Progression du quiz");
    progressWrap.setAttribute("aria-valuemin", "0");
    progressWrap.setAttribute("aria-valuemax", "100");
    progressWrap.setAttribute("aria-valuenow", "0");
    progressWrap.id = "quiz-progress";
    progressWrap.appendChild(el("div", "quiz-progress__bar"));
    root.appendChild(progressWrap);

    // conteneur étape
    const stepHost = el("div", "glass-card");
    stepHost.id = "quiz-step-host";
    root.appendChild(stepHost);
  }

  /* ----------- AFFICHAGE D'UNE ÉTAPE ----------- */
  function showStep(idx) {
    state.currentStep = idx;
    const host = $("#quiz-step-host");
    host.innerHTML = "";

    const total = state.config.questions.length;

    if (idx === 0) {
      renderIntro(host);
      updateProgress(0);
    } else if (idx > 0 && idx <= total) {
      renderQuestion(host, idx - 1);
      updateProgress((idx - 1) / total * 100);
    } else {
      renderResult(host);
      updateProgress(100);
    }
  }

  function updateProgress(pct) {
    const bar = $(".quiz-progress__bar");
    if (bar) bar.style.width = pct + "%";
    const wrap = $("#quiz-progress");
    if (wrap) wrap.setAttribute("aria-valuenow", String(Math.round(pct)));
  }

  /* ----------- ÉCRAN D'INTRODUCTION ----------- */
  function renderIntro(host) {
    const cfg = state.config;

    host.appendChild(el("h2", null, cfg.title));

    if (cfg.sequence) {
      const seq = el("p", "text-muted", `Séquence : ${cfg.sequence}`);
      host.appendChild(seq);
    }

    const meta = el("div", "card__meta");
    meta.style.borderTop = "none";
    meta.style.marginTop = "0";
    meta.style.paddingTop = "0";
    meta.appendChild(el("span", null, `${cfg.questions.length} questions`));
    if (cfg.duration) meta.appendChild(el("span", null, `Durée estimée : ${cfg.duration}`));
    if (cfg.level) meta.appendChild(el("span", null, `Niveau : ${cfg.level}`));
    host.appendChild(meta);

    if (cfg.intro) {
      const intro = el("p", "mt-5", cfg.intro);
      host.appendChild(intro);
    }

    // formulaire identification
    const form = el("form");
    form.id = "quiz-intro-form";
    form.style.marginTop = "var(--space-5)";

    form.innerHTML = `
      <div class="form-field">
        <label for="firstname">Ton prénom <span class="required" aria-hidden="true">*</span></label>
        <input type="text" id="firstname" name="firstname" required maxlength="40"
               autocomplete="given-name" aria-required="true" />
      </div>
      <div class="form-field">
        <label for="classGroup">Ta classe <span class="required" aria-hidden="true">*</span></label>
        <select id="classGroup" name="classGroup" required aria-required="true">
          <option value="">— Choisis ta classe —</option>
          <option value="3M5">3<sup>e</sup> M5 (LVA)</option>
          <option value="3ANGLAI1">3<sup>e</sup> NON SI</option>
          <option value="4M7">4<sup>e</sup> M7 (LVA)</option>
          <option value="4M4">4<sup>e</sup> M4 (NON SI)</option>
          <option value="4ANGL_L1">4<sup>e</sup> LCE</option>
          <option value="6M4">6<sup>e</sup> M4 (LVA)</option>
          <option value="1EUROANG1">1<sup>re</sup> Euro</option>
          <option value="TG6ANGLAIS_1">Terminale</option>
          <option value="autre">Autre</option>
        </select>
      </div>
      <div class="form-field">
        <label for="email">Ton e-mail <span class="text-muted" style="font-weight: 400;">(facultatif — pour recevoir tes résultats)</span></label>
        <input type="email" id="email" name="email" maxlength="80" autocomplete="email"
               placeholder="prenom.nom@eleve.egd.mg" />
      </div>
    `;

    const actions = el("div", "quiz-actions");
    const startBtn = el("button", "btn btn--accent btn--lg", "Commencer le quiz");
    startBtn.type = "submit";
    actions.appendChild(startBtn);
    form.appendChild(actions);

    form.addEventListener("submit", (ev) => {
      ev.preventDefault();
      const fd = new FormData(form);
      state.student = {
        firstname: (fd.get("firstname") || "").toString().trim(),
        classGroup: (fd.get("classGroup") || "").toString().trim(),
        email: (fd.get("email") || "").toString().trim(),
      };
      if (!state.student.firstname || !state.student.classGroup) return;
      showStep(1);
      window.scrollTo({ top: 0, behavior: "smooth" });
    });

    host.appendChild(form);
  }

  /* ----------- AFFICHAGE D'UNE QUESTION ----------- */
  function renderQuestion(host, qIdx) {
    const q = state.config.questions[qIdx];
    const total = state.config.questions.length;

    const head = el("div");
    head.style.display = "flex";
    head.style.justifyContent = "space-between";
    head.style.alignItems = "center";
    head.style.marginBottom = "var(--space-4)";
    head.appendChild(el("span", "text-muted", `Question ${qIdx + 1} sur ${total}`));
    head.appendChild(el("span", "text-muted", `Bonjour ${state.student.firstname} · ${state.student.classGroup}`));
    host.appendChild(head);

    // Énoncé
    const stem = el("div", "quiz-question");
    const num = el("span", "quiz-question-num", String(qIdx + 1));
    stem.appendChild(num);
    stem.appendChild(document.createTextNode(q.prompt));
    host.appendChild(stem);

    // Image facultative
    if (q.image) {
      const fig = el("figure");
      const img = el("img");
      img.src = q.image.src;
      img.alt = q.image.alt || "";
      fig.appendChild(img);
      if (q.image.caption) fig.appendChild(el("figcaption", null, q.image.caption));
      host.appendChild(fig);
    }

    // Audio facultatif
    if (q.audio) {
      const audio = document.createElement("audio");
      audio.controls = true;
      audio.preload = "metadata";
      audio.className = "audio-player";
      audio.src = q.audio.src;
      host.appendChild(audio);
      if (q.audio.note) host.appendChild(el("p", "text-muted mb-5", q.audio.note));
    }

    // Champ de réponse selon le type
    const previousAnswer = state.answers[qIdx];

    if (q.type === "qcm" || q.type === "vrai-faux") {
      const choices = q.type === "vrai-faux"
        ? [{ value: "vrai", label: "Vrai (True)" }, { value: "faux", label: "Faux (False)" }]
        : q.options.map((opt, i) => ({
            value: String(i),
            label: typeof opt === "string" ? opt : opt.label,
          }));

      const list = el("div", "quiz-options");
      choices.forEach((c) => {
        const labelEl = el("label", "quiz-option");
        const radio = document.createElement("input");
        radio.type = "radio";
        radio.name = `q-${qIdx}`;
        radio.value = c.value;
        if (previousAnswer && previousAnswer.value === c.value) {
          radio.checked = true;
          labelEl.classList.add("is-selected");
        }
        radio.addEventListener("change", () => {
          state.answers[qIdx] = { value: c.value };
          list.querySelectorAll(".quiz-option").forEach((o) => o.classList.remove("is-selected"));
          labelEl.classList.add("is-selected");
        });
        labelEl.appendChild(radio);
        labelEl.appendChild(document.createTextNode(c.label));
        list.appendChild(labelEl);
      });
      host.appendChild(list);

    } else if (q.type === "saisie") {
      const inp = document.createElement("input");
      inp.type = "text";
      inp.className = "quiz-input";
      inp.placeholder = q.placeholder || "Tape ta réponse en anglais…";
      inp.maxLength = 200;
      if (previousAnswer && previousAnswer.value) inp.value = previousAnswer.value;
      inp.addEventListener("input", () => {
        state.answers[qIdx] = { value: inp.value.trim() };
      });
      host.appendChild(inp);

    } else if (q.type === "multi") {
      // Cases à cocher (plusieurs bonnes réponses)
      const list = el("div", "quiz-options");
      q.options.forEach((opt, i) => {
        const lbl = typeof opt === "string" ? opt : opt.label;
        const labelEl = el("label", "quiz-option");
        const cb = document.createElement("input");
        cb.type = "checkbox";
        cb.name = `q-${qIdx}`;
        cb.value = String(i);
        const prevSet = previousAnswer && previousAnswer.values
          ? new Set(previousAnswer.values)
          : new Set();
        if (prevSet.has(String(i))) {
          cb.checked = true;
          labelEl.classList.add("is-selected");
        }
        cb.addEventListener("change", () => {
          const checked = Array.from(list.querySelectorAll("input:checked")).map((c) => c.value);
          state.answers[qIdx] = { values: checked };
          labelEl.classList.toggle("is-selected", cb.checked);
        });
        labelEl.appendChild(cb);
        labelEl.appendChild(document.createTextNode(lbl));
        list.appendChild(labelEl);
      });
      host.appendChild(list);
    }

    // Boutons
    const actions = el("div", "quiz-actions");
    const prevBtn = el("button", "btn btn--secondary", "Précédent");
    prevBtn.type = "button";
    prevBtn.disabled = qIdx === 0;
    prevBtn.addEventListener("click", () => {
      showStep(qIdx);
      window.scrollTo({ top: 0, behavior: "smooth" });
    });

    const nextLabel = qIdx + 1 === total ? "Terminer le quiz" : "Suivant";
    const nextBtn = el("button", "btn btn--accent", nextLabel);
    nextBtn.type = "button";
    nextBtn.addEventListener("click", () => {
      if (qIdx + 1 === total) {
        finalize();
      } else {
        showStep(qIdx + 2);
        window.scrollTo({ top: 0, behavior: "smooth" });
      }
    });

    actions.appendChild(prevBtn);
    actions.appendChild(nextBtn);
    host.appendChild(actions);
  }

  /* ----------- ÉVALUATION D'UNE QUESTION ----------- */
  function gradeQuestion(q, ans) {
    if (!ans) return false;

    if (q.type === "qcm" || q.type === "vrai-faux") {
      return String(ans.value) === String(q.answer);

    } else if (q.type === "saisie") {
      const norm = (s) => (s || "")
        .toString()
        .trim()
        .toLowerCase()
        .replace(/[.,;:!?'"]/g, "")
        .replace(/\s+/g, " ");
      const accepted = Array.isArray(q.answer) ? q.answer : [q.answer];
      return accepted.some((a) => norm(a) === norm(ans.value));

    } else if (q.type === "multi") {
      const expected = (q.answer || []).map(String).sort();
      const given = (ans.values || []).map(String).sort();
      return expected.length === given.length &&
             expected.every((v, i) => v === given[i]);
    }

    return false;
  }

  /* ----------- FINALISATION ----------- */
  function finalize() {
    state.submittedAt = new Date().toISOString();
    showStep(state.config.questions.length + 1);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  /* ----------- ÉCRAN DE RÉSULTAT + CORRECTION ----------- */
  function renderResult(host) {
    const cfg = state.config;
    const total = cfg.questions.length;
    let correctCount = 0;
    const detail = cfg.questions.map((q, i) => {
      const ok = gradeQuestion(q, state.answers[i]);
      if (ok) correctCount++;
      return { q, ans: state.answers[i], ok };
    });

    const score20 = Math.round((correctCount / total) * 20);

    const resultHead = el("div", "quiz-result");
    const scoreLine = el("div");
    const scoreNum = el("span", "quiz-result__score", String(correctCount));
    const scoreTotal = el("span", "quiz-result__total", ` / ${total}`);
    scoreLine.appendChild(scoreNum);
    scoreLine.appendChild(scoreTotal);
    resultHead.appendChild(scoreLine);

    const note = el("p", null, `Soit ${score20} / 20`);
    note.style.fontSize = "var(--font-size-xl)";
    note.style.fontWeight = "600";
    note.style.color = "var(--grey-700)";
    resultHead.appendChild(note);

    let message = "Quiz terminé.";
    if (correctCount === total) message = "Excellent ! Toutes les réponses sont justes.";
    else if (correctCount >= total * 0.8) message = "Très bon travail !";
    else if (correctCount >= total * 0.5) message = "Bon début — relis la correction pour progresser.";
    else message = "Il faut revoir le cours. Pas de panique, on s'en occupe ensemble.";

    resultHead.appendChild(el("p", "quiz-result__message", message));
    host.appendChild(resultHead);

    // Correction question par question
    const corrTitle = el("h3", null, "Correction détaillée");
    corrTitle.style.marginTop = "var(--space-6)";
    host.appendChild(corrTitle);

    detail.forEach((d, i) => {
      const block = el("div", "glass-card");
      block.style.marginBottom = "var(--space-4)";
      block.style.borderLeft = `4px solid ${d.ok ? "var(--success-500)" : "var(--error-500)"}`;

      const header = el("div");
      header.style.display = "flex";
      header.style.justifyContent = "space-between";
      header.style.marginBottom = "var(--space-3)";
      header.appendChild(el("strong", null, `Question ${i + 1}`));
      header.appendChild(el("span", null, d.ok ? "✓ Correct" : "✗ Incorrect"));
      block.appendChild(header);

      block.appendChild(el("p", null, d.q.prompt));

      // réponse correcte explicite
      const exp = el("div", d.ok ? "quiz-feedback quiz-feedback--success" : "quiz-feedback quiz-feedback--error");
      const expectedText = formatExpectedAnswer(d.q);
      exp.innerHTML = `<strong>${d.ok ? "Bonne réponse" : "Réponse attendue"}&nbsp;:</strong> ${expectedText}`;
      block.appendChild(exp);

      if (d.q.explanation) {
        const why = el("p", "text-muted");
        why.style.marginTop = "var(--space-3)";
        why.style.fontSize = "var(--font-size-sm)";
        why.innerHTML = `<strong>Explication&nbsp;:</strong> ${d.q.explanation}`;
        block.appendChild(why);
      }

      host.appendChild(block);
    });

    // Bouton envoi mail
    const sendCard = el("div", "glass-card glass--colored");
    sendCard.style.marginTop = "var(--space-6)";
    sendCard.style.textAlign = "center";

    sendCard.appendChild(el("h3", null, "Envoyer mes résultats"));
    sendCard.appendChild(el("p", null, `Tes résultats seront envoyés à Mme FALIMANANA${state.student.email ? " et à toi-même" : ""}, avec la correction détaillée.`));

    const sendBtn = el("button", "btn btn--accent btn--lg", "Envoyer à Mme FALIMANANA");
    sendBtn.type = "button";
    sendBtn.id = "quiz-send-btn";
    sendBtn.addEventListener("click", () => sendResults({ correctCount, score20, detail, sendBtn }));
    sendCard.appendChild(sendBtn);

    const status = el("p", "text-muted", "");
    status.id = "quiz-send-status";
    status.style.marginTop = "var(--space-3)";
    sendCard.appendChild(status);

    host.appendChild(sendCard);

    // Bouton retour
    const back = el("div", "quiz-actions");
    back.style.justifyContent = "center";
    const homeBtn = el("a", "btn btn--secondary", "Retour à l'accueil");
    homeBtn.href = "../../index.html";
    back.appendChild(homeBtn);
    host.appendChild(back);
  }

  function formatExpectedAnswer(q) {
    if (q.type === "qcm") {
      const correct = q.options[parseInt(q.answer, 10)];
      return typeof correct === "string" ? correct : correct.label;
    }
    if (q.type === "vrai-faux") {
      return q.answer === "vrai" ? "Vrai" : "Faux";
    }
    if (q.type === "saisie") {
      const accepted = Array.isArray(q.answer) ? q.answer : [q.answer];
      return accepted.map(a => `<em>${escapeHtml(a)}</em>`).join(" ou ");
    }
    if (q.type === "multi") {
      return (q.answer || [])
        .map(i => {
          const opt = q.options[parseInt(i, 10)];
          return typeof opt === "string" ? opt : opt.label;
        })
        .join(", ");
    }
    return "";
  }

  function escapeHtml(s) {
    return String(s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#039;");
  }

  /* ----------- ENVOI VERS APPS SCRIPT ----------- */
  function sendResults({ correctCount, score20, detail, sendBtn }) {
    const status = $("#quiz-send-status");
    sendBtn.disabled = true;
    status.textContent = "Envoi en cours…";
    status.className = "text-muted";

    const payload = {
      quizId: state.config.id,
      quizTitle: state.config.title,
      quizSequence: state.config.sequence || "",
      level: state.config.level || "",
      student: state.student,
      score: { correct: correctCount, total: state.config.questions.length, score20 },
      startedAt: state.startedAt,
      submittedAt: state.submittedAt,
      answers: detail.map((d, i) => ({
        index: i + 1,
        question: d.q.prompt,
        type: d.q.type,
        studentAnswer: formatStudentAnswer(d.q, d.ans),
        expectedAnswer: stripHtml(formatExpectedAnswer(d.q)),
        correct: d.ok,
      })),
      teacherEmail: "salamo.falimanana@egd.mg",
    };

    if (APPS_SCRIPT_URL.includes("REMPLACEZ_PAR_VOTRE_ID")) {
      console.warn("APPS_SCRIPT_URL non configuré — affichage local uniquement");
      console.log("Payload :", payload);
      status.textContent = "(Mode test : Apps Script non encore configuré. Données loggées en console.)";
      status.className = "quiz-feedback quiz-feedback--error";
      sendBtn.disabled = false;
      return;
    }

    fetch(APPS_SCRIPT_URL, {
      method: "POST",
      mode: "no-cors", // Apps Script renvoie sans CORS — on ne peut pas lire la réponse
      headers: { "Content-Type": "text/plain;charset=utf-8" },
      body: JSON.stringify(payload),
    })
      .then(() => {
        status.textContent = "Tes résultats ont bien été envoyés à Mme FALIMANANA. Merci !";
        status.className = "quiz-feedback quiz-feedback--success";
        sendBtn.style.display = "none";
      })
      .catch((err) => {
        console.error(err);
        status.textContent = "Erreur d'envoi. Demande à Mme FALIMANANA, ou réessaie plus tard.";
        status.className = "quiz-feedback quiz-feedback--error";
        sendBtn.disabled = false;
      });
  }

  function formatStudentAnswer(q, ans) {
    if (!ans) return "(non répondu)";
    if (q.type === "qcm") {
      const opt = q.options[parseInt(ans.value, 10)];
      return typeof opt === "string" ? opt : (opt ? opt.label : ans.value);
    }
    if (q.type === "vrai-faux") return ans.value === "vrai" ? "Vrai" : "Faux";
    if (q.type === "saisie") return ans.value || "(vide)";
    if (q.type === "multi") {
      return (ans.values || []).map(i => {
        const opt = q.options[parseInt(i, 10)];
        return typeof opt === "string" ? opt : (opt ? opt.label : i);
      }).join(", ");
    }
    return "";
  }

  function stripHtml(s) { return String(s).replace(/<[^>]+>/g, ""); }

  /* ----------- API PUBLIQUE ----------- */
  global.QuizEngine = { init };

})(window);

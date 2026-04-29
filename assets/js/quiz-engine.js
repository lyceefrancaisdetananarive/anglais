/* =========================================================
   MOTEUR DE QUIZ — Plateforme Anglais LFT (v2)
   Mme FALIMANANA · Inspiration Pix + EvalAng
   =========================================================
   Types d'activités supportés :
     - qcm           : choix unique
     - multi         : choix multiple (cases à cocher)
     - vrai-faux     : Vrai / Faux
     - saisie        : texte libre
     - audio-qcm     : extrait audio + question
     - image-qcm     : image + question
     - matching      : associer deux colonnes
     - ordering      : remettre dans l'ordre
     - cloze         : texte à trous (menus déroulants)

   Usage minimal :
   <script src="../../assets/js/quiz-engine.js"></script>
   <script>
     QuizEngine.init({
       id: "...", title: "...", level: "...",
       questions: [ ... ]
     });
   </script>
   ========================================================= */

(function (global) {
  "use strict";

  /* ----------- ENDPOINT APPS SCRIPT ----------- */
  // Déployé v3 (28/04/2026) — projet "Plateforme Anglais LFT — Mailer"
  const APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbw4OnyOW08yOFGD91dTVcnDxJj4jA6Z5xmFCE-TbPQHDBNxTMv0aFZexj8BvFU-MClxWg/exec";

  /* ----------- ÉTAT ----------- */
  const state = {
    config: null,
    student: null,
    currentStep: 0,
    answers: [],
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
  const html = (tag, cls, h) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (h !== undefined) n.innerHTML = h;
    return n;
  };
  const shuffle = (arr) => {
    const a = arr.slice();
    for (let i = a.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
  };
  const escapeHtml = (s) =>
    String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#039;");

  /* ----------- INIT ----------- */
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

  /* ----------- COQUILLE ----------- */
  function renderShell() {
    const root = $("#quiz-root");
    if (!root) return;
    root.innerHTML = "";
    root.classList.add("quiz-shell");

    // Barre de progression Pix-like
    const progress = el("div", "quiz-progress-pix");
    progress.id = "quiz-progress";
    progress.setAttribute("role", "progressbar");
    progress.setAttribute("aria-label", "Progression du quiz");
    const total = state.config.questions.length;
    for (let i = 0; i <= total; i++) {
      const step = el("div", "quiz-progress-pix__step");
      step.dataset.idx = String(i);
      const dot = el("div", "quiz-progress-pix__dot");
      const lbl = el("div", "quiz-progress-pix__label",
        i === 0 ? "Intro" : (i === total ? "Score" : String(i)));
      step.appendChild(dot);
      step.appendChild(lbl);
      progress.appendChild(step);
    }
    root.appendChild(progress);

    // Score live (badge)
    const liveScore = el("div", "quiz-livescore");
    liveScore.id = "quiz-livescore";
    liveScore.style.display = "none";
    liveScore.innerHTML = '<span class="quiz-livescore__icon">★</span><span class="quiz-livescore__value" id="quiz-livescore-val">0</span><span class="quiz-livescore__total"></span>';
    root.appendChild(liveScore);

    const stepHost = el("div", "glass-card quiz-step-card");
    stepHost.id = "quiz-step-host";
    root.appendChild(stepHost);
  }

  function updateProgress(idx) {
    const total = state.config.questions.length;
    const steps = document.querySelectorAll(".quiz-progress-pix__step");
    steps.forEach((s, i) => {
      s.classList.remove("is-current", "is-done");
      if (i < idx) s.classList.add("is-done");
      if (i === idx) s.classList.add("is-current");
    });
    const live = $("#quiz-livescore");
    if (idx > 0 && idx <= total) {
      live.style.display = "inline-flex";
      const correct = state.answers
        .slice(0, idx - 1)
        .filter((a, i) => a !== null && gradeQuestion(state.config.questions[i], a))
        .length;
      $("#quiz-livescore-val").textContent = String(correct);
      live.querySelector(".quiz-livescore__total").textContent = " / " + (idx - 1);
    } else {
      live.style.display = "none";
    }
  }

  function showStep(idx) {
    state.currentStep = idx;
    const host = $("#quiz-step-host");
    host.innerHTML = "";
    const total = state.config.questions.length;
    if (idx === 0) renderIntro(host);
    else if (idx > 0 && idx <= total) renderQuestion(host, idx - 1);
    else renderResult(host);
    updateProgress(idx);
  }

  /* ----------- INTRO ----------- */
  function renderIntro(host) {
    const cfg = state.config;

    if (cfg.heroImage) {
      host.appendChild(html("div", "quiz-hero-image",
        `<img src="${escapeHtml(cfg.heroImage)}" alt="" />`));
    }

    host.appendChild(el("h2", "quiz-intro-title", cfg.title));
    if (cfg.sequence) host.appendChild(el("p", "text-muted", "Séquence : " + cfg.sequence));

    const meta = el("div", "quiz-intro-meta");
    meta.innerHTML = `
      <div class="quiz-meta-card">
        <div class="quiz-meta-card__value">${cfg.questions.length}</div>
        <div class="quiz-meta-card__label">questions</div>
      </div>
      ${cfg.duration ? `<div class="quiz-meta-card"><div class="quiz-meta-card__value">${escapeHtml(cfg.duration)}</div><div class="quiz-meta-card__label">durée</div></div>` : ""}
      ${cfg.level ? `<div class="quiz-meta-card"><div class="quiz-meta-card__value">${escapeHtml(cfg.level)}</div><div class="quiz-meta-card__label">niveau</div></div>` : ""}
    `;
    host.appendChild(meta);

    if (cfg.intro) host.appendChild(html("p", "quiz-intro-text", cfg.intro));

    // Aperçu des types d'activités
    const types = [...new Set(cfg.questions.map(q => q.type))];
    if (types.length > 1) {
      const labels = {
        "qcm": "QCM", "multi": "cases à cocher", "vrai-faux": "Vrai/Faux",
        "saisie": "saisie libre", "audio-qcm": "🎧 écoute",
        "image-qcm": "🖼️ image", "matching": "🔗 association",
        "ordering": "↕️ remise en ordre", "cloze": "📝 texte à trous",
      };
      const list = types.map(t => `<span class="quiz-type-badge">${labels[t] || t}</span>`).join("");
      host.appendChild(html("div", "quiz-types-preview",
        "<strong>Tu vas rencontrer :</strong> " + list));
    }

    const form = el("form");
    form.id = "quiz-intro-form";
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
          <option value="3M5">3e M5 (LVA)</option>
          <option value="3ANGLAI1">3e NON SI</option>
          <option value="4M7">4e M7 (LVA)</option>
          <option value="4M4">4e M4 (NON SI)</option>
          <option value="4ANGL_L1">4e LCE</option>
          <option value="6M4">6e M4 (LVA)</option>
          <option value="1EUROANG1">1re Euro</option>
          <option value="TG6ANGLAIS_1">Terminale</option>
          <option value="autre">Autre</option>
        </select>
      </div>
      <div class="form-field">
        <label for="email">Ton e-mail <span class="text-muted" style="font-weight: 400;">(facultatif — pour recevoir tes résultats)</span></label>
        <input type="email" id="email" name="email" maxlength="80" autocomplete="email"
               placeholder="prenom.nom@eleve.egd.mg" />
      </div>
      <div class="quiz-actions">
        <button type="submit" class="btn btn--accent btn--lg">Commencer le quiz →</button>
      </div>
    `;
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

  /* ----------- QUESTION (dispatcher) ----------- */
  function renderQuestion(host, qIdx) {
    const q = state.config.questions[qIdx];
    const total = state.config.questions.length;

    const head = el("div", "quiz-q-head");
    head.innerHTML = `
      <span class="quiz-q-num">Question ${qIdx + 1} <small>/ ${total}</small></span>
      <span class="quiz-q-greet">${escapeHtml(state.student.firstname)} · ${escapeHtml(state.student.classGroup)}</span>
    `;
    host.appendChild(head);

    const renderers = {
      "qcm":        renderQCM,
      "multi":      renderMulti,
      "vrai-faux":  renderVraiFaux,
      "saisie":     renderSaisie,
      "audio-qcm":  renderAudioQCM,
      "image-qcm":  renderImageQCM,
      "matching":   renderMatching,
      "ordering":   renderOrdering,
      "cloze":      renderCloze,
    };
    (renderers[q.type] || renderQCM)(host, q, qIdx);

    const actions = el("div", "quiz-actions");
    const prevBtn = el("button", "btn btn--secondary", "← Précédent");
    prevBtn.type = "button";
    prevBtn.disabled = qIdx === 0;
    prevBtn.addEventListener("click", () => {
      showStep(qIdx);
      window.scrollTo({ top: 0, behavior: "smooth" });
    });
    const nextBtn = el("button", "btn btn--accent",
      qIdx + 1 === total ? "Voir mon score 🏆" : "Suivant →");
    nextBtn.type = "button";
    nextBtn.addEventListener("click", () => {
      if (qIdx + 1 === total) finalize();
      else { showStep(qIdx + 2); window.scrollTo({ top: 0, behavior: "smooth" }); }
    });
    actions.appendChild(prevBtn);
    actions.appendChild(nextBtn);
    host.appendChild(actions);
  }

  /* ----------- RENDERERS ----------- */
  function appendStem(host, q, qIdx) {
    const stem = el("div", "quiz-question");
    stem.appendChild(el("span", "quiz-question-num", String(qIdx + 1)));
    stem.appendChild(html("span", "quiz-question-text", q.prompt));
    host.appendChild(stem);
  }

  function appendImage(host, image) {
    if (!image || !image.src) return;
    const fig = el("figure", "quiz-figure");
    const img = el("img");
    img.src = image.src;
    img.alt = image.alt || "";
    img.loading = "lazy";
    fig.appendChild(img);
    if (image.caption) fig.appendChild(html("figcaption", null, image.caption));
    host.appendChild(fig);
  }

  function renderRadioOptions(host, q, qIdx, options) {
    const list = el("div", "quiz-options");
    const prev = state.answers[qIdx];
    options.forEach((opt, i) => {
      const lbl = typeof opt === "string" ? opt : opt.label;
      const labelEl = el("label", "quiz-option");
      const r = document.createElement("input");
      r.type = "radio";
      r.name = "q-" + qIdx;
      r.value = String(i);
      if (prev && prev.value === String(i)) {
        r.checked = true;
        labelEl.classList.add("is-selected");
      }
      r.addEventListener("change", () => {
        state.answers[qIdx] = { value: String(i) };
        list.querySelectorAll(".quiz-option").forEach(o => o.classList.remove("is-selected"));
        labelEl.classList.add("is-selected");
      });
      labelEl.appendChild(r);
      labelEl.appendChild(html("span", null, lbl));
      list.appendChild(labelEl);
    });
    host.appendChild(list);
  }

  function renderQCM(host, q, qIdx) {
    appendStem(host, q, qIdx);
    if (q.image) appendImage(host, q.image);
    renderRadioOptions(host, q, qIdx, q.options);
  }

  function renderMulti(host, q, qIdx) {
    appendStem(host, q, qIdx);
    if (q.image) appendImage(host, q.image);
    const list = el("div", "quiz-options");
    const prev = state.answers[qIdx];
    const prevSet = prev && prev.values ? new Set(prev.values) : new Set();
    q.options.forEach((opt, i) => {
      const lbl = typeof opt === "string" ? opt : opt.label;
      const labelEl = el("label", "quiz-option");
      const cb = document.createElement("input");
      cb.type = "checkbox";
      cb.name = "q-" + qIdx;
      cb.value = String(i);
      if (prevSet.has(String(i))) {
        cb.checked = true;
        labelEl.classList.add("is-selected");
      }
      cb.addEventListener("change", () => {
        const checked = Array.from(list.querySelectorAll("input:checked")).map(c => c.value);
        state.answers[qIdx] = { values: checked };
        labelEl.classList.toggle("is-selected", cb.checked);
      });
      labelEl.appendChild(cb);
      labelEl.appendChild(html("span", null, lbl));
      list.appendChild(labelEl);
    });
    host.appendChild(list);
  }

  function renderVraiFaux(host, q, qIdx) {
    appendStem(host, q, qIdx);
    if (q.image) appendImage(host, q.image);
    const choices = [
      { value: "vrai", label: "✓ Vrai (True)", cls: "quiz-vf-true" },
      { value: "faux", label: "✗ Faux (False)", cls: "quiz-vf-false" }
    ];
    const list = el("div", "quiz-vf-grid");
    const prev = state.answers[qIdx];
    choices.forEach(c => {
      const labelEl = el("label", "quiz-option quiz-vf-option " + c.cls);
      const r = document.createElement("input");
      r.type = "radio";
      r.name = "q-" + qIdx;
      r.value = c.value;
      if (prev && prev.value === c.value) {
        r.checked = true;
        labelEl.classList.add("is-selected");
      }
      r.addEventListener("change", () => {
        state.answers[qIdx] = { value: c.value };
        list.querySelectorAll(".quiz-option").forEach(o => o.classList.remove("is-selected"));
        labelEl.classList.add("is-selected");
      });
      labelEl.appendChild(r);
      labelEl.appendChild(html("span", "quiz-vf-label", c.label));
      list.appendChild(labelEl);
    });
    host.appendChild(list);
  }

  function renderSaisie(host, q, qIdx) {
    appendStem(host, q, qIdx);
    if (q.image) appendImage(host, q.image);
    const inp = document.createElement("input");
    inp.type = "text";
    inp.className = "quiz-input";
    inp.placeholder = q.placeholder || "Tape ta réponse en anglais…";
    inp.maxLength = 200;
    const prev = state.answers[qIdx];
    if (prev && prev.value) inp.value = prev.value;
    inp.addEventListener("input", () => {
      state.answers[qIdx] = { value: inp.value.trim() };
    });
    host.appendChild(inp);
  }

  function renderAudioQCM(host, q, qIdx) {
    appendStem(host, q, qIdx);
    const wrap = el("div", "quiz-audio-wrap");
    if (q.audioCaption)
      wrap.appendChild(html("p", "quiz-audio-caption", "🎧 " + escapeHtml(q.audioCaption)));
    const audio = document.createElement("audio");
    audio.controls = true;
    audio.preload = "metadata";
    audio.src = q.audioSrc;
    audio.className = "quiz-audio-player";
    wrap.appendChild(audio);
    if (q.audioHint)
      wrap.appendChild(html("p", "quiz-audio-hint", "💡 " + escapeHtml(q.audioHint)));
    host.appendChild(wrap);
    renderRadioOptions(host, q, qIdx, q.options);
  }

  function renderImageQCM(host, q, qIdx) {
    appendStem(host, q, qIdx);
    appendImage(host, { src: q.imageSrc, alt: q.imageAlt || "", caption: q.imageCaption });
    renderRadioOptions(host, q, qIdx, q.options);
  }

  function renderMatching(host, q, qIdx) {
    appendStem(host, q, qIdx);
    if (q.hint) host.appendChild(html("p", "quiz-hint", "💡 " + escapeHtml(q.hint)));

    if (!state.answers[qIdx] || !state.answers[qIdx].matches) {
      state.answers[qIdx] = { matches: {} };
    }
    const matches = state.answers[qIdx].matches;

    // Une seule liste mélangée des labels droits
    const rightChoices = q.pairs.map(p => p.right);

    const wrap = el("div", "quiz-matching");
    q.pairs.forEach((pair, i) => {
      const row = el("div", "quiz-matching__row");
      row.innerHTML = `
        <span class="quiz-matching__bullet">${String.fromCharCode(65 + i)}</span>
        <span class="quiz-matching__left">${escapeHtml(pair.left)}</span>
        <span class="quiz-matching__arrow">→</span>
        <select class="quiz-matching__select" data-idx="${i}">
          <option value="">— choisir —</option>
          ${rightChoices.map(r => `<option value="${escapeHtml(r)}" ${matches[i] === r ? "selected" : ""}>${escapeHtml(r)}</option>`).join("")}
        </select>
      `;
      wrap.appendChild(row);
    });
    host.appendChild(wrap);

    wrap.querySelectorAll("select").forEach(sel => {
      sel.addEventListener("change", () => {
        const idx = parseInt(sel.dataset.idx, 10);
        state.answers[qIdx].matches[idx] = sel.value;
      });
    });
  }

  function renderOrdering(host, q, qIdx) {
    appendStem(host, q, qIdx);
    if (q.hint) host.appendChild(html("p", "quiz-hint", "💡 " + escapeHtml(q.hint)));

    if (!state.answers[qIdx] || !state.answers[qIdx].order) {
      state.answers[qIdx] = { order: shuffle(q.items.map((_, i) => i)) };
    }
    const wrap = el("ol", "quiz-ordering");
    state.answers[qIdx].order.forEach((origIdx, pos) => {
      const li = el("li", "quiz-ordering__item");
      li.dataset.pos = String(pos);
      li.innerHTML = `
        <span class="quiz-ordering__num">${pos + 1}</span>
        <span class="quiz-ordering__text">${escapeHtml(q.items[origIdx])}</span>
        <span class="quiz-ordering__btns">
          <button type="button" class="quiz-ordering__btn" data-dir="up" aria-label="Monter">▲</button>
          <button type="button" class="quiz-ordering__btn" data-dir="down" aria-label="Descendre">▼</button>
        </span>`;
      wrap.appendChild(li);
    });
    host.appendChild(wrap);

    wrap.querySelectorAll(".quiz-ordering__btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const li = btn.closest("li");
        const pos = parseInt(li.dataset.pos, 10);
        const order = state.answers[qIdx].order;
        const dir = btn.dataset.dir;
        if (dir === "up" && pos > 0) [order[pos], order[pos - 1]] = [order[pos - 1], order[pos]];
        if (dir === "down" && pos < order.length - 1) [order[pos], order[pos + 1]] = [order[pos + 1], order[pos]];
        renderQuestion($("#quiz-step-host"), qIdx);
      });
    });
  }

  function renderCloze(host, q, qIdx) {
    appendStem(host, q, qIdx);
    if (q.image) appendImage(host, q.image);

    if (!state.answers[qIdx] || !state.answers[qIdx].gaps) {
      state.answers[qIdx] = { gaps: q.parts.filter(p => p.gap).map(() => null) };
    }
    const sentence = el("div", "quiz-cloze");
    let gapIdx = 0;
    q.parts.forEach(part => {
      if (part.text !== undefined) {
        sentence.appendChild(html("span", "quiz-cloze__text", escapeHtml(part.text)));
      } else if (part.gap) {
        const gIdx = gapIdx;
        const select = document.createElement("select");
        select.className = "quiz-cloze__select";
        const optEmpty = document.createElement("option");
        optEmpty.value = "";
        optEmpty.textContent = "— … —";
        select.appendChild(optEmpty);
        part.gap.forEach((opt, i) => {
          const o = document.createElement("option");
          o.value = String(i);
          o.textContent = opt;
          if (state.answers[qIdx].gaps[gIdx] === String(i)) o.selected = true;
          select.appendChild(o);
        });
        select.addEventListener("change", () => {
          state.answers[qIdx].gaps[gIdx] = select.value;
        });
        sentence.appendChild(select);
        gapIdx++;
      }
    });
    host.appendChild(sentence);
  }

  /* ----------- ÉVALUATION ----------- */
  function gradeQuestion(q, ans) {
    if (!ans) return false;
    const graders = {
      "qcm": (q, a) => String(a.value) === String(q.answer),
      "multi": (q, a) => {
        const exp = (q.answer || []).map(String).sort();
        const got = (a.values || []).map(String).sort();
        return exp.length === got.length && exp.every((v, i) => v === got[i]);
      },
      "vrai-faux": (q, a) => String(a.value) === String(q.answer),
      "saisie": (q, a) => {
        const norm = s => (s || "").toString().trim().toLowerCase()
          .replace(/[.,;:!?'"]/g, "").replace(/\s+/g, " ");
        const accepted = Array.isArray(q.answer) ? q.answer : [q.answer];
        return accepted.some(x => norm(x) === norm(a.value));
      },
      "audio-qcm": (q, a) => String(a.value) === String(q.answer),
      "image-qcm": (q, a) => String(a.value) === String(q.answer),
      "matching": (q, a) => {
        if (!a.matches) return false;
        return q.pairs.every((p, i) => a.matches[i] === p.right);
      },
      "ordering": (q, a) => {
        if (!a.order) return false;
        return a.order.every((idx, pos) => idx === pos);
      },
      "cloze": (q, a) => {
        if (!a.gaps) return false;
        const gaps = q.parts.filter(p => p.gap);
        return gaps.every((p, i) => String(a.gaps[i]) === String(p.answer));
      },
    };
    return (graders[q.type] || graders["qcm"])(q, ans);
  }

  /* ----------- FORMATAGE ----------- */
  function formatExpected(q) {
    switch (q.type) {
      case "qcm": case "audio-qcm": case "image-qcm": {
        const o = q.options[parseInt(q.answer, 10)];
        return typeof o === "string" ? o : (o ? o.label : "");
      }
      case "vrai-faux": return q.answer === "vrai" ? "Vrai" : "Faux";
      case "saisie":
        return (Array.isArray(q.answer) ? q.answer : [q.answer])
          .map(a => `<em>${escapeHtml(a)}</em>`).join(" ou ");
      case "multi":
        return (q.answer || []).map(i => {
          const o = q.options[parseInt(i, 10)];
          return typeof o === "string" ? o : (o ? o.label : i);
        }).join(", ");
      case "matching":
        return q.pairs.map(p =>
          `<strong>${escapeHtml(p.left)}</strong> → ${escapeHtml(p.right)}`).join(" · ");
      case "ordering":
        return q.items.map((it, i) =>
          `<strong>${i + 1}.</strong> ${escapeHtml(it)}`).join(" · ");
      case "cloze":
        return q.parts.filter(p => p.gap).map((p, i) =>
          `<strong>${i + 1}.</strong> <em>${escapeHtml(p.gap[parseInt(p.answer, 10)])}</em>`).join(" · ");
      default: return "";
    }
  }

  function formatStudentAnswer(q, ans) {
    if (!ans) return "(non répondu)";
    switch (q.type) {
      case "qcm": case "audio-qcm": case "image-qcm": {
        const o = q.options[parseInt(ans.value, 10)];
        return typeof o === "string" ? o : (o ? o.label : ans.value);
      }
      case "vrai-faux": return ans.value === "vrai" ? "Vrai" : "Faux";
      case "saisie":   return ans.value || "(vide)";
      case "multi":    return (ans.values || []).map(i => {
        const o = q.options[parseInt(i, 10)];
        return typeof o === "string" ? o : (o ? o.label : i);
      }).join(", ");
      case "matching":
        if (!ans.matches) return "(non rempli)";
        return q.pairs.map((p, i) => `${p.left} → ${ans.matches[i] || "?"}`).join(" · ");
      case "ordering":
        if (!ans.order) return "(non rempli)";
        return ans.order.map((origIdx, pos) =>
          `${pos + 1}. ${q.items[origIdx]}`).join(" · ");
      case "cloze":
        if (!ans.gaps) return "(non rempli)";
        return q.parts.filter(p => p.gap).map((p, i) => {
          const v = ans.gaps[i];
          return v != null ? p.gap[parseInt(v, 10)] : "?";
        }).join(" · ");
      default: return "";
    }
  }

  /* ----------- FINALISATION ----------- */
  function finalize() {
    state.submittedAt = new Date().toISOString();
    showStep(state.config.questions.length + 1);
    window.scrollTo({ top: 0, behavior: "smooth" });
  }

  /* ----------- RÉSULTAT ----------- */
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

    const hero = el("div", "quiz-result-hero");
    hero.innerHTML = `
      <div class="quiz-result-circle">
        <svg viewBox="0 0 120 120" class="quiz-result-circle__svg" aria-hidden="true">
          <circle cx="60" cy="60" r="54" class="quiz-result-circle__bg"/>
          <circle cx="60" cy="60" r="54" class="quiz-result-circle__fg"
                  style="stroke-dasharray: ${(correctCount / total) * 339.292} 339.292"/>
        </svg>
        <div class="quiz-result-circle__center">
          <div class="quiz-result-circle__num">${correctCount}<small>/${total}</small></div>
          <div class="quiz-result-circle__sub">${score20}/20</div>
        </div>
      </div>
      <div class="quiz-result-msg">
        ${correctCount === total ? "🏆 Excellent ! Toutes les réponses sont justes." :
          correctCount >= total * 0.8 ? "🎉 Très bon travail !" :
          correctCount >= total * 0.5 ? "👍 Bon début — relis la correction pour progresser." :
          "💪 Il faut revoir le cours. Pas de panique, on s'en occupe ensemble."}
      </div>
    `;
    host.appendChild(hero);

    host.appendChild(html("h3", "quiz-corr-title", "Correction détaillée"));
    detail.forEach((d, i) => {
      const block = el("div", "quiz-corr-card " + (d.ok ? "is-success" : "is-error"));
      block.innerHTML = `
        <div class="quiz-corr-head">
          <strong>Question ${i + 1}</strong>
          <span class="quiz-corr-status">${d.ok ? "✓ Correct" : "✗ Incorrect"}</span>
        </div>
        <p class="quiz-corr-prompt">${d.q.prompt}</p>
        <div class="quiz-corr-feedback ${d.ok ? "quiz-feedback--success" : "quiz-feedback--error"}">
          <strong>${d.ok ? "Bonne réponse" : "Réponse attendue"} :</strong> ${formatExpected(d.q)}
        </div>
        ${d.q.explanation ? `<p class="quiz-corr-expl"><strong>Explication :</strong> ${d.q.explanation}</p>` : ""}
      `;
      host.appendChild(block);
    });

    const sendCard = el("div", "glass-card glass--colored quiz-send-card");
    sendCard.innerHTML = `
      <h3>📧 Envoyer mes résultats</h3>
      <p>Tes résultats seront envoyés à Mme FALIMANANA${state.student.email ? " et à toi-même" : ""}, avec la correction détaillée.</p>
    `;
    const sendBtn = el("button", "btn btn--accent btn--lg", "Envoyer à Mme FALIMANANA");
    sendBtn.id = "quiz-send-btn";
    sendBtn.addEventListener("click", () => sendResults({ correctCount, score20, detail, sendBtn }));
    sendCard.appendChild(sendBtn);
    const status = html("p", "text-muted", "");
    status.id = "quiz-send-status";
    sendCard.appendChild(status);
    host.appendChild(sendCard);

    const back = el("div", "quiz-actions");
    back.style.justifyContent = "center";
    const homeBtn = el("a", "btn btn--secondary", "← Retour à l'accueil");
    homeBtn.href = "../../index.html";
    const printBtn = el("button", "btn btn--secondary", "🖨️ Imprimer cette page");
    printBtn.type = "button";
    printBtn.addEventListener("click", () => window.print());
    back.appendChild(homeBtn);
    back.appendChild(printBtn);
    host.appendChild(back);
  }

  /* ----------- ENVOI APPS SCRIPT ----------- */
  function sendResults({ correctCount, score20, detail, sendBtn }) {
    const status = $("#quiz-send-status");
    sendBtn.disabled = true;
    status.textContent = "Envoi en cours…";
    status.className = "text-muted";

    const stripHtml = s => String(s).replace(/<[^>]+>/g, "");
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
        question: stripHtml(d.q.prompt),
        type: d.q.type,
        studentAnswer: stripHtml(formatStudentAnswer(d.q, d.ans)),
        expectedAnswer: stripHtml(formatExpected(d.q)),
        correct: d.ok,
      })),
      teacherEmail: "salamo.falimanana@egd.mg",
    };

    fetch(APPS_SCRIPT_URL, {
      method: "POST",
      mode: "no-cors",
      keepalive: true,
      headers: { "Content-Type": "text/plain;charset=utf-8" },
      body: JSON.stringify(payload),
    })
      .then(() => {
        status.textContent = "✓ Tes résultats ont bien été envoyés à Mme FALIMANANA. Merci !";
        status.className = "quiz-feedback quiz-feedback--success";
        sendBtn.style.display = "none";
      })
      .catch(err => {
        console.error(err);
        status.textContent = "❌ Erreur d'envoi. Demande à Mme FALIMANANA, ou réessaie plus tard.";
        status.className = "quiz-feedback quiz-feedback--error";
        sendBtn.disabled = false;
      });
  }

  /* ----------- API ----------- */
  global.QuizEngine = { init };

})(window);

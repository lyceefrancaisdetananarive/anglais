/* =========================================================
   ANALYTICS — Plateforme Anglais LFT
   Mme FALIMANANA · Comptage de visites anonyme
   =========================================================
   Principes :
   - Aucun cookie, aucun identifiant unique
   - Aucune IP collectée (Apps Script ne la lit pas)
   - Respect de Do Not Track (DNT)
   - Pas de fingerprinting agressif
   - Données minimales : type d'appareil, OS, navigateur, langue,
     timezone (= pays approximatif), résolution écran, page visitée
   ========================================================= */

(function () {
  "use strict";

  /* === MÊME ENDPOINT QUE LES QUIZ === */
  const APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbw4OnyOW08yOFGD91dTVcnDxJj4jA6Z5xmFCE-TbPQHDBNxTMv0aFZexj8BvFU-MClxWg/exec";

  /* === RESPECT « DO NOT TRACK » === */
  if (navigator.doNotTrack === "1" ||
      window.doNotTrack === "1" ||
      navigator.msDoNotTrack === "1") {
    return;
  }

  /* === DÉDUPLICATION : 1 ping par page par session === */
  const sessionKey = "lft_anglais_visit_" + location.pathname;
  if (sessionStorage.getItem(sessionKey)) return;
  sessionStorage.setItem(sessionKey, String(Date.now()));

  /* === DÉTECTION DU TYPE D'APPAREIL === */
  function detectDeviceType(ua) {
    if (/iPad|tablet|Tab/i.test(ua) ||
        (/Android/i.test(ua) && !/Mobile/i.test(ua))) return "tablet";
    if (/Mobi|iPhone|Android|webOS|BlackBerry|IEMobile|Opera Mini/i.test(ua)) return "mobile";
    return "desktop";
  }

  /* === DÉTECTION DE LA MARQUE/MODÈLE === */
  function detectBrand(ua) {
    if (/iPhone/i.test(ua)) return "Apple iPhone";
    if (/iPad/i.test(ua))   return "Apple iPad";
    if (/iPod/i.test(ua))   return "Apple iPod";
    if (/Macintosh|Mac OS/i.test(ua)) return "Apple Mac";

    // Android : tenter d'extraire la marque
    const androidMatch = ua.match(/Android[^;)]*;\s*([^;)]+)/);
    if (androidMatch) {
      const model = androidMatch[1].trim().split(" Build/")[0];
      // Marques fréquentes
      if (/SM-|Galaxy|Samsung/i.test(model))    return "Samsung " + model;
      if (/Pixel/i.test(model))                 return "Google " + model;
      if (/Mi |Redmi|POCO|Xiaomi/i.test(model)) return "Xiaomi " + model;
      if (/HUAWEI|Honor/i.test(model))          return "Huawei " + model;
      if (/OPPO/i.test(model))                  return "OPPO " + model;
      if (/Nokia/i.test(model))                 return "Nokia " + model;
      if (/Tecno|TECNO/i.test(model))           return "Tecno " + model;   // courant en Afrique
      if (/Itel|ITEL/i.test(model))             return "Itel " + model;    // courant en Afrique
      if (/Infinix|INFINIX/i.test(model))       return "Infinix " + model;
      return "Android " + model;
    }
    if (/Android/i.test(ua)) return "Android (générique)";

    if (/Windows/i.test(ua)) return "PC Windows";
    if (/Linux/i.test(ua))   return "PC Linux";
    if (/CrOS/i.test(ua))    return "Chromebook";

    return "Autre";
  }

  /* === DÉTECTION DE L'OS === */
  function detectOS(ua) {
    let m;
    if ((m = ua.match(/iPhone OS (\d+_\d+)/i)))  return "iOS " + m[1].replace("_", ".");
    if ((m = ua.match(/iPad; CPU OS (\d+_\d+)/i))) return "iPadOS " + m[1].replace("_", ".");
    if ((m = ua.match(/Android (\d+(?:\.\d+)?)/i))) return "Android " + m[1];
    if ((m = ua.match(/Mac OS X (\d+[._]\d+(?:[._]\d+)?)/i))) return "macOS " + m[1].replace(/_/g, ".");
    if (/Windows NT 10\.0/i.test(ua)) return "Windows 10/11";
    if (/Windows NT 6\.3/i.test(ua))  return "Windows 8.1";
    if (/Windows NT 6\.2/i.test(ua))  return "Windows 8";
    if (/Windows NT 6\.1/i.test(ua))  return "Windows 7";
    if (/Linux/i.test(ua))            return "Linux";
    if (/CrOS/i.test(ua))             return "ChromeOS";
    return "Inconnu";
  }

  /* === DÉTECTION DU NAVIGATEUR === */
  function detectBrowser(ua) {
    let m;
    // Edge en premier (User-Agent contient aussi Chrome/Safari)
    if ((m = ua.match(/Edg\/(\d+)/i))) return "Edge " + m[1];
    if ((m = ua.match(/OPR\/(\d+)/i))) return "Opera " + m[1];
    if ((m = ua.match(/Firefox\/(\d+)/i))) return "Firefox " + m[1];
    if ((m = ua.match(/Chrome\/(\d+)/i))) return "Chrome " + m[1];
    if ((m = ua.match(/Version\/(\d+).*Safari/i))) return "Safari " + m[1];
    if (/Safari/i.test(ua)) return "Safari";
    return "Autre";
  }

  /* === COLLECTE === */
  const ua = navigator.userAgent || "";
  const data = {
    type:        "visit",
    page:        location.pathname || "/",
    title:       (document.title || "").substring(0, 200),
    deviceType:  detectDeviceType(ua),
    deviceBrand: detectBrand(ua),
    osName:      detectOS(ua),
    browser:     detectBrowser(ua),
    language:    navigator.language || "",
    timezone:    (function () {
      try { return Intl.DateTimeFormat().resolvedOptions().timeZone || ""; }
      catch (e) { return ""; }
    })(),
    screen:      [screen.width, screen.height].join("x"),
    referrer:    (function () {
      if (!document.referrer) return "(direct)";
      try { return new URL(document.referrer).hostname; }
      catch (e) { return "(autre)"; }
    })(),
    visitedAt:   new Date().toISOString(),
  };

  /* === ENVOI EN « FIRE-AND-FORGET » === */
  if (APPS_SCRIPT_URL.includes("REMPLACEZ_PAR_VOTRE_ID")) {
    console.info("[Analytics] mode test :", data);
    return;
  }

  // On ne veut surtout pas bloquer la page si l'envoi échoue.
  // navigator.sendBeacon est idéal mais ne supporte pas no-cors,
  // donc on utilise fetch en mode no-cors qui ignore les erreurs réseau.
  try {
    fetch(APPS_SCRIPT_URL, {
      method: "POST",
      mode: "no-cors",
      keepalive: true,
      headers: { "Content-Type": "text/plain;charset=utf-8" },
      body: JSON.stringify(data),
    }).catch(function () { /* silencieux */ });
  } catch (e) {
    /* silencieux : on ne dégrade jamais l'expérience utilisateur */
  }
})();

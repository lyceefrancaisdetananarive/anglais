# Espace Anglais — Lycée Français de Tananarive

> Plateforme web pédagogique d'anglais pour les classes de Mme **Salamo FALIMANANA**, enseignante au **Lycée Français de Tananarive** (établissement AEFE en gestion directe, Madagascar).

[![Déploiement Pages](https://img.shields.io/badge/déploiement-GitHub%20Pages-000091?style=flat&logo=github)](#)
[![DSFR](https://img.shields.io/badge/design-DSFR-000091?style=flat)](https://www.systeme-de-design.gouv.fr/)
[![Accessibilité](https://img.shields.io/badge/accessibilité-RGAA%20AA-18753c?style=flat)](#)
[![Licence](https://img.shields.io/badge/licence-pédagogique%20interne-e6007e?style=flat)](#)

---

## Sommaire

1. [Présentation du projet](#1-présentation-du-projet)
2. [Pour démarrer (3 minutes)](#2-pour-démarrer-3-minutes)
3. [Architecture du repo](#3-architecture-du-repo)
4. [Configuration Apps Script (cœur backend)](#4-configuration-apps-script-cœur-backend)
5. [Déploiement sur GitHub Pages](#5-déploiement-sur-github-pages)
6. [Comment ajouter un nouveau quiz](#6-comment-ajouter-un-nouveau-quiz)
7. [Charte graphique et accessibilité](#7-charte-graphique-et-accessibilité)
8. [Plan de sprints](#8-plan-de-sprints)

---

## 1. Présentation du projet

Cette plateforme rassemble les **séquences pédagogiques**, **quiz interactifs** et **fiches d'activités imprimables** utilisés par Mme FALIMANANA pour enseigner l'anglais en :

- **6e** (M4 — LVA)
- **4e** (M7 LVA, M4 NON SI, ANGL L1 LCE)
- **3e** (M5 LVA, ANGLAI1 NON SI)
- **1ère euro** (1EUROANG1 — Approfondissement Linguistique)
- **Terminale** (TG6ANGLAIS_1)

Les quiz peuvent être partagés par lien aux élèves. À la fin du quiz, les résultats sont :
- **archivés automatiquement** dans une feuille Google Sheets ;
- **envoyés par mail à l'enseignante** (et à l'élève s'il a saisi son adresse), avec la note et la correction détaillée.

Les fiches d'activité imprimables (PDF) respectent la **charte graphique AEFE-Marque État 12-2023**.

### Principes fondateurs

- 🇫🇷 **Système de Design de l'État (DSFR)** — palette officielle, typographie Marianne™
- 🎨 **Identité LFT** — accent magenta du logo
- 🪞 **Liquid glass** — touches modernes (`backdrop-filter`) sur les zones gamifiées
- ♿ **Accessibilité RGAA AA** — contrastes, ARIA, navigation clavier, `prefers-reduced-motion`
- 📱 **Responsive** — mobile, tablette, ordinateur, impression
- 📚 **Programme officiel** — conforme au BO Éducation Nationale (cycle 4 et lycée)

---

## 2. Pour démarrer (3 minutes)

```bash
# Cloner le repo (après push initial)
git clone https://github.com/lyceefrancaisdetananarive/anglais.git
cd anglais

# Tester en local — n'importe quel serveur statique fait l'affaire
python3 -m http.server 8080
# → http://localhost:8080
```

Aucune dépendance npm, aucun build : c'est du HTML/CSS/JS pur.

---

## 3. Architecture du repo

```
anglais/
├── index.html                # Tableau de bord (point d'entrée)
├── README.md                 # Ce fichier
├── .gitignore
├── .github/
│   └── workflows/
│       └── pages.yml         # Déploiement auto sur GitHub Pages
│
├── assets/
│   ├── css/
│   │   └── style.css         # Thème complet (DSFR + LFT + liquid glass)
│   ├── js/
│   │   └── quiz-engine.js    # Moteur de quiz statique
│   ├── fonts/                # Marianne en woff2 (6 graisses)
│   ├── img/                  # Logos LFT, AEFE
│   └── audio/                # Documents sonores des séquences
│
├── quiz/                     # Quiz interactifs par niveau
│   ├── 6e/
│   ├── 4e/
│   └── 3e/
│       └── street-art.html   # ★ Quiz exemple — Sprint 1
│
├── sequences/                # Pages dédiées aux séquences (Sprint 2)
│   ├── 6e/
│   ├── 4e/
│   └── 3e/
│
├── pdf-imprimables/          # Bibliothèque PDF — fiches d'activité
│   └── fiche_dnl_svt_1ere.pdf
│
└── apps-script/
    └── Code.gs               # Backend Google Apps Script (mail + Sheets)
```

---

## 4. Configuration Apps Script (cœur backend)

> Cette étape est **à faire UNE SEULE FOIS** au déploiement initial. Le script archive les résultats et envoie les mails à l'enseignante et à l'élève.

### Étape 1 — Créer le projet Apps Script

1. Aller sur [script.google.com](https://script.google.com/) connectée avec le compte `salamo.falimanana@egd.mg`.
2. **Nouveau projet** → renommer en *« Plateforme Anglais LFT — Mailer »*.
3. Coller le contenu de `apps-script/Code.gs` dans l'éditeur.
4. Vérifier que `TEACHER_EMAIL` est correct en haut du fichier (ligne 16).

### Étape 2 — Tester en local Apps Script

1. Cliquer sur la fonction **`testManuel`** dans la liste déroulante puis sur **▶ Exécuter**.
2. Autoriser les permissions demandées (envoi de mail, accès Sheets, accès Drive).
3. Vérifier que :
   - un mail est arrivé à `salamo.falimanana@egd.mg` ;
   - une feuille *« Plateforme Anglais LFT — Résultats quiz »* a été créée dans le Drive.

### Étape 3 — Publier comme application web

1. Cliquer sur **Déployer → Nouveau déploiement**.
2. Type : **Application Web**.
3. Description : `v1 — Réception des résultats quiz`.
4. Exécuter en tant que : **Moi** (Mme FALIMANANA).
5. Qui peut accéder : **Tout le monde** (anonyme — nécessaire pour que les élèves puissent envoyer sans être connectés à Google).
6. Cliquer sur **Déployer** puis **Autoriser**.
7. **Copier l'URL** qui finit par `/exec` (du type `https://script.google.com/macros/s/AKfycby.../exec`).

### Étape 4 — Brancher l'URL côté frontend

Ouvrir `assets/js/quiz-engine.js`, ligne 12 :

```js
const APPS_SCRIPT_URL = "https://script.google.com/macros/s/REMPLACEZ_PAR_VOTRE_ID/exec";
```

Remplacer par l'URL copiée à l'étape 3, commiter et pusher.

> 💡 **Test** : ouvrir le quiz Street Art, le passer en entier, cliquer sur *Envoyer mes résultats*. Vérifier la réception du mail et la nouvelle ligne dans la feuille Sheets.

---

## 5. Déploiement sur GitHub Pages

Le workflow `.github/workflows/pages.yml` est préconfiguré. Étapes :

1. **Créer le repo** sur GitHub : [github.com/lyceefrancaisdetananarive/anglais](https://github.com/lyceefrancaisdetananarive/anglais)
2. **Pousser le code** :
   ```bash
   git remote add origin https://github.com/lyceefrancaisdetananarive/anglais.git
   git push -u origin main
   ```
3. Aller dans **Settings → Pages**.
4. *Source* : sélectionner **GitHub Actions**.
5. Le déploiement démarre automatiquement à chaque push.
6. URL publique : `https://lyceefrancaisdetananarive.github.io/anglais/`

---

## 6. Comment ajouter un nouveau quiz

1. **Dupliquer** le fichier `quiz/3e/street-art.html` dans le bon sous-dossier de niveau.
2. **Renommer** le fichier (ex. `quiz/4e/voyages-australie.html`).
3. **Adapter** la balise `<title>` et le bloc d'en-tête.
4. **Modifier le bloc `<script>`** en bas de page : changer `id`, `title`, `level`, `sequence`, `intro`, et la liste `questions`.

### Format des questions

Le moteur supporte **4 types** :

```js
// QCM (un seul choix correct)
{
  type: "qcm",
  prompt: "Quelle est la capitale de l'Angleterre ?",
  options: ["Cardiff", "London", "Edinburgh", "Dublin"],
  answer: 1,                       // index 0-based de la bonne réponse
  explanation: "Optionnel — affichée dans la correction.",
}

// Vrai / Faux
{
  type: "vrai-faux",
  prompt: "Banksy est un artiste français.",
  answer: "faux",
}

// Saisie libre (la comparaison ignore casse, ponctuation, espaces multiples)
{
  type: "saisie",
  prompt: "Conjugue 'to be' à la 1re personne du singulier au présent.",
  placeholder: "I ...",
  answer: ["i am", "i'm"],         // tableau de réponses acceptées
}

// Cases à cocher (plusieurs bonnes réponses)
{
  type: "multi",
  prompt: "Coche les expressions correctes pour donner son avis.",
  options: ["I think", "I am agree", "In my opinion", "According to me"],
  answer: ["0", "2"],              // indices comme strings
}
```

### Médias (image et audio)

Sur n'importe quelle question on peut ajouter :

```js
image: {
  src: "../../assets/img/sequences/banksy-girl-balloon.jpg",
  alt: "Œuvre Girl with Balloon de Banksy",
  caption: "Banksy, Girl with Balloon, Londres, 2002.",
},
audio: {
  src: "../../assets/audio/eval_co_3e_flight5.mp3",
  note: "Écoute attentivement deux fois avant de répondre.",
},
```

### Mettre à jour le tableau de bord

Dans `index.html`, augmenter le compteur de quiz dans la carte du niveau et la statistique globale.

---

## 7. Charte graphique et accessibilité

### Palette principale

| Token | Hex | Usage |
|---|---|---|
| Bleu France 500 | `#000091` | Couleur primaire — boutons, liens, titres |
| Rouge Marianne | `#e1000f` | Erreurs, accents tricolores |
| Magenta LFT | `#e6007e` | Accent ludique — quiz, badges, hover |
| Bleu marine LFT | `#003b5c` | Mise en page institutionnelle |
| Succès | `#18753c` | Réponses correctes |
| Avertissement | `#b34000` | Quiz partiels |
| Erreur | `#ce0500` | Réponses incorrectes |

### Typographie — Marianne (officielle de l'État)

6 graisses livrées dans `assets/fonts/` (woff2) : Light, Regular, Italic, Medium, Bold, ExtraBold.

### Audit RGAA — checklist Sprint 1

- [x] Contrastes ≥ 4.5:1 sur le texte normal (palette DSFR validée)
- [x] Skip-link en début de page
- [x] Landmarks ARIA (`<header>`, `<main>`, `<footer>`, `role="banner"`...)
- [x] Labels explicites sur tous les formulaires
- [x] `aria-current` sur le lien de page courante
- [x] Support `prefers-reduced-motion`
- [x] Focus visible sur tous les éléments interactifs
- [x] Hiérarchie sémantique des titres (h1 → h2 → h3)
- [ ] Audit Lighthouse complet (Sprint 4)
- [ ] Audit RGAA externe (Sprint 4)

---

## 8. Plan de sprints

| Sprint | Objectifs | État |
|---|---|---|
| **Sprint 1** | Squelette + charte + dashboard + 1 quiz exemple 3e + Apps Script | ✅ Livré |
| **Sprint 2** | 4 séquences par niveau (6e/4e/3e) + génération PDF imprimable | ⏳ À venir |
| **Sprint 3** | 1ère APPROF LING + Terminale + bibliothèque DNL SVT | ⏳ |
| **Sprint 4** | NON SI/LCE + audit RGAA AA externe + doc enseignante | ⏳ |

---

## Crédits

- **Conception pédagogique** : Mme Salamo FALIMANANA — Lycée Français de Tananarive
- **Développement** : avec l'aide de Claude (Anthropic)
- **Inspirations** : DSFR — Système de Design de l'État · Charte AEFE-Marque État · Try n' Fly (manuel scolaire)

## Licence

Code source publié à des fins pédagogiques internes au Lycée Français de Tananarive. Usage hors LFT : nous contacter ([salamo.falimanana@egd.mg](mailto:salamo.falimanana@egd.mg)).

Logos AEFE / Marianne / République française : usages soumis à la Charte de la Marque État (décembre 2023).

Marianne™ : police domaine publique, créée pour l'État français.

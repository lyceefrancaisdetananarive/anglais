/* =========================================================
   PROGRESSION ANNUELLE — Plateforme Anglais LFT 2025-2026
   Mme FALIMANANA · Conforme BO Eduscol
   =========================================================
   Sources :
   - BO Eduscol : programme cycle 4 et lycée LVA
   - Référentiel CECRL
   - Manuels Try n' Fly (Hatier) 6e/4e/3e
   - Inspiration : Cambridge English, Linguascope, Twinkl, Pix
   - Adaptation AEFE Madagascar : ancrage local
   ========================================================= */

window.PROGRESSION_ANNUELLE = {

  /* ====================================================== */
  /* 6e LVA — A1                                             */
  /* ====================================================== */
  "6e": {
    label: "6ème LVA",
    cecrl: "A1",
    classe: "6M4 (Mme FALIMANANA)",
    horaire: "3h hebdomadaires",
    programme: "Cycle 3 — Découverte de l'anglais",
    couleur: "linear-gradient(135deg, var(--success-500), var(--bf-500))",
    intro: "Première année d'anglais au collège. L'objectif est de poser des bases solides : se présenter, parler de soi et de son environnement immédiat (école, famille, goûts), maîtriser l'alphabet, les nombres, les jours de la semaine. Approche résolument <strong>ludique et orale</strong> avec jeux de rôle, chants et saynètes.",
    sequences: [
      {
        n: 1, periode: "T1 (sept-oct)",
        titre: "Welcome to Big Ben Academy!",
        theme: "Premiers pas — l'école imaginaire à Londres",
        axe: "Langages — l'identité personnelle",
        langue: "Verbe <em>to be</em>, alphabet, nombres 1-20, déterminants possessifs",
        lexique: "Salutations, nationalités, école, couleurs, jours",
        culturel: "Big Ben, Londres, système scolaire britannique (uniforme, houses)",
        tache: "Carte de présentation audio (1 min)",
        cecrl: "A1",
        statut: "live",
        url: "../quiz/6e/welcome-big-ben.html"
      },
      {
        n: 2, periode: "T1 (nov-déc)",
        titre: "My Family Tree",
        theme: "La famille et les proches",
        axe: "Langages — environnement familier",
        langue: "<em>Have got</em>, déterminants possessifs (his/her), pluriels irréguliers",
        lexique: "Famille (mum, dad, sister, grandparents), animaux domestiques",
        culturel: "Familles royales britanniques, pets in the UK",
        tache: "Présenter son arbre généalogique en 8 phrases",
        cecrl: "A1",
        statut: "live",
        url: "../quiz/6e/family-tree.html"
      },
      {
        n: 3, periode: "T2 (janv-fév)",
        titre: "What I Love",
        theme: "Goûts, hobbies et préférences",
        axe: "Langages — exprimer ses goûts",
        langue: "Présent simple (I like / I don't like), verbes d'action",
        lexique: "Sports, musique, films, jeux, hobbies (~30 mots)",
        culturel: "Sports britanniques (cricket, rugby), Harry Potter, K-pop",
        tache: "Mini-podcast sur ses 5 hobbies favoris (2 min)",
        cecrl: "A1",
        statut: "live",
        url: "../quiz/6e/what-i-love.html"
      },
      {
        n: 4, periode: "T2 (mars)",
        titre: "Let's Eat!",
        theme: "Alimentation et goûts culinaires",
        axe: "Rencontres culturelles — habitudes alimentaires",
        langue: "Quantifieurs (some, any, a lot of), question forms",
        lexique: "Aliments, repas, partitifs (a slice of, a glass of)",
        culturel: "Petit-déjeuner anglais, fish and chips, food à Madagascar",
        tache: "Menu du jour bilingue à présenter à la cantine",
        cecrl: "A1",
        statut: "live",
        url: "../quiz/6e/lets-eat.html"
      },
      {
        n: 5, periode: "T3 (avril)",
        titre: "Everyday Life in London",
        theme: "Une journée type en ville",
        axe: "Voyages et migrations — découvrir une grande ville",
        langue: "Présent simple, prépositions de lieu (in/on/at), heures",
        lexique: "Lieux de la ville, activités quotidiennes, transports",
        culturel: "Métro de Londres (Tube), Buckingham Palace, Camden Market",
        tache: "Itinéraire commenté d'une journée à Londres (vidéo 3 min)",
        cecrl: "A1",
        statut: "live",
        url: "../quiz/6e/london-life.html"
      },
      {
        n: 6, periode: "T3 (mai-juin)",
        titre: "My Holidays in Madagascar",
        theme: "Vacances et météo — pont local",
        axe: "Rencontres culturelles — promouvoir Madagascar en anglais",
        langue: "Modal <em>can/can't</em>, futur (be going to), météo",
        lexique: "Vacances, météo, paysages, activités outdoor",
        culturel: "Tourisme à Madagascar (Nosy Be, Tana, lémuriens)",
        tache: "Brochure touristique de Madagascar pour des élèves anglais",
        cecrl: "A1+",
        statut: "todo"
      }
    ]
  },

  /* ====================================================== */
  /* 4e LVA — A2                                             */
  /* ====================================================== */
  "4e": {
    label: "4ème LVA",
    cecrl: "A2",
    classe: "4M7 (Mme FALIMANANA) · LVA standard",
    horaire: "3h hebdomadaires",
    programme: "Cycle 4 — Approfondissement",
    couleur: "linear-gradient(135deg, var(--bf-500), var(--lft-magenta))",
    intro: "L'anglais s'enrichit en 4<sup>e</sup> avec l'introduction du <strong>prétérit</strong>, des comparatifs et des modaux. Les élèves découvrent des thématiques plus complexes : voyages, environnement, sport, culture musicale. La <strong>lecture cursive</strong> entre dans le programme avec des romans courts adaptés.",
    sequences: [
      {
        n: 1, periode: "T1 (sept-oct)",
        titre: "Stuck at Big Bay School",
        theme: "Une rentrée en Nouvelle-Zélande",
        axe: "École et société — vie scolaire ailleurs",
        langue: "Présent simple vs continu, comparatifs, modaux <em>have to/must</em>",
        lexique: "École, recess, uniforme, sentiments",
        culturel: "Nouvelle-Zélande (Aotearoa), peuple māori, kia ora",
        tache: "Journal d'un nouvel élève (300 mots)",
        cecrl: "A1+/A2",
        statut: "live",
        url: "../quiz/4e/stuck-big-bay.html"
      },
      {
        n: 2, periode: "T1 (nov-déc)",
        titre: "Sport Heroes",
        theme: "Biographies de grands sportifs anglophones",
        axe: "Représentations de soi — figures inspirantes",
        langue: "Prétérit simple (régulier + irréguliers), modaux <em>can/could</em>",
        lexique: "Sports, biographie, succès, échecs, persévérance",
        culturel: "Serena Williams, Usain Bolt, David Beckham, sport à Madagascar",
        tache: "Mini-biographie d'un sportif (200 mots) + oral 2 min",
        cecrl: "A2",
        statut: "live",
        url: "../quiz/4e/sport-heroes.html"
      },
      {
        n: 3, periode: "T2 (janv-fév)",
        titre: "Climate Action Now",
        theme: "Environnement et engagement des jeunes",
        axe: "École et société — engagement citoyen",
        langue: "Modaux d'obligation (<em>must, should, have to</em>), futur (will)",
        lexique: "Environnement, déchets, énergies, écogestes",
        culturel: "Greta Thunberg, Fridays for Future, déforestation à Madagascar",
        tache: "Affiche bilingue d'écogestes + débat de 5 min",
        cecrl: "A2",
        statut: "live",
        url: "../quiz/4e/climate-action.html"
      },
      {
        n: 4, periode: "T2 (mars)",
        titre: "An Australian Journey",
        theme: "Voyage initiatique en Australie autochtone",
        axe: "Rencontres culturelles — peuples premiers",
        langue: "Prétérit (récit), connecteurs temporels (then, after, finally)",
        lexique: "Voyage, paysages, animaux australiens, peuples autochtones",
        culturel: "Aborigènes, Uluru, Dreamtime, Sydney",
        tache: "Carnet de voyage illustré (4 pages)",
        cecrl: "A2",
        statut: "live",
        url: "../quiz/4e/australian-journey.html"
      },
      {
        n: 5, periode: "T3 (avril-mai)",
        titre: "Music Through the Decades",
        theme: "Histoire de la musique anglophone",
        axe: "Langages — la musique comme expression",
        langue: "Present perfect (since/for), prétérit, voix passive",
        lexique: "Musique, instruments, succès, charts, festivals",
        culturel: "Beatles, Elvis, Bob Marley, Beyoncé, salegy malgache",
        tache: "Présenter un artiste en 3 min (oral)",
        cecrl: "A2+",
        statut: "todo"
      },
      {
        n: 6, periode: "T3 (mai-juin)",
        titre: "My Town, My Story",
        theme: "Décrire et raconter son quartier",
        axe: "Représentations de soi — ancrage local",
        langue: "Present perfect (have been), il y a (there is/are), prépositions",
        lexique: "Ville, monuments, histoire personnelle, anecdotes",
        culturel: "Quartiers de Tana, Antaninarenina, Analakely, marché des fleurs",
        tache: "Visite guidée filmée de son quartier (4 min)",
        cecrl: "A2+",
        statut: "todo"
      }
    ]
  },

  /* ====================================================== */
  /* 4e NON SI — Section Internationale                       */
  /* ====================================================== */
  "4e-non-si": {
    label: "4ème NON SI",
    cecrl: "A2/B1",
    classe: "4M4 (Mme FALIMANANA) · Section Internationale Britannique",
    horaire: "6h hebdomadaires (4h langue + 2h littérature)",
    programme: "Programme renforcé OIB — Lecture intégrale + civilisation",
    couleur: "linear-gradient(135deg, var(--lft-magenta-dark), var(--bf-500))",
    intro: "Programme exigeant centré sur la <strong>littérature de jeunesse anglophone</strong> et l'étude de la <strong>civilisation britannique</strong>. Lecture intégrale d'œuvres, analyse littéraire (point of view, characterization, themes), préparation à long terme à l'<strong>OIB (Option Internationale du Baccalauréat)</strong>.",
    sequences: [
      {
        n: 1, periode: "T1",
        titre: "Matilda — Roald Dahl (1988)",
        theme: "Pouvoir, abus d'autorité et résistance",
        axe: "Littérature jeunesse britannique — humour noir",
        langue: "Past simple, vocabulaire littéraire (theme, character, plot)",
        lexique: "Lexique de la littérature, sentiments, descriptions",
        culturel: "Roald Dahl, écoles britanniques, dark humour",
        tache: "Critique littéraire (300 mots) + book trailer",
        cecrl: "A2/B1",
        statut: "live",
        url: "../quiz/non-si/matilda.html"
      },
      {
        n: 2, periode: "T2",
        titre: "The Giver — Lois Lowry (1993)",
        theme: "Dystopie, contrôle social, mémoire collective",
        axe: "Fiction et société — utopies/dystopies",
        langue: "Voix passive, conditional, vocabulaire abstrait",
        lexique: "Société, contrôle, émotions, choix, liberté",
        culturel: "Littérature dystopique YA (Lowry, Collins, Roth)",
        tache: "Essai 350 mots : Would you live in The Community?",
        cecrl: "B1",
        statut: "todo"
      },
      {
        n: 3, periode: "T3",
        titre: "British Institutions",
        theme: "Monarchie, Parlement, Brexit",
        axe: "Civilisation — institutions britanniques",
        langue: "Modaux de probabilité, structures complexes",
        lexique: "Politique, institutions, pouvoirs, médias",
        culturel: "Parliament, monarchy, devolution, Brexit, Commonwealth",
        tache: "Présentation orale (8 min) — une institution",
        cecrl: "B1",
        statut: "todo"
      }
    ]
  },

  /* ====================================================== */
  /* 4e LCE — Langues et Cultures Européennes                 */
  /* ====================================================== */
  "4e-lce": {
    label: "4ème LCE",
    cecrl: "A2+ (objectif culturel)",
    classe: "4ANGL L1 (Mme FALIMANANA) · LCE",
    horaire: "2h hebdomadaires",
    programme: "Option d'approfondissement culturel",
    couleur: "linear-gradient(135deg, var(--or, #C9A027), var(--lft-magenta))",
    intro: "Option à finalité <strong>culturelle</strong> plutôt que linguistique pure. Trois modules thématiques pour découvrir les civilisations anglophones européennes (Royaume-Uni, Irlande) et leurs liens avec le continent. Évaluation par positionnement de compétences.",
    sequences: [
      {
        n: 1, periode: "T1 — Module 1",
        titre: "Britain & Europe",
        theme: "Histoire des relations RU-Continent",
        axe: "Voyages et migrations — Europe",
        langue: "Discours rapporté, expressions historiques",
        lexique: "Histoire, politique, conquête, intégration",
        culturel: "Conquête normande, Tudors, EU, Brexit",
        tache: "Chronologie commentée des grandes étapes",
        cecrl: "A2+",
        statut: "live",
        url: "../quiz/lce/britain-europe.html"
      },
      {
        n: 2, periode: "T2 — Module 2",
        titre: "Ireland: A Story of Resilience",
        theme: "Identité irlandaise et résilience",
        axe: "Représentations de soi — culture celte",
        langue: "Past tenses, narration",
        lexique: "Identité, résilience, mythologie, musique",
        culturel: "Grande Famine, Troubles, Yeats, Joyce, U2",
        tache: "Mini-exposé en binôme sur une figure irlandaise",
        cecrl: "A2+",
        statut: "live",
        url: "../quiz/lce/ireland.html"
      },
      {
        n: 3, periode: "T3 — Module 3",
        titre: "Migrations & Identities",
        theme: "Mouvements de population qui ont façonné l'Europe",
        axe: "Voyages et migrations — diaspora",
        langue: "Conditionnel, vocabulaire de la migration",
        lexique: "Migration, identité, intégration, hybridité",
        culturel: "Huguenots, Jewish refugees, Polish migration, Windrush",
        tache: "Portrait écrit d'un migrant fictif (200 mots)",
        cecrl: "A2+/B1",
        statut: "todo"
      }
    ]
  },

  /* ====================================================== */
  /* 3e LVA — A2+/B1                                         */
  /* ====================================================== */
  "3e": {
    label: "3ème LVA",
    cecrl: "A2+/B1",
    classe: "3M5 (Mme FALIMANANA) · LVA standard",
    horaire: "3h hebdomadaires",
    programme: "Cycle 4 — Préparation DNB",
    couleur: "linear-gradient(135deg, var(--lft-magenta), var(--lft-magenta-dark))",
    intro: "Année de consolidation et préparation au <strong>Diplôme National du Brevet (DNB)</strong>. Les élèves abordent des thèmes citoyens engagés (street art, droits civiques, environnement), maîtrisent la <strong>voix passive</strong> et les <strong>modaux complexes</strong>. Premiers pas vers la rigueur littéraire (lecture cursive A2/B1).",
    sequences: [
      {
        n: 1, periode: "T1 (sept-oct)",
        titre: "Welcome to America",
        theme: "Civilisation américaine — découverte",
        axe: "Rencontres culturelles — États-Unis",
        langue: "Prétérit (révision), voix passive, biographie",
        lexique: "USA (états, culture pop, food), histoire récente",
        culturel: "Indépendance, Civil War, Civil Rights, contemporary",
        tache: "Biographie d'un.e Américain.e marquant.e (250 mots)",
        cecrl: "A2+",
        statut: "live",
        url: "../quiz/3e/welcome-to-america.html"
      },
      {
        n: 2, periode: "T1 (nov-déc)",
        titre: "Street Art: The Voice of the Wall",
        theme: "L'art urbain comme contestation",
        axe: "Langages — art et engagement",
        langue: "Voix passive (présent + prétérit), verbes d'opinion, modaux",
        lexique: "Art urbain (stencil, mural, tag), opinion, engagement",
        culturel: "Banksy, Keith Haring, Shepard Fairey, street art à Tana",
        tache: "Musée virtuel <em>The Tana Street Gallery</em>",
        cecrl: "A2+/B1",
        statut: "live",
        url: "../quiz/3e/street-art.html"
      },
      {
        n: 3, periode: "T2 (janv-fév)",
        titre: "Frankenstein — Mary Shelley",
        theme: "Roman gothique et création scientifique",
        axe: "Langages — fiction et morale",
        langue: "Prétérit simple/continu, voix passive au prétérit",
        lexique: "Description morale/physique, émotions, ambiances gothiques",
        culturel: "Romantisme britannique, Shelley, Frankenstein dans la pop culture",
        tache: "Écrire son histoire de monstre (350 mots)",
        cecrl: "A2+/B1",
        statut: "live",
        url: "../quiz/3e/frankenstein.html"
      },
      {
        n: 4, periode: "T2 (mars)",
        titre: "The Secret of Jatbula Trail",
        theme: "Lecture cursive : Australie autochtone",
        axe: "Rencontres culturelles — peuples premiers",
        langue: "Prétérit irrégulier, modaux d'obligation, conditionnel",
        lexique: "Randonnée, nature, art rupestre, Dreamtime",
        culturel: "Jawoyn, Anangu, Uluru, Stolen Generations",
        tache: "Carnet de bord d'une randonnée imaginaire (250 mots)",
        cecrl: "A2/B1",
        statut: "live",
        url: "../quiz/3e/jatbula-trail.html"
      },
      {
        n: 5, periode: "T3 (avril-mai)",
        titre: "Women Who Changed History",
        theme: "Figures féminines marquantes",
        axe: "Représentations de soi — diversité et inclusion",
        langue: "Present perfect (impact contemporain), voix passive",
        lexique: "Biographie, lutte, droits, succès",
        culturel: "Malala, Rosa Parks, Marie Curie, Mae Jemison, Ranavalona III",
        tache: "Exposition collaborative <em>Women in History</em> (digital ou papier)",
        cecrl: "B1",
        statut: "live",
        url: "../quiz/3e/women-in-history.html"
      },
      {
        n: 6, periode: "T3 (juin)",
        titre: "My DNB Project",
        theme: "Préparation à l'oral du DNB (Histoire des Arts ou Parcours)",
        axe: "Synthèse — projet personnel",
        langue: "Connecteurs argumentatifs, expressions d'opinion",
        lexique: "Outils de présentation orale, argumentation",
        culturel: "Méthodologie de l'oral DNB, gestion du stress",
        tache: "Oral blanc DNB (5 min + questions)",
        cecrl: "B1",
        statut: "todo"
      }
    ]
  },

  /* ====================================================== */
  /* 3e NON SI                                                */
  /* ====================================================== */
  "3e-non-si": {
    label: "3ème NON SI",
    cecrl: "B1/B2",
    classe: "3ANGLAI1 (Mme FALIMANANA) · Section Internationale",
    horaire: "6h hebdomadaires",
    programme: "Programme renforcé OIB",
    couleur: "linear-gradient(135deg, var(--lft-magenta-dark), var(--bf-500))",
    intro: "Niveau B1+/B2 attendu. Lecture intégrale d'œuvres complexes, étude approfondie de la <strong>civilisation américaine</strong>, analyse littéraire avancée. Continue la préparation longue à l'OIB.",
    sequences: [
      {
        n: 1, periode: "T1",
        titre: "The Curious Incident of the Dog in the Night-Time",
        theme: "Mark Haddon — autisme et narration subjective",
        axe: "Diversité et inclusion — neurodiversité",
        langue: "Point of view, narration first person, complex sentences",
        lexique: "Lexique psychologique, mathématiques, rituels",
        culturel: "Banlieue anglaise, autisme, neurodiversité",
        tache: "Analyse littéraire (450 mots) du point de vue narrateur",
        cecrl: "B1+",
        statut: "live",
        url: "../quiz/non-si/curious-incident.html"
      },
      {
        n: 2, periode: "T2",
        titre: "US Civil Rights Movement",
        theme: "Histoire des droits civiques aux États-Unis",
        axe: "Citoyenneté — droits et libertés",
        langue: "Voix passive, structures argumentatives, discours indirect",
        lexique: "Droits, ségrégation, lutte, marche, leader",
        culturel: "MLK, Rosa Parks, Malcolm X, BLM, héritage contemporain",
        tache: "Discours type MLK : 'I have a dream...' (oral 5 min)",
        cecrl: "B2",
        statut: "live",
        url: "../quiz/non-si/civil-rights.html"
      },
      {
        n: 3, periode: "T3",
        titre: "Short Stories — Roald Dahl & Neil Gaiman",
        theme: "L'art de la nouvelle anglaise",
        axe: "Langages — narration courte",
        langue: "Past perfect, twist narratif, vocabulaire stylistique",
        lexique: "Suspense, twist, narrateur peu fiable",
        culturel: "Tradition anglaise de la short story",
        tache: "Écrire sa propre nouvelle avec twist (500 mots)",
        cecrl: "B2",
        statut: "todo"
      }
    ]
  },

  /* ====================================================== */
  /* 1ère euro APPROF LING                                    */
  /* ====================================================== */
  "1ere": {
    label: "1ère euro · APPROF LING",
    cecrl: "B1/B2",
    classe: "1EUROANG1 (Mme FALIMANANA) · Section Européenne",
    horaire: "1h hebdomadaire (en plus de la LV1)",
    programme: "Approfondissement Linguistique — section européenne",
    couleur: "linear-gradient(135deg, var(--success-500), var(--bf-500))",
    intro: "Heure d'enseignement <strong>renforcé en anglais</strong> qui prolonge la DNL SVT. Les élèves lisent et commentent des <strong>textes scientifiques en anglais</strong> sur la biodiversité, le climat, les écosystèmes. Préparation à la mention <em>« Section européenne »</em> au baccalauréat (Terminale).",
    sequences: [
      {
        n: 1, periode: "T1 (sept-oct)",
        titre: "Madagascar's Biodiversity: A Living Laboratory",
        theme: "Endémisme et conservation à Madagascar",
        axe: "DNL SVT — biodiversité",
        langue: "Vocabulaire scientifique, voix passive, modaux d'argumentation",
        lexique: "Endémisme, hotspot, déforestation, conservation",
        culturel: "Madagascar comme hotspot mondial, IUCN, WWF",
        tache: "<em>Policy brief</em> de conservation (250 mots) + oral 5 min",
        cecrl: "B1/B2",
        statut: "live",
        url: "../quiz/1ere/biodiversity.html"
      },
      {
        n: 2, periode: "T1-T2 (nov-déc)",
        titre: "Climate Change & Tropical Cyclones",
        theme: "Phénomènes climatiques affectant Madagascar",
        axe: "DNL SVT — climatologie",
        langue: "Modaux de probabilité, voix passive, données statistiques",
        lexique: "Météorologie, océans, hurricane, mitigation",
        culturel: "Cyclones Batsirai, Freddy, GIEC, Madagascar vulnérable",
        tache: "Analyse d'un graphique météorologique (200 mots)",
        cecrl: "B1+/B2",
        statut: "live",
        url: "../quiz/1ere/climate-cyclones.html"
      },
      {
        n: 3, periode: "T2 (janv-fév)",
        titre: "Sustainable Development Goals",
        theme: "Les 17 Objectifs de Développement Durable de l'ONU",
        axe: "Citoyenneté mondiale — engagement",
        langue: "Conditional, future perfect, expressions d'engagement",
        lexique: "ODD, pauvreté, inégalités, développement durable",
        culturel: "ONU, Agenda 2030, Madagascar et les ODD",
        tache: "Présentation TED-style sur un ODD (5 min)",
        cecrl: "B2",
        statut: "live",
        url: "../quiz/1ere/sdgs.html"
      },
      {
        n: 4, periode: "T2-T3 (mars)",
        titre: "Coral Reefs and Ocean Health",
        theme: "Récifs coralliens et santé des océans",
        axe: "DNL SVT — écosystèmes marins",
        langue: "Vocabulaire scientifique, comparatifs, données",
        lexique: "Récifs, blanchissement, biodiversité marine, pollution plastique",
        culturel: "Récifs malgaches, Grande Barrière de Corail, plastiques",
        tache: "Article scientifique simplifié pour le journal du lycée",
        cecrl: "B2",
        statut: "todo"
      },
      {
        n: 5, periode: "T3 (avril-mai)",
        titre: "Towards Terminale: Reading Scientific Papers",
        theme: "Lire un article scientifique en anglais",
        axe: "Méthodologie — lecture experte",
        langue: "Structures académiques, abréviations, citations",
        lexique: "Méthodologie scientifique, abstract, conclusion",
        culturel: "Revues (Nature, Science), peer-review, Open Access",
        tache: "Résumé d'un article authentique (Nature) — 200 mots",
        cecrl: "B2",
        statut: "todo"
      }
    ]
  },

  /* ====================================================== */
  /* Terminale LVA — 8 axes culturels du Bac                  */
  /* ====================================================== */
  "terminale": {
    label: "Terminale LVA",
    cecrl: "B2/C1",
    classe: "TG6ANGLAIS_1 (Mme FALIMANANA)",
    horaire: "3h hebdomadaires",
    programme: "Programme officiel Bac LVA — 8 axes culturels",
    couleur: "linear-gradient(135deg, var(--bf-500), var(--lft-magenta-dark))",
    intro: "Année du <strong>Baccalauréat</strong>. Le programme officiel impose 8 <strong>axes culturels</strong> à étudier sur 2 ans (1<sup>re</sup> + Tle). Travail intensif sur les compétences orales (épreuve oral du bac, ETLV) et écrites (compréhension + expression argumentée). Niveau visé : B2 vers C1.",
    sequences: [
      {
        n: 1, periode: "T1 (sept-oct)",
        titre: "Identities & Exchanges",
        theme: "Migration, diaspora, multiculturalisme britannique",
        axe: "Axe 1 du Bac — Identités et échanges",
        langue: "Subordonnées relatives, conditionnels mixtes, discours rapporté",
        lexique: "Migration (push/pull factors), identité, hybridité",
        culturel: "Windrush, Brick Lane, diaspora malgache au RU",
        tache: "Essai argumenté 300 mots + oral type Bac (10 min)",
        cecrl: "B2/C1",
        statut: "live",
        url: "../quiz/terminale/identities-exchanges.html"
      },
      {
        n: 2, periode: "T1 (nov)",
        titre: "Public Space and Private Space",
        theme: "Frontière vie privée / vie publique à l'ère numérique",
        axe: "Axe 2 du Bac — Espaces privés et publics",
        langue: "Modaux de jugement (should have, ought to), conditionnels",
        lexique: "Données, surveillance, RGPD, paparazzi",
        culturel: "Phone hacking, Cambridge Analytica, Snowden",
        tache: "Débat type bac sur le droit à l'oubli (oral)",
        cecrl: "B2/C1",
        statut: "live",
        url: "../quiz/terminale/public-private.html"
      },
      {
        n: 3, periode: "T2 (déc-janv)",
        titre: "Art and Power",
        theme: "L'art comme contestation politique",
        axe: "Axe 3 du Bac — Art et pouvoir",
        langue: "Voix passive (formes complexes), structures emphatiques",
        lexique: "Art engagé, contestation, propagande, mémoire",
        culturel: "Banksy (lien 3e), Picasso (Guernica), Kara Walker, Ai Weiwei",
        tache: "Analyse d'œuvre (350 mots) + présentation orale 8 min",
        cecrl: "B2/C1",
        statut: "live",
        url: "../quiz/terminale/art-and-power.html"
      },
      {
        n: 4, periode: "T2 (fév)",
        titre: "Citizenship and Virtual Worlds",
        theme: "Réseaux sociaux, fake news, démocratie numérique",
        axe: "Axe 4 du Bac — Citoyenneté et mondes virtuels",
        langue: "Discours rapporté, modaux de doute, lexique d'argumentation",
        lexique: "Fake news, deepfake, troll, viral, fact-checking",
        culturel: "Cambridge Analytica, Capitol Hill 2021, IA générative",
        tache: "Article d'opinion 350 mots — fake news",
        cecrl: "B2/C1",
        statut: "live",
        url: "../quiz/terminale/citizenship-virtual.html"
      },
      {
        n: 5, periode: "T3 (mars)",
        titre: "Fictions and Realities",
        theme: "Utopies, dystopies, narration",
        axe: "Axe 5 du Bac — Fictions et réalités",
        langue: "Past perfect, conditionnels, registres",
        lexique: "Utopie, dystopie, fiction, vraisemblance",
        culturel: "1984 (Orwell), Brave New World, Black Mirror, Atwood",
        tache: "Réécriture de la fin d'une dystopie (400 mots)",
        cecrl: "B2/C1",
        statut: "todo"
      },
      {
        n: 6, periode: "T3 (avril)",
        titre: "Scientific Innovation and Responsibility",
        theme: "IA, génétique, éthique scientifique",
        axe: "Axe 6 du Bac — Innovations scientifiques",
        langue: "Modaux de jugement, conditionnel passé",
        lexique: "Génétique, IA, éthique, responsabilité",
        culturel: "CRISPR, ChatGPT, transhumanisme, Hippocrate",
        tache: "Mini-conférence type TED (5 min) sur une innovation",
        cecrl: "C1",
        statut: "todo"
      },
      {
        n: 7, periode: "T3 (mai)",
        titre: "Diversity and Inclusion",
        theme: "Représentation, racisme, féminisme, LGBT+",
        axe: "Axe 7 du Bac — Diversité et inclusion",
        langue: "Inclusive language, structures emphatiques",
        lexique: "Diversité, inclusion, biais, discrimination",
        culturel: "BLM, #MeToo, Pride, peuples autochtones",
        tache: "Manifeste de classe (200 mots) + débat",
        cecrl: "B2/C1",
        statut: "live",
        url: "../quiz/terminale/diversity-inclusion.html"
      },
      {
        n: 8, periode: "T3 (mai-juin)",
        titre: "Territory and Memory",
        theme: "Colonialisme, mémoires plurielles",
        axe: "Axe 8 du Bac — Territoire et mémoire",
        langue: "Past perfect, vocabulaire historiographique",
        lexique: "Colonisation, indépendance, mémoire, héritage",
        culturel: "Empire britannique, indépendance Madagascar 1960, Commonwealth",
        tache: "Synthèse de documents type Bac (400 mots)",
        cecrl: "C1",
        statut: "todo"
      }
    ]
  }
};

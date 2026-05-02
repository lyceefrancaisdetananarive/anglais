"""
Générateur des évaluations imprimables pour chaque séquence.

Pour chaque séquence (40 au total) on produit 3 PDF :
  - eval_diagnostique_{niveau}_{slug}.pdf  (~10 min, début de séquence)
  - eval_formative_{niveau}_{slug}.pdf     (~20 min, mi-séquence)
  - eval_sommative_{niveau}_{slug}.pdf     (~40 min, fin de séquence,
                                             grille de notation tâche finale)

Soit 120 PDF prêts à imprimer, mise en page institutionnelle AEFE/LFT,
contenu structuré directement à partir de progression.json.
"""

import os
import json
import re
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    HRFlowable, KeepTogether,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# ============================================================
#   POLICES, PALETTE, CHEMINS
# ============================================================
FONT_DIR = "/System/Library/Fonts/Supplemental"
pdfmetrics.registerFont(TTFont("Sans",            f"{FONT_DIR}/Arial.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold",       f"{FONT_DIR}/Arial Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Italic",     f"{FONT_DIR}/Arial Italic.ttf"))
pdfmetrics.registerFont(TTFont("Sans-BoldItalic", f"{FONT_DIR}/Arial Bold Italic.ttf"))
pdfmetrics.registerFontFamily("Sans",
    normal="Sans", bold="Sans-Bold",
    italic="Sans-Italic", boldItalic="Sans-BoldItalic")

BLEU_FRANCE = HexColor("#000091")
BLEU_AEFE   = HexColor("#003B5C")
ROUGE_FR    = HexColor("#E1000F")
MAGENTA_LFT = HexColor("#E6007E")
OR          = HexColor("#C9A027")
NOIR        = HexColor("#161616")
GRIS_FONCE  = HexColor("#3D3D3D")
GRIS_MOYEN  = HexColor("#7A7A7A")
GRIS_CLAIR  = HexColor("#E8E8E8")
GRIS_TC     = HexColor("#F5F5F5")
JAUNE_PALE  = HexColor("#FFF8E1")
BLEU_PALE   = HexColor("#E5F1F7")
VERT_PALE   = HexColor("#E8F5E9")
ROSE_PALE   = HexColor("#FCE4EC")

ROOT      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO_LFT  = os.path.join(ROOT, "assets", "img", "logo-lft-rond.png")
LOGO_AEFE = os.path.join(ROOT, "assets", "img", "logo-aefe-egd.png")
PROG_PATH = os.path.join(ROOT, "assets", "data", "progression.json")
LEX_PATH  = os.path.join(ROOT, "assets", "data", "lexique-sequences.json")
OUT_DIR   = os.path.dirname(__file__)

# Lexique enrichi (titre → liste [en, ipa, fr])
with open(LEX_PATH, "r", encoding="utf-8") as _f:
    LEXIQUE_SEQUENCES = json.load(_f)


def get_lex_words(seq_titre, n=8):
    """Retourne jusqu'à n mots anglais authentiques (sans IPA/FR)
    pour la séquence donnée. Fallback sur split du seq.lexique."""
    rows = LEXIQUE_SEQUENCES.get(seq_titre)
    if isinstance(rows, list) and rows:
        return [r[0] for r in rows[:n]]
    return None


# ============================================================
#   STYLES
# ============================================================
base = getSampleStyleSheet()
S = {
    "h1": ParagraphStyle("h1", parent=base["Heading1"],
        fontName="Sans-Bold", fontSize=18, leading=22,
        textColor=BLEU_FRANCE, spaceBefore=8, spaceAfter=8),
    "h2": ParagraphStyle("h2", parent=base["Heading2"],
        fontName="Sans-Bold", fontSize=12.5, leading=16,
        textColor=BLEU_FRANCE, spaceBefore=8, spaceAfter=4),
    "h3": ParagraphStyle("h3", parent=base["Heading3"],
        fontName="Sans-Bold", fontSize=11, leading=14,
        textColor=MAGENTA_LFT, spaceBefore=6, spaceAfter=4),
    "body": ParagraphStyle("body", parent=base["BodyText"],
        fontName="Sans", fontSize=10.5, leading=15,
        textColor=NOIR, alignment=TA_JUSTIFY, spaceAfter=4),
    "lead": ParagraphStyle("lead", parent=base["BodyText"],
        fontName="Sans-Italic", fontSize=10.5, leading=15,
        textColor=GRIS_FONCE, spaceAfter=8),
    "small": ParagraphStyle("small", parent=base["BodyText"],
        fontName="Sans", fontSize=8.5, leading=11,
        textColor=GRIS_MOYEN),
    "small_c": ParagraphStyle("small_c", parent=base["BodyText"],
        fontName="Sans", fontSize=8.5, leading=11,
        textColor=GRIS_MOYEN, alignment=TA_CENTER),
    "th": ParagraphStyle("th", parent=base["BodyText"],
        fontName="Sans-Bold", fontSize=9.5, leading=12,
        textColor=white, alignment=TA_LEFT),
    "td": ParagraphStyle("td", parent=base["BodyText"],
        fontName="Sans", fontSize=9.5, leading=13, textColor=NOIR),
    "qcm_opt": ParagraphStyle("qcm_opt", parent=base["BodyText"],
        fontName="Sans", fontSize=10, leading=14,
        textColor=NOIR, leftIndent=14, spaceAfter=2),
    "info": ParagraphStyle("info", parent=base["BodyText"],
        fontName="Sans-Italic", fontSize=9.5, leading=12,
        textColor=GRIS_FONCE, alignment=TA_CENTER),
}


# ============================================================
#   HELPERS
# ============================================================
def slugify(s):
    s = s.lower()
    s = re.sub(r"['']", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def strip_html(s):
    if not s: return ""
    return re.sub(r"<[^>]+>", "", s)


def split_lex(s, n=8):
    if not s: return []
    items = re.split(r"[,;·]", strip_html(s))
    return [x.strip() for x in items if x.strip()][:n]


# ============================================================
#   EN-TÊTE / PIED DE PAGE
# ============================================================
NIVEAU_INFO = {
    "6e":         {"label": "6ᵉ"},
    "4e":         {"label": "4ᵉ LV1"},
    "4e-non-si":  {"label": "4ᵉ NON SI"},
    "4e-lce":     {"label": "4ᵉ LCE"},
    "3e":         {"label": "3ᵉ LV1"},
    "3e-non-si":  {"label": "3ᵉ NON SI"},
    "1ere":       {"label": "1ʳᵉ euro"},
    "terminale":  {"label": "Tᵉ LVA"},
}

EVAL_TYPES = {
    "diagnostique": {
        "label": "ÉVALUATION DIAGNOSTIQUE",
        "color": BLEU_AEFE,
        "duree": "10 minutes",
        "moment": "En début de séquence",
        "but": (
            "Cette évaluation diagnostique sert à <b>positionner</b> "
            "l'élève au début de la séquence. Elle n'est pas notée — "
            "elle permet à l'enseignante d'identifier les acquis et "
            "les besoins."
        ),
    },
    "formative": {
        "label": "ÉVALUATION FORMATIVE",
        "color": MAGENTA_LFT,
        "duree": "20 minutes",
        "moment": "Au milieu de la séquence",
        "but": (
            "Cette évaluation formative permet à l'élève de "
            "<b>vérifier ses progrès</b> à mi-parcours. Elle est "
            "souvent notée par compétences (et non par une note "
            "chiffrée), pour aider à orienter les remédiations."
        ),
    },
    "sommative": {
        "label": "ÉVALUATION SOMMATIVE",
        "color": ROUGE_FR,
        "duree": "40 à 60 minutes",
        "moment": "En fin de séquence",
        "but": (
            "Évaluation sommative — <b>tâche finale</b> de la séquence. "
            "L'élève mobilise tous les acquis (lexique, faits de langue, "
            "repères culturels) pour produire une réalisation langagière "
            "évaluée selon une grille de compétences."
        ),
    },
}


def draw_header(canv, doc, ctx):
    canv.saveState()
    page_w, page_h = A4

    # Bandeau blanc + filet doré
    canv.setFillColor(white)
    canv.rect(0, page_h - 2.6*cm, page_w, 2.6*cm, stroke=0, fill=1)
    canv.setFillColor(OR)
    canv.rect(0, page_h - 2.65*cm, page_w, 0.05*cm, stroke=0, fill=1)

    # Logos
    if os.path.exists(LOGO_AEFE):
        canv.drawImage(LOGO_AEFE, 1.4*cm, page_h - 2.2*cm,
                       width=2.7*cm, height=1.4*cm,
                       preserveAspectRatio=True, mask='auto')
    if os.path.exists(LOGO_LFT):
        canv.drawImage(LOGO_LFT, page_w - 3.1*cm, page_h - 2.3*cm,
                       width=1.8*cm, height=1.8*cm,
                       preserveAspectRatio=True, mask='auto')

    # Titre central
    canv.setFillColor(BLEU_FRANCE)
    canv.setFont("Sans-Bold", 10)
    canv.drawCentredString(page_w/2, page_h - 1.0*cm, "LYCÉE FRANÇAIS DE TANANARIVE")
    canv.setFont("Sans", 8.5)
    canv.setFillColor(GRIS_FONCE)
    canv.drawCentredString(page_w/2, page_h - 1.45*cm,
                           "Établissement en gestion directe · AEFE")
    canv.setFillColor(MAGENTA_LFT)
    canv.setFont("Sans-Italic", 8)
    canv.drawCentredString(page_w/2, page_h - 1.85*cm,
                           f"Anglais · {ctx['classe_label']} · "
                           f"Mme S. FALIMANANA")

    # Bandeau bas du header : type + séquence
    canv.setFillColor(ctx['eval_color'])
    canv.setFont("Sans-Bold", 8)
    canv.drawString(1.4*cm, page_h - 2.45*cm, ctx['eval_label'])
    canv.setFillColor(GRIS_FONCE)
    canv.drawRightString(page_w - 1.4*cm, page_h - 2.45*cm,
                         f"Séq. — {ctx['titre_court']}")
    canv.restoreState()


def draw_footer(canv, doc, ctx):
    canv.saveState()
    page_w, _ = A4
    canv.setFillColor(BLEU_FRANCE)
    canv.rect(0, 0.95*cm, page_w/3, 0.12*cm, stroke=0, fill=1)
    canv.setFillColor(white)
    canv.rect(page_w/3, 0.95*cm, page_w/3, 0.12*cm, stroke=0, fill=1)
    canv.setFillColor(ROUGE_FR)
    canv.rect(2*page_w/3, 0.95*cm, page_w/3, 0.12*cm, stroke=0, fill=1)

    canv.setFillColor(GRIS_MOYEN)
    canv.setFont("Sans", 7.5)
    canv.drawString(1.4*cm, 0.5*cm,
        f"© LFT · {ctx['titre'][:60]} · Mme S. FALIMANANA")
    canv.drawRightString(page_w - 1.4*cm, 0.5*cm,
        f"Page {canv.getPageNumber()}")
    canv.restoreState()


# ============================================================
#   COMPOSANTS
# ============================================================
def make_top_banner(ctx):
    """Bandeau couleur d'évaluation avec titre + métadonnées."""
    rows = [[
        Paragraph(
            f'<font color="white" size="16"><b>{ctx["eval_label"]}</b></font>',
            S["body"]),
        Paragraph(
            f'<font color="white" size="10">{ctx["duree"]} · {ctx["moment"]}</font>',
            S["body"]),
    ]]
    t = Table(rows, colWidths=[12*cm, 5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), ctx['eval_color']),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    return t


def make_seq_info(ctx):
    """Encadré : titre de la séquence + thème + CECRL."""
    rows = [
        [Paragraph(f'<b>Séquence :</b> {ctx["titre"]}', S["body"])],
        [Paragraph(f'<b>Thème :</b> <i>{ctx["theme"]}</i>', S["body"])],
        [Paragraph(
            f'<b>Niveau CECRL :</b> {ctx["cecrl"]} &nbsp;&nbsp;&nbsp; '
            f'<b>Période :</b> {ctx["periode"]}',
            S["body"])],
    ]
    t = Table(rows, colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BACKGROUND", (0, 0), (-1, -1), GRIS_TC),
        ("BOX", (0, 0), (-1, -1), 0.5, GRIS_CLAIR),
    ]))
    return t


def make_eval_intro(ctx):
    """Encart « But de l'évaluation »."""
    rows = [
        [Paragraph(f'<font color="{ctx["eval_color"].hexval().replace("0x", "#")}"><b>BUT DE CETTE ÉVALUATION</b></font>', S["h3"])],
        [Paragraph(EVAL_TYPES[ctx["eval_type"]]["but"], S["body"])],
    ]
    t = Table(rows, colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BACKGROUND", (0, 0), (-1, -1), JAUNE_PALE),
        ("BOX", (0, 0), (-1, -1), 0.5, OR),
    ]))
    return t


def make_eleve_box():
    """Bloc d'identification élève."""
    rows = [[
        Paragraph('<b>Nom et prénom :</b> _________________________________',
                  S["body"]),
        Paragraph('<b>Classe :</b> _____________ &nbsp; <b>Date :</b> _____________',
                  S["body"]),
    ]]
    t = Table(rows, colWidths=[10*cm, 7*cm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("BACKGROUND", (0, 0), (-1, -1), white),
        ("BOX", (0, 0), (-1, -1), 0.5, GRIS_CLAIR),
    ]))
    return t


def make_qcm_question(num, prompt, options):
    rows = [[Paragraph(f'<b>{num}.</b> {prompt}', S["body"])]]
    for letter, text in options:
        rows.append([Paragraph(f'☐ &nbsp; <b>{letter}.</b> {text}',
                                S["qcm_opt"])])
    t = Table(rows, colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return KeepTogether(t)


def make_open_question(num, prompt, lignes=3):
    items = [[Paragraph(f'<b>{num}.</b> {prompt}', S["body"])]]
    for _ in range(lignes):
        items.append([HRFlowable(width="100%", thickness=0.4,
                                  color=GRIS_CLAIR,
                                  spaceBefore=14, spaceAfter=2)])
    t = Table(items, colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return KeepTogether(t)


def make_grid_competences(critères):
    """Grille d'évaluation 4 niveaux (A1+/A2/B1/B2 selon contexte)."""
    rows = [[
        Paragraph("Compétence", S["th"]),
        Paragraph("Non acquis", S["th"]),
        Paragraph("En cours", S["th"]),
        Paragraph("Maîtrisé", S["th"]),
        Paragraph("Très bonne maîtrise", S["th"]),
    ]]
    for c in critères:
        rows.append([
            Paragraph(c, S["td"]),
            Paragraph("☐", S["td"]),
            Paragraph("☐", S["td"]),
            Paragraph("☐", S["td"]),
            Paragraph("☐", S["td"]),
        ])
    t = Table(rows, colWidths=[6.5*cm, 2.5*cm, 2.5*cm, 2.5*cm, 3*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLEU_AEFE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, GRIS_TC]),
        ("BOX", (0, 0), (-1, -1), 0.5, GRIS_CLAIR),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, GRIS_CLAIR),
    ]))
    return t


# ============================================================
#   GÉNÉRATEURS DE CONTENU PAR TYPE D'ÉVALUATION
# ============================================================
def build_diagnostique(ctx, seq):
    """5 questions courtes : QCM lexique + V/F culturel + amorce production."""
    # Priorité au lexique enrichi (anglais authentique)
    lex = get_lex_words(seq["titre"], 6) or split_lex(seq.get("lexique", ""), 6)
    theme = strip_html(seq.get("theme") or seq.get("titre"))
    culturel = strip_html(seq.get("culturel", ""))

    story = []
    story.append(Paragraph(
        '<font color="#003B5C"><b>I. Vocabulaire — ce que tu sais déjà</b></font>',
        S["h2"]))
    story.append(Paragraph(
        f'En t\'appuyant sur le titre et le thème de la séquence '
        f'(<i>{theme}</i>), réponds en quelques mots aux 3 questions :',
        S["lead"]))

    story.append(make_open_question(1,
        f"Cite 3 mots anglais que tu associes au thème <i>« {theme} »</i>.",
        lignes=2))
    story.append(Spacer(1, 4))

    story.append(make_open_question(2,
        "Donne la traduction française d'un mot que tu ne connais pas "
        f"(au choix dans : {', '.join(lex[:5]) if lex else 'le lexique de la séquence'}).",
        lignes=2))
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        '<font color="#003B5C"><b>II. Compréhension — vrai ou faux</b></font>',
        S["h2"]))
    story.append(Paragraph(
        f'À ton avis, ces affirmations sur la séquence <i>« {seq["titre"]} »</i> '
        f'sont-elles vraies ou fausses ? Coche la case correspondante.',
        S["lead"]))

    affirmations = [
        f"Cette séquence aborde principalement le thème <i>{theme}</i>.",
        f"Les repères culturels concernent {culturel[:80] if culturel else 'le monde anglophone'}.",
        "Cette séquence se déroule sur 6 à 8 séances de 55 minutes.",
    ]
    for i, aff in enumerate(affirmations, start=3):
        story.append(make_qcm_question(i, aff, [
            ("V", "Vrai"), ("F", "Faux"),
        ]))
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 6))
    story.append(Paragraph(
        '<font color="#003B5C"><b>III. Expression — amorce</b></font>',
        S["h2"]))
    story.append(make_open_question(6,
        f"En 2-3 phrases en anglais (ou en français si besoin), "
        f"qu'as-tu envie d'apprendre dans cette séquence sur "
        f"<i>« {theme} »</i> ?",
        lignes=4))
    return story


def build_formative(ctx, seq):
    """Lexique + grammaire + mini-compréhension."""
    # Priorité au lexique enrichi (anglais authentique)
    lex = get_lex_words(seq["titre"], 8) or split_lex(seq.get("lexique", ""), 8)
    langue = strip_html(seq.get("langue", "structures grammaticales"))
    theme = strip_html(seq.get("theme") or seq.get("titre"))

    story = []
    story.append(Paragraph(
        '<font color="#E6007E"><b>I. Lexique — vocabulaire de la séquence</b></font>',
        S["h2"]))
    story.append(Paragraph(
        "Traduis en français les mots/expressions ci-dessous. "
        "Si tu ne les connais pas, écris « ? ».",
        S["lead"]))

    # Tableau lexique avec colonne pour la traduction
    rows = [[
        Paragraph("Anglais", S["th"]),
        Paragraph("Traduction (à compléter)", S["th"]),
    ]]
    for it in (lex or ["(lexique à fournir)"])[:8]:
        rows.append([
            Paragraph(f"<b>{it}</b>", S["td"]),
            Paragraph("&nbsp;", S["td"]),
        ])
    t = Table(rows, colWidths=[7*cm, 10*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLEU_FRANCE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, GRIS_TC]),
        ("BOX", (0, 0), (-1, -1), 0.5, GRIS_CLAIR),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, GRIS_CLAIR),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

    story.append(Paragraph(
        '<font color="#E6007E"><b>II. Faits de langue — application</b></font>',
        S["h2"]))
    story.append(Paragraph(
        f"Cette séquence mobilise : <b>{langue}</b>. "
        "Forme 3 phrases qui mobilisent ces structures.",
        S["lead"]))
    for i in range(1, 4):
        story.append(make_open_question(i,
            f"Phrase {i} (mobiliser la structure étudiée) :",
            lignes=2))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 8))
    story.append(Paragraph(
        '<font color="#E6007E"><b>III. Mini-compréhension</b></font>',
        S["h2"]))
    story.append(Paragraph(
        f"En t'appuyant sur ce que tu as travaillé en classe au sujet "
        f"de <i>« {theme} »</i>, réponds à la question suivante en "
        f"4-5 phrases en anglais :",
        S["lead"]))

    story.append(make_open_question(4,
        f"<b>What did you learn about <i>{theme}</i> ?</b> "
        f"(Mobilise au moins 4 mots du lexique de la séquence.)",
        lignes=6))
    return story


def build_sommative(ctx, seq):
    """Grille d'évaluation de la tâche finale."""
    tache = strip_html(seq.get("tache", "Tâche finale"))
    story = []
    story.append(Paragraph(
        '<font color="#E1000F"><b>TÂCHE FINALE — CONSIGNE</b></font>',
        S["h2"]))
    story.append(Paragraph(
        f'<b>{tache}</b>',
        S["body"]))
    story.append(Spacer(1, 8))

    story.append(Paragraph(
        '<font color="#E1000F"><b>GRILLE D\'ÉVALUATION PAR COMPÉTENCES</b></font>',
        S["h2"]))
    story.append(Paragraph(
        "Cette grille est cochée par l'enseignante au moment de la "
        "correction. Elle constitue le retour formatif détaillé.",
        S["lead"]))

    competences = [
        "Recevabilité linguistique (correction grammaticale)",
        "Prononciation / Orthographe",
        "Étendue et précision du lexique",
        "Cohérence et organisation des idées",
        "Pertinence par rapport à la tâche",
        "Originalité, engagement personnel",
        "Mobilisation des faits de langue de la séquence",
        "Mobilisation des repères culturels",
    ]
    story.append(make_grid_competences(competences))

    story.append(Spacer(1, 14))
    story.append(Paragraph(
        '<font color="#E1000F"><b>APPRÉCIATION DE L\'ENSEIGNANTE</b></font>',
        S["h2"]))
    for _ in range(6):
        story.append(HRFlowable(width="100%", thickness=0.4,
                                color=GRIS_CLAIR,
                                spaceBefore=16, spaceAfter=2))

    story.append(Spacer(1, 14))
    story.append(Paragraph(
        '<font color="#E1000F"><b>NOTE OU NIVEAU GLOBAL</b></font>',
        S["h2"]))
    rows = [[
        Paragraph("Note chiffrée (sur 20)", S["td"]),
        Paragraph("&nbsp;", S["td"]),
        Paragraph("Niveau global", S["td"]),
        Paragraph("☐ Non acquis &nbsp; ☐ En cours &nbsp; ☐ Maîtrisé "
                  "&nbsp; ☐ Très bonne maîtrise", S["td"]),
    ]]
    t = Table(rows, colWidths=[4.5*cm, 2.5*cm, 3*cm, 7*cm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("BOX", (0, 0), (-1, -1), 0.5, GRIS_CLAIR),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, GRIS_CLAIR),
        ("BACKGROUND", (1, 0), (1, 0), GRIS_TC),
    ]))
    story.append(t)
    return story


# ============================================================
#   GÉNÉRATEUR PRINCIPAL
# ============================================================
def build_eval_pdf(ctx, story_builder, seq):
    out_path = os.path.join(OUT_DIR, ctx['filename'])

    def first_page(canv, doc):
        draw_header(canv, doc, ctx); draw_footer(canv, doc, ctx)
    def later_pages(canv, doc):
        draw_header(canv, doc, ctx); draw_footer(canv, doc, ctx)

    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=3.0*cm, bottomMargin=1.5*cm,
        title=f"{ctx['eval_label']} — {ctx['titre']}",
        author="Mme Salamo FALIMANANA — LFT",
    )

    story = []
    story.append(make_top_banner(ctx))
    story.append(Spacer(1, 8))
    story.append(make_seq_info(ctx))
    story.append(Spacer(1, 6))
    story.append(make_eval_intro(ctx))
    story.append(Spacer(1, 8))
    story.append(make_eleve_box())
    story.append(Spacer(1, 12))

    # Contenu spécifique
    story.extend(story_builder(ctx, seq))

    doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)


def build_for_sequence(niveau_key, seq):
    """Génère 3 PDF pour une séquence."""
    info = NIVEAU_INFO[niveau_key]
    slug_seq = slugify(seq["titre"])
    safe_dir = niveau_key.replace("-", "_")
    titre_court = re.sub(r"\s*\(\d{4}\)", "", seq["titre"])
    titre_court = re.sub(r"[:—–].*$", "", titre_court).strip()[:32]

    base_ctx = {
        "titre": seq["titre"],
        "titre_court": titre_court,
        "theme": strip_html(seq.get("theme", "")),
        "classe_label": info["label"],
        "cecrl": seq.get("cecrl", ""),
        "periode": seq.get("periode", ""),
    }

    builders = {
        "diagnostique": build_diagnostique,
        "formative": build_formative,
        "sommative": build_sommative,
    }

    for eval_type, builder in builders.items():
        ev = EVAL_TYPES[eval_type]
        ctx = {
            **base_ctx,
            "eval_type": eval_type,
            "eval_label": ev["label"],
            "eval_color": ev["color"],
            "duree": ev["duree"],
            "moment": ev["moment"],
            "filename": f"eval_{eval_type}_{safe_dir}_{slug_seq.replace('-', '_')}.pdf",
        }
        build_eval_pdf(ctx, builder, seq)
    return 3


def main():
    print("Génération des 3 évaluations par séquence (40 séquences)...")
    with open(PROG_PATH, "r", encoding="utf-8") as f:
        prog = json.load(f)

    total = 0
    for niveau_key, niveau_data in prog.items():
        if niveau_key not in NIVEAU_INFO:
            continue
        for seq in niveau_data["sequences"]:
            n = build_for_sequence(niveau_key, seq)
            total += n
            print(f"  ✓ {niveau_key} — {seq['titre'][:40]} ({n} PDF)")
    print(f"\nTerminé : {total} PDF d'évaluation générés.")


if __name__ == "__main__":
    main()

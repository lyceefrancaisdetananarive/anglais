"""
Générateur de fiches d'activité PDF — Plateforme Anglais LFT
Mme Salamo FALIMANANA · Mise en page institutionnelle AEFE.

Génère 3 fiches en un appel :
  - 6e_welcome_big_ben_academy.pdf
  - 4e_stuck_at_big_bay_school.pdf
  - 3e_secret_jatbula_trail.pdf

Usage : python generate_sequences_pdf.py
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    Flowable, HRFlowable, KeepTogether,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# === POLICES UNICODE ============================================
ARIAL_DIR = "/System/Library/Fonts/Supplemental"
pdfmetrics.registerFont(TTFont("Sans",            f"{ARIAL_DIR}/Arial.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold",       f"{ARIAL_DIR}/Arial Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Italic",     f"{ARIAL_DIR}/Arial Italic.ttf"))
pdfmetrics.registerFont(TTFont("Sans-BoldItalic", f"{ARIAL_DIR}/Arial Bold Italic.ttf"))
pdfmetrics.registerFontFamily("Sans",
    normal="Sans", bold="Sans-Bold",
    italic="Sans-Italic", boldItalic="Sans-BoldItalic")

# === PALETTE ====================================================
BLEU_AEFE  = HexColor("#003B5C")
BLEU_FRANCE= HexColor("#000091")
BLEU_CLAIR = HexColor("#0073A8")
OR         = HexColor("#C9A027")
ROUGE_FR   = HexColor("#C8102E")
MAGENTA_LFT= HexColor("#E6007E")
GRIS_FONCE = HexColor("#3D3D3D")
GRIS_MOYEN = HexColor("#7A7A7A")
GRIS_CLAIR = HexColor("#E8E8E8")
GRIS_TC    = HexColor("#F5F5F5")
FOND       = HexColor("#FAFAF7")

OUT_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================================================
#   STYLES
# ============================================================
base_styles = getSampleStyleSheet()

styles = {
    "title":    ParagraphStyle("title", parent=base_styles["Title"],
                fontName="Sans-Bold", fontSize=24, leading=30,
                textColor=BLEU_AEFE, alignment=TA_CENTER, spaceAfter=10),
    "subtitle": ParagraphStyle("subtitle", parent=base_styles["Normal"],
                fontName="Sans-Italic", fontSize=12, leading=16,
                textColor=GRIS_FONCE, alignment=TA_CENTER, spaceAfter=6),
    "h1":       ParagraphStyle("h1", parent=base_styles["Heading1"],
                fontName="Sans-Bold", fontSize=17, leading=22,
                textColor=BLEU_AEFE, spaceBefore=14, spaceAfter=10),
    "h2":       ParagraphStyle("h2", parent=base_styles["Heading2"],
                fontName="Sans-Bold", fontSize=13, leading=17,
                textColor=BLEU_CLAIR, spaceBefore=10, spaceAfter=6),
    "body":     ParagraphStyle("body", parent=base_styles["BodyText"],
                fontName="Sans", fontSize=10, leading=14,
                textColor=GRIS_FONCE, alignment=TA_JUSTIFY, spaceAfter=6),
    "bullet":   ParagraphStyle("bullet", parent=base_styles["BodyText"],
                fontName="Sans", fontSize=10, leading=13,
                textColor=GRIS_FONCE, leftIndent=14, spaceAfter=2),
    "small":    ParagraphStyle("small", parent=base_styles["BodyText"],
                fontName="Sans", fontSize=8.5, leading=11,
                textColor=GRIS_MOYEN),
    "small_c":  ParagraphStyle("small_c", parent=base_styles["BodyText"],
                fontName="Sans", fontSize=8.5, leading=11,
                textColor=GRIS_MOYEN, alignment=TA_CENTER),
    "th":       ParagraphStyle("th", parent=base_styles["BodyText"],
                fontName="Sans-Bold", fontSize=9.5, leading=12,
                textColor=white, alignment=TA_LEFT),
    "td":       ParagraphStyle("td", parent=base_styles["BodyText"],
                fontName="Sans", fontSize=9, leading=12,
                textColor=GRIS_FONCE),
    "td_b":     ParagraphStyle("td_b", parent=base_styles["BodyText"],
                fontName="Sans-Bold", fontSize=9, leading=12,
                textColor=BLEU_AEFE),
    "quote":    ParagraphStyle("quote", parent=base_styles["BodyText"],
                fontName="Sans-Italic", fontSize=10, leading=14,
                textColor=GRIS_FONCE, leftIndent=16, rightIndent=16,
                spaceBefore=6, spaceAfter=6, borderPadding=8,
                backColor=GRIS_TC, alignment=TA_LEFT),
}


# ============================================================
#   CANVAS — header / footer / cover
# ============================================================
def make_header_footer(spec):
    """Retourne deux fonctions canvas adaptées à la séquence."""

    def cover(canv, doc):
        canv.saveState()
        page_w, page_h = A4

        canv.setFillColor(FOND)
        canv.rect(0, 0, page_w, page_h, stroke=0, fill=1)

        # Bandeau bleu marine
        canv.setFillColor(BLEU_AEFE)
        canv.rect(0, page_h - 5*cm, page_w, 5*cm, stroke=0, fill=1)

        # Filet doré
        canv.setFillColor(OR)
        canv.rect(0, page_h - 5.1*cm, page_w, 0.12*cm, stroke=0, fill=1)

        # Bande latérale magenta LFT
        canv.setFillColor(MAGENTA_LFT)
        canv.rect(0, 0, 0.5*cm, page_h - 5*cm, stroke=0, fill=1)

        # Bande latérale droite tricolore
        canv.setFillColor(BLEU_FRANCE)
        canv.rect(page_w - 0.5*cm, 0, 0.16*cm, page_h, stroke=0, fill=1)
        canv.setFillColor(white)
        canv.rect(page_w - 0.34*cm, 0, 0.16*cm, page_h, stroke=0, fill=1)
        canv.setFillColor(ROUGE_FR)
        canv.rect(page_w - 0.18*cm, 0, 0.18*cm, page_h, stroke=0, fill=1)

        # Logo AEFE stylisé (cercle blanc avec AEFE)
        s = 2.3*cm
        canv.setFillColor(white)
        canv.circle(2*cm + s/2, page_h - 3.5*cm + s/2, s/2 - 2, stroke=0, fill=1)
        canv.setFillColor(BLEU_AEFE)
        canv.setFont("Sans-Bold", 12)
        canv.drawCentredString(2*cm + s/2, page_h - 3.5*cm + s/2 - 4, "AEFE")

        # Logo LFT stylisé
        canv.setFillColor(white)
        canv.roundRect(page_w - 2*cm - s, page_h - 3.5*cm, s, s, 8, stroke=0, fill=1)
        canv.setFillColor(BLEU_AEFE)
        canv.setFont("Sans-Bold", 11)
        canv.drawCentredString(page_w - 2*cm - s/2, page_h - 3.5*cm + s/2 - 3, "LFT")
        canv.setFillColor(MAGENTA_LFT)
        canv.setFont("Sans-Bold", 8)
        canv.drawCentredString(page_w - 2*cm - s/2, page_h - 3.5*cm + s*0.22, "★")

        # Textes de l'en-tête
        canv.setFillColor(white)
        canv.setFont("Sans-Bold", 12)
        canv.drawCentredString(page_w/2, page_h - 2.0*cm,
                               "AGENCE POUR L'ENSEIGNEMENT FRANÇAIS À L'ÉTRANGER")
        canv.setFont("Sans", 9)
        canv.drawCentredString(page_w/2, page_h - 2.5*cm,
                               "Lycée Français de Tananarive · Madagascar")
        canv.setFillColor(OR)
        canv.setFont("Sans-Italic", 9)
        canv.drawCentredString(page_w/2, page_h - 3.0*cm,
                               f"Anglais · {spec['niveau']}")

        # Pied
        canv.setFillColor(BLEU_AEFE)
        canv.rect(0, 0, page_w, 2.2*cm, stroke=0, fill=1)
        canv.setFillColor(OR)
        canv.rect(0, 2.2*cm, page_w, 0.1*cm, stroke=0, fill=1)
        canv.setFillColor(white)
        canv.setFont("Sans-Bold", 10)
        canv.drawCentredString(page_w/2, 1.4*cm, "Document pédagogique interne")
        canv.setFont("Sans", 9)
        canv.drawCentredString(page_w/2, 0.95*cm,
                               "Mme Salamo FALIMANANA — Enseignante d'anglais")
        canv.setFont("Sans-Italic", 8)
        canv.drawCentredString(page_w/2, 0.55*cm, "Année scolaire 2025-2026")

        canv.restoreState()

    def hf(canv, doc):
        canv.saveState()
        page_w, page_h = A4

        # En-tête
        canv.setFillColor(BLEU_AEFE)
        canv.rect(0, page_h - 1.6*cm, page_w, 1.6*cm, stroke=0, fill=1)
        canv.setFillColor(OR)
        canv.rect(0, page_h - 1.7*cm, page_w, 0.08*cm, stroke=0, fill=1)
        canv.setFillColor(white)
        canv.setFont("Sans-Bold", 9)
        canv.drawString(2*cm, page_h - 0.8*cm,
                        "AEFE — Lycée Français de Tananarive")
        canv.setFont("Sans", 8)
        canv.drawString(2*cm, page_h - 1.25*cm,
                        f"Anglais · {spec['niveau']}")
        canv.setFont("Sans-Bold", 9)
        canv.drawRightString(page_w - 2*cm, page_h - 0.8*cm, spec['titre_court'])
        canv.setFont("Sans-Italic", 8)
        canv.drawRightString(page_w - 2*cm, page_h - 1.25*cm, "Mme FALIMANANA")

        # Pied
        canv.setFillColor(BLEU_AEFE)
        canv.rect(0, 1.2*cm, page_w, 0.04*cm, stroke=0, fill=1)
        canv.setFillColor(GRIS_FONCE)
        canv.setFont("Sans", 8)
        canv.drawString(2*cm, 0.7*cm, f"Salamo FALIMANANA — {spec['niveau']}")
        canv.setFont("Sans-Bold", 8)
        canv.drawCentredString(page_w/2, 0.7*cm, spec['titre_anglais'])
        canv.setFont("Sans", 8)
        canv.drawRightString(page_w - 2*cm, 0.7*cm, f"Page {doc.page}")

        canv.restoreState()

    return cover, hf


# ============================================================
#   FLOWABLES UTILITAIRES
# ============================================================
class SessionBanner(Flowable):
    def __init__(self, num, title_en, title_fr, duration, width=17*cm):
        super().__init__()
        self.num = num; self.title_en = title_en; self.title_fr = title_fr
        self.duration = duration; self.width = width; self.height = 2.0*cm

    def draw(self):
        c = self.canv
        c.setFillColor(BLEU_AEFE)
        c.rect(0, 0, self.width, self.height, stroke=0, fill=1)
        c.setFillColor(OR)
        c.rect(0, 0, self.width, 0.07*cm, stroke=0, fill=1)
        c.setFillColor(MAGENTA_LFT)
        c.circle(1.3*cm, self.height/2, 0.7*cm, stroke=0, fill=1)
        c.setFillColor(white)
        c.setFont("Sans-Bold", 18)
        c.drawCentredString(1.3*cm, self.height/2 - 6, str(self.num))
        c.setFont("Sans-Bold", 13)
        c.drawString(2.7*cm, self.height/2 + 2, self.title_en)
        c.setFont("Sans-Italic", 9)
        c.drawString(2.7*cm, self.height/2 - 11, self.title_fr)
        c.setFont("Sans", 9)
        c.drawRightString(self.width - 0.3*cm, self.height/2 - 3, self.duration)


def section_label(text, color=MAGENTA_LFT):
    t = Table(
        [[Paragraph(f'<font color="white"><b>{text}</b></font>', styles["td"])]],
        colWidths=[17*cm], rowHeights=[0.6*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def info_table(rows):
    data = []
    for k, v in rows:
        data.append([
            Paragraph(f'<font color="#003B5C"><b>{k}</b></font>', styles["td"]),
            Paragraph(v, styles["td"]),
        ])
    t = Table(data, colWidths=[5*cm, 12*cm])
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, GRIS_CLAIR),
        ("BACKGROUND", (0, 0), (-1, -1), white),
    ]))
    return t


def step_table(steps):
    head = [
        Paragraph("ÉTAPE", styles["th"]),
        Paragraph("ACTIVITÉ", styles["th"]),
        Paragraph("DURÉE", styles["th"]),
        Paragraph("MODALITÉ", styles["th"]),
    ]
    data = [head]
    for i, (stage, activity, dur, mod) in enumerate(steps, 1):
        data.append([
            Paragraph(f"<b>{i}. {stage}</b>", styles["td_b"]),
            Paragraph(activity, styles["td"]),
            Paragraph(dur, styles["td"]),
            Paragraph(mod, styles["td"]),
        ])
    t = Table(data, colWidths=[3.2*cm, 8.3*cm, 2.3*cm, 3.2*cm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLEU_AEFE),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [GRIS_TC, white]),
        ("LINEBELOW", (0, 0), (-1, 0), 1.5, OR),
        ("LINEBELOW", (0, 1), (-1, -1), 0.3, GRIS_CLAIR),
    ]))
    return t


def vocab_table(rows):
    head = [Paragraph("MOT", styles["th"]),
            Paragraph("PRONONCIATION", styles["th"]),
            Paragraph("TRADUCTION / DÉFINITION", styles["th"])]
    data = [head]
    for en, ph, fr in rows:
        data.append([
            Paragraph(f"<b>{en}</b>", styles["td_b"]),
            Paragraph(f"<i>{ph}</i>", styles["td"]),
            Paragraph(fr, styles["td"]),
        ])
    t = Table(data, colWidths=[5*cm, 4*cm, 8*cm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), MAGENTA_LFT),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, GRIS_TC]),
        ("LINEBELOW", (0, 0), (-1, 0), 1.5, OR),
    ]))
    return t


# ============================================================
#   STORY BUILDER GÉNÉRIQUE
# ============================================================
def build_story(spec):
    s = []

    # ===== Couverture =====
    s.append(Spacer(1, 6.5*cm))
    s.append(Paragraph("FICHE D'ACTIVITÉ", styles["subtitle"]))
    s.append(Spacer(1, 0.2*cm))
    s.append(Paragraph(
        f'<font color="#003B5C"><b>{spec["titre_anglais"]}</b></font>',
        styles["title"]))
    if spec.get("sous_titre"):
        s.append(Paragraph(
            f'<font color="#E6007E"><i>{spec["sous_titre"]}</i></font>',
            styles["subtitle"]))
    s.append(Spacer(1, 0.5*cm))
    s.append(HRFlowable(width="40%", thickness=1.2, color=OR,
                        spaceBefore=4, spaceAfter=12, hAlign="CENTER"))

    s.append(info_table([
        ("Discipline",       "Anglais — Langue Vivante A"),
        ("Niveau",           spec["niveau"]),
        ("CECRL visé",       spec["cecrl"]),
        ("Volume horaire",   spec["duree"]),
        ("Programme",        spec["programme"]),
        ("Tâche finale",     spec["tache_finale"]),
        ("Date de mise à jour", "Avril 2026"),
    ]))

    s.append(PageBreak())

    # ===== Présentation =====
    s.append(Spacer(1, 0.4*cm))
    s.append(Paragraph("Présentation de la séquence", styles["h1"]))
    s.append(HRFlowable(width="100%", thickness=0.5, color=OR,
                        spaceBefore=2, spaceAfter=8))

    for para in spec["presentation"]:
        s.append(Paragraph(para, styles["body"]))

    s.append(Paragraph("Objectifs", styles["h2"]))
    for item in spec["objectifs"]:
        s.append(Paragraph("• " + item, styles["bullet"]))

    if spec.get("liens"):
        s.append(Paragraph("Liens interdisciplinaires", styles["h2"]))
        for item in spec["liens"]:
            s.append(Paragraph("• " + item, styles["bullet"]))

    if spec.get("citation"):
        s.append(Spacer(1, 0.3*cm))
        s.append(Paragraph(spec["citation"], styles["quote"]))

    s.append(PageBreak())

    # ===== Déroulement =====
    s.append(Spacer(1, 0.3*cm))
    s.append(SessionBanner(
        spec.get("session_num", 1),
        spec["banner_en"],
        spec["banner_fr"],
        spec["banner_duree"],
    ))
    s.append(Spacer(1, 0.4*cm))

    s.append(section_label("DÉROULEMENT TYPE D'UNE SÉANCE", MAGENTA_LFT))
    s.append(Spacer(1, 0.2*cm))
    s.append(step_table(spec["etapes"]))

    s.append(Spacer(1, 0.4*cm))
    s.append(KeepTogether([
        section_label("LEXIQUE CLÉ", MAGENTA_LFT),
        Spacer(1, 0.2*cm),
        vocab_table(spec["vocab"]),
    ]))

    s.append(PageBreak())

    # ===== Évaluation =====
    s.append(Spacer(1, 0.3*cm))
    s.append(Paragraph("Évaluation et tâche finale", styles["h1"]))
    s.append(HRFlowable(width="100%", thickness=0.5, color=OR,
                        spaceBefore=2, spaceAfter=8))

    s.append(Paragraph("Critères d'évaluation", styles["h2"]))

    eval_data = [[
        Paragraph("<b>Compétence</b>", styles["th"]),
        Paragraph("<b>Critère</b>", styles["th"]),
        Paragraph("<b>Indicateur de réussite</b>", styles["th"]),
    ]]
    for crit, ind, val in spec["criteres"]:
        eval_data.append([
            Paragraph(f"<b>{crit}</b>", styles["td_b"]),
            Paragraph(ind, styles["td"]),
            Paragraph(val, styles["td"]),
        ])
    et = Table(eval_data, colWidths=[3.5*cm, 5.5*cm, 8*cm], repeatRows=1)
    et.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLEU_AEFE),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [GRIS_TC, white]),
        ("LINEBELOW", (0, 0), (-1, 0), 1.5, OR),
        ("LINEBELOW", (0, 1), (-1, -1), 0.3, GRIS_CLAIR),
    ]))
    s.append(et)

    s.append(Spacer(1, 0.4*cm))
    s.append(Paragraph("Quiz interactif et envoi automatique", styles["h2"]))
    s.append(Paragraph(
        f"Cette séquence dispose d'un <b>quiz numérique</b> de 10 questions accessible "
        f"à l'adresse <code>{spec['quiz_url']}</code>. "
        f"À la soumission, les résultats sont automatiquement archivés dans la feuille "
        f"<i>Plateforme Anglais LFT — Résultats quiz</i> et envoyés par mail à "
        f"l'enseignante (et à l'élève s'il a saisi son adresse).",
        styles["body"]))

    if spec.get("note_finale"):
        s.append(Spacer(1, 0.4*cm))
        nb = Table([[Paragraph(spec["note_finale"], styles["body"])]],
                   colWidths=[17*cm])
        nb.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), HexColor("#FFF8E1")),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("RIGHTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ("LINEABOVE", (0, 0), (-1, -1), 3, OR),
        ]))
        s.append(nb)

    s.append(Spacer(1, 0.5*cm))
    s.append(HRFlowable(width="50%", thickness=0.5, color=OR,
                        spaceBefore=2, spaceAfter=8, hAlign="CENTER"))
    s.append(Paragraph(
        "Document conçu par <b>Mme Salamo FALIMANANA</b><br/>"
        "Lycée Français de Tananarive — Année scolaire 2025-2026",
        styles["small_c"]))

    return s


# ============================================================
#   GÉNÉRATION
# ============================================================
def generate(spec):
    out_path = os.path.join(OUT_DIR, spec["filename"])
    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.2*cm, bottomMargin=1.8*cm,
        title=f"{spec['titre_anglais']} — {spec['niveau']}",
        author="Salamo FALIMANANA",
        subject=f"Fiche d'activité — Anglais {spec['niveau']}",
    )
    cover, hf = make_header_footer(spec)
    doc.build(build_story(spec), onFirstPage=cover, onLaterPages=hf)
    print(f"✓ {out_path}")


# ============================================================
#   SPECS DES 3 SÉQUENCES
# ============================================================

SPEC_6E = {
    "filename": "fiche_6e_welcome_big_ben.pdf",
    "niveau": "6ème — A1",
    "cecrl": "Niveau A1 (découverte)",
    "duree": "6 séances × 1 heure",
    "programme": "Cycle 3 — communication courante, école, identité",
    "titre_anglais": "Welcome to Big Ben Academy!",
    "titre_court": "Welcome 6e",
    "sous_titre": "Ta première rentrée à Londres",
    "tache_finale": "Carte de présentation audio (1 min)",

    "presentation": [
        "Cette première séquence de l'année initie les élèves de 6<sup>e</sup> à l'anglais "
        "en se projetant dans une école imaginaire à Londres : la <b>Big Ben Academy</b>. "
        "Les élèves se présenteront, parleront de leurs goûts, de leur emploi du temps et "
        "découvriront quelques éléments emblématiques de la culture britannique.",

        "L'approche est résolument <b>ludique et orale</b> : jeux de rôle, chants pour "
        "mémoriser l'alphabet et les nombres, mini-saynètes en binôme. La fiche outils "
        "d'auto-évaluation accompagne l'élève pour suivre ses progrès.",
    ],

    "objectifs": [
        "<b>Linguistiques :</b> verbe <i>to be</i> (affirmatif, négatif, interrogatif), "
        "déterminants possessifs (my, your), pronoms personnels sujets, alphabet, nombres jusqu'à 20.",
        "<b>Lexicaux :</b> nationalités, salutations, école (subjects, objects), couleurs, jours de la semaine.",
        "<b>Phonologiques :</b> alphabet anglais (chant), accent de mot, intonation des questions.",
        "<b>Culturels :</b> Big Ben, Londres, le système scolaire britannique (uniforme, houses).",
        "<b>Pragmatiques :</b> se présenter, demander/donner des informations personnelles, épeler son nom.",
    ],

    "liens": [
        "<b>EMC :</b> respect de la différence et des origines.",
        "<b>Géographie :</b> les pays du Commonwealth, la place de l'anglais dans le monde.",
        "<b>Musique :</b> apprentissage de chants traditionnels (ABC song).",
    ],

    "citation": "« Hello! My name is _____. I'm 11 years old. I'm from Madagascar. Nice to meet you! »",

    "session_num": 1,
    "banner_en": "Hello, world!",
    "banner_fr": "Séance type d'introduction",
    "banner_duree": "55 min · classe entière",

    "etapes": [
        ("Warm-up", "Chant de l'ABC en chœur. Affichage des lettres au tableau. Élèves répètent.", "5 min", "Classe"),
        ("Anticipation", "Projection d'une photo de Big Ben. <em>What do you see? What's the weather like?</em>", "5 min", "Classe"),
        ("Découverte", "Vidéo courte (1 min) : un élève se présente à Big Ben Academy. Repérage des structures clés.", "10 min", "Individuel"),
        ("Lexique", "Distribution de la <i>word bank</i>. Mime des nationalités à deviner.", "10 min", "Pairs"),
        ("Production", "En binôme : « Hi, my name is… ». Inversion des rôles.", "15 min", "Pairs"),
        ("Trace écrite", "Recopier 3 phrases-modèles dans le cahier.", "5 min", "Individuel"),
        ("Exit ticket", "Dire son prénom en l'épelant à voix haute devant la classe.", "5 min", "Classe"),
    ],

    "vocab": [
        ("hello / hi",        "/həˈloʊ/, /haɪ/",          "bonjour / salut"),
        ("my name is",        "/maɪ neɪm ɪz/",            "je m'appelle…"),
        ("I am / I'm",        "/aɪ æm/",                  "je suis"),
        ("How old are you?",  "/haʊ oʊld ɑːr juː/",       "Quel âge as-tu ?"),
        ("Where are you from?", "/wer ɑːr juː frʌm/",     "D'où viens-tu ?"),
        ("year",              "/jɪər/",                   "année (pour l'âge)"),
        ("school",            "/skuːl/",                  "école"),
        ("classroom",         "/ˈklæsruːm/",              "salle de classe"),
        ("teacher",           "/ˈtiːtʃər/",               "professeur"),
        ("Nice to meet you!", "/naɪs tə miːt juː/",       "Enchanté !"),
    ],

    "criteres": [
        ("EOC", "Présentation orale enregistrée (1 min)",
         "Donne son prénom, son âge, sa nationalité de manière intelligible."),
        ("Phonologie", "Prononciation et intonation",
         "Alphabet correctement prononcé, intonation montante des questions."),
        ("Lexique", "Mobilisation du vocabulaire",
         "Utilise au moins 6 mots de la <i>word bank</i> en contexte."),
        ("Soin", "Cahier et travaux écrits",
         "Soins, écriture lisible, copie correcte des phrases-modèles."),
    ],

    "quiz_url": "/quiz/6e/welcome-big-ben.html",

    "note_finale":
        "<b>Note pour l'enseignante :</b> cette séquence dispose aussi d'audios d'évaluation "
        "issus du manuel <i>Try n' Fly 6<sup>e</sup></i> (édition 2025), disponibles dans le "
        "dossier <code>Audios évaluations Try n' Fly 6e/</code>.",
}


SPEC_4E = {
    "filename": "fiche_4e_stuck_at_big_bay_school.pdf",
    "niveau": "4ème — A1+/A2",
    "cecrl": "Niveau A1+ vers A2",
    "duree": "7 séances × 1 heure",
    "programme": "Cycle 4 — Rencontres avec d'autres cultures, École et société",
    "titre_anglais": "Stuck at Big Bay School",
    "titre_court": "Big Bay 4e",
    "sous_titre": "Lecture cursive : une rentrée en Nouvelle-Zélande",
    "tache_finale": "Journal d'un nouvel élève (300 mots)",

    "presentation": [
        "Séquence centrée sur la <b>lecture cursive</b> du roman <i>Stuck at Big Bay School</i> "
        "(Hatier, 2024) — niveau A1+ adapté pour des 4<sup>e</sup>. Le récit suit un adolescent "
        "qui découvre la vie scolaire dans une petite ville côtière de Nouvelle-Zélande.",

        "Au-delà de la compréhension de l'écrit, cette séquence permet de découvrir la "
        "culture maorie (greetings <i>kia ora</i>, marae, haka), de travailler le contraste "
        "entre <b>présent simple et présent continu</b>, ainsi que les comparatifs.",
    ],

    "objectifs": [
        "<b>Linguistiques :</b> présent simple vs continu, comparatifs des adjectifs courts et longs, "
        "modaux <i>have to / must</i>, adverbes de fréquence, prétérit régulier (introduction).",
        "<b>Lexicaux :</b> école (subjects, recess, uniform), vie quotidienne, sentiments, "
        "lexique de la côte (beach, bay, bush).",
        "<b>Culturels :</b> Nouvelle-Zélande (Aotearoa), peuple māori, écoles du Commonwealth.",
        "<b>Pragmatiques :</b> raconter sa journée, comparer deux situations, décrire un lieu, "
        "exprimer un ressenti.",
    ],

    "liens": [
        "<b>Géographie :</b> l'Océanie, l'archipel néo-zélandais, climat tempéré océanique.",
        "<b>Histoire :</b> colonisation britannique, traité de Waitangi (1840), peuples premiers.",
        "<b>EMC :</b> identité, intégration, regard sur la différence.",
    ],

    "citation": "« Kia ora! Welcome to Big Bay School. We don't have many students here, but we have the best beach in Aotearoa. »",

    "session_num": 1,
    "banner_en": "Welcome to Aotearoa",
    "banner_fr": "Séance type — entrée dans le récit",
    "banner_duree": "55 min · classe entière",

    "etapes": [
        ("Anticipation", "Carte de la NZ projetée. <em>What do you know about New Zealand?</em>", "10 min", "Classe"),
        ("Lecture", "Lecture du chapitre 1 (3 pages). Repérage des personnages et du lieu.", "15 min", "Individuel"),
        ("Compréhension", "Questionnaire QCM sur le chapitre. Vérification en binôme puis classe.", "10 min", "Pairs → classe"),
        ("Lexique", "Word web autour du mot <i>school</i> à compléter avec le vocabulaire du chapitre.", "10 min", "Groupes 4"),
        ("Réflexion langue", "Repérage des verbes au présent simple vs continu. Construction de la règle.", "10 min", "Classe"),
        ("Trace écrite", "Recopier la règle + 3 phrases d'exemple tirées du texte.", "5 min", "Individuel"),
        ("Devoirs", "Lire le chapitre 2 + écrire 5 questions à poser au narrateur.", "5 min", "Individuel"),
    ],

    "vocab": [
        ("kia ora",          "/ˈkiː.ə ˈɔː.rə/",           "salut (māori)"),
        ("recess / break",   "/ˈriː.ses/, /breɪk/",       "récréation"),
        ("uniform",          "/ˈjuː.nɪ.fɔːrm/",           "uniforme scolaire"),
        ("subject",          "/ˈsʌb.dʒekt/",              "matière scolaire"),
        ("classmate",        "/ˈklæs.meɪt/",              "camarade de classe"),
        ("bay",              "/beɪ/",                     "baie (côte)"),
        ("bush",             "/bʊʃ/",                     "brousse, forêt australe"),
        ("to be stuck",      "/tə bi stʌk/",              "être coincé / bloqué"),
        ("homesick",         "/ˈhoʊm.sɪk/",               "qui a le mal du pays"),
        ("haka",             "/ˈhɑː.kə/",                 "danse traditionnelle māorie"),
    ],

    "criteres": [
        ("CE", "Compréhension du roman",
         "Identifie personnages, lieux, actions principales. Repère implicites."),
        ("EE", "Journal d'un nouvel élève (300 mots)",
         "Récit cohérent à la 1<sup>re</sup> personne, présent simple/continu correctement employés."),
        ("Lexique", "Vocabulaire de la séquence",
         "Mobilise au moins 8 mots de la <i>vocab list</i> en contexte."),
        ("Culture", "Connaissance de la NZ",
         "Cite 3 faits culturels (māori, géographie, école)."),
    ],

    "quiz_url": "/quiz/4e/stuck-big-bay.html",

    "note_finale":
        "<b>Différenciation :</b> deux versions du livre sont disponibles (texte standard et "
        "<b>format DYS</b>). Les évaluations finales du manuel Try n' Fly 4<sup>e</sup> existent "
        "aussi en version DYS dans le dossier de classe.",
}


SPEC_3E = {
    "filename": "fiche_3e_secret_jatbula_trail.pdf",
    "niveau": "3ème — A2/B1",
    "cecrl": "Niveau A2 vers B1",
    "duree": "6 séances × 1 heure",
    "programme": "Cycle 4 — Rencontres avec d'autres cultures, Voyages et migrations",
    "titre_anglais": "The Secret of Jatbula Trail",
    "titre_court": "Jatbula 3e",
    "sous_titre": "Lecture cursive : 62 km dans le bush australien",
    "tache_finale": "Carnet de bord d'une randonnée imaginaire (250 mots)",

    "presentation": [
        "Séquence de lecture cursive autour du roman <i>The Secret of Jatbula Trail</i> "
        "(Hatier, 2024, niveau A2). Le Jatbula Trail est un sentier de randonnée de 62 km "
        "dans le <b>Northern Territory</b> australien, en territoire <b>Jawoyn</b>.",

        "À travers le récit d'une randonnée initiatique, les élèves consolident le "
        "<b>prétérit</b> (régulier et irrégulier), abordent les <b>modaux d'obligation</b> et "
        "les conseils, et découvrent l'histoire des peuples autochtones d'Australie : "
        "Dreamtime, art rupestre, sites sacrés.",
    ],

    "objectifs": [
        "<b>Linguistiques :</b> prétérit simple (régulier et irrégulier), modaux <i>must / "
        "have to / should</i>, connecteurs logiques (however, although, because of).",
        "<b>Lexicaux :</b> randonnée (trail, gear, campsite), nature (waterfall, billabong, "
        "rock art), ressentis et émotions.",
        "<b>Phonologiques :</b> prononciation des -ed (/t/ /d/ /ɪd/), accentuation des verbes irréguliers.",
        "<b>Culturels :</b> peuples autochtones (Jawoyn, Anangu), Dreamtime, Uluru, "
        "histoire coloniale.",
        "<b>Pragmatiques :</b> raconter une expérience passée, donner un conseil, exprimer "
        "une opposition, décrire un paysage.",
    ],

    "liens": [
        "<b>SVT / Géographie :</b> écosystèmes du bush, mousson tropicale, biodiversité.",
        "<b>Histoire :</b> colonisation britannique de l'Australie (1788), <i>Stolen Generations</i>, "
        "<i>National Sorry Day</i>.",
        "<b>Arts plastiques :</b> art rupestre, peinture aborigène contemporaine.",
    ],

    "citation": "« Walking the Jatbula isn't just a hike. It's a 50,000-year-old story written on the rocks — if you know how to read it. »",

    "session_num": 1,
    "banner_en": "Into the Top End",
    "banner_fr": "Séance type — entrée dans le récit",
    "banner_duree": "55 min · classe entière",

    "etapes": [
        ("Anticipation", "Drone footage (1 min) du Top End. Brainstorming en anglais.", "10 min", "Classe"),
        ("Lecture", "Chapitre 1 lu individuellement (4 pages).", "15 min", "Individuel"),
        ("CE — questions", "Questions ouvertes B1 / QCM A2 selon différenciation.", "10 min", "Individuel"),
        ("Lexique", "Carte mentale autour de <i>the bush</i>. Cycle vocabulaire ↔ image.", "10 min", "Pairs"),
        ("Langue", "Repérage des prétérits dans le texte : régulier/irrégulier. Tableau.", "10 min", "Classe"),
        ("Production", "5 phrases au prétérit décrivant ce que le narrateur a fait pendant le chapitre.", "5 min", "Individuel"),
    ],

    "vocab": [
        ("trail / track",      "/treɪl/, /træk/",          "sentier"),
        ("billabong",          "/ˈbɪl.ə.bɒŋ/",             "trou d'eau (mot autochtone)"),
        ("waterhole",          "/ˈwɔː.tər.hoʊl/",          "point d'eau"),
        ("rock art",           "/rɒk ɑːrt/",               "art rupestre"),
        ("Dreamtime",          "/ˈdriːm.taɪm/",            "Temps du Rêve (mythologie)"),
        ("ancestor",           "/ˈæn.ses.tər/",            "ancêtre"),
        ("sacred",             "/ˈseɪ.krɪd/",              "sacré"),
        ("to camp",            "/tə kæmp/",                "camper"),
        ("backpack",           "/ˈbæk.pæk/",               "sac à dos"),
        ("flora and fauna",    "/ˈflɔː.rə ənd ˈfɔː.nə/",   "flore et faune"),
    ],

    "criteres": [
        ("CE", "Compréhension du roman",
         "Saisit les enjeux du récit, repère les implicites culturels."),
        ("EE", "Carnet de bord (250 mots)",
         "Récit cohérent au prétérit, lexique de la randonnée et de la nature."),
        ("Langue", "Prétérit + modaux",
         "≥ 5 prétérits corrects (dont 2 irréguliers), ≥ 1 modal de conseil."),
        ("Culture", "Histoire autochtone",
         "Mobilise au moins 2 références culturelles (Dreamtime, Uluru, Jatbula…)."),
    ],

    "quiz_url": "/quiz/3e/jatbula-trail.html",

    "note_finale":
        "<b>Pont avec la 1<sup>re</sup> euro :</b> cette séquence prépare à la lecture de "
        "documents scientifiques en anglais sur la biodiversité (cf. fiche DNL SVT 1<sup>re</sup> "
        "<i>Madagascar's Biodiversity</i>). Les concepts d'<i>endemism</i> et <i>habitat</i> "
        "introduits ici seront approfondis l'année suivante.",
}


SPEC_TERMINALE = {
    "filename": "fiche_terminale_identities_exchanges.pdf",
    "niveau": "Terminale — B2/C1",
    "cecrl": "Niveau B2 vers C1 — préparation Bac",
    "duree": "8 séances × 1 heure",
    "programme": "Programme Bac LVA — Axe culturel n°1",
    "titre_anglais": "Identities & Exchanges",
    "titre_court": "Identities Tle",
    "sous_titre": "Migration, diaspora et identités plurielles",
    "tache_finale": "Essai argumenté de 300 mots + oral type Bac (10 min)",

    "presentation": [
        "Première séquence du programme de Terminale, ancrée dans <b>l'axe culturel "
        "« Identités et échanges »</b>. Elle explore les phénomènes migratoires "
        "contemporains à travers le prisme de la <b>diaspora malgache</b> au Royaume-Uni "
        "(près de 4 000 personnes), en dialogue avec d'autres diasporas anglophones "
        "(caribéenne, sud-asiatique).",

        "L'objectif est double : (1) consolider les structures complexes attendues au "
        "niveau B2 (subordonnées relatives, conditionnels mixtes, discours rapporté) ; "
        "(2) outiller l'élève pour <b>l'épreuve écrite et orale du Bac</b> "
        "(compréhension de l'écrit, expression argumentée, présentation de dossier).",
    ],

    "objectifs": [
        "<b>Linguistiques :</b> subordonnées relatives (who, which, whose, where), conditionnels "
        "mixtes (past perfect + would), discours rapporté, connecteurs de concession (despite, although, "
        "even though).",
        "<b>Lexicaux :</b> migration (push/pull factors, settlement, integration), identité "
        "(belonging, hybridity, hyphenated identity), expressions imagées (to feel torn, "
        "salad bowl vs melting pot).",
        "<b>Culturels :</b> Windrush generation (1948-1971), British-Asian literature "
        "(Salman Rushdie, Monica Ali, Hanif Kureishi), diaspora malgache à Londres.",
        "<b>Pragmatiques :</b> argumenter à l'écrit (essai 300 mots), présenter un dossier "
        "à l'oral, défendre une thèse, reformuler.",
        "<b>Méthodologiques :</b> préparer un dossier d'oral du Bac, organiser ses notes en "
        "5 minutes de préparation.",
    ],

    "liens": [
        "<b>HGGSP :</b> migrations internationales, frontières, citoyenneté.",
        "<b>SES :</b> sociologie de l'intégration, capital culturel, mobilité sociale.",
        "<b>Histoire :</b> empire britannique, décolonisation, Commonwealth.",
        "<b>Lettres :</b> littérature postcoloniale, écriture du soi, autofiction.",
    ],

    "citation": "« Multiculturalism is not just a fact, it is also a value. The salad bowl is no longer a metaphor — it is the everyday reality of London, Birmingham, and Manchester. »",

    "session_num": 1,
    "banner_en": "What does it mean to belong?",
    "banner_fr": "Séance type — entrée dans l'axe",
    "banner_duree": "55 min · classe entière",

    "etapes": [
        ("Anticipation", "Carte interactive : projeter la diaspora malgache au RU (Office for National Statistics).", "10 min", "Classe"),
        ("Reading", "Lecture de l'incipit de <i>Brick Lane</i> (Monica Ali). Repérage du point de vue.", "15 min", "Individuel"),
        ("Vocabulary", "Word web autour de <i>identity / belonging</i>. Distinction push/pull factors.", "10 min", "Pairs"),
        ("Listening", "Podcast BBC <i>The Migration Museum</i> (3 min) — note-taking guidée.", "10 min", "Individuel"),
        ("Speaking", "Mini-débat : <i>« Is multiculturalism a strength or a challenge? »</i> Argumenter en 2 min.", "10 min", "Pairs → classe"),
    ],

    "vocab": [
        ("diaspora",            "/daɪˈæs.pər.ə/",            "diaspora — population dispersée, identité partagée"),
        ("hyphenated identity", "/ˈhaɪ.fə.neɪ.tɪd/",         "identité hyphénée (ex. British-Malagasy)"),
        ("settlement",          "/ˈset.əl.mənt/",            "installation (d'une communauté)"),
        ("to assimilate",       "/əˈsɪm.ɪ.leɪt/",            "s'assimiler (perdre ses spécificités)"),
        ("to integrate",        "/ˈɪn.tɪ.ɡreɪt/",            "s'intégrer (sans perdre son identité)"),
        ("to feel torn",        "/tə fiːl tɔːrn/",           "se sentir déchiré, partagé"),
        ("homeland",            "/ˈhoʊm.lænd/",              "pays d'origine, terre natale"),
        ("Windrush generation", "/ˈwɪnd.rʌʃ/",               "génération antillaise arrivée au RU 1948-71"),
        ("salad bowl",          "/ˈsæl.əd boʊl/",            "métaphore : cultures coexistant sans se fondre"),
        ("melting pot",         "/ˈmel.tɪŋ pɒt/",            "métaphore : fusion des cultures en une"),
    ],

    "criteres": [
        ("CE", "Compréhension de l'écrit — texte 600 mots",
         "Saisit la thèse, identifie les implicites, repère le point de vue."),
        ("EE", "Essai argumenté de 300 mots",
         "Plan en 3 parties, ≥ 4 connecteurs, mobilise au moins 2 références culturelles."),
        ("EOC", "Présentation orale du dossier (8 min)",
         "Plan clair, références précises, prononciation soignée, fluidité."),
        ("EOI", "Entretien (10 min)",
         "Réponses précises, capacité à reformuler, à nuancer, à défendre une thèse."),
        ("Langue", "Structures complexes",
         "Maîtrise des relatives, conditionnels mixtes, discours rapporté."),
    ],

    "quiz_url": "/quiz/terminale/identities-exchanges.html",

    "note_finale":
        "<b>Liaison avec d'autres axes :</b> les concepts d'<i>hybridity</i> et de <i>belonging</i> "
        "introduits ici résonneront dans l'axe « Diversité et inclusion » et dans l'axe « Territoire "
        "et mémoire ». Penser à les ré-investir au fil de l'année pour densifier le dossier d'oral du Bac.",
}


# ============================================================
#   ENTRY POINT
# ============================================================
if __name__ == "__main__":
    for spec in [SPEC_6E, SPEC_4E, SPEC_3E, SPEC_TERMINALE]:
        generate(spec)
    print("\n4 fiches PDF générées dans pdf-imprimables/")

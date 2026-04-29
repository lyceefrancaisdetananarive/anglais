"""
Génération de la fiche d'activité PDF — Street Art 3e (PILOTE V2)
Plateforme Anglais LFT — Mme Salamo FALIMANANA

Refonte pro :
  - Logos officiels AEFE et LFT (fichiers PNG embarqués)
  - Photographies Unsplash en pleine page
  - QR code intégré pointant vers le quiz en ligne
  - Mise en page magazine (encadrés, infographies, palette tricolore)
  - Activités prêtes à imprimer ET version en ligne synchronisée
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    Flowable, HRFlowable, KeepTogether, Image as RLImage,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import qrcode
import os
from io import BytesIO

# === POLICES ===========================================================
FONT_DIR = "/System/Library/Fonts/Supplemental"
pdfmetrics.registerFont(TTFont("Sans",            f"{FONT_DIR}/Arial.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold",       f"{FONT_DIR}/Arial Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Italic",     f"{FONT_DIR}/Arial Italic.ttf"))
pdfmetrics.registerFont(TTFont("Sans-BoldItalic", f"{FONT_DIR}/Arial Bold Italic.ttf"))
pdfmetrics.registerFontFamily("Sans",
    normal="Sans", bold="Sans-Bold",
    italic="Sans-Italic", boldItalic="Sans-BoldItalic")

# === PALETTE LFT/AEFE ==================================================
BLEU_AEFE   = HexColor("#003B5C")
BLEU_FRANCE = HexColor("#000091")
OR          = HexColor("#C9A027")
ROUGE_FR    = HexColor("#C8102E")
MAGENTA_LFT = HexColor("#E6007E")
GRIS_FONCE  = HexColor("#3D3D3D")
GRIS_MOYEN  = HexColor("#7A7A7A")
GRIS_CLAIR  = HexColor("#E8E8E8")
GRIS_TC     = HexColor("#F5F5F5")
NOIR        = HexColor("#161616")
FOND_CREME  = HexColor("#FAFAF7")

# === CHEMINS ==========================================================
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO_LFT = os.path.join(ROOT, "assets", "img", "logo-lft.png")
LOGO_AEFE = os.path.join(ROOT, "assets", "img", "logo-aefe-egd.png")
IMG_DIR = os.path.join(ROOT, "assets", "img", "sequences", "street-art")
OUT_FILE = os.path.join(os.path.dirname(__file__), "fiche_3e_street_art_pilote.pdf")

QUIZ_URL = "https://lyceefrancaisdetananarive.github.io/anglais/quiz/3e/street-art.html"


# ============================================================
#   QR CODE EN MEMOIRE
# ============================================================
def make_qr_image(url):
    """Génère un QR code en mémoire et retourne un BytesIO PNG."""
    qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_M,
                       box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#003B5C", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


# ============================================================
#   STYLES
# ============================================================
base = getSampleStyleSheet()
styles = {
    "title_xl": ParagraphStyle("title_xl", parent=base["Title"],
        fontName="Sans-Bold", fontSize=32, leading=38,
        textColor=white, alignment=TA_LEFT, spaceAfter=8),
    "title_serif": ParagraphStyle("title_serif", parent=base["Title"],
        fontName="Sans-BoldItalic", fontSize=24, leading=30,
        textColor=BLEU_AEFE, alignment=TA_CENTER, spaceAfter=10),
    "subtitle": ParagraphStyle("subtitle", parent=base["Normal"],
        fontName="Sans-Italic", fontSize=12, leading=16,
        textColor=white, alignment=TA_LEFT, spaceAfter=6),
    "h1": ParagraphStyle("h1", parent=base["Heading1"],
        fontName="Sans-Bold", fontSize=20, leading=26,
        textColor=BLEU_AEFE, spaceBefore=14, spaceAfter=10),
    "h2": ParagraphStyle("h2", parent=base["Heading2"],
        fontName="Sans-Bold", fontSize=14, leading=18,
        textColor=MAGENTA_LFT, spaceBefore=10, spaceAfter=6,
        textTransform="uppercase", letterSpacing=1),
    "h3": ParagraphStyle("h3", parent=base["Heading3"],
        fontName="Sans-Bold", fontSize=12, leading=15,
        textColor=BLEU_AEFE, spaceBefore=8, spaceAfter=4),
    "body": ParagraphStyle("body", parent=base["BodyText"],
        fontName="Sans", fontSize=10.5, leading=15,
        textColor=NOIR, alignment=TA_JUSTIFY, spaceAfter=6),
    "lead": ParagraphStyle("lead", parent=base["BodyText"],
        fontName="Sans-Italic", fontSize=12, leading=18,
        textColor=GRIS_FONCE, alignment=TA_LEFT, spaceAfter=10),
    "bullet": ParagraphStyle("bullet", parent=base["BodyText"],
        fontName="Sans", fontSize=10, leading=14,
        textColor=NOIR, leftIndent=14, spaceAfter=2),
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
        fontName="Sans", fontSize=9.5, leading=13,
        textColor=NOIR),
    "td_b": ParagraphStyle("td_b", parent=base["BodyText"],
        fontName="Sans-Bold", fontSize=9.5, leading=13,
        textColor=BLEU_AEFE),
    "quote_big": ParagraphStyle("quote_big", parent=base["BodyText"],
        fontName="Sans-Italic", fontSize=14, leading=22,
        textColor=BLEU_AEFE, alignment=TA_CENTER,
        leftIndent=30, rightIndent=30, spaceBefore=10, spaceAfter=10),
    "vocab_en": ParagraphStyle("vocab_en", parent=base["BodyText"],
        fontName="Sans-Bold", fontSize=11, leading=14,
        textColor=BLEU_AEFE),
    "vocab_phon": ParagraphStyle("vocab_phon", parent=base["BodyText"],
        fontName="Sans-Italic", fontSize=10, leading=13,
        textColor=GRIS_MOYEN),
    "vocab_fr": ParagraphStyle("vocab_fr", parent=base["BodyText"],
        fontName="Sans", fontSize=10, leading=14,
        textColor=NOIR),
    "answer_field": ParagraphStyle("answer_field", parent=base["BodyText"],
        fontName="Sans", fontSize=10, leading=24,
        textColor=GRIS_MOYEN),
}


# ============================================================
#   CANVAS — couverture, en-tête/pied
# ============================================================
def draw_cover(canv, doc):
    """Page de couverture magazine."""
    canv.saveState()
    page_w, page_h = A4

    # Photo hero plein cadre (pour la couverture)
    hero_path = os.path.join(IMG_DIR, "banksy-style-mural.jpg")
    if os.path.exists(hero_path):
        canv.drawImage(hero_path, 0, page_h * 0.45, width=page_w,
                       height=page_h * 0.55, preserveAspectRatio=False, mask='auto')

    # Voile sombre sur la photo (bottom)
    canv.setFillColorRGB(0, 0.05, 0.15, alpha=0.55)
    canv.rect(0, page_h * 0.45, page_w, page_h * 0.55, stroke=0, fill=1)

    # Bandeau supérieur — logos officiels
    canv.setFillColor(white)
    canv.rect(0, page_h - 2.8*cm, page_w, 2.8*cm, stroke=0, fill=1)
    canv.setFillColor(OR)
    canv.rect(0, page_h - 2.85*cm, page_w, 0.05*cm, stroke=0, fill=1)

    # Logo AEFE-EGD à gauche
    if os.path.exists(LOGO_AEFE):
        canv.drawImage(LOGO_AEFE, 1.5*cm, page_h - 2.4*cm,
                       width=2.2*cm, height=2.2*cm,
                       preserveAspectRatio=True, mask='auto')

    # Logo LFT à droite
    if os.path.exists(LOGO_LFT):
        canv.drawImage(LOGO_LFT, page_w - 3.7*cm, page_h - 2.4*cm,
                       width=2.2*cm, height=2.2*cm,
                       preserveAspectRatio=True, mask='auto')

    # Texte central de l'en-tête
    canv.setFillColor(BLEU_AEFE)
    canv.setFont("Sans-Bold", 11)
    canv.drawCentredString(page_w/2, page_h - 1.2*cm,
                           "LYCÉE FRANÇAIS DE TANANARIVE")
    canv.setFont("Sans", 9)
    canv.drawCentredString(page_w/2, page_h - 1.7*cm,
                           "Établissement en gestion directe · AEFE")
    canv.setFillColor(MAGENTA_LFT)
    canv.setFont("Sans-Italic", 8.5)
    canv.drawCentredString(page_w/2, page_h - 2.2*cm,
                           "Espace Anglais — Mme Salamo FALIMANANA")

    # Titre de la séquence (sur la photo)
    canv.setFillColor(white)
    canv.setFont("Sans-Italic", 11)
    canv.drawString(2*cm, page_h * 0.75 + 1.2*cm, "FICHE D'ACTIVITÉ · CLASSE DE 3ᵉ")

    canv.setFont("Sans-Bold", 38)
    canv.drawString(2*cm, page_h * 0.75 - 0.5*cm, "Street Art")

    canv.setFillColor(MAGENTA_LFT)
    canv.setFont("Sans-BoldItalic", 24)
    canv.drawString(2*cm, page_h * 0.75 - 2.0*cm, "The Voice of the Wall")

    # Tags en bas du visuel
    canv.setFillColor(white)
    canv.setFont("Sans", 9)
    tags = ["A2+/B1", "8 séances", "10 activités", "DNB"]
    x = 2*cm
    for tag in tags:
        w = canv.stringWidth(tag, "Sans", 9) + 16
        canv.setFillColorRGB(1, 1, 1, alpha=0.2)
        canv.roundRect(x, page_h * 0.45 + 0.6*cm, w, 0.7*cm, 5, stroke=0, fill=1)
        canv.setFillColor(white)
        canv.drawCentredString(x + w/2, page_h * 0.45 + 0.85*cm, tag)
        x += w + 8

    # Section basse — palette tricolore + métadonnées
    canv.setFillColor(FOND_CREME)
    canv.rect(0, 0, page_w, page_h * 0.45, stroke=0, fill=1)

    # Filets tricolores décoratifs
    bar_y = page_h * 0.45 - 0.15*cm
    canv.setFillColor(BLEU_FRANCE)
    canv.rect(0, bar_y, page_w/3, 0.15*cm, stroke=0, fill=1)
    canv.setFillColor(white)
    canv.rect(page_w/3, bar_y, page_w/3, 0.15*cm, stroke=0, fill=1)
    canv.setFillColor(ROUGE_FR)
    canv.rect(2*page_w/3, bar_y, page_w/3, 0.15*cm, stroke=0, fill=1)

    # Encadré « Edito »
    canv.setFillColor(BLEU_AEFE)
    canv.setFont("Sans-Bold", 11)
    canv.drawString(2*cm, page_h * 0.40, "L'ART URBAIN AU SERVICE DU LANGAGE")

    canv.setFillColor(NOIR)
    canv.setFont("Sans", 10)
    edito = [
        "À travers la figure énigmatique de Banksy et",
        "d'autres artistes anglophones, cette séquence",
        "invite les élèves de 3ᵉ à découvrir la voix",
        "engagée du street art : voix passive, expression",
        "de l'opinion, débat citoyen.",
    ]
    y = page_h * 0.36
    for line in edito:
        canv.drawString(2*cm, y, line)
        y -= 0.5*cm

    # Tâche finale en colonne droite
    canv.setFillColor(MAGENTA_LFT)
    canv.setFont("Sans-Bold", 10)
    canv.drawString(page_w/2 + 0.5*cm, page_h * 0.40, "TÂCHE FINALE")

    canv.setFillColor(NOIR)
    canv.setFont("Sans", 10)
    tache = [
        "Création collaborative d'un musée virtuel :",
        "« The Tana Street Gallery ».",
        "Chaque élève prépare une fiche descriptive",
        "et un audio-guide d'1 à 2 minutes pour",
        "présenter une œuvre street art de son choix.",
    ]
    y = page_h * 0.36
    for line in tache:
        canv.drawString(page_w/2 + 0.5*cm, y, line)
        y -= 0.5*cm

    # Pied de couverture — date & QR code aperçu
    canv.setFillColor(BLEU_AEFE)
    canv.rect(0, 0, page_w, 2.5*cm, stroke=0, fill=1)
    canv.setFillColor(OR)
    canv.rect(0, 2.5*cm, page_w, 0.1*cm, stroke=0, fill=1)

    canv.setFillColor(white)
    canv.setFont("Sans-Bold", 11)
    canv.drawString(2*cm, 1.7*cm, "Année scolaire 2025-2026")
    canv.setFont("Sans", 9)
    canv.drawString(2*cm, 1.2*cm, "Document pédagogique interne · LFT")
    canv.setFont("Sans-Italic", 9)
    canv.drawString(2*cm, 0.7*cm, "Mme Salamo FALIMANANA — salamo.falimanana@egd.mg")

    # QR code dans le coin droit du pied
    qr_buf = make_qr_image(QUIZ_URL)
    canv.drawImage(ImageReader(qr_buf),
                   page_w - 3*cm, 0.4*cm, width=2.0*cm, height=2.0*cm,
                   preserveAspectRatio=True, mask='auto')
    canv.setFillColor(white)
    canv.setFont("Sans", 7.5)
    canv.drawCentredString(page_w - 2*cm, 0.2*cm, "Quiz en ligne")

    canv.restoreState()


def draw_header_footer(canv, doc):
    """En-tête et pied de page des pages intérieures."""
    canv.saveState()
    page_w, page_h = A4

    # En-tête
    canv.setFillColor(BLEU_AEFE)
    canv.rect(0, page_h - 1.7*cm, page_w, 1.7*cm, stroke=0, fill=1)
    canv.setFillColor(OR)
    canv.rect(0, page_h - 1.78*cm, page_w, 0.06*cm, stroke=0, fill=1)

    # Logo AEFE petit format à gauche
    if os.path.exists(LOGO_AEFE):
        canv.drawImage(LOGO_AEFE, 1.2*cm, page_h - 1.5*cm,
                       width=1.2*cm, height=1.2*cm,
                       preserveAspectRatio=True, mask='auto')
    # Logo LFT petit format à droite
    if os.path.exists(LOGO_LFT):
        canv.drawImage(LOGO_LFT, page_w - 2.4*cm, page_h - 1.5*cm,
                       width=1.2*cm, height=1.2*cm,
                       preserveAspectRatio=True, mask='auto')

    canv.setFillColor(white)
    canv.setFont("Sans-Bold", 9.5)
    canv.drawCentredString(page_w/2, page_h - 0.85*cm,
                           "Street Art: The Voice of the Wall")
    canv.setFont("Sans-Italic", 8)
    canv.drawCentredString(page_w/2, page_h - 1.3*cm,
                           "Anglais 3ᵉ · A2+/B1 · LFT")

    # Pied
    canv.setFillColor(BLEU_AEFE)
    canv.rect(0, 1.0*cm, page_w, 0.04*cm, stroke=0, fill=1)
    canv.setFillColor(GRIS_FONCE)
    canv.setFont("Sans", 8)
    canv.drawString(2*cm, 0.55*cm, "Mme FALIMANANA — Lycée Français de Tananarive")
    canv.setFont("Sans", 8)
    canv.drawRightString(page_w - 2*cm, 0.55*cm, f"Page {doc.page}")
    canv.setFont("Sans-Italic", 7.5)
    canv.drawCentredString(page_w/2, 0.55*cm, "Ressource interne · 2025-2026")

    canv.restoreState()


# ============================================================
#   FLOWABLES UTILITAIRES
# ============================================================
class ActivityBanner(Flowable):
    """Bannière d'activité (numéro + titre + type + durée)."""
    def __init__(self, num, title, activity_type, duration, width=17*cm):
        super().__init__()
        self.num = num
        self.title = title
        self.activity_type = activity_type
        self.duration = duration
        self.width = width
        self.height = 2.2*cm

    def draw(self):
        c = self.canv
        # Fond marine
        c.setFillColor(BLEU_AEFE)
        c.rect(0, 0, self.width, self.height, stroke=0, fill=1)
        # Liseré doré bas
        c.setFillColor(OR)
        c.rect(0, 0, self.width, 0.06*cm, stroke=0, fill=1)
        # Cercle magenta avec numéro
        c.setFillColor(MAGENTA_LFT)
        c.circle(1.5*cm, self.height/2, 0.85*cm, stroke=0, fill=1)
        c.setFillColor(white)
        c.setFont("Sans-Bold", 22)
        c.drawCentredString(1.5*cm, self.height/2 - 8, str(self.num))
        # Titre
        c.setFillColor(white)
        c.setFont("Sans-Bold", 14)
        c.drawString(2.9*cm, self.height/2 + 6, self.title)
        # Type d'activité (badge)
        c.setFillColorRGB(1, 1, 1, alpha=0.2)
        type_w = c.stringWidth(self.activity_type, "Sans", 9) + 14
        c.roundRect(2.9*cm, self.height/2 - 18, type_w, 0.55*cm, 4, stroke=0, fill=1)
        c.setFillColor(white)
        c.setFont("Sans", 9)
        c.drawCentredString(2.9*cm + type_w/2, self.height/2 - 14, self.activity_type)
        # Durée
        c.setFont("Sans", 9.5)
        c.drawRightString(self.width - 0.4*cm, self.height/2 - 4, "⏱ " + self.duration)


def section_label(text, color=MAGENTA_LFT):
    t = Table([[Paragraph(f'<font color="white"><b>{text}</b></font>', styles["td"])]],
              colWidths=[17*cm], rowHeights=[0.6*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), color),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    return t


def info_grid(rows):
    """Grille d'infos clé/valeur (2 colonnes)."""
    data = []
    for k, v in rows:
        data.append([
            Paragraph(f"<b>{k}</b>", styles["td_b"]),
            Paragraph(v, styles["td"]),
        ])
    t = Table(data, colWidths=[5*cm, 12*cm])
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, -2), 0.3, GRIS_CLAIR),
        ("BACKGROUND", (0, 0), (-1, -1), white),
    ]))
    return t


def vocab_grid(rows):
    """Grille de vocabulaire en 3 colonnes."""
    head = [
        Paragraph("MOT", styles["th"]),
        Paragraph("PRONONCIATION", styles["th"]),
        Paragraph("TRADUCTION / DÉFINITION", styles["th"]),
    ]
    data = [head]
    for en, ph, fr in rows:
        data.append([
            Paragraph(en, styles["vocab_en"]),
            Paragraph(ph, styles["vocab_phon"]),
            Paragraph(fr, styles["vocab_fr"]),
        ])
    t = Table(data, colWidths=[4.5*cm, 4*cm, 8.5*cm], repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), MAGENTA_LFT),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, GRIS_TC]),
        ("LINEBELOW", (0, 0), (-1, 0), 1.5, OR),
    ]))
    return t


def answer_lines(n=3, width=17*cm):
    """N lignes vides pour réponse manuscrite."""
    rows = [[""]] * n
    t = Table(rows, colWidths=[width], rowHeights=[0.9*cm] * n)
    t.setStyle(TableStyle([
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, GRIS_MOYEN),
    ]))
    return t


def qr_block(url, label, size=2.5*cm):
    """Bloc QR code avec libellé."""
    qr_buf = make_qr_image(url)
    img = RLImage(qr_buf, width=size, height=size)
    t = Table([[img], [Paragraph(label, styles["small_c"])]],
              colWidths=[size + 0.5*cm])
    t.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("TOPPADDING", (0, 1), (-1, 1), 4),
    ]))
    return t


# ============================================================
#   STORY BUILDER
# ============================================================
def build_story():
    s = []

    # ===== PAGE 1 : COUVERTURE (gérée par draw_cover) =====
    s.append(PageBreak())

    # ===== PAGE 2 : Présentation de la séquence =====
    s.append(Spacer(1, 0.4*cm))
    s.append(Paragraph("Présentation de la séquence", styles["h1"]))
    s.append(HRFlowable(width="100%", thickness=0.6, color=OR, spaceBefore=2, spaceAfter=10))

    s.append(Paragraph(
        '<font color="#003B5C"><b>« Anonymity is part of the work. »</b></font> — '
        'Banksy résume ainsi la philosophie qui anime tout le street art contemporain.',
        styles["lead"]))

    s.append(Paragraph(
        "Cette séquence invite les élèves de 3<sup>e</sup> à explorer le <b>street art</b> "
        "à travers la figure énigmatique de Banksy et d'autres artistes urbains du monde "
        "anglophone. Elle conjugue la <b>découverte culturelle</b>, le <b>débat citoyen</b> "
        "(<i>art ou vandalisme&nbsp;?</i>) et la <b>consolidation linguistique</b> du "
        "niveau A2 vers B1.",
        styles["body"]))

    s.append(Paragraph(
        "Adaptée d'une séquence lycée du <em>groupe interlangues numérique de l'académie "
        "d'Amiens (2019/2020)</em>, elle a été redécoupée et étayée pour le cycle 4&nbsp;: "
        "étapes plus courtes, scaffolding renforcé, différenciation à deux niveaux (A2 / B1), "
        "tâche finale ancrée dans le contexte malgache.",
        styles["body"]))

    s.append(Spacer(1, 0.3*cm))
    s.append(info_grid([
        ("Niveau CECRL",     "A2 → B1"),
        ("Volume horaire",   "8 séances × 1 heure (~6 semaines)"),
        ("Programme",        "Cycle 4 — axes <i>Langages</i>, <i>Rencontres avec d'autres cultures</i>, <i>École et société</i>"),
        ("Tâche finale",     "Musée virtuel <i>The Tana Street Gallery</i>"),
        ("Évaluation",       "CO + CE + EE + EOC + EOI"),
        ("Mise à jour",      "29 avril 2026"),
    ]))

    s.append(Spacer(1, 0.5*cm))

    # Encadré QR code
    qr_intro = Table([[
        Paragraph(
            "<b>Le quiz numérique en ligne</b><br/><br/>"
            "Cette fiche s'accompagne d'un quiz interactif de 10 activités variées : "
            "<i>image, audio, association, remise en ordre, texte à trous, QCM, saisie</i>. "
            "Les élèves peuvent y accéder directement via leur smartphone en scannant le "
            "QR code ci-contre, ou en tapant l'URL :"
            "<br/><br/>"
            f'<font color="#000091"><b>{QUIZ_URL}</b></font>'
            "<br/><br/>"
            "À la soumission, les résultats sont automatiquement archivés et envoyés "
            "à l'enseignante.",
            styles["body"]),
        qr_block(QUIZ_URL, "Scanner pour accéder au quiz", size=3.2*cm),
    ]], colWidths=[12*cm, 5*cm])
    qr_intro.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#FFF8E1")),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("LINEABOVE", (0, 0), (-1, -1), 3, OR),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    s.append(qr_intro)

    s.append(Spacer(1, 0.4*cm))

    # Objectifs en deux colonnes
    obj_data = [
        [
            Paragraph('<font color="#E6007E"><b>OBJECTIFS LINGUISTIQUES</b></font>', styles["td"]),
            Paragraph('<font color="#E6007E"><b>OBJECTIFS CULTURELS</b></font>', styles["td"]),
        ],
        [
            Paragraph(
                "• Voix passive (présent + prétérit)<br/>"
                "• Verbes d'opinion (<i>I think, in my opinion…</i>)<br/>"
                "• Modaux (<i>should, could, might</i>)<br/>"
                "• Connecteurs (<i>however, whereas</i>)<br/>"
                "• Lexique de l'art urbain (stencil, mural, tag…)<br/>"
                "• Phonologie : -ed (/t/, /d/, /ɪd/)",
                styles["body"]),
            Paragraph(
                "• Banksy et son anonymat<br/>"
                "• Street art à NYC, Londres, Bristol<br/>"
                "• Musées anglophones (Tate, MoMA)<br/>"
                "• Le débat <i>art vs. vandalism</i><br/>"
                "• Pont avec le street art à Tana<br/>"
                "• Engagement et message politique",
                styles["body"]),
        ],
    ]
    obj_t = Table(obj_data, colWidths=[8.5*cm, 8.5*cm])
    obj_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GRIS_TC),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBETWEEN", (0, 0), (-1, -1), 0.5, GRIS_CLAIR),
    ]))
    s.append(obj_t)

    s.append(PageBreak())

    # ===== PAGE 3 : Activité 1 — Image (vocabulaire) =====
    s.append(Spacer(1, 0.3*cm))
    s.append(ActivityBanner(1, "Vocabulaire visuel", "🖼️ Image + QCM", "5 min"))
    s.append(Spacer(1, 0.4*cm))

    s.append(Paragraph(
        "Observe attentivement la photographie ci-dessous, puis réponds à la question.",
        styles["body"]))

    img_path = os.path.join(IMG_DIR, "banksy-style-mural.jpg")
    if os.path.exists(img_path):
        img = RLImage(img_path, width=17*cm, height=11*cm, kind="proportional")
        s.append(img)
        s.append(Paragraph("<i>Photo : Unsplash · usage pédagogique LFT</i>", styles["small_c"]))

    s.append(Spacer(1, 0.4*cm))
    s.append(Paragraph("<b>Question 1.</b> Quelle technique l'artiste a-t-il utilisée pour créer cette œuvre ?", styles["h3"]))
    s.append(Paragraph(
        "☐ <b>A.</b> A tag (a quick signature with spray paint)<br/>"
        "☐ <b>B.</b> A stencil (a paper template + spray paint)<br/>"
        "☐ <b>C.</b> A sticker (a printed adhesive)<br/>"
        "☐ <b>D.</b> A mosaic (small pieces of glass or tile)",
        styles["body"]))

    s.append(Spacer(1, 0.3*cm))
    s.append(Paragraph(
        "<b>💡 Indice :</b> regarde les contours nets et les surfaces de couleur uniforme — "
        "c'est typique d'une technique précise utilisée par Banksy.",
        styles["lead"]))

    s.append(PageBreak())

    # ===== PAGE 4 : Activité 2 — Audio CO =====
    s.append(Spacer(1, 0.3*cm))
    s.append(ActivityBanner(2, "Compréhension orale", "🎧 Audio + QCM", "8 min"))
    s.append(Spacer(1, 0.4*cm))

    s.append(Paragraph(
        "Pour cette activité, scanne le QR code ci-dessous avec ton téléphone afin d'écouter "
        "l'extrait audio. Tu peux l'écouter <b>deux fois</b>.",
        styles["body"]))

    s.append(Spacer(1, 0.3*cm))
    s.append(qr_block(QUIZ_URL, "Écouter l'audio (Q.2 du quiz)", size=4.5*cm))

    s.append(Spacer(1, 0.5*cm))
    s.append(Paragraph(
        "<b>Question 2.</b> What is the main topic of this audio extract?",
        styles["h3"]))
    s.append(Paragraph(
        "☐ <b>A.</b> A famous painter's biography<br/>"
        "☐ <b>B.</b> Street art and urban culture<br/>"
        "☐ <b>C.</b> A football match in London<br/>"
        "☐ <b>D.</b> A weather report",
        styles["body"]))

    s.append(Spacer(1, 0.4*cm))
    s.append(Paragraph(
        "<b>📝 Note tes mots-clés (3 minimum) :</b>", styles["h3"]))
    s.append(answer_lines(3))

    s.append(PageBreak())

    # ===== PAGE 5 : Activité 3 — Matching =====
    s.append(Spacer(1, 0.3*cm))
    s.append(ActivityBanner(3, "Match the artist", "🔗 Association", "5 min"))
    s.append(Spacer(1, 0.4*cm))

    s.append(Paragraph(
        "Relie chaque artiste à son œuvre la plus célèbre.",
        styles["body"]))

    s.append(Spacer(1, 0.3*cm))

    match_data = [
        [Paragraph("<b>ARTISTE</b>", styles["th"]), "", Paragraph("<b>ŒUVRE</b>", styles["th"])],
        [Paragraph("<b>A.</b> Banksy",          styles["body"]), "→",
         Paragraph("<b>1.</b> SAMO© tags (NYC, late 1970s)",      styles["body"])],
        [Paragraph("<b>B.</b> Keith Haring",    styles["body"]), "→",
         Paragraph("<b>2.</b> Hope (Obama portrait, 2008)",       styles["body"])],
        [Paragraph("<b>C.</b> Shepard Fairey",  styles["body"]), "→",
         Paragraph("<b>3.</b> Crack is Wack (NYC, 1986)",         styles["body"])],
        [Paragraph("<b>D.</b> J.-M. Basquiat",  styles["body"]), "→",
         Paragraph("<b>4.</b> Girl with Balloon (London, 2002)",  styles["body"])],
    ]
    match_t = Table(match_data, colWidths=[7*cm, 1*cm, 9*cm])
    match_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), MAGENTA_LFT),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (1, 1), (1, -1), "CENTER"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, GRIS_TC]),
        ("LINEBELOW", (0, 0), (-1, 0), 1.5, OR),
        ("FONTNAME", (1, 1), (1, -1), "Sans-Bold"),
        ("TEXTCOLOR", (1, 1), (1, -1), MAGENTA_LFT),
        ("FONTSIZE", (1, 1), (1, -1), 14),
    ]))
    s.append(match_t)

    s.append(Spacer(1, 0.5*cm))
    s.append(Paragraph("<b>Tes réponses :</b>", styles["h3"]))
    answer_grid = Table([
        ["A → ___", "B → ___", "C → ___", "D → ___"],
    ], colWidths=[4.25*cm] * 4, rowHeights=[1.2*cm])
    answer_grid.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Sans-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 14),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TEXTCOLOR", (0, 0), (-1, -1), BLEU_AEFE),
        ("BACKGROUND", (0, 0), (-1, -1), GRIS_TC),
        ("BOX", (0, 0), (-1, -1), 0.5, GRIS_MOYEN),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, GRIS_MOYEN),
    ]))
    s.append(answer_grid)

    s.append(PageBreak())

    # ===== PAGE 6 : Activité 4 — Cloze (voix passive) =====
    s.append(Spacer(1, 0.3*cm))
    s.append(ActivityBanner(4, "Voix passive", "📝 Texte à trous", "10 min"))
    s.append(Spacer(1, 0.4*cm))

    s.append(Paragraph(
        "Complète ce texte sur Banksy en choisissant la bonne forme verbale parmi les "
        "propositions. Souligne ta réponse.",
        styles["body"]))

    s.append(Spacer(1, 0.3*cm))

    cloze_text = (
        '<font color="#003B5C">This famous mural </font>'
        '<font color="#E6007E">[ was painted / is painting / paints / has been paint ]</font>'
        '<font color="#003B5C"> by Banksy in 2010. The wall </font>'
        '<font color="#E6007E">[ is photograph / was photographed / photographs / has photograph ]</font>'
        '<font color="#003B5C"> by hundreds of tourists every day. Today, the artwork </font>'
        '<font color="#E6007E">[ protects / is protecting / is protected / protected ]</font>'
        '<font color="#003B5C"> by a sheet of plexiglas.</font>'
    )

    cloze_box = Table([[Paragraph(cloze_text, styles["body"])]], colWidths=[17*cm])
    cloze_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), GRIS_TC),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LINEABOVE", (0, 0), (-1, -1), 3, MAGENTA_LFT),
    ]))
    s.append(cloze_box)

    s.append(Spacer(1, 0.5*cm))
    s.append(Paragraph("<b>Mémo — La voix passive</b>", styles["h3"]))
    s.append(Paragraph(
        "<b>Construction :</b> sujet + <b>BE</b> (au temps voulu) + <b>participe passé</b> + (<i>by</i> + agent)<br/>"
        "<b>Présent simple :</b> The wall <b>is painted</b> every year.<br/>"
        "<b>Prétérit :</b> The mural <b>was painted</b> in 2010.<br/>"
        "<b>Présent perfect :</b> The artwork <b>has been protected</b>.<br/>"
        "<b>Présent continu :</b> The wall <b>is being repainted</b>.",
        styles["body"]))

    s.append(PageBreak())

    # ===== PAGE 7 : Lexique illustré =====
    s.append(Spacer(1, 0.3*cm))
    s.append(Paragraph("Lexique de l'art urbain", styles["h1"]))
    s.append(HRFlowable(width="100%", thickness=0.6, color=OR, spaceBefore=2, spaceAfter=10))

    s.append(vocab_grid([
        ("stencil",            "/ˈsten.səl/",            "pochoir (technique signature de Banksy)"),
        ("mural",              "/ˈmjʊə.rəl/",            "fresque murale, peinture sur grand mur"),
        ("graffiti",           "/ɡrəˈfiː.ti/",           "graffiti — œuvres ou écrits sur murs"),
        ("tag",                "/tæɡ/",                  "tag, signature à la bombe"),
        ("spray paint",        "/spreɪ peɪnt/",          "peinture en bombe aérosol"),
        ("canvas",             "/ˈkæn.vəs/",             "toile (de peintre) — sens propre & figuré"),
        ("street artist",      "/striːt ˈɑː.tɪst/",      "artiste de rue, street artist"),
        ("provocative",        "/prəˈvɒk.ə.tɪv/",        "provocateur, qui pousse à la réflexion"),
        ("meaningful",         "/ˈmiː.nɪŋ.fəl/",         "porteur de sens, signifiant"),
        ("to denounce",        "/tə dɪˈnaʊns/",          "dénoncer (une injustice, un système)"),
        ("to raise awareness", "/tə reɪz əˈweə.nəs/",    "sensibiliser à un problème"),
        ("anonymous",          "/əˈnɒn.ɪ.məs/",          "anonyme — caractéristique de Banksy"),
    ]))

    s.append(Spacer(1, 0.5*cm))

    # Citation centrale
    quote_box = Table([[
        Paragraph(
            '« Art should comfort the disturbed and disturb the comfortable. »<br/><br/>'
            '<font size="9" color="#7A7A7A"><i>— Banksy</i></font>',
            styles["quote_big"])
    ]], colWidths=[17*cm])
    quote_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#003B5C")),
        ("LEFTPADDING", (0, 0), (-1, -1), 30),
        ("RIGHTPADDING", (0, 0), (-1, -1), 30),
        ("TOPPADDING", (0, 0), (-1, -1), 24),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 24),
        ("TEXTCOLOR", (0, 0), (-1, -1), white),
    ]))
    # Re-style the paragraph to be white
    quote_text_white = ParagraphStyle("qw", parent=styles["quote_big"],
                                       textColor=white, fontSize=14)
    quote_box = Table([[Paragraph(
        '« Art should comfort the disturbed and disturb the comfortable. »<br/><br/>'
        '<font size="9"><i>— Banksy</i></font>',
        quote_text_white)
    ]], colWidths=[17*cm])
    quote_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BLEU_AEFE),
        ("LEFTPADDING", (0, 0), (-1, -1), 30),
        ("RIGHTPADDING", (0, 0), (-1, -1), 30),
        ("TOPPADDING", (0, 0), (-1, -1), 24),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 24),
    ]))
    s.append(quote_box)

    s.append(PageBreak())

    # ===== PAGE 8 : Grille d'évaluation =====
    s.append(Spacer(1, 0.3*cm))
    s.append(Paragraph("Grille d'évaluation finale", styles["h1"]))
    s.append(HRFlowable(width="100%", thickness=0.6, color=OR, spaceBefore=2, spaceAfter=10))

    s.append(Paragraph(
        "Évaluation positive par compétences — la tâche finale (musée virtuel) "
        "est notée sur 20 points selon les critères suivants&nbsp;:",
        styles["body"]))

    eval_data = [
        [Paragraph("<b>Compétence</b>", styles["th"]),
         Paragraph("<b>Critère</b>", styles["th"]),
         Paragraph("<b>Indicateur de réussite</b>", styles["th"]),
         Paragraph("<b>/ pts</b>", styles["th"])],
        [Paragraph("<b>EE</b><br/>Fiche écrite", styles["td_b"]),
         Paragraph("Contenu de la fiche", styles["td"]),
         Paragraph("Décrit l'œuvre, son auteur, son contexte et son message.", styles["td"]),
         Paragraph("/ 4", styles["td_b"])],
        [Paragraph("<b>EE</b><br/>Voix passive", styles["td_b"]),
         Paragraph("Maîtrise grammaticale", styles["td"]),
         Paragraph("Voix passive utilisée correctement (≥ 2 occurrences). Lexique de l'art mobilisé.", styles["td"]),
         Paragraph("/ 3", styles["td_b"])],
        [Paragraph("<b>EOC</b><br/>Audio-guide", styles["td_b"]),
         Paragraph("Réalisation orale (1-2 min)", styles["td"]),
         Paragraph("Fluidité, prise de parole spontanée (notes seulement), prononciation -ed.", styles["td"]),
         Paragraph("/ 6", styles["td_b"])],
        [Paragraph("<b>EOI</b><br/>Visite virtuelle", styles["td_b"]),
         Paragraph("Interaction avec les pairs", styles["td"]),
         Paragraph("Pose une question pertinente, répond à un visiteur, justifie son avis.", styles["td"]),
         Paragraph("/ 4", styles["td_b"])],
        [Paragraph("<b>Soin</b>", styles["td_b"]),
         Paragraph("Présentation et créativité", styles["td"]),
         Paragraph("Mise en page lisible, image de qualité, originalité du choix.", styles["td"]),
         Paragraph("/ 3", styles["td_b"])],
    ]
    eval_t = Table(eval_data, colWidths=[3*cm, 4.5*cm, 7.5*cm, 1.5*cm], repeatRows=1)
    eval_t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLEU_AEFE),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [GRIS_TC, white]),
        ("LINEBELOW", (0, 0), (-1, 0), 1.5, OR),
        ("LINEBELOW", (0, 1), (-1, -1), 0.3, GRIS_CLAIR),
        ("BOX", (0, 0), (-1, -1), 0.5, GRIS_CLAIR),
        ("ALIGN", (3, 1), (3, -1), "CENTER"),
    ]))
    s.append(eval_t)

    s.append(Spacer(1, 0.5*cm))

    # Encadré final + QR
    final_block = Table([[
        Paragraph(
            "<b>📲 Le saviez-vous ?</b><br/><br/>"
            "Cette fiche existe en <b>version interactive en ligne</b>. Les élèves peuvent "
            "passer le quiz directement depuis leur smartphone — leurs résultats sont "
            "automatiquement archivés et envoyés à Mme FALIMANANA, avec la correction "
            "détaillée. Idéal pour une évaluation diagnostique en début de séquence ou "
            "pour un travail à la maison.",
            styles["body"]),
        qr_block(QUIZ_URL, "Quiz Street Art", size=3*cm),
    ]], colWidths=[12.5*cm, 4.5*cm])
    final_block.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), HexColor("#FCE4EC")),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LINEABOVE", (0, 0), (-1, -1), 3, MAGENTA_LFT),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    s.append(final_block)

    s.append(Spacer(1, 0.6*cm))
    s.append(HRFlowable(width="50%", thickness=0.5, color=OR,
                        spaceBefore=2, spaceAfter=8, hAlign="CENTER"))
    s.append(Paragraph(
        "Document conçu par <b>Mme Salamo FALIMANANA</b><br/>"
        "Lycée Français de Tananarive — Année scolaire 2025-2026<br/>"
        "<i>Photographies : Unsplash · Quiz interactif sur lyceefrancaisdetananarive.github.io/anglais</i>",
        styles["small_c"]))

    return s


# ============================================================
#   GÉNÉRATION
# ============================================================
def build_pdf():
    doc = SimpleDocTemplate(
        OUT_FILE, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.2*cm, bottomMargin=1.5*cm,
        title="Street Art: The Voice of the Wall — Anglais 3e — LFT",
        author="Mme Salamo FALIMANANA",
        subject="Fiche d'activité Anglais 3e — Street Art (refonte pilote v2)",
    )
    doc.build(build_story(), onFirstPage=draw_cover, onLaterPages=draw_header_footer)
    print(f"✓ PDF pilote généré : {OUT_FILE}")


if __name__ == "__main__":
    build_pdf()

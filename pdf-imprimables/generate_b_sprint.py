"""
Sprint B — Génération des 3 PDF magazines manquants pour atteindre
1 PDF par niveau sur la plateforme Anglais LFT.

Production :
  - fiche_4e_non_si_the_giver.pdf
  - fiche_4e_lce_britain_europe.pdf
  - fiche_3e_non_si_curious_incident.pdf

Format reproductible :
  - Couverture typographique (logos AEFE + LFT, palette tricolore, QR code)
  - Page intro pédagogique (axe BO, CECRL, tâche finale, objectifs)
  - Page lexique + activités prêtes à imprimer
  - Page tâche finale + ressources + QR rappel
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
import qrcode
import os
from io import BytesIO


# === POLICES ============================================================
FONT_DIR = "/System/Library/Fonts/Supplemental"
pdfmetrics.registerFont(TTFont("Sans",            f"{FONT_DIR}/Arial.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Bold",       f"{FONT_DIR}/Arial Bold.ttf"))
pdfmetrics.registerFont(TTFont("Sans-Italic",     f"{FONT_DIR}/Arial Italic.ttf"))
pdfmetrics.registerFont(TTFont("Sans-BoldItalic", f"{FONT_DIR}/Arial Bold Italic.ttf"))
pdfmetrics.registerFontFamily("Sans",
    normal="Sans", bold="Sans-Bold",
    italic="Sans-Italic", boldItalic="Sans-BoldItalic")

# === PALETTE ============================================================
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

# === CHEMINS ============================================================
ROOT     = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO_LFT = os.path.join(ROOT, "assets", "img", "logo-lft.png")
LOGO_AEFE = os.path.join(ROOT, "assets", "img", "logo-aefe-egd.png")
OUT_DIR  = os.path.dirname(__file__)


# ============================================================
#   QR CODE
# ============================================================
def make_qr_buffer(url, color="#003B5C"):
    qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_M,
                       box_size=10, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color=color, back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


# ============================================================
#   STYLES
# ============================================================
base = getSampleStyleSheet()
S = {
    "h1":    ParagraphStyle("h1", parent=base["Heading1"],
        fontName="Sans-Bold", fontSize=20, leading=26,
        textColor=BLEU_AEFE, spaceBefore=10, spaceAfter=10),
    "h2":    ParagraphStyle("h2", parent=base["Heading2"],
        fontName="Sans-Bold", fontSize=13, leading=17,
        textColor=MAGENTA_LFT, spaceBefore=10, spaceAfter=6),
    "h3":    ParagraphStyle("h3", parent=base["Heading3"],
        fontName="Sans-Bold", fontSize=11, leading=14,
        textColor=BLEU_AEFE, spaceBefore=6, spaceAfter=4),
    "body":  ParagraphStyle("body", parent=base["BodyText"],
        fontName="Sans", fontSize=10.5, leading=15,
        textColor=NOIR, alignment=TA_JUSTIFY, spaceAfter=6),
    "lead":  ParagraphStyle("lead", parent=base["BodyText"],
        fontName="Sans-Italic", fontSize=11.5, leading=17,
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
    "th":   ParagraphStyle("th", parent=base["BodyText"],
        fontName="Sans-Bold", fontSize=9.5, leading=12,
        textColor=white, alignment=TA_LEFT),
    "td":   ParagraphStyle("td", parent=base["BodyText"],
        fontName="Sans", fontSize=9.5, leading=13,
        textColor=NOIR),
    "td_b": ParagraphStyle("td_b", parent=base["BodyText"],
        fontName="Sans-Bold", fontSize=9.5, leading=13,
        textColor=BLEU_AEFE),
    "vocab_en":   ParagraphStyle("vocab_en", parent=base["BodyText"],
        fontName="Sans-Bold", fontSize=10.5, leading=14, textColor=BLEU_AEFE),
    "vocab_phon": ParagraphStyle("vocab_phon", parent=base["BodyText"],
        fontName="Sans-Italic", fontSize=9.5, leading=12, textColor=GRIS_MOYEN),
    "vocab_fr":   ParagraphStyle("vocab_fr", parent=base["BodyText"],
        fontName="Sans", fontSize=10, leading=14, textColor=NOIR),
    "answer":     ParagraphStyle("answer", parent=base["BodyText"],
        fontName="Sans", fontSize=10, leading=24, textColor=GRIS_MOYEN),
    "quote": ParagraphStyle("quote", parent=base["BodyText"],
        fontName="Sans-Italic", fontSize=12, leading=18,
        textColor=BLEU_AEFE, alignment=TA_CENTER,
        leftIndent=24, rightIndent=24, spaceBefore=8, spaceAfter=8),
}


# ============================================================
#   HEADER / FOOTER courants
# ============================================================
def draw_header(canv, doc, ctx):
    """Bandeau supérieur identique sur toutes les pages courantes."""
    canv.saveState()
    page_w, page_h = A4
    canv.setFillColor(white)
    canv.rect(0, page_h - 2.4*cm, page_w, 2.4*cm, stroke=0, fill=1)
    canv.setFillColor(OR)
    canv.rect(0, page_h - 2.45*cm, page_w, 0.05*cm, stroke=0, fill=1)

    if os.path.exists(LOGO_AEFE):
        canv.drawImage(LOGO_AEFE, 1.2*cm, page_h - 2.1*cm,
                       width=1.9*cm, height=1.9*cm,
                       preserveAspectRatio=True, mask='auto')
    if os.path.exists(LOGO_LFT):
        canv.drawImage(LOGO_LFT, page_w - 3.1*cm, page_h - 2.1*cm,
                       width=1.9*cm, height=1.9*cm,
                       preserveAspectRatio=True, mask='auto')

    canv.setFillColor(BLEU_AEFE)
    canv.setFont("Sans-Bold", 10.5)
    canv.drawCentredString(page_w/2, page_h - 1.05*cm, ctx["title"].upper())
    canv.setFont("Sans", 8.5)
    canv.setFillColor(GRIS_FONCE)
    canv.drawCentredString(page_w/2, page_h - 1.55*cm,
                           f"{ctx['level']} · {ctx['classe']} · Mme Salamo FALIMANANA")
    canv.setFillColor(MAGENTA_LFT)
    canv.setFont("Sans-Italic", 8)
    canv.drawCentredString(page_w/2, page_h - 2.0*cm,
                           f"Séquence {ctx['seq_n']} — {ctx['axe']}")
    canv.restoreState()


def draw_footer(canv, doc, ctx):
    canv.saveState()
    page_w, _ = A4
    # Filets tricolores
    canv.setFillColor(BLEU_FRANCE)
    canv.rect(0, 1.0*cm, page_w/3, 0.12*cm, stroke=0, fill=1)
    canv.setFillColor(white)
    canv.rect(page_w/3, 1.0*cm, page_w/3, 0.12*cm, stroke=0, fill=1)
    canv.setFillColor(ROUGE_FR)
    canv.rect(2*page_w/3, 1.0*cm, page_w/3, 0.12*cm, stroke=0, fill=1)

    canv.setFillColor(GRIS_MOYEN)
    canv.setFont("Sans", 8)
    canv.drawString(1.5*cm, 0.55*cm,
        f"© Lycée Français de Tananarive · {ctx['title']} · Mme S. FALIMANANA")
    canv.drawRightString(page_w - 1.5*cm, 0.55*cm,
        f"Page {canv.getPageNumber()}")
    canv.restoreState()


# ============================================================
#   COUVERTURE TYPOGRAPHIQUE (sans image hero)
# ============================================================
def draw_cover(canv, doc, ctx):
    canv.saveState()
    page_w, page_h = A4

    # Bandeau magenta supérieur (~30% de la page)
    canv.setFillColor(MAGENTA_LFT)
    canv.rect(0, page_h * 0.55, page_w, page_h * 0.45, stroke=0, fill=1)

    # Bande décorative bleu AEFE
    canv.setFillColor(BLEU_AEFE)
    canv.rect(0, page_h * 0.55, page_w, 0.4*cm, stroke=0, fill=1)

    # En-tête blanc avec logos
    canv.setFillColor(white)
    canv.rect(0, page_h - 2.8*cm, page_w, 2.8*cm, stroke=0, fill=1)
    canv.setFillColor(OR)
    canv.rect(0, page_h - 2.85*cm, page_w, 0.05*cm, stroke=0, fill=1)

    if os.path.exists(LOGO_AEFE):
        canv.drawImage(LOGO_AEFE, 1.5*cm, page_h - 2.4*cm,
                       width=2.2*cm, height=2.2*cm,
                       preserveAspectRatio=True, mask='auto')
    if os.path.exists(LOGO_LFT):
        canv.drawImage(LOGO_LFT, page_w - 3.7*cm, page_h - 2.4*cm,
                       width=2.2*cm, height=2.2*cm,
                       preserveAspectRatio=True, mask='auto')

    canv.setFillColor(BLEU_AEFE)
    canv.setFont("Sans-Bold", 11)
    canv.drawCentredString(page_w/2, page_h - 1.2*cm, "LYCÉE FRANÇAIS DE TANANARIVE")
    canv.setFont("Sans", 9)
    canv.drawCentredString(page_w/2, page_h - 1.7*cm,
                           "Établissement en gestion directe · AEFE")
    canv.setFillColor(MAGENTA_LFT)
    canv.setFont("Sans-Italic", 8.5)
    canv.drawCentredString(page_w/2, page_h - 2.2*cm,
                           "Espace Anglais — Mme Salamo FALIMANANA")

    # Titre + sous-titre sur le bandeau magenta
    canv.setFillColor(white)
    canv.setFont("Sans-Italic", 12)
    canv.drawString(2*cm, page_h * 0.85,
                    f"FICHE D'ACTIVITÉ · CLASSE DE {ctx['classe_label']}")

    canv.setFont("Sans-Bold", 34)
    title = ctx["title"]
    # Si le titre est trop long, le tronquer ou couper
    canv.drawString(2*cm, page_h * 0.74, title[:32])

    canv.setFillColor(white)
    canv.setFont("Sans-BoldItalic", 18)
    canv.drawString(2*cm, page_h * 0.66, ctx["subtitle"])

    # Tags (pills)
    canv.setFont("Sans", 9)
    tags = [ctx["level"], ctx["seances"], ctx["activites_count"], ctx["axe_court"]]
    x = 2*cm
    for tag in tags:
        w = canv.stringWidth(tag, "Sans", 9) + 16
        canv.setFillColorRGB(1, 1, 1, alpha=0.22)
        canv.roundRect(x, page_h * 0.58, w, 0.7*cm, 5, stroke=0, fill=1)
        canv.setFillColor(white)
        canv.drawCentredString(x + w/2, page_h * 0.58 + 0.25*cm, tag)
        x += w + 8

    # Section basse — fond crème
    canv.setFillColor(FOND_CREME)
    canv.rect(0, 0, page_w, page_h * 0.55, stroke=0, fill=1)

    # Filets tricolores entre les deux moitiés
    bar_y = page_h * 0.55 - 0.15*cm
    canv.setFillColor(BLEU_FRANCE)
    canv.rect(0, bar_y, page_w/3, 0.15*cm, stroke=0, fill=1)
    canv.setFillColor(white)
    canv.rect(page_w/3, bar_y, page_w/3, 0.15*cm, stroke=0, fill=1)
    canv.setFillColor(ROUGE_FR)
    canv.rect(2*page_w/3, bar_y, page_w/3, 0.15*cm, stroke=0, fill=1)

    # Édito
    canv.setFillColor(BLEU_AEFE)
    canv.setFont("Sans-Bold", 11)
    canv.drawString(2*cm, page_h * 0.50, ctx["edito_title"])

    canv.setFillColor(NOIR)
    canv.setFont("Sans", 10)
    y = page_h * 0.46
    for line in ctx["edito_lines"]:
        canv.drawString(2*cm, y, line)
        y -= 0.5*cm

    # Métadonnées
    canv.setFillColor(BLEU_AEFE)
    canv.setFont("Sans-Bold", 10)
    canv.drawString(2*cm, page_h * 0.27, "AU SOMMAIRE")
    canv.setFillColor(NOIR)
    canv.setFont("Sans", 9.5)
    y = page_h * 0.23
    sommaire = [
        f"› Pédagogie & objectifs (axe BO, CECRL, tâche finale)",
        f"› Lexique académique illustré ({len(ctx['vocab'])} entrées)",
        f"› Activités imprimables (compréhension + production)",
        f"› Tâche finale & ressources externes",
    ]
    for s in sommaire:
        canv.drawString(2*cm, y, s)
        y -= 0.45*cm

    # QR code en bas à droite
    qr_buf = make_qr_buffer(ctx["quiz_url"])
    from reportlab.lib.utils import ImageReader
    canv.drawImage(ImageReader(qr_buf), page_w - 4.2*cm, 1.5*cm,
                   width=2.8*cm, height=2.8*cm, mask='auto')
    canv.setFillColor(BLEU_AEFE)
    canv.setFont("Sans-Bold", 9)
    canv.drawString(page_w - 8.5*cm, 3.2*cm, "Le quiz en ligne")
    canv.setFillColor(GRIS_FONCE)
    canv.setFont("Sans", 8.5)
    canv.drawString(page_w - 8.5*cm, 2.7*cm, "Scannez ce QR code pour accéder")
    canv.drawString(page_w - 8.5*cm, 2.3*cm, "au quiz interactif synchronisé")
    canv.drawString(page_w - 8.5*cm, 1.9*cm, "(résultats archivés automatiquement).")
    canv.setFillColor(MAGENTA_LFT)
    canv.setFont("Sans-Italic", 8)
    canv.drawString(page_w - 8.5*cm, 1.5*cm, ctx["quiz_url"])

    canv.restoreState()


# ============================================================
#   MISE EN PAGE — fonctions builder
# ============================================================
def make_section_title(text):
    return Paragraph(text, S["h1"])


def make_h2(text):
    return Paragraph(text, S["h2"])


def make_para(text):
    return Paragraph(text, S["body"])


def make_pedago_table(ctx):
    rows = [
        [Paragraph("Axe culturel", S["th"]),
         Paragraph(ctx["axe"], S["td"])],
        [Paragraph("Niveau CECRL", S["th"]),
         Paragraph(ctx["level"], S["td"])],
        [Paragraph("Durée prévue", S["th"]),
         Paragraph(ctx["duree"], S["td"])],
        [Paragraph("Compétences travaillées", S["th"]),
         Paragraph(ctx["competences"], S["td"])],
        [Paragraph("Activités langagières", S["th"]),
         Paragraph(ctx["activites_lang"], S["td"])],
        [Paragraph("Tâche finale (évaluation)", S["th"]),
         Paragraph(f"<b>{ctx['tache_finale']}</b>", S["td"])],
    ]
    t = Table(rows, colWidths=[5.5*cm, 11.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), BLEU_AEFE),
        ("TEXTCOLOR", (0, 0), (0, -1), white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (1, 0), (1, -1), [white, GRIS_TC]),
        ("BOX", (0, 0), (-1, -1), 0.5, GRIS_CLAIR),
        ("INNERGRID", (0, 0), (-1, -1), 0.3, GRIS_CLAIR),
    ]))
    return t


def make_objectifs_box(ctx):
    items = [Paragraph(f"• {o}", S["bullet"]) for o in ctx["objectifs"]]
    inner = [[Paragraph("OBJECTIFS PÉDAGOGIQUES", S["h2"])]] + [[i] for i in items]
    t = Table(inner, colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), MAGENTA_LFT),
        ("TEXTCOLOR", (0, 0), (0, 0), white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("BOX", (0, 0), (-1, -1), 0.5, GRIS_CLAIR),
    ]))
    return t


def make_vocab_table(vocab_list):
    rows = [[
        Paragraph("Anglais", S["th"]),
        Paragraph("Phonétique", S["th"]),
        Paragraph("Français", S["th"]),
    ]]
    for en, phon, fr in vocab_list:
        rows.append([
            Paragraph(en, S["vocab_en"]),
            Paragraph(phon, S["vocab_phon"]),
            Paragraph(fr, S["vocab_fr"]),
        ])
    t = Table(rows, colWidths=[5.5*cm, 5*cm, 6.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLEU_AEFE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, GRIS_TC]),
        ("BOX", (0, 0), (-1, -1), 0.5, GRIS_CLAIR),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, GRIS_CLAIR),
    ]))
    return t


def make_activity_box(num, titre, consigne, lignes_reponse=4):
    """Encadré activité avec lignes pour réponse manuscrite."""
    head = Paragraph(
        f'<font color="#E6007E"><b>ACTIVITÉ {num}</b></font>  '
        f'<font color="#003B5C"><b>{titre}</b></font>',
        S["h3"])
    cons = Paragraph(consigne, S["body"])
    lines = []
    for _ in range(lignes_reponse):
        lines.append(Paragraph("&nbsp;", S["answer"]))
        lines.append(HRFlowable(width="100%", thickness=0.5, color=GRIS_CLAIR))

    inner = [[head], [cons]] + [[ln] for ln in lines]
    t = Table(inner, colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BACKGROUND", (0, 0), (0, 0), HexColor("#F0F4F8")),
        ("BOX", (0, 0), (-1, -1), 0.6, BLEU_AEFE),
    ]))
    return KeepTogether(t)


def make_qcm_box(num, titre, question, options):
    head = Paragraph(
        f'<font color="#E6007E"><b>ACTIVITÉ {num}</b></font>  '
        f'<font color="#003B5C"><b>{titre}</b></font>',
        S["h3"])
    q = Paragraph(question, S["body"])
    opts = []
    for letter, text in options:
        opts.append(Paragraph(f'<b>☐  {letter}.</b>  {text}', S["bullet"]))
    inner = [[head], [q]] + [[o] for o in opts]
    t = Table(inner, colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BACKGROUND", (0, 0), (0, 0), HexColor("#F0F4F8")),
        ("BOX", (0, 0), (-1, -1), 0.6, BLEU_AEFE),
    ]))
    return KeepTogether(t)


def make_resources_table(resources):
    rows = [[Paragraph("Type", S["th"]),
             Paragraph("Référence", S["th"]),
             Paragraph("Lien / accès", S["th"])]]
    for typ, ref, link in resources:
        rows.append([
            Paragraph(typ, S["td_b"]),
            Paragraph(ref, S["td"]),
            Paragraph(f'<font color="#7A7A7A">{link}</font>', S["td"]),
        ])
    t = Table(rows, colWidths=[3.2*cm, 7.8*cm, 6*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLEU_AEFE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, GRIS_TC]),
        ("BOX", (0, 0), (-1, -1), 0.5, GRIS_CLAIR),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, GRIS_CLAIR),
    ]))
    return t


def make_quiz_qr_block(quiz_url):
    """Bloc QR + URL pour la fin du document."""
    qr_buf = make_qr_buffer(quiz_url)
    from reportlab.platypus import Image as RLImage
    qr_img = RLImage(qr_buf, width=3.5*cm, height=3.5*cm)

    text = Paragraph(
        f'<font color="#E6007E"><b>QUIZ EN LIGNE — RÉSULTATS ARCHIVÉS</b></font><br/><br/>'
        f'<font color="#003B5C">Scannez le QR code ci-contre pour accéder au quiz '
        f'interactif synchronisé. Vos résultats seront archivés automatiquement '
        f'(Google Sheets) et un récapitulatif sera envoyé par e-mail.</font><br/><br/>'
        f'<font color="#7A7A7A"><i>{quiz_url}</i></font>',
        S["body"])
    t = Table([[qr_img, text]], colWidths=[4*cm, 13*cm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("BACKGROUND", (0, 0), (-1, -1), FOND_CREME),
        ("BOX", (0, 0), (-1, -1), 0.6, MAGENTA_LFT),
    ]))
    return t


# ============================================================
#   GENERATEUR PRINCIPAL
# ============================================================
def build_pdf(ctx, out_filename):
    out_path = os.path.join(OUT_DIR, out_filename)

    def first_page(canv, doc): draw_cover(canv, doc, ctx)
    def later_pages(canv, doc):
        draw_header(canv, doc, ctx)
        draw_footer(canv, doc, ctx)

    doc = SimpleDocTemplate(out_path, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=2.8*cm, bottomMargin=1.6*cm,
        title=ctx["title"], author="Mme Salamo FALIMANANA — LFT")

    story = []

    # ---- PAGE 1 : couverture (rendue par draw_cover) ----
    story.append(PageBreak())  # forcer la couverture seule

    # ---- PAGE 2 : pédagogie + lexique ----
    story.append(make_section_title("Pédagogie & objectifs"))
    story.append(Paragraph(ctx["intro_pedago"], S["lead"]))
    story.append(make_pedago_table(ctx))
    story.append(Spacer(1, 10))
    story.append(make_objectifs_box(ctx))
    story.append(Spacer(1, 12))

    story.append(make_h2("Lexique académique"))
    story.append(Paragraph(ctx["lexique_intro"], S["body"]))
    story.append(make_vocab_table(ctx["vocab"]))

    story.append(PageBreak())

    # ---- PAGE 3 : activités imprimables ----
    story.append(make_section_title("Activités prêtes à imprimer"))
    story.append(Paragraph(ctx["activites_intro"], S["lead"]))
    for act in ctx["activites"]:
        if act["type"] == "qcm":
            story.append(make_qcm_box(act["num"], act["titre"], act["q"], act["options"]))
        else:
            story.append(make_activity_box(act["num"], act["titre"],
                                           act["consigne"], act.get("lignes", 4)))
        story.append(Spacer(1, 8))

    story.append(PageBreak())

    # ---- PAGE 4 : tâche finale + ressources + QR ----
    story.append(make_section_title("Tâche finale & ressources"))
    story.append(Paragraph(f'<b>{ctx["tache_finale"]}</b>', S["lead"]))
    story.append(Paragraph(ctx["tache_detail"], S["body"]))
    story.append(Spacer(1, 8))

    if ctx.get("citation"):
        story.append(Paragraph(f'« {ctx["citation"]} »', S["quote"]))
        story.append(Paragraph(f'<i>— {ctx["citation_auteur"]}</i>', S["small_c"]))
        story.append(Spacer(1, 10))

    story.append(make_h2("Ressources externes"))
    story.append(make_resources_table(ctx["resources"]))
    story.append(Spacer(1, 14))

    story.append(make_quiz_qr_block(ctx["quiz_url"]))

    doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)
    print(f"  ✓ {out_filename}")


# ============================================================
#   CONTENU DES 3 PDF
# ============================================================
PDF_THE_GIVER = {
    "title": "The Giver",
    "subtitle": "Lois Lowry · Dystopia & Memory",
    "level": "B1",
    "classe_label": "4ᵉ NON SI",
    "classe": "Section Internationale",
    "seq_n": 2,
    "axe": "Fiction et société — utopies/dystopies",
    "axe_court": "Fiction & société",
    "seances": "8 séances",
    "activites_count": "4 activités imprimables",
    "duree": "8 séances de 55 min · ~7h30",
    "competences": "Compréhension écrite (CE), Expression orale en continu (EOC), Expression écrite (EE)",
    "activites_lang": "Lecture suivie d'extraits, débat de classe, écriture créative",
    "tache_finale": "Essai argumentatif (350 mots) : <i>Would you live in The Community?</i>",
    "edito_title": "DYSTOPIE ET MÉMOIRE COLLECTIVE",
    "edito_lines": [
        "Publié en 1993 et lauréat de la Newbery Medal,",
        "<i>The Giver</i> de Lois Lowry est devenu un classique",
        "de la littérature dystopique pour adolescents.",
        "Le roman interroge nos rapports à la mémoire,",
        "à la liberté et à la conformité — autant de thèmes",
        "essentiels en classe de 4ᵉ NON SI.",
    ],
    "intro_pedago": (
        "Cette séquence propose un parcours de lecture suivi du roman "
        "<i>The Giver</i> (Lois Lowry, 1993). À travers le destin de Jonas, "
        "élu <i>Receiver of Memory</i>, les élèves explorent les ressorts "
        "des sociétés totalitaires et la valeur de la mémoire collective. "
        "Mobilisation des structures conditionnelles et de la voix passive."
    ),
    "objectifs": [
        "Comprendre les caractéristiques d'une dystopie (Sameness, contrôle, euphémismes).",
        "Repérer les choix narratifs (focalisation interne, narrateur peu fiable).",
        "Mobiliser la voix passive et le conditionnel pour analyser une société imaginaire.",
        "Construire une argumentation orale et écrite sur la liberté individuelle.",
        "Mettre en relation <i>The Giver</i> avec d'autres dystopies YA (Collins, Roth).",
    ],
    "lexique_intro": (
        "Lexique central pour aborder le roman et conduire les activités d'analyse. "
        "À mémoriser pour la séance 4 (interrogation orale ou écrite)."
    ),
    "vocab": [
        ("dystopia",      "/dɪsˈtəʊpiə/",     "dystopie, société imaginaire négative"),
        ("Sameness",      "/ˈseɪmnəs/",       "uniformité (concept clé du roman)"),
        ("release",       "/rɪˈliːs/",        "« release » (euphémisme : euthanasie)"),
        ("memory",        "/ˈmemᵊri/",        "mémoire, souvenir"),
        ("the Receiver",  "/ðə rɪˈsiːvə/",   "le Receveur (rôle de Jonas)"),
        ("the Giver",     "/ðə ˈɡɪvə/",      "le Donneur (mentor)"),
        ("conformity",    "/kənˈfɔːmᵊti/",    "conformisme"),
        ("free will",     "/friː ˈwɪl/",     "libre arbitre"),
        ("conditioning",  "/kənˈdɪʃᵊnɪŋ/",   "conditionnement"),
        ("Stirrings",     "/ˈstɜːrɪŋz/",     "« émois », pulsions adolescentes"),
        ("Ceremony",      "/ˈserəməni/",     "cérémonie (rite de passage)"),
        ("rebellion",     "/rɪˈbeljᵊn/",     "rébellion, révolte"),
    ],
    "activites_intro": (
        "Ces activités peuvent être imprimées et utilisées en classe. "
        "Une version interactive en ligne est disponible via le QR code."
    ),
    "activites": [
        {
            "type": "qcm", "num": 1,
            "titre": "Compréhension de chapitre",
            "q": "Pourquoi Jonas est-il choisi comme <i>Receiver of Memory</i> "
                 "lors de la <i>Ceremony of Twelves</i> ?",
            "options": [
                ("A", "Parce qu'il est le plus fort physiquement de sa classe."),
                ("B", "Parce qu'il a les <i>Capacity to See Beyond</i> et les qualités requises."),
                ("C", "Parce que ses parents le recommandent au Council."),
                ("D", "Parce qu'il est volontaire."),
            ],
        },
        {
            "type": "qcm", "num": 2,
            "titre": "Vocabulaire — euphémismes",
            "q": "Dans The Community, <i>« release »</i> signifie en réalité…",
            "options": [
                ("A", "Une libération joyeuse vers une vie nouvelle."),
                ("B", "Un voyage de retraite."),
                ("C", "L'euthanasie des bébés faibles, des vieillards ou des contrevenants."),
                ("D", "Un rite religieux."),
            ],
        },
        {
            "type": "free", "num": 3,
            "titre": "Voix passive — réécriture",
            "consigne": "Réécris ces phrases à la voix passive :<br/>"
                        "1) <i>The Giver transmits memories to Jonas.</i><br/>"
                        "2) <i>The Council releases unfit babies.</i><br/>"
                        "3) <i>Pills suppress the Stirrings.</i>",
            "lignes": 5,
        },
        {
            "type": "free", "num": 4,
            "titre": "Production écrite — débat",
            "consigne": "En 80-100 mots, donne ton avis : "
                        "<i>« Sameness brings peace, but at what cost? »</i> "
                        "Mobilise le conditionnel et au moins trois mots du lexique.",
            "lignes": 7,
        },
    ],
    "tache_detail": (
        "À l'issue de la séquence, l'élève rédige un essai argumentatif de "
        "350 mots autour de la question <i>Would you live in The Community?</i> "
        "L'essai mobilise au moins deux scènes du roman, trois éléments du "
        "lexique et une structure complexe (conditional ou voix passive). "
        "Évaluation : grille B1 (cohérence des idées, richesse lexicale, "
        "correction grammaticale, conviction)."
    ),
    "citation": "The worst part of holding the memories is not the pain. It's the loneliness of it.",
    "citation_auteur": "The Giver — Lois Lowry",
    "resources": [
        ("Roman", "<i>The Giver</i>, Lois Lowry (1993, HMH Books)", "ISBN 978-0-544-33626-1"),
        ("Film", "<i>The Giver</i>, Phillip Noyce (2014)", "Walden Media · 1h37"),
        ("Article", "Lowry, L. — Newbery acceptance speech (1994)", "<i>Horn Book Magazine</i>"),
        ("Vidéo", "TED-Ed — How to recognize a dystopia", "ed.ted.com"),
        ("Quiz", "Quiz interactif The Giver — LFT", "QR code ci-dessous"),
    ],
    "quiz_url": "https://lyceefrancaisdetananarive.github.io/anglais/quiz/4e/the-giver.html",
}


PDF_BRITAIN_EUROPE = {
    "title": "Britain & Europe",
    "subtitle": "From Romans to Brexit",
    "level": "A2+",
    "classe_label": "4ᵉ LCE",
    "classe": "Langues et Cultures Européennes",
    "seq_n": 1,
    "axe": "Civilisation — relations Royaume-Uni / Continent",
    "axe_court": "Civilisation",
    "seances": "10 séances",
    "activites_count": "4 activités imprimables",
    "duree": "10 séances de 55 min · ~9h",
    "competences": "Compréhension orale (CO), Médiation, Expression orale en continu (EOC)",
    "activites_lang": "Documents iconographiques, frise chronologique, débat",
    "tache_finale": "Frise interactive RU-Continent (3 époques clés) + présentation orale 5 min",
    "edito_title": "DEUX RIVES, MILLE ANS D'HISTOIRE",
    "edito_lines": [
        "Le Royaume-Uni et le Continent sont deux acteurs",
        "indissociables de l'histoire européenne. Des invasions",
        "romaines au Brexit (2020), en passant par la Magna Carta",
        "et les guerres napoléoniennes : explorer ces relations,",
        "c'est comprendre la construction même de l'Europe",
        "moderne. Module culturel d'ouverture.",
    ],
    "intro_pedago": (
        "Premier module de l'option <strong>LCE</strong>, cette séquence "
        "ouvre un parcours culturel transversal entre le Royaume-Uni et le "
        "continent européen. À travers cinq grandes périodes (Roman Britain, "
        "Norman Conquest, Tudors, Napoleonic Wars, EU-Brexit), les élèves "
        "construisent une frise visuelle et apprennent à manier le "
        "vocabulaire de l'Histoire en anglais."
    ),
    "objectifs": [
        "Identifier 5 périodes clés des relations RU-Europe (Romains, Normands, Tudors, Napoléon, UE/Brexit).",
        "Manier le vocabulaire de la civilisation britannique (Crown, Parliament, Empire).",
        "Lire et présenter une frise chronologique en anglais.",
        "Comparer les institutions britanniques et continentales (monarchies, républiques).",
        "Comprendre les enjeux du Brexit et du Commonwealth.",
    ],
    "lexique_intro": (
        "Lexique de la civilisation britannique. Les termes en gras sont "
        "à connaître pour la frise chronologique de la séance 7."
    ),
    "vocab": [
        ("invasion",       "/ɪnˈveɪʒᵊn/",      "invasion, conquête"),
        ("settlement",     "/ˈsetᵊlmənt/",     "colonie, implantation"),
        ("the Crown",      "/ðə kraʊn/",       "la Couronne (institution)"),
        ("Parliament",     "/ˈpɑːləmənt/",    "Parlement (Westminster)"),
        ("monarchy",       "/ˈmɒnəki/",        "monarchie"),
        ("Empire",         "/ˈempaɪə/",        "empire colonial"),
        ("Commonwealth",   "/ˈkɒmənwelθ/",    "Commonwealth (56 États)"),
        ("Reformation",    "/ˌrefəˈmeɪʃᵊn/",   "Réforme protestante"),
        ("alliance",       "/əˈlaɪᵊns/",      "alliance militaire/diplomatique"),
        ("treaty",         "/ˈtriːti/",        "traité international"),
        ("Brexit",         "/ˈbreksɪt/",      "British Exit (sortie de l'UE)"),
        ("referendum",     "/ˌrefᵊˈrendəm/",  "référendum populaire"),
    ],
    "activites_intro": (
        "Sélection d'activités combinant lecture iconographique, "
        "vocabulaire historique et production orale."
    ),
    "activites": [
        {
            "type": "qcm", "num": 1,
            "titre": "Chronologie — la conquête normande",
            "q": "En quelle année Guillaume le Conquérant débarque-t-il en Angleterre ?",
            "options": [
                ("A", "1066 (Battle of Hastings)."),
                ("B", "1215 (Magna Carta)."),
                ("C", "1485 (Bosworth Field)."),
                ("D", "1603 (James I unifies crowns)."),
            ],
        },
        {
            "type": "qcm", "num": 2,
            "titre": "Brexit — date et contexte",
            "q": "À quelle date le Royaume-Uni est-il officiellement sorti de l'Union européenne ?",
            "options": [
                ("A", "23 juin 2016 (jour du référendum)."),
                ("B", "31 janvier 2020 (sortie effective)."),
                ("C", "1 janvier 2021 (fin de la transition)."),
                ("D", "9 mai 2025."),
            ],
        },
        {
            "type": "free", "num": 3,
            "titre": "Médiation — frise chronologique",
            "consigne": "À l'aide du document distribué en classe, place dans l'ordre "
                        "ces 5 événements (en anglais) : <i>Roman invasion · Norman Conquest · "
                        "Reformation · Napoleonic Wars · UK joins EEC</i>.",
            "lignes": 5,
        },
        {
            "type": "free", "num": 4,
            "titre": "Expression orale — Commonwealth",
            "consigne": "En 80 mots maximum, présente le Commonwealth : "
                        "Combien de membres ? Quels exemples ? Quel rôle joue le monarque ? "
                        "Mobilise au moins quatre mots du lexique.",
            "lignes": 6,
        },
    ],
    "tache_detail": (
        "À l'issue de la séquence, chaque élève prépare une frise chronologique "
        "illustrée (papier ou numérique via Canva / Genially) qui retrace 3 époques "
        "clés au choix des relations RU-Continent. Présentation orale de 5 min en "
        "anglais devant la classe (avec posters ou slides). Évaluation par "
        "positionnement de compétences (objectif culturel LCE, A2+)."
    ),
    "citation": "Britain is part of Europe—and not part of Europe.",
    "citation_auteur": "Hugh Gaitskell, 1962",
    "resources": [
        ("Manuel", "<i>BBC Bitesize — KS3 History</i>", "bbc.co.uk/bitesize"),
        ("Vidéo", "<i>The History of Britain in 5 minutes</i>", "BBC Teach (YouTube)"),
        ("Documentaire", "<i>The Story of Brexit</i>, BBC (2020)", "BBC iPlayer"),
        ("Article", "<i>Magna Carta and its legacy</i>", "British Library — bl.uk"),
        ("Quiz", "Quiz Britain & Europe — LFT (à venir)", "QR ci-dessous"),
    ],
    "quiz_url": "https://lyceefrancaisdetananarive.github.io/anglais/quiz/4e/britain-europe.html",
}


PDF_CURIOUS_INCIDENT = {
    "title": "The Curious Incident",
    "subtitle": "Mark Haddon · Neurodiversity & Voice",
    "level": "B1",
    "classe_label": "3ᵉ NON SI",
    "classe": "Section Internationale",
    "seq_n": 2,
    "axe": "Littérature — voix narratives et neurodiversité",
    "axe_court": "Littérature",
    "seances": "10 séances",
    "activites_count": "4 activités imprimables",
    "duree": "10 séances de 55 min · ~9h",
    "competences": "Compréhension écrite (CE), Expression écrite (EE), Médiation",
    "activites_lang": "Lecture suivie, écriture créative, débat sur la neurodiversité",
    "tache_finale": "Réécriture créative (300 mots) : un événement vu par Christopher",
    "edito_title": "ENTRER DANS UNE AUTRE FAÇON DE PENSER",
    "edito_lines": [
        "<i>The Curious Incident of the Dog in the Night-Time</i>",
        "(Mark Haddon, 2003) raconte une enquête menée par",
        "Christopher Boone, 15 ans, dont l'esprit fonctionne",
        "différemment (autisme implicite). Roman primé,",
        "adapté au théâtre (Tony Award 2015), il invite à",
        "découvrir la neurodiversité et le pouvoir de la voix narrative.",
    ],
    "intro_pedago": (
        "Cette séquence propose un parcours autour du roman "
        "<i>The Curious Incident of the Dog in the Night-Time</i> "
        "(Mark Haddon, 2003). À travers la voix singulière de Christopher, "
        "les élèves découvrent les enjeux de la <strong>neurodiversité</strong>, "
        "explorent les choix narratifs (focalisation interne, présent narratif) "
        "et préparent l'épreuve écrite du DNB."
    ),
    "objectifs": [
        "Comprendre la voix narrative singulière de Christopher (focalisation interne, présent narratif).",
        "Identifier les marqueurs textuels du « cerveau neurodivergent » (logique, listes, dessins).",
        "Mobiliser le past simple et le present perfect pour analyser le récit.",
        "Argumenter sur la représentation des handicaps cognitifs en littérature.",
        "Préparer le format DNB (compréhension de texte + expression écrite).",
    ],
    "lexique_intro": (
        "Lexique pour aborder le roman et la thématique de la neurodiversité. "
        "Items en gras à mémoriser pour la séance 5."
    ),
    "vocab": [
        ("neurodiversity",  "/ˌnjʊərəʊdaɪˈvɜːsᵊti/", "neurodiversité"),
        ("autism",          "/ˈɔːtɪzᵊm/",            "autisme"),
        ("on the spectrum", "/ɒn ðə ˈspektrəm/",      "sur le spectre autistique"),
        ("investigation",   "/ɪnˌvestɪˈɡeɪʃᵊn/",     "enquête, investigation"),
        ("clue",            "/kluː/",                 "indice"),
        ("witness",         "/ˈwɪtnəs/",              "témoin"),
        ("first-person",    "/ˌfɜːst ˈpɜːsᵊn/",     "narrateur à la première personne"),
        ("narrator",        "/nəˈreɪtə/",             "narrateur"),
        ("perspective",     "/pəˈspektɪv/",           "point de vue, perspective"),
        ("logic",           "/ˈlɒdʒɪk/",              "logique"),
        ("pattern",         "/ˈpætᵊn/",              "motif, schéma"),
        ("overwhelmed",     "/ˌəʊvəˈwelmd/",          "submergé (par les sens)"),
    ],
    "activites_intro": (
        "Activités prêtes à imprimer combinant compréhension de texte, "
        "exercices grammaticaux et production écrite (format DNB)."
    ),
    "activites": [
        {
            "type": "qcm", "num": 1,
            "titre": "Compréhension — le détective amateur",
            "q": "Quel modèle littéraire Christopher prend-il pour modèle dans son enquête ?",
            "options": [
                ("A", "Hercule Poirot (Agatha Christie)."),
                ("B", "Sherlock Holmes (Conan Doyle)."),
                ("C", "Miss Marple (Agatha Christie)."),
                ("D", "Inspector Maigret (Simenon)."),
            ],
        },
        {
            "type": "qcm", "num": 2,
            "titre": "Voix narrative",
            "q": "Le roman est principalement narré à la…",
            "options": [
                ("A", "3ᵉ personne omnisciente."),
                ("B", "1ʳᵉ personne (Christopher narrateur)."),
                ("C", "2ᵉ personne (« vous »)."),
                ("D", "Forme épistolaire."),
            ],
        },
        {
            "type": "free", "num": 3,
            "titre": "Past simple vs Present perfect",
            "consigne": "Conjugue les verbes entre parenthèses :<br/>"
                        "1) Last week, Wellington <i>(to be)</i> killed.<br/>"
                        "2) Christopher <i>(to investigate)</i> the case for several days now.<br/>"
                        "3) He <i>(never / to take)</i> the train alone before this novel.",
            "lignes": 5,
        },
        {
            "type": "free", "num": 4,
            "titre": "Expression écrite — réécriture",
            "consigne": "Imagine une scène de la vie quotidienne (acheter un ticket de bus, "
                        "passer un examen…) racontée par Christopher en 80-100 mots. "
                        "Conserve sa voix : phrases courtes, listes, logique implacable.",
            "lignes": 7,
        },
    ],
    "tache_detail": (
        "Production écrite finale (DNB-friendly) : 300 mots — l'élève réécrit "
        "un événement marquant de sa propre vie en adoptant la voix de Christopher "
        "Boone. Critères d'évaluation : fidélité à la voix narrative (présent, "
        "logique, listes), richesse lexicale (au moins 6 mots du lexique), "
        "correction grammaticale, créativité."
    ),
    "citation": "Prime numbers are what is left when you have taken all the patterns away.",
    "citation_auteur": "The Curious Incident — Mark Haddon",
    "resources": [
        ("Roman", "<i>The Curious Incident…</i>, Mark Haddon (2003)", "ISBN 978-0-099-45025-2"),
        ("Théâtre", "Adaptation Simon Stephens (NT 2012, Tony Award 2015)", "National Theatre"),
        ("Audio", "BBC Radio 4 — interview Mark Haddon", "bbc.co.uk/sounds"),
        ("Vidéo", "TED — Temple Grandin <i>The world needs all kinds of minds</i>", "ted.com"),
        ("Quiz", "Quiz The Curious Incident — LFT (à venir)", "QR ci-dessous"),
    ],
    "quiz_url": "https://lyceefrancaisdetananarive.github.io/anglais/quiz/3e/curious-incident.html",
}


# ============================================================
#   ENTRY POINT
# ============================================================
def main():
    print("Sprint B — génération des PDF magazines manquants...")
    build_pdf(PDF_THE_GIVER,         "fiche_4e_non_si_the_giver.pdf")
    build_pdf(PDF_BRITAIN_EUROPE,    "fiche_4e_lce_britain_europe.pdf")
    build_pdf(PDF_CURIOUS_INCIDENT,  "fiche_3e_non_si_curious_incident.pdf")
    print("Sprint B terminé : 3 PDF générés.")


if __name__ == "__main__":
    main()

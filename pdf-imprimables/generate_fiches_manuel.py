"""
Phase B — Refonte des fiches d'activité au format MANUEL.

Caractéristiques :
  - Format moderne, simple et pédagogique (style manuel scolaire)
  - Logos AEFE et LFT visibles, bien dimensionnés en en-tête
  - Pas de liste d'objectifs ni de tableau pédagogique institutionnel
  - Activités prêtes à l'emploi : warm-up, lexique illustré, lecture,
    faits de langue, production, tâche finale
  - QR code intégré vers l'activité d'entraînement en ligne
  - 4 pages A4

Génère 1 PDF par séquence définie dans le dict FICHES.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    HRFlowable, KeepTogether, Image as RLImage,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
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
BLEU_FRANCE = HexColor("#000091")   # Bleu France DSFR
BLEU_AEFE   = HexColor("#003B5C")
ROUGE_FR    = HexColor("#E1000F")   # Rouge Marianne
MAGENTA_LFT = HexColor("#E6007E")
OR          = HexColor("#C9A027")
NOIR        = HexColor("#161616")
GRIS_FONCE  = HexColor("#3D3D3D")
GRIS_MOYEN  = HexColor("#7A7A7A")
GRIS_CLAIR  = HexColor("#E8E8E8")
GRIS_TC     = HexColor("#F5F5F5")
FOND_CREME  = HexColor("#FAFAF7")
JAUNE_PALE  = HexColor("#FFF8E1")
BLEU_PALE   = HexColor("#E5F1F7")

# === CHEMINS ============================================================
ROOT      = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGO_LFT  = os.path.join(ROOT, "assets", "img", "logo-lft.png")
LOGO_AEFE = os.path.join(ROOT, "assets", "img", "logo-aefe-egd.png")
OUT_DIR   = os.path.dirname(__file__)


# ============================================================
#   QR CODE
# ============================================================
def make_qr(url, color="#000091"):
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
#   STYLES TYPOGRAPHIQUES
# ============================================================
base = getSampleStyleSheet()
S = {
    "h1": ParagraphStyle("h1", parent=base["Heading1"],
        fontName="Sans-Bold", fontSize=18, leading=22,
        textColor=BLEU_FRANCE, spaceBefore=10, spaceAfter=8),
    "h2": ParagraphStyle("h2", parent=base["Heading2"],
        fontName="Sans-Bold", fontSize=14, leading=18,
        textColor=BLEU_FRANCE, spaceBefore=8, spaceAfter=6),
    "h3": ParagraphStyle("h3", parent=base["Heading3"],
        fontName="Sans-Bold", fontSize=11, leading=14,
        textColor=MAGENTA_LFT, spaceBefore=6, spaceAfter=4),
    "body": ParagraphStyle("body", parent=base["BodyText"],
        fontName="Sans", fontSize=10.5, leading=15,
        textColor=NOIR, alignment=TA_JUSTIFY, spaceAfter=4),
    "bullet": ParagraphStyle("bullet", parent=base["BodyText"],
        fontName="Sans", fontSize=10, leading=14,
        textColor=NOIR, leftIndent=14, spaceAfter=2),
    "lead": ParagraphStyle("lead", parent=base["BodyText"],
        fontName="Sans-Italic", fontSize=11, leading=16,
        textColor=GRIS_FONCE, spaceAfter=8),
    "small": ParagraphStyle("small", parent=base["BodyText"],
        fontName="Sans", fontSize=8.5, leading=11,
        textColor=GRIS_MOYEN),
    "small_c": ParagraphStyle("small_c", parent=base["BodyText"],
        fontName="Sans", fontSize=8.5, leading=11,
        textColor=GRIS_MOYEN, alignment=TA_CENTER),
    "td": ParagraphStyle("td", parent=base["BodyText"],
        fontName="Sans", fontSize=9.5, leading=13, textColor=NOIR),
    "th": ParagraphStyle("th", parent=base["BodyText"],
        fontName="Sans-Bold", fontSize=9.5, leading=12,
        textColor=white, alignment=TA_LEFT),
    "vocab_en": ParagraphStyle("vocab_en", parent=base["BodyText"],
        fontName="Sans-Bold", fontSize=10.5, leading=13, textColor=BLEU_FRANCE),
    "vocab_phon": ParagraphStyle("vocab_phon", parent=base["BodyText"],
        fontName="Sans-Italic", fontSize=9.5, leading=12, textColor=GRIS_MOYEN),
    "vocab_fr": ParagraphStyle("vocab_fr", parent=base["BodyText"],
        fontName="Sans", fontSize=10, leading=13, textColor=NOIR),
    "answer": ParagraphStyle("answer", parent=base["BodyText"],
        fontName="Sans", fontSize=10, leading=22, textColor=GRIS_MOYEN),
    "quote": ParagraphStyle("quote", parent=base["BodyText"],
        fontName="Sans-Italic", fontSize=11, leading=16,
        textColor=BLEU_AEFE, alignment=TA_CENTER,
        leftIndent=20, rightIndent=20, spaceBefore=6, spaceAfter=6),
    "tag": ParagraphStyle("tag", parent=base["BodyText"],
        fontName="Sans-Bold", fontSize=9, leading=11,
        textColor=white, alignment=TA_CENTER),
}


# ============================================================
#   BANDEAU EN-TÊTE — logos AEFE + LFT bien visibles
# ============================================================
def draw_header_band(canv, doc, ctx, page_num):
    """Bandeau institutionnel en haut de chaque page (sauf couverture)."""
    canv.saveState()
    page_w, page_h = A4

    # Fond blanc + bord doré
    canv.setFillColor(white)
    canv.rect(0, page_h - 2.6*cm, page_w, 2.6*cm, stroke=0, fill=1)
    canv.setFillColor(OR)
    canv.rect(0, page_h - 2.65*cm, page_w, 0.05*cm, stroke=0, fill=1)

    # Logo AEFE (gauche) — paysage, hauteur ~1.4cm pour bonne visibilité
    if os.path.exists(LOGO_AEFE):
        canv.drawImage(LOGO_AEFE, 1.4*cm, page_h - 2.2*cm,
                       width=2.7*cm, height=1.4*cm,
                       preserveAspectRatio=True, mask='auto')

    # Logo LFT (droite) — carré
    if os.path.exists(LOGO_LFT):
        canv.drawImage(LOGO_LFT, page_w - 3.2*cm, page_h - 2.3*cm,
                       width=1.8*cm, height=1.8*cm,
                       preserveAspectRatio=True, mask='auto')

    # Texte central
    canv.setFillColor(BLEU_FRANCE)
    canv.setFont("Sans-Bold", 10)
    canv.drawCentredString(page_w/2, page_h - 1.0*cm,
                           "LYCÉE FRANÇAIS DE TANANARIVE")
    canv.setFont("Sans", 8.5)
    canv.setFillColor(GRIS_FONCE)
    canv.drawCentredString(page_w/2, page_h - 1.45*cm,
                           "Établissement en gestion directe · AEFE")
    canv.setFillColor(MAGENTA_LFT)
    canv.setFont("Sans-Italic", 8)
    canv.drawCentredString(page_w/2, page_h - 1.85*cm,
                           f"Anglais · {ctx['classe_label']} · "
                           f"Mme S. FALIMANANA")

    # Mention discrète niveau + séquence à droite
    canv.setFillColor(BLEU_FRANCE)
    canv.setFont("Sans-Bold", 8)
    canv.drawString(1.4*cm, page_h - 2.45*cm,
                    f"FICHE D'ACTIVITÉ — {ctx['classe_label'].upper()}")
    canv.drawRightString(page_w - 1.4*cm, page_h - 2.45*cm,
                         f"Séquence — {ctx['titre_court']}")

    canv.restoreState()


# ============================================================
#   PIED DE PAGE
# ============================================================
def draw_footer(canv, doc, ctx):
    canv.saveState()
    page_w, _ = A4
    # Filets tricolores
    canv.setFillColor(BLEU_FRANCE)
    canv.rect(0, 0.95*cm, page_w/3, 0.12*cm, stroke=0, fill=1)
    canv.setFillColor(white)
    canv.rect(page_w/3, 0.95*cm, page_w/3, 0.12*cm, stroke=0, fill=1)
    canv.setFillColor(ROUGE_FR)
    canv.rect(2*page_w/3, 0.95*cm, page_w/3, 0.12*cm, stroke=0, fill=1)

    canv.setFillColor(GRIS_MOYEN)
    canv.setFont("Sans", 7.5)
    canv.drawString(1.4*cm, 0.5*cm,
        f"© LFT · {ctx['titre']} · Mme S. FALIMANANA")
    canv.drawRightString(page_w - 1.4*cm, 0.5*cm,
        f"Page {canv.getPageNumber()}")
    canv.restoreState()


# ============================================================
#   COUVERTURE — éditoriale, logos visibles
# ============================================================
def draw_cover(canv, doc, ctx):
    canv.saveState()
    page_w, page_h = A4

    # ---- BANDEAU SUPÉRIEUR — institutionnel, logos visibles ----
    # Hauteur 3.5 cm pour bien aérer les logos
    canv.setFillColor(white)
    canv.rect(0, page_h - 3.5*cm, page_w, 3.5*cm, stroke=0, fill=1)
    canv.setFillColor(OR)
    canv.rect(0, page_h - 3.55*cm, page_w, 0.05*cm, stroke=0, fill=1)

    # Logo AEFE — bien visible (h=2 cm)
    if os.path.exists(LOGO_AEFE):
        canv.drawImage(LOGO_AEFE, 1.5*cm, page_h - 3.0*cm,
                       width=4.0*cm, height=2.1*cm,
                       preserveAspectRatio=True, mask='auto')

    # Logo LFT — bien visible (côté 2.4 cm)
    if os.path.exists(LOGO_LFT):
        canv.drawImage(LOGO_LFT, page_w - 4.0*cm, page_h - 3.05*cm,
                       width=2.4*cm, height=2.4*cm,
                       preserveAspectRatio=True, mask='auto')

    # Texte central de l'en-tête
    canv.setFillColor(BLEU_FRANCE)
    canv.setFont("Sans-Bold", 12)
    canv.drawCentredString(page_w/2, page_h - 1.4*cm, "LYCÉE FRANÇAIS DE TANANARIVE")
    canv.setFillColor(GRIS_FONCE)
    canv.setFont("Sans", 9.5)
    canv.drawCentredString(page_w/2, page_h - 1.9*cm,
                           "Établissement en gestion directe · AEFE · Madagascar")
    canv.setFillColor(MAGENTA_LFT)
    canv.setFont("Sans-Italic", 9)
    canv.drawCentredString(page_w/2, page_h - 2.3*cm,
                           "Espace pédagogique d'anglais · Mme Salamo FALIMANANA")
    canv.setFillColor(BLEU_FRANCE)
    canv.setFont("Sans-Bold", 8.5)
    canv.drawCentredString(page_w/2, page_h - 2.85*cm,
                           "lyceefrancaisdetananarive.github.io/anglais")

    # ---- BANDEAU MAGENTA + TITRE ÉDITORIAL ----
    title_y_top = page_h - 3.5*cm
    title_h = 7.5*cm

    # Bandeau magenta
    canv.setFillColor(MAGENTA_LFT)
    canv.rect(0, title_y_top - title_h, page_w, title_h, stroke=0, fill=1)

    # Filet bleu sous le bandeau
    canv.setFillColor(BLEU_FRANCE)
    canv.rect(0, title_y_top - title_h - 0.3*cm, page_w, 0.3*cm, stroke=0, fill=1)

    # Suréclairage radial subtil (effet)
    canv.setFillColorRGB(1, 1, 1, alpha=0.08)
    canv.circle(page_w * 0.85, title_y_top - 1.5*cm, 4*cm, stroke=0, fill=1)

    # Étiquette niveau / séquence (en haut du bandeau)
    canv.setFillColor(white)
    canv.setFont("Sans-Italic", 11)
    canv.drawString(2*cm, title_y_top - 1.2*cm,
                    f"FICHE D'ACTIVITÉ · {ctx['classe_label'].upper()} · {ctx['cecrl']}")

    # Titre principal
    canv.setFillColor(white)
    canv.setFont("Sans-Bold", 32)
    canv.drawString(2*cm, title_y_top - 2.8*cm, ctx['titre'][:32])

    # Sous-titre / thème
    canv.setFillColor(white)
    canv.setFont("Sans-BoldItalic", 16)
    canv.drawString(2*cm, title_y_top - 4.0*cm, ctx['theme'])

    # Tags (pills)
    canv.setFont("Sans", 9.5)
    tags = [ctx['cecrl'], ctx['periode'], ctx['nb_seances'], ctx.get('axe_court', '')]
    x = 2*cm
    for tag in tags:
        if not tag:
            continue
        w = canv.stringWidth(tag, "Sans", 9.5) + 18
        canv.setFillColorRGB(1, 1, 1, alpha=0.22)
        canv.roundRect(x, title_y_top - 5.3*cm, w, 0.75*cm, 6, stroke=0, fill=1)
        canv.setFillColor(white)
        canv.drawCentredString(x + w/2, title_y_top - 5.05*cm, tag)
        x += w + 8

    # Citation / amorce sous le titre
    if ctx.get('citation'):
        canv.setFillColor(white)
        canv.setFont("Sans-Italic", 10)
        canv.drawString(2*cm, title_y_top - 6.6*cm,
                        f'« {ctx["citation"][:80]} »')

    # ---- ZONE BASSE (fond crème) ---------------------------
    pres_y_top = title_y_top - title_h - 0.3*cm
    canv.setFillColor(FOND_CREME)
    canv.rect(0, 0, page_w, pres_y_top, stroke=0, fill=1)

    # Bloc « AU FIL DE CETTE FICHE »
    canv.setFillColor(BLEU_FRANCE)
    canv.setFont("Sans-Bold", 11)
    canv.drawString(2*cm, pres_y_top - 1.0*cm, "AU FIL DE CETTE FICHE")

    canv.setFillColor(NOIR)
    canv.setFont("Sans", 10)
    intro_lines = ctx['intro_lines']
    y = pres_y_top - 1.6*cm
    for line in intro_lines:
        canv.drawString(2*cm, y, line)
        y -= 0.5*cm

    # ---- ENCART « SOMMAIRE » (centre) ----
    box_y = 5.6*cm
    box_h = 4.2*cm
    canv.setFillColor(white)
    canv.roundRect(2*cm, box_y, page_w - 4*cm, box_h, 8, stroke=0, fill=1)
    canv.setStrokeColor(BLEU_FRANCE)
    canv.setLineWidth(0.5)
    canv.roundRect(2*cm, box_y, page_w - 4*cm, box_h, 8, stroke=1, fill=0)

    canv.setFillColor(BLEU_FRANCE)
    canv.setFont("Sans-Bold", 10.5)
    canv.drawString(2.5*cm, box_y + box_h - 0.7*cm, "AU SOMMAIRE DE CETTE FICHE")

    canv.setFont("Sans", 9.5)
    canv.setFillColor(NOIR)
    rubriques = [
        ("1.", "Lexique de la séquence — vocabulaire à mémoriser, illustré"),
        ("2.", "Document support + questions de compréhension"),
        ("3.", "Faits de langue — règle, exemples, exercice d'application"),
        ("4.", "Activité de production écrite ou orale"),
        ("→", "Tâche finale — projet à présenter, critères de réussite"),
    ]
    yy = box_y + box_h - 1.4*cm
    for num, txt in rubriques:
        canv.setFillColor(MAGENTA_LFT)
        canv.setFont("Sans-Bold", 9.5)
        canv.drawString(2.5*cm, yy, num)
        canv.setFillColor(NOIR)
        canv.setFont("Sans", 9.5)
        canv.drawString(3.4*cm, yy, txt)
        yy -= 0.5*cm

    # ---- BLOC QR CODE BAS DE PAGE (encadré aussi) ----
    canv.setFillColor(BLEU_PALE)
    canv.roundRect(2*cm, 1.3*cm, page_w - 4*cm, 3.8*cm, 8, stroke=0, fill=1)

    qr_buf = make_qr(ctx['quiz_url'])
    canv.drawImage(ImageReader(qr_buf), page_w - 5.4*cm, 1.6*cm,
                   width=3.2*cm, height=3.2*cm, mask='auto')

    canv.setFillColor(BLEU_FRANCE)
    canv.setFont("Sans-Bold", 11)
    canv.drawString(2.5*cm, 4.5*cm, "L'ACTIVITÉ D'ENTRAÎNEMENT EN LIGNE")
    canv.setFillColor(GRIS_FONCE)
    canv.setFont("Sans", 9.5)
    canv.drawString(2.5*cm, 3.95*cm, "Scannez ce QR code (ou recopiez l'adresse)")
    canv.drawString(2.5*cm, 3.5*cm, "pour faire l'activité interactive synchronisée.")
    canv.drawString(2.5*cm, 3.05*cm, "Retour automatique par e-mail à l'enseignante.")
    canv.setFillColor(MAGENTA_LFT)
    canv.setFont("Sans-Italic", 8.5)
    canv.drawString(2.5*cm, 2.6*cm, ctx['quiz_url'])

    # Mention pied de couverture
    canv.setFillColor(GRIS_MOYEN)
    canv.setFont("Sans", 7.5)
    canv.drawString(2*cm, 0.8*cm,
                    "Document à conserver dans le cahier d'anglais · "
                    "Mme Salamo FALIMANANA")

    canv.restoreState()


# ============================================================
#   COMPOSANTS PAGES INTÉRIEURES
# ============================================================
def make_h1(text):
    return Paragraph(text, S["h1"])

def make_h2(text):
    return Paragraph(text, S["h2"])

def make_h3(text):
    return Paragraph(text, S["h3"])

def make_p(text):
    return Paragraph(text, S["body"])

def make_lead(text):
    return Paragraph(text, S["lead"])


def make_vocab_table(rows_data):
    """Table de lexique : EN | phonétique | FR | exemple/illustration."""
    rows = [[
        Paragraph("Anglais", S["th"]),
        Paragraph("Phonétique", S["th"]),
        Paragraph("Français", S["th"]),
    ]]
    for en, phon, fr in rows_data:
        rows.append([
            Paragraph(en, S["vocab_en"]),
            Paragraph(phon, S["vocab_phon"]),
            Paragraph(fr, S["vocab_fr"]),
        ])
    t = Table(rows, colWidths=[5.0*cm, 4.5*cm, 7.5*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), BLEU_FRANCE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [white, GRIS_TC]),
        ("BOX", (0, 0), (-1, -1), 0.5, GRIS_CLAIR),
        ("INNERGRID", (0, 0), (-1, -1), 0.25, GRIS_CLAIR),
    ]))
    return t


def make_doc_card(title, body_html):
    """Encadré « Document support » : texte + intitulé."""
    inner = [
        [Paragraph(f'<font color="#000091"><b>{title}</b></font>', S["h2"])],
        [Paragraph(body_html, S["body"])],
    ]
    t = Table(inner, colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("BACKGROUND", (0, 0), (-1, -1), BLEU_PALE),
        ("BOX", (0, 0), (-1, -1), 0.6, BLEU_FRANCE),
    ]))
    return KeepTogether(t)


def make_question_block(question, lignes=4):
    """Question avec lignes pour réponse manuscrite."""
    items = [[Paragraph(question, S["body"])]]
    for _ in range(lignes):
        items.append([HRFlowable(width="100%", thickness=0.4, color=GRIS_CLAIR,
                                  spaceBefore=14, spaceAfter=2)])
    t = Table(items, colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    return KeepTogether(t)


def make_section_h1(num, title, color=BLEU_FRANCE):
    """Titre de grande section avec numéro stylisé (style manuel)."""
    color_hex = "#" + color.hexval()[2:] if hasattr(color, "hexval") else "#000091"
    html = (
        f'<font color="{color_hex}" size="22"><b>{num}</b></font>'
        f' &nbsp; <font color="#000091" size="18"><b>{title}</b></font>'
    )
    return Paragraph(html, ParagraphStyle("h1num", parent=base["Heading1"],
        fontName="Sans-Bold", fontSize=18, leading=24,
        spaceBefore=12, spaceAfter=10))


def make_grammar_box(title, intro, examples):
    """Encadré « Notice grammaticale » : titre + explication + exemples."""
    items = [
        [Paragraph(f'<font color="#E6007E"><b>{title.upper()}</b></font>', S["h2"])],
        [Paragraph(intro, S["body"])],
    ]
    for ex in examples:
        items.append([Paragraph(f'  •  <i>{ex}</i>', S["body"])])

    t = Table(items, colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BACKGROUND", (0, 0), (-1, -1), JAUNE_PALE),
        ("BOX", (0, 0), (-1, -1), 0.6, OR),
    ]))
    return KeepTogether(t)


def make_task_card(consigne, criteres):
    """Carte de tâche finale (consigne + critères de réussite)."""
    items = [
        [Paragraph('<font color="#E6007E"><b>TÂCHE FINALE</b></font>', S["h1"])],
        [Paragraph(consigne, S["body"])],
        [Spacer(1, 4)],
        [Paragraph('<font color="#000091"><b>Critères de réussite</b></font>', S["h3"])],
    ]
    for c in criteres:
        items.append([Paragraph(f'<font color="#E6007E">▪</font> &nbsp; {c}', S["body"])])

    t = Table(items, colWidths=[17*cm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("BACKGROUND", (0, 0), (-1, -1), white),
        ("BOX", (0, 0), (-1, -1), 1.5, MAGENTA_LFT),
    ]))
    return t


# ============================================================
#   GENERATEUR PRINCIPAL
# ============================================================
def build_fiche(ctx):
    out_path = os.path.join(OUT_DIR, ctx['filename'])

    def first_page(canv, doc):  draw_cover(canv, doc, ctx)
    def later_pages(canv, doc):
        draw_header_band(canv, doc, ctx, canv.getPageNumber())
        draw_footer(canv, doc, ctx)

    doc = SimpleDocTemplate(
        out_path, pagesize=A4,
        leftMargin=2*cm, rightMargin=2*cm,
        topMargin=3.0*cm, bottomMargin=1.5*cm,
        title=ctx['titre'], author="Mme Salamo FALIMANANA — LFT",
    )

    story = []
    story.append(PageBreak())

    # ---- PAGE 2 — LEXIQUE + COMPRÉHENSION ------------------
    story.append(make_section_h1("1.", "Lexique de la séquence"))
    story.append(make_lead(
        "Voici le lexique à connaître pour cette séquence. "
        "À mémoriser et à réinvestir dans les activités qui suivent."
    ))
    story.append(make_vocab_table(ctx['vocab']))
    story.append(Spacer(1, 12))

    story.append(make_section_h1("2.", "Document support"))
    story.append(make_doc_card(ctx['doc_titre'], ctx['doc_text']))
    story.append(Spacer(1, 8))

    story.append(make_h2("Compréhension"))
    for q in ctx['questions']:
        story.append(make_question_block(q, lignes=2))
        story.append(Spacer(1, 6))

    story.append(PageBreak())

    # ---- PAGE 3 — FAITS DE LANGUE + PRODUCTION -------------
    story.append(make_section_h1("3.", "Faits de langue"))
    story.append(make_grammar_box(
        ctx['grammar_titre'],
        ctx['grammar_intro'],
        ctx['grammar_examples'],
    ))
    story.append(Spacer(1, 8))

    if ctx.get('grammar_exo'):
        story.append(make_h3("Exercice d'application"))
        story.append(make_p(ctx['grammar_exo']))
        story.append(Spacer(1, 4))
        for _ in range(4):
            story.append(HRFlowable(width="100%", thickness=0.4,
                                    color=GRIS_CLAIR,
                                    spaceBefore=12, spaceAfter=2))

    story.append(Spacer(1, 14))
    story.append(make_section_h1("4.", "Activité de production"))
    story.append(make_p(ctx['production_consigne']))
    story.append(Spacer(1, 4))
    for _ in range(8):
        story.append(HRFlowable(width="100%", thickness=0.4,
                                color=GRIS_CLAIR,
                                spaceBefore=14, spaceAfter=2))

    story.append(PageBreak())

    # ---- PAGE 4 — TÂCHE FINALE + RESSOURCES ----------------
    story.append(make_task_card(ctx['tache_consigne'], ctx['tache_criteres']))
    story.append(Spacer(1, 12))

    if ctx.get('citation'):
        story.append(Paragraph(f'« {ctx["citation"]} »', S["quote"]))
        if ctx.get('citation_auteur'):
            story.append(Paragraph(f'<i>— {ctx["citation_auteur"]}</i>',
                                   S["small_c"]))
        story.append(Spacer(1, 10))

    if ctx.get('pour_aller_plus_loin'):
        story.append(make_h2("Pour aller plus loin"))
        for r in ctx['pour_aller_plus_loin']:
            story.append(Paragraph(
                f'<font color="#E6007E"><b>›</b></font> &nbsp; {r}', S["bullet"]))

    doc.build(story, onFirstPage=first_page, onLaterPages=later_pages)
    print(f"  ✓ {ctx['filename']}")


# ============================================================
#   CONTENUS PÉDAGOGIQUES — 9 SÉQUENCES
# ============================================================
FICHES = []

# --- 6e — Welcome to Big Ben Academy! ----------------------
FICHES.append({
    "filename": "fiche_6e_welcome_big_ben.pdf",
    "titre": "Welcome to Big Ben Academy!",
    "titre_court": "Welcome to Big Ben",
    "theme": "First day at school",
    "classe_label": "6ᵉ",
    "cecrl": "A1",
    "periode": "T1 (sept-oct)",
    "nb_seances": "6 séances",
    "axe_court": "School & me",
    "intro_lines": [
        "Cette fiche t'accompagne dans ta première séquence d'anglais",
        "au collège. Tu vas apprendre à te présenter, à dire ton âge,",
        "ta nationalité, et à parler de ton emploi du temps.",
        "Garde cette fiche dans ton cahier — tu y reviendras !",
    ],
    "vocab": [
        ("Hello / Hi",     "/həˈləʊ/, /haɪ/", "Bonjour / Salut"),
        ("My name is…",    "/maɪ ˈneɪm ɪz/",  "Je m'appelle…"),
        ("I'm … years old","/aɪm ... jɪərz əʊld/", "J'ai … ans"),
        ("a pupil",        "/ə ˈpjuːpəl/",    "un·e élève"),
        ("a classroom",    "/ə ˈklɑːsruːm/",  "une salle de classe"),
        ("a timetable",    "/ə ˈtaɪmˌteɪbəl/","un emploi du temps"),
        ("Monday — Friday","/ˈmʌndi/ /ˈfraɪdi/", "lundi — vendredi"),
        ("English",        "/ˈɪŋɡlɪʃ/",       "l'anglais"),
        ("Maths",          "/mæθs/",          "les maths"),
        ("PE (Physical Ed.)","/piː iː/",      "EPS"),
    ],
    "doc_titre": "Read — Sarah's first day",
    "doc_text": (
        "<i>Hi! My name is Sarah. I'm 11 years old and I'm French. "
        "I live in Antananarivo. Today is Monday, my first day at "
        "Big Ben Academy. My favourite subjects are English, Maths "
        "and Art. I have PE on Wednesday and Friday. I'm very excited!</i>"
    ),
    "questions": [
        "Where does Sarah live? Write a full sentence.",
        "How old is she? What grade do you think she is in?",
        "When does she have PE?",
        "What are her favourite subjects?",
    ],
    "grammar_titre": "Le verbe TO BE au présent",
    "grammar_intro": (
        "Pour <b>se présenter</b> et <b>parler de soi</b>, on utilise "
        "le verbe <b>to be</b>. Trois formes simples à mémoriser :"
    ),
    "grammar_examples": [
        "I <b>am</b> French. → I<b>'m</b> French.",
        "She <b>is</b> 11 years old. → She<b>'s</b> 11 years old.",
        "We <b>are</b> happy. → We<b>'re</b> happy.",
    ],
    "grammar_exo": (
        "<b>À toi !</b> Complète avec <i>am</i>, <i>is</i> ou <i>are</i> :<br/>"
        "1. My name ___ Tom. &nbsp;&nbsp; 2. They ___ in class 6M4. <br/>"
        "3. I ___ 11 years old. &nbsp;&nbsp; 4. We ___ from Madagascar."
    ),
    "production_consigne": (
        "<b>Présente-toi en 4-5 phrases.</b> Donne ton prénom, ton "
        "âge, ta nationalité, ta ville et tes 2 matières préférées. "
        "Utilise <i>I am / I'm</i> et le vocabulaire de la séquence."
    ),
    "tache_consigne": (
        "Enregistre une <b>carte de présentation audio</b> (1 minute) "
        "que tu enverras à un·e correspondant·e anglophone. Présente-toi : "
        "ton prénom, ton âge, ta nationalité, ta ville, ton école, "
        "tes matières préférées, ton emploi du temps."
    ),
    "tache_criteres": [
        "<b>Recevabilité linguistique</b> — prononciation claire, intonation",
        "<b>Cohérence</b> — au moins 5 phrases qui se suivent",
        "<b>Lexique</b> — mots de la séquence (école, matières, jours)",
        "<b>Faits de langue</b> — verbe <i>to be</i> bien utilisé",
    ],
    "citation": "The journey of a thousand miles begins with one step.",
    "citation_auteur": "Lao Tzu",
    "pour_aller_plus_loin": [
        "BBC Learning English — Schools around the world (vidéo 5 min)",
        "Chanson : <i>The Days of the Week</i> (Singing Walrus)",
        "App : Duolingo — module Greetings",
    ],
    "quiz_url": "https://lyceefrancaisdetananarive.github.io/anglais/quiz/6e/welcome-big-ben.html",
})

# --- 4e LVA — Stuck at Big Bay School ---------------------
FICHES.append({
    "filename": "fiche_4e_stuck_at_big_bay_school.pdf",
    "titre": "Stuck at Big Bay School",
    "titre_court": "Stuck at Big Bay",
    "theme": "Lecture cursive — Nouvelle-Zélande",
    "classe_label": "4ᵉ LV1",
    "cecrl": "A2",
    "periode": "T1 (oct-nov)",
    "nb_seances": "8 séances",
    "axe_court": "Voyages & cultures",
    "intro_lines": [
        "Cette séquence est une lecture cursive du roman jeunesse",
        "« Stuck at Big Bay School » de Helen Lehndorf. Tu vas découvrir",
        "la vie d'un collège en Nouvelle-Zélande, la culture māorie,",
        "et apprendre à comparer (comparatives & superlatives).",
    ],
    "vocab": [
        ("a school day",    "/ə ˈskuːl deɪ/",    "une journée d'école"),
        ("a classmate",     "/ə ˈklɑːsmeɪt/",    "un camarade de classe"),
        ("a uniform",       "/ə ˈjuːnɪfɔːm/",    "un uniforme"),
        ("a marae (Māori)", "/ə ˈmɑːraɪ/",       "lieu de rassemblement māori"),
        ("a haka (Māori)",  "/ə ˈhɑːkə/",        "danse cérémonielle"),
        ("kia ora (Māori)", "/ˌkiːə ˈɔːrə/",     "bonjour, bienvenue"),
        ("a backpack",      "/ə ˈbækpæk/",       "un sac à dos"),
        ("homework",        "/ˈhəʊmwɜːk/",       "les devoirs"),
        ("to be stuck",     "/tə biː stʌk/",     "être bloqué·e"),
        ("a North Island",  "/ə nɔːθ ˈaɪlənd/",  "île du Nord (NZ)"),
    ],
    "doc_titre": "Read — At Big Bay School",
    "doc_text": (
        "<i>It's Monday morning at Big Bay School in Wellington, "
        "New Zealand. Lily and her classmates are wearing their school "
        "uniforms. The teacher, Mr Tane, welcomes them with a friendly "
        "« kia ora! ». Lily is excited: today, students will learn the "
        "haka. Outside, the bay is bigger than ever, and the wind is "
        "stronger than yesterday — but the classroom feels like home.</i>"
    ),
    "questions": [
        "Where does the story take place?",
        "What does the teacher say at the beginning of class? What does it mean?",
        "What are the students going to learn that day?",
        "Find two comparatives in the text and translate them.",
    ],
    "grammar_titre": "Les comparatifs et superlatifs",
    "grammar_intro": (
        "Pour <b>comparer</b> deux éléments, on utilise <b>-er than</b> "
        "(adj. court) ou <b>more … than</b> (adj. long). Pour le "
        "<b>superlatif</b> : <b>the -est</b> ou <b>the most …</b>."
    ),
    "grammar_examples": [
        "The bay is <b>bigger than</b> ever.",
        "The wind is <b>stronger than</b> yesterday.",
        "Lily is <b>the most excited</b> student in the class.",
    ],
    "grammar_exo": (
        "<b>À toi !</b> Complète avec le comparatif ou superlatif :<br/>"
        "1. Maths is ___ (difficult) than Art.<br/>"
        "2. New Zealand is ___ (small) than Australia.<br/>"
        "3. Lily is ___ (talkative) student in her class."
    ),
    "production_consigne": (
        "<b>Compare ton collège</b> (le LFT) à Big Bay School. "
        "Écris 5-6 phrases avec au moins 3 comparatifs et 1 superlatif. "
        "Évoque l'uniforme, les camarades, les matières, le climat."
    ),
    "tache_consigne": (
        "Imagine que tu reçois Lily au LFT pour 1 semaine. "
        "Rédige une <b>lettre de bienvenue</b> (~150 mots) où tu lui "
        "présentes ton collège, ses différences avec Big Bay School, "
        "et un programme d'activités pour sa visite à Madagascar."
    ),
    "tache_criteres": [
        "<b>Recevabilité linguistique</b> — orthographe, ponctuation, syntaxe",
        "<b>Cohérence</b> — structure d'une lettre, idées organisées",
        "<b>Lexique</b> — vocabulaire scolaire et culturel mobilisé",
        "<b>Comparatifs / superlatifs</b> — au moins 3 utilisés correctement",
    ],
    "citation": "The world is a book and those who do not travel read only one page.",
    "citation_auteur": "Saint Augustine",
    "pour_aller_plus_loin": [
        "Helen Lehndorf — <i>Stuck at Big Bay School</i> (roman, 2019)",
        "BBC Earth — <i>New Zealand from above</i> (documentaire YouTube)",
        "Carte interactive : <i>Discover the marae of Aotearoa</i>",
    ],
    "quiz_url": "https://lyceefrancaisdetananarive.github.io/anglais/quiz/4e/stuck-big-bay.html",
})

# --- 4e NON SI — The Giver --------------------------------
FICHES.append({
    "filename": "fiche_4e_non_si_the_giver.pdf",
    "titre": "The Giver — Lois Lowry (1993)",
    "titre_court": "The Giver",
    "theme": "Lois Lowry · Dystopia & Memory",
    "classe_label": "4ᵉ NON SI",
    "cecrl": "B1",
    "periode": "T2 (jan-fév)",
    "nb_seances": "8 séances",
    "axe_court": "Fiction & société",
    "intro_lines": [
        "Tu vas découvrir « The Giver » de Lois Lowry, un classique",
        "de la littérature dystopique. À travers Jonas, élu Receiver",
        "of Memory, tu interrogeras la liberté individuelle, la mémoire",
        "collective et les sociétés totalitaires.",
    ],
    "vocab": [
        ("a dystopia",     "/dɪsˈtəʊpiə/",     "une dystopie"),
        ("Sameness",       "/ˈseɪmnəs/",       "uniformité (concept clé)"),
        ("a release",      "/ə rɪˈliːs/",      "un « release » (euphémisme)"),
        ("a memory",       "/ə ˈmemᵊri/",      "un souvenir, une mémoire"),
        ("the Receiver",   "/ðə rɪˈsiːvə/",    "le Receveur (rôle de Jonas)"),
        ("conformity",     "/kənˈfɔːmᵊti/",    "le conformisme"),
        ("free will",      "/friː ˈwɪl/",      "le libre arbitre"),
        ("conditioning",   "/kənˈdɪʃᵊnɪŋ/",    "le conditionnement"),
        ("Stirrings",      "/ˈstɜːrɪŋz/",      "« émois » (pulsions)"),
        ("rebellion",      "/rɪˈbeljᵊn/",      "rébellion, révolte"),
    ],
    "doc_titre": "Read — Chapter 1, opening",
    "doc_text": (
        "<i>It was almost December, and Jonas was beginning to be "
        "frightened. No. Wrong word, Jonas thought. Frightened meant "
        "that deep, sickening feeling of something terrible about to "
        "happen. […] He had waited a long time for this special "
        "December. Now that it was almost upon him, he wasn't frightened, "
        "but he was… he searched his mind for the right word. Apprehensive, "
        "Jonas finally decided.</i>"
    ),
    "questions": [
        "What is Jonas's first emotion in this passage? Why does he reject the word « frightened »?",
        "What word does he finally choose, and what does it tell us about him?",
        "What is the « special December » Jonas is waiting for? (Use chapter 1 hints)",
        "Find one example of free indirect speech in this extract.",
    ],
    "grammar_titre": "La voix passive (passive voice)",
    "grammar_intro": (
        "Dans une dystopie, beaucoup d'actions sont subies plutôt qu'agies. "
        "On utilise la <b>voix passive</b> : <b>to be + past participle</b>. "
        "Met l'accent sur l'objet/le patient, pas sur l'agent."
    ),
    "grammar_examples": [
        "Memories <b>are transmitted</b> to Jonas by the Giver.",
        "Babies <b>are released</b> when they are unfit.",
        "Stirrings <b>are suppressed</b> by daily pills.",
    ],
    "grammar_exo": (
        "<b>À toi !</b> Réécris à la voix passive :<br/>"
        "1. The Council assigns roles to the Twelves.<br/>"
        "2. The Community erased painful memories.<br/>"
        "3. The Giver chose Jonas as the new Receiver."
    ),
    "production_consigne": (
        "<b>What does « release » really mean?</b> En 80-100 mots, "
        "explique l'écart entre le sens officiel du mot dans The "
        "Community et sa signification réelle. Utilise au moins "
        "2 phrases passives et 4 mots du lexique."
    ),
    "tache_consigne": (
        "<b>Would you live in The Community?</b> Rédige un essai "
        "argumentatif de 350 mots autour de cette question. Mobilise "
        "au moins deux scènes du roman, trois éléments du lexique "
        "et une structure complexe (passive ou conditional)."
    ),
    "tache_criteres": [
        "<b>Argumentation</b> — thèse claire, arguments structurés (3 paragraphes)",
        "<b>Référence au roman</b> — au moins 2 scènes/personnages cités",
        "<b>Lexique</b> — mobilisation du vocabulaire de la dystopie",
        "<b>Faits de langue</b> — passive voice et/ou conditional présents",
    ],
    "citation": "The worst part of holding the memories is not the pain. It's the loneliness of it.",
    "citation_auteur": "The Giver — Lois Lowry",
    "pour_aller_plus_loin": [
        "Lois Lowry — <i>The Giver</i> (roman, 1993, HMH Books)",
        "Phillip Noyce — <i>The Giver</i> (film, 2014)",
        "TED-Ed — <i>How to recognize a dystopia</i> (vidéo 6 min)",
    ],
    "quiz_url": "https://lyceefrancaisdetananarive.github.io/anglais/quiz/4e/the-giver.html",
})


# ============================================================
#   AUTO-FILL — Génération à partir de progression.json
# ============================================================
import json
import re

PROGRESSION_PATH = os.path.join(ROOT, "assets", "data", "progression.json")
BASE_URL = "https://lyceefrancaisdetananarive.github.io/anglais"

# Mapping niveauKey → libellé classe + slug du dossier sequences/
NIVEAU_INFO = {
    "6e":         {"label": "6ᵉ",          "slug_dir": "6e"},
    "4e":         {"label": "4ᵉ LV1",      "slug_dir": "4e"},
    "4e-non-si":  {"label": "4ᵉ NON SI",   "slug_dir": "4e-non-si"},
    "4e-lce":     {"label": "4ᵉ LCE",      "slug_dir": "4e-lce"},
    "3e":         {"label": "3ᵉ LV1",      "slug_dir": "3e"},
    "3e-non-si":  {"label": "3ᵉ NON SI",   "slug_dir": "3e-non-si"},
    "1ere":       {"label": "1ʳᵉ euro",    "slug_dir": "1ere"},
    "terminale":  {"label": "Tᵉ LVA",      "slug_dir": "terminale"},
}


def slugify(s):
    s = s.lower()
    # Retirer les apostrophes typographiques
    s = re.sub(r"['']", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def shorten_titre(titre):
    """Titre court pour en-tête de page."""
    # Retire (1993), :, etc., garde 25 chars max
    short = re.sub(r"\s*\(\d{4}\)", "", titre)
    short = re.sub(r"[:—–].*$", "", short).strip()
    return short[:32]


def axe_court(axe):
    """Réduit l'axe culturel à 2-3 mots pour les pills."""
    if not axe:
        return ""
    # Couper avant ' — ' ou ' - '
    return axe.split(" — ")[0].split(" - ")[0].split(",")[0].strip()[:24]


def autobuild_vocab(lexique_str):
    """Découpe le seq.lexique en entrées de table.
    L'enseignante pourra enrichir manuellement."""
    if not lexique_str:
        return [("(à compléter)", "", "(traduction à ajouter)")]
    items = [x.strip() for x in re.split(r"[,;]", lexique_str) if x.strip()]
    rows = []
    for it in items[:10]:
        # Heuristique : si « ... (xxx) », xxx = traduction
        m = re.match(r"^(.*?)\s*\((.+)\)\s*$", it)
        if m:
            en, fr = m.group(1).strip(), m.group(2).strip()
        else:
            en, fr = it, "—"
        rows.append((en, "", fr))
    return rows


def autobuild_questions(theme):
    """Questions de compréhension génériques."""
    return [
        f"What is the main topic of this document?",
        f"Quote two key elements about the theme « {theme} ».",
        f"What is the author's tone / point of view?",
        f"What new word(s) did you discover in this text?",
    ]


def autobuild_intro_lines(seq, niveau_label):
    return [
        f"Cette fiche t'accompagne dans la séquence",
        f"« {seq['titre'][:50]} » ({niveau_label}).",
        f"Tu y trouveras le lexique, les faits de langue,",
        f"un document support et la tâche finale à préparer.",
    ]


def strip_html(s):
    """Retire les balises HTML pour usage dans titres ou tags simples."""
    if not s:
        return ""
    return re.sub(r"<[^>]+>", "", s)


def autobuild_grammar(seq):
    langue_clean = strip_html(seq.get("langue", "Faits de langue de la séquence"))
    return {
        "titre": langue_clean[:60],
        "intro": (
            "Cette séquence mobilise les structures suivantes : "
            f"<i>{langue_clean}</i>. "
            "Manipule-les en contexte ci-dessous."
        ),
        "examples": [
            "Exemple à compléter par l'enseignante en classe.",
            "Trace écrite construite collectivement après les activités.",
        ],
        "exo": (
            "<b>À toi !</b> En t'appuyant sur le document support, "
            "rédige 3 phrases qui mobilisent les structures de la séquence."
        ),
    }


def auto_fill_ctx(niveau_key, seq):
    """Crée un ctx complet à partir des données de progression."""
    info = NIVEAU_INFO[niveau_key]
    slug_seq = slugify(seq["titre"])
    grammar = autobuild_grammar(seq)
    quiz_url = f"{BASE_URL}/sequences/{info['slug_dir']}/{slug_seq}.html"

    # Filename : niveau + slug séquence
    safe_dir = info["slug_dir"].replace("-", "_")
    filename = f"fiche_{safe_dir}_{slug_seq.replace('-', '_')}.pdf"

    tache_clean = strip_html(seq.get("tache", "Tâche finale à préciser"))
    theme_clean = strip_html(seq.get("theme", ""))

    return {
        "filename": filename,
        "titre": seq["titre"],
        "titre_court": shorten_titre(seq["titre"]),
        "theme": theme_clean,
        "classe_label": info["label"],
        "cecrl": seq.get("cecrl", ""),
        "periode": seq.get("periode", ""),
        "nb_seances": "6 à 8 séances",
        "axe_court": axe_court(seq.get("axe", "")),
        "intro_lines": autobuild_intro_lines(seq, info["label"]),
        "vocab": autobuild_vocab(strip_html(seq.get("lexique", ""))),
        "doc_titre": f"Read — {theme_clean[:50] or seq['titre'][:50]}",
        "doc_text": (
            "<i>(Document support à fournir par l'enseignante. "
            "Cet emplacement accueillera un texte court, un dialogue, "
            "un extrait audio transcrit ou une image légendée en "
            "lien avec le thème de la séquence.)</i>"
        ),
        "questions": autobuild_questions(theme_clean),
        "grammar_titre": grammar["titre"],
        "grammar_intro": grammar["intro"],
        "grammar_examples": grammar["examples"],
        "grammar_exo": grammar["exo"],
        "production_consigne": (
            f"<b>Production guidée.</b> En 80-100 mots, prépare un "
            f"premier jet en lien avec la tâche finale : "
            f"<i>{tache_clean}</i>."
        ),
        "tache_consigne": tache_clean,
        "tache_criteres": [
            "<b>Recevabilité linguistique</b> — correction, prononciation",
            "<b>Cohérence</b> — structure, organisation des idées",
            "<b>Lexique</b> — mobilisation du vocabulaire de la séquence",
            "<b>Faits de langue</b> — structures de la séquence utilisées",
        ],
        "citation": None,
        "citation_auteur": None,
        "pour_aller_plus_loin": [
            f"Bibliothèque PDF du LFT — autres fiches du niveau {info['label']}",
            f"Activité interactive en ligne synchronisée (cf. QR code)",
            f"Eduscol — programmes officiels d'anglais",
        ],
        "quiz_url": quiz_url,
    }


# Index des séquences déjà couvertes par un override (par titre)
OVERRIDES_BY_TITRE = {f["titre"]: f for f in FICHES}


def build_all():
    """Génère 1 PDF par séquence définie dans progression.json.
    Utilise les overrides FICHES pour les 3 séquences vitrines."""
    with open(PROGRESSION_PATH, "r", encoding="utf-8") as f:
        prog = json.load(f)

    total = 0
    for niveau_key, niveau_data in prog.items():
        if niveau_key not in NIVEAU_INFO:
            continue
        for seq in niveau_data["sequences"]:
            ctx = OVERRIDES_BY_TITRE.get(seq["titre"]) or auto_fill_ctx(niveau_key, seq)
            build_fiche(ctx)
            total += 1
    print(f"\nTerminé : {total} fiche(s) générée(s).")


# ============================================================
#   ENTRY POINT
# ============================================================
def main():
    print("Phase B+ — génération des 40 fiches au format manuel...")
    build_all()


if __name__ == "__main__":
    main()

import io
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer



def _escape_html(text):
    """Escape characters that would break ReportLab's mini-HTML markup."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _inline_markdown(text):
    """Convert simple **bold** markdown into ReportLab <b> tags."""
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)


def generate_recommendation_pdf(crop, disease, confidence, treatment_advice):
    """
    Build a PDF report that contains ONLY the AI-generated treatment
    recommendation (plus a small header with crop/disease for context).
    Returns a BytesIO buffer ready to be used with st.download_button.
    """

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        topMargin=0.8 * inch,
        bottomMargin=0.8 * inch,
        leftMargin=0.8 * inch,
        rightMargin=0.8 * inch,
    )

    styles = getSampleStyleSheet()
    bullet_style = ParagraphStyle(
        "BulletStyle",
        parent=styles["Normal"],
        leftIndent=16,
        spaceAfter=4,
    )
    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["Normal"],
        spaceAfter=6,
    )

    story = []

    story.append(Paragraph("🌿 Flora - AI Plant Treatment Report", styles["Title"]))
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"<b>Crop:</b> {_escape_html(crop)}", body_style))
    story.append(Paragraph(f"<b>Diagnosed Disease:</b> {_escape_html(disease)}", body_style))
    if confidence:
        story.append(Paragraph(f"<b>Confidence:</b> {confidence:.2f}%", body_style))

    story.append(Spacer(1, 14))
    story.append(Paragraph("AI Treatment Recommendation", styles["Heading2"]))
    story.append(Spacer(1, 6))

    # The AI recommendation is plain markdown text, so convert the common
    # markdown constructs (#, ##, ###, -, **bold**) into PDF-friendly output.
    for raw_line in (treatment_advice or "").split("\n"):
        line = raw_line.strip()

        if not line:
            story.append(Spacer(1, 6))
            continue

        if set(line) <= {"-", "—", "="}:
            continue

        if line.startswith("### "):
            story.append(Paragraph(_escape_html(line[4:]), styles["Heading3"]))
        elif line.startswith("## "):
            story.append(Paragraph(_escape_html(line[3:]), styles["Heading2"]))
        elif line.startswith("# "):
            story.append(Paragraph(_escape_html(line[2:]), styles["Heading1"]))
        elif line.startswith("- ") or line.startswith("* "):
            story.append(Paragraph("• " + _inline_markdown(_escape_html(line[2:])), bullet_style))
        else:
            story.append(Paragraph(_inline_markdown(_escape_html(line)), body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer
from PyPDF2 import PdfWriter, PdfReader
import io
import os

from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A4

from reportlab.pdfbase import pdfmetrics 
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont 
from config import *

pdfmetrics.registerFont(TTFont('Calibri', os.path.join(ASSETS_DIR, 'calibri-bold.ttf')))

def make_pdf(form_dict, index):
    packet = io.BytesIO()
    canvas = Canvas(packet, pagesize=A4)
    canvas.translate(0, A4[1])

    canvas.setFont("Calibri", 12)

    for field, positions in FIELDS.items():
        if len(positions) > 1:
            address = form_dict[field]
            if len(address) < FIRST_BOUND:
                canvas.drawString(positions[0][0] * inch + SPACING[0], -positions[0][1] * inch + SPACING[1], address)
            elif len(address) < SECOND_BOUND:
                canvas.drawString(positions[0][0] * inch + SPACING[0], -positions[0][1] * inch + SPACING[1], address[:FIRST_BOUND])
                canvas.drawString(positions[1][0] * inch + SPACING[0], -positions[1][1] * inch + SPACING[1], address[FIRST_BOUND:])
            else:
                canvas.drawString(positions[0][0] * inch + SPACING[0], -positions[0][1] * inch + SPACING[1], address[:FIRST_BOUND])
                canvas.drawString(positions[1][0] * inch + SPACING[0], -positions[1][1] * inch + SPACING[1], address[FIRST_BOUND:SECOND_BOUND])
                canvas.drawString(positions[2][0] * inch + SPACING[0], -positions[2][1] * inch + SPACING[1], address[SECOND_BOUND:])
        else:
            gender_offset = 0
            if field == "Gender" and form_dict[field] == "(Male)":
                gender_offset += 0.15
            canvas.drawString((positions[0][0] + gender_offset) * inch + SPACING[0], -positions[0][1] * inch + SPACING[1], form_dict[field])

    canvas.save()

    new_pdf = PdfReader(packet)
    existing_pdf = PdfReader(os.path.join(ASSETS_DIR, "template.pdf"))

    output = PdfWriter()

    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)

    output_stream = open(os.path.join(OUTPUT_DIR, f"{index}.pdf"), "wb")
    output.write(output_stream)

    packet.close()
    output_stream.close()

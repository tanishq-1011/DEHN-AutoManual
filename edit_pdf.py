import fitz  # PyMuPDF
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()

pdf_path = os.getenv("DOCUMENT_EDIT_TARGET_PATH")
pptx_output_path = os.getenv("EDITED_DOCUMENT_PATH_PPTX")

# Slide size in inches (A4 landscape, you can adjust if you want)
SLIDE_WIDTH_IN = 11.69
SLIDE_HEIGHT_IN = 8.27

doc = fitz.open(pdf_path)
prs = Presentation()
prs.slide_width = Inches(SLIDE_WIDTH_IN)
prs.slide_height = Inches(SLIDE_HEIGHT_IN)

def pdf_to_ppt_coords(x0, y0, x1, y1, page_rect):
    """Convert PDF coords to PPTX coords in inches using actual page rect."""
    page_width = page_rect.width
    page_height = page_rect.height
    # Adjust coordinates relative to page rect origin (x0,y0)
    ppt_x0 = (x0 - page_rect.x0) / page_width * SLIDE_WIDTH_IN
    # Flip y axis because PDF origin bottom-left, PPTX origin top-left
    ppt_y0 = (page_height - (y1 - page_rect.y0)) / page_height * SLIDE_HEIGHT_IN
    ppt_w = (x1 - x0) / page_width * SLIDE_WIDTH_IN
    ppt_h = (y1 - y0) / page_height * SLIDE_HEIGHT_IN
    return ppt_x0, ppt_y0, ppt_w, ppt_h

for page_index, page in enumerate(doc):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # Blank slide
    page_rect = page.rect

    # Extract text blocks: (x0,y0,x1,y1,text)
    text_blocks = [
        (b[0], b[1], b[2], b[3], b[4])
        for b in page.get_text("blocks")
        if b[4].strip()
    ]

    # Add text boxes
    for x0, y0, x1, y1, text in text_blocks:
        left_in, top_in, width_in, height_in = pdf_to_ppt_coords(x0, y0, x1, y1, page_rect)
        textbox = slide.shapes.add_textbox(Inches(left_in), Inches(top_in), Inches(width_in), Inches(height_in))
        tf = textbox.text_frame
        tf.clear()
        tf.margin_top = 0
        tf.margin_bottom = 0
        tf.margin_left = 0
        tf.margin_right = 0
        tf.word_wrap = True

        p = tf.paragraphs[0]
        p.text = text.strip()

        box_height_pt = height_in * 72
        line_count = text.strip().count("\n") + 1
        scale_factor = 0.45 if line_count == 1 else 0.35
        font_pt = max(6, min(40, int(box_height_pt * scale_factor)))

        for run in p.runs:
            run.font.size = Pt(font_pt)
            run.font.color.rgb = RGBColor(0, 0, 0)

        textbox.line.color.rgb = RGBColor(255, 0, 0)

    # Extract and add images
    page_dict = page.get_text("dict")
    images_placed = 0
    for block in page_dict["blocks"]:
        if "image" in block:
            x0, y0, x1, y1 = block["bbox"]
            left_in, top_in, width_in, height_in = pdf_to_ppt_coords(x0, y0, x1, y1, page_rect)

            # Extract image by xref
            xref = block["image"]
            pix = fitz.Pixmap(doc, xref)
            if pix.n - pix.alpha < 4:  # can be saved as PNG directly
                img_bytes = pix.tobytes("png")
            else:  # CMYK: convert to RGB first
                pix = fitz.Pixmap(fitz.csRGB, pix)
                img_bytes = pix.tobytes("png")
            pix = None

            slide.shapes.add_picture(BytesIO(img_bytes), Inches(left_in), Inches(top_in), Inches(width_in), Inches(height_in))
            images_placed += 1

print(f"Placed {images_placed} images on page {page_index + 1}")

prs.save(pptx_output_path)
print(f"PPTX saved to: {pptx_output_path}")

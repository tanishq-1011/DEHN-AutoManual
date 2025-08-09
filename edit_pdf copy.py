import fitz
import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image
import io

load_dotenv()

pdf_path = os.getenv("DOCUMENT_EDIT_TARGET_PATH")
output_path = os.getenv("EDITED_DOCUMENT_PATH")

# Step 1: Extract PDF page as image + bounding boxes
doc = fitz.open(pdf_path)
page = doc[0]  # just first page for demo

blocks = page.get_text("blocks")
bbox_texts = []
for block in blocks:
    x0, y0, x1, y1, text, *_ = block
    if text.strip():
        bbox_texts.append({
            "rect": (x0, y0, x1, y1),
            "original": text.strip()
        })

# Render PDF page as image
pix = page.get_pixmap()
img = Image.open(io.BytesIO(pix.tobytes("png")))

# Step 2: UI
st.title("Edit generated PDF")
st.image(img, caption="Page Preview")

updated_texts = []
for i, item in enumerate(bbox_texts):
    new_text = st.text_area(
        f"Block {i+1} ({item['rect']})",
        value=item['original'],
        height=80
    )
    updated_texts.append((item["rect"], new_text))

# Step 3: Save
if st.button("Save PDF"):
    for rect, text in updated_texts:
        page.add_redact_annot(fitz.Rect(rect), fill=(1, 1, 1))
    page.apply_redactions()

    for rect, text in updated_texts:
        # page.insert_textbox(fitz.Rect(rect), text, fontsize=6, fontname="helv", align=0)
        x0, y0, x1, y1 = rect
        page.insert_text((x0, y0), text, fontsize=6, fontname="helv")

    doc.save(output_path)
    st.success(f"PDF saved to {output_path}")

import fitz  # PyMuPDF
import deepl
from dotenv import load_dotenv
import os
import re

load_dotenv()

pdf_path = os.getenv("DOCUMENT_PATH")
output_path = os.getenv("TRANSLATED_DOCUMENT_PATH")
auth_key = os.getenv("DEEPL_KEY")
translator = deepl.Translator(auth_key)

doc = fitz.open(pdf_path)

for page in doc:
    blocks = page.get_text("blocks")  # [(x0, y0, x1, y1, text, block_no, type), ...]
    for block in blocks:
        x0, y0, x1, y1, text, *_ = block
        if text.strip():
            result = translator.translate_text(text, target_lang="EN-GB")
            page.add_redact_annot(fitz.Rect(x0, y0, x1, y1), fill=(1,1,1))
            page.apply_redactions()
            page.insert_text((x0, y0), result.text, fontsize=6, fontname="helv")
            print(f"Translated text: {result.text}")
            # print(f"Original text: {text.strip()}")

doc.save(output_path)

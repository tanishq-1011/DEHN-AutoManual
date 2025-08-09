import sys
import fitz  # PyMuPDF
import deepl
import os
from dotenv import load_dotenv
from PyQt6.QtWidgets import (
    QApplication, QGraphicsScene, QGraphicsView,
    QGraphicsPixmapItem, QTextEdit, QPushButton, QVBoxLayout, QWidget
)
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import QRectF, Qt
from PIL import Image
import io

load_dotenv()

app = QApplication(sys.argv)

pdf_path = os.getenv("DOCUMENT_PATH")
output_path = os.getenv("TRANSLATED_DOCUMENT_PATH")
auth_key = os.getenv("DEEPL_KEY")
translator = deepl.Translator(auth_key)

doc = fitz.open(pdf_path)
page = doc[0]  # demo on first page only

# Get page image
pix = page.get_pixmap(dpi=150)
img = Image.open(io.BytesIO(pix.tobytes("png")))
qimg = QImage(img.tobytes(), img.width, img.height, QImage.Format.Format_RGB888)
pixmap = QPixmap.fromImage(qimg)

# Extract bounding boxes and translations
blocks = page.get_text("blocks")
bbox_texts = []
for block in blocks:
    x0, y0, x1, y1, text, *_ = block
    if text.strip():
        translated = translator.translate_text(text, target_lang="EN-GB").text
        bbox_texts.append(((x0, y0, x1, y1), translated))


class PDFEditor(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Direct PDF Translation Editor")
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)

        # Add PDF image as background
        self.scene.addItem(QGraphicsPixmapItem(pixmap))

        # Create editable text boxes for each bounding box
        self.text_edits = []
        for rect, text in bbox_texts:
            x0, y0, x1, y1 = rect
            width = x1 - x0
            height = y1 - y0

            editor = QTextEdit()
            editor.setPlainText(text)
            editor.setGeometry(int(x0), int(y0), int(width), int(height))
            editor.setStyleSheet("background-color: rgba(255,255,255,180); font-size:10pt;")
            editor.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            editor.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.scene.addWidget(editor)
            self.text_edits.append((rect, editor))

        # Save button
        self.save_button = QPushButton("Save PDF")
        self.save_button.clicked.connect(self.save_pdf)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(self.save_button)
        self.setLayout(layout)

    def save_pdf(self):
        for rect, editor in self.text_edits:
            x0, y0, x1, y1 = rect
            text = editor.toPlainText()

            page.add_redact_annot(fitz.Rect(rect), fill=(1, 1, 1))
        page.apply_redactions()

        for rect, editor in self.text_edits:
            text = editor.toPlainText()
            page.insert_textbox(fitz.Rect(rect), text, fontsize=6, fontname="helv", align=0)

        doc.save(output_path)
        print(f"PDF saved to {output_path}")


# app = QApplication(sys.argv)
window = PDFEditor()
window.show()
sys.exit(app.exec())

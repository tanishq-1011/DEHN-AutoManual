# DEHN Product User-Manual Generator

This project is a web application for generating user manuals (PDF) for DEHN products using product data in JSON format. It leverages OpenAI (via OpenRouter) for language translation and ReportLab for PDF creation, with a modern UI built using Streamlit.

## Features
- **Upload Product Data**: Upload a JSON file containing product information and user tasks.
- **Automatic Translation**: User tasks are translated (e.g., to German) using an LLM API.
- **PDF Generation**: Generates a user manual PDF with product image, tasks in multiple languages, and a DEHN watermark.
- **Modern UI**: Clean, branded interface with custom styles and download button.

## How It Works
1. **Upload** a product JSON file via the web interface.
2. **Click** the "Generate User-Manual" button.
3. The app:
   - Reads the product data
   - Translates user tasks
   - Generates a PDF with the product image and tasks in English and German
   - Adds a watermark for confidentiality
4. **Download** the generated PDF.

## File Structure
- `app.py` — Streamlit web app for UI and workflow
- `make_pdf.py` — PDF generation and translation logic
- `capacitor_data.json` — Example product data (JSON)
- `image.jpg` — Example product image
- `output.pdf` — Example output PDF
- `utils.py` — (Optional) Utility functions

## Requirements
- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [ReportLab](https://www.reportlab.com/)
- [OpenAI Python SDK](https://github.com/openai/openai-python)

Install dependencies:
```bash
pip install streamlit reportlab openai
```

## Usage
1. Place your product image as `image.jpg` in the project folder.
2. Prepare your product data as a JSON file (see `capacitor_data.json` for format).
3. Run the app:
   ```bash
   streamlit run app.py
   ```
4. Use the web UI to upload your JSON and generate the PDF.

## JSON Format Example
```json
{
  "product_id": "CAP-EL-2200uF-16V-RBC",
  "user_tasks": [
    "Install the capacitor according to the circuit diagram.",
    "Ensure the voltage does not exceed 16V."
  ]
}
```

## Notes
- The app uses OpenRouter for LLM translation. You must provide a valid API key in `make_pdf.py`.
- The output PDF is named `<product_id>_user-manual.pdf`.
- The watermark and styles are DEHN-branded.

## License
This project is for demonstration and internal use only. Not for commercial distribution.

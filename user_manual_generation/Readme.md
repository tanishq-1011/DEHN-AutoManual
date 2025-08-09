
# ⚡️📕 DEHN Product User-Manual Generator 🚀

Welcome to the **DEHN Product User-Manual Generator**! This web app lets you instantly create beautiful, branded user manuals (PDF) for DEHN products — just upload your product data and go! 🛠️✨

> **Sample data and image are already included in this repo!**
> - `capacitor_data.json` (sample product data)
> - `image.jpg` (sample product image)

It uses OpenAI (via OpenRouter) for smart language translation and ReportLab for stunning PDF creation, all wrapped in a modern, interactive Streamlit UI.


## ✨ Features
- 📤 **Upload Product Data**: Upload a JSON file with product info and user tasks.
- 🌍 **Automatic Translation**: Instantly translate user tasks (e.g., to German) using an LLM API.
- 🖨️ **PDF Generation**: Get a user manual PDF with product image, tasks in multiple languages, and a DEHN watermark.
- 🎨 **Modern UI**: Clean, branded interface with custom styles and a big download button.


## 🚦 How It Works
1. **Upload** a product JSON file (or use the included `capacitor_data.json`) via the web interface.
2. **Click** the "🛠️ Generate User-Manual" button.
3. The app will:
   - 🧠 Read the product data
   - 🌐 Translate user tasks
   - 🖼️ Add the product image (use your own or the included `image.jpg`)
   - 📄 Generate a PDF with tasks in English and German
   - 🔒 Add a DEHN Confidential watermark
4. **Download** your shiny new PDF!


## 📁 File Structure
- `app.py` — Streamlit web app for UI and workflow
- `make_pdf.py` — PDF generation and translation logic
- `capacitor_data.json` — **Sample product data** (ready to use!)
- `image.jpg` — **Sample product image** (ready to use!)
- `output.pdf` — Example output PDF
- `utils.py` — (Optional) Utility functions


## 🧰 Requirements
- Python 3.8+
- [Streamlit](https://streamlit.io/)
- [ReportLab](https://www.reportlab.com/)
- [OpenAI Python SDK](https://github.com/openai/openai-python)

Install everything in one go:
```bash
pip install streamlit reportlab openai
```


## 🚀 Usage
1. Use the included `image.jpg` and `capacitor_data.json` for instant results, or add your own!
2. Run the app:
   ```bash
   streamlit run app.py
   ```
3. Use the web UI to upload your JSON and generate the PDF. That's it!


## 📝 JSON Format Example
```json
{
  "product_id": "CAP-EL-2200uF-16V-RBC",
  "user_tasks": [
    "Install the capacitor according to the circuit diagram.",
    "Ensure the voltage does not exceed 16V."
  ]
}
```


## ℹ️ Notes
- 🤖 The app uses OpenRouter for LLM translation. You must provide a valid API key in `make_pdf.py`.
- 📄 The output PDF is named `<product_id>_user-manual.pdf`.
- 🛡️ The watermark and styles are DEHN-branded.


## 📜 License
This project is for demonstration and internal use only. Not for commercial distribution.

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from openai import OpenAI
import json


open_router_key = ""
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=open_router_key,  # Replace with your OpenRouter API key
)


#convert to JSON
def get_product_data(json_path):
    with open(json_path, 'r') as file:
        data = json.load(file)
    return data

def get_llm_response(prompt):
    completion = client.chat.completions.create(
        extra_headers={},
        extra_body={},
        model="z-ai/glm-4.5-air:free", #"google/gemma-3n-e2b-it:free",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return completion.choices[0].message.content


#run get_llm_response paralley for 5 times
def run_parallel_requests(product_tasks, language):
    from concurrent.futures import ThreadPoolExecutor, as_completed
    num_requests = len(language)
    responses = []
    with ThreadPoolExecutor(max_workers=num_requests) as executor:
        prompts = [f"Translate the following text to {lang}: {product_tasks}. return the answer in <answer> </answer> tags" for lang in language]
        futures = [executor.submit(get_llm_response, prompt) for prompt in prompts]
        for future in as_completed(futures):
            responses.append(future.result())
    return responses




def create_pdf(image_path, strings, product_id):
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import Color

    styles = getSampleStyleSheet()
    style_normal = styles["Normal"]

    # Custom centered title style
    style_title = ParagraphStyle(
        "Title",
        parent=styles["Heading1"],
        alignment=1,  # 0=left, 1=center, 2=right
        fontSize=16,
        spaceAfter=12
    )

    output_pdf = product_id + "_user-manual.pdf"
    doc = SimpleDocTemplate(output_pdf, pagesize=A4)
    story = []

    # Title row (centered)
    title_text = f"Product: {product_id}"
    story.append(Paragraph(title_text, style_title))
    story.append(Spacer(1, 0.2 * inch))

    # Image row
    img = Image(image_path, width=4 * inch, height=3 * inch)
    story.append(img)
    story.append(Spacer(1, 0.5 * inch))

    # Two columns row
    para1 = Paragraph(strings[0].replace("\n", "<br/>"), style_normal)
    para2 = Paragraph(strings[1].replace("\n", "<br/>"), style_normal)

    table_data = [[para1, para2]]

    table = Table(table_data, colWidths=[(A4[0] - 2 * inch) / 2] * 2)
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
    ]))

    story.append(table)

    # Watermark function
    def add_watermark(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica-Bold", 48)
        canvas.setFillColor(Color(0.89, 0, 0.043, alpha=0.08))  # DEHN red, very transparent
        canvas.translate(A4[0]/2, A4[1]/2)
        canvas.rotate(30)
        canvas.drawCentredString(0, 0, "DEHN Confidential")
        canvas.restoreState()

    doc.build(story, onFirstPage=add_watermark, onLaterPages=add_watermark)
    print("PDF saved as", output_pdf)


def main(json_path):
    #json_path = "capacitor_data.json"  # Replace with your JSON file path
    product_data = get_product_data(json_path)
    product_img_path = "image.jpg"
    product_tasks = "\n".join(product_data['user_tasks']) 
    translates = []
    languages = ["german"]
    translates = run_parallel_requests(product_tasks,languages)
    all_language_tasks = []
    all_language_tasks.append(product_tasks)
    all_language_tasks.extend(translates)
    all_language_tasks[0] = "EN\n" + all_language_tasks[0]
    all_language_tasks[1] = "DE\n" + all_language_tasks[1]

    create_pdf(product_img_path, all_language_tasks, product_data['product_id'])


import os
import json
import requests
from dotenv import load_dotenv

def generate_json_from_md():
    # Load environment variables
    load_dotenv()

    groq_key = os.getenv("GROQ_KEY")
    groq_model = os.getenv("GROQ_MODEL")
    md_path = os.getenv("MD_PATH")
    json_output_path = os.getenv("JSON_OUTPUT_PATH")

    if not groq_key:
        raise ValueError("GROQ_KEY not found in .env file.")
    if not groq_model:
        raise ValueError("GROQ_MODEL not found in .env file.")
    if not md_path:
        raise ValueError("MD_PATH not found in .env file.")
    if not json_output_path:
        raise ValueError("JSON_OUTPUT_PATH not found in .env file.")

    # Read markdown content
    with open(md_path.strip('"'), "r", encoding="utf-8") as f:
        md_content = f.read()

    # System prompt to transform into JSON
    system_prompt = (
        "You are a helpful assistant that converts Markdown technical documentation into JSON. "
        "The JSON should be an array of objects. "
        "Each object should have: "
        "id (incremental starting from 1), title (string from heading), and content (string with section text). "
        "Preserve all section content exactly, without changing language or meaning. "
        "Remove markdown formatting but keep plain text. "
        "Do not add any fields that are not requested. "
        "Output only valid JSON, no extra text."
    )

    # Prepare Groq API request
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {groq_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": groq_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Convert the following Markdown to JSON:\n\n{md_content}"}
        ],
        "temperature": 0
    }

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    result = response.json()
    json_text = result["choices"][0]["message"]["content"]

    # Parse JSON to ensure validity
    try:
        json_data = json.loads(json_text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Model returned invalid JSON: {e}\nOutput was:\n{json_text}")

    # Save JSON to file
    with open(json_output_path.strip('"'), "w", encoding="utf-8") as f:
        json.dump(json_data, f, ensure_ascii=False, indent=2)

    print(f"JSON saved to {json_output_path.strip('"')}")

if __name__ == "__main__":
    generate_json_from_md()

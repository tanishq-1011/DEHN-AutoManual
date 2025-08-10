import os
from dotenv import load_dotenv
from markitdown import MarkItDown

def convert_pdf_to_markdown(pdf_path, output_path):
    """
    Convert a PDF file to Markdown format.
    
    :param pdf_path: Path to the input PDF file.
    :param output_path: Path to save the output Markdown file.
    """
    try:
        md = MarkItDown(enable_plugins=False) # Set to True to enable plugins
        result = md.convert(pdf_path)
        # Save the markdown content to the output file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result.text_content)
        print(f"Markdown saved to {output_path}")
    except ImportError:
        print("markitdown is not installed. Please install it using 'pip install markitdown'.")

if __name__ == "__main__":
    # Load variables from .env file
    load_dotenv()

    # Get DOCUMENT_PATH value
    document_path = os.getenv("DOCUMENT_PATH")

    if document_path is None:
        raise ValueError("DOCUMENT_PATH not found in .env file.")

    print(f"DOCUMENT_PATH: {document_path}")
    output_path = document_path.replace('.pdf', '.md')
    convert_pdf_to_markdown(document_path, output_path)
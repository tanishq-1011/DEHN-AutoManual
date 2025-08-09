import streamlit as st
import os
from make_pdf import main

# Brand colors
DEHN_RED = "#E3000B"
DEHN_DARK_GREY = "#1F1F1E"
DEHN_WHITE = "#FFFFFF"
DEHN_DARKER_RED = "#A4130E"

def save_uploaded_file(uploaded_file):
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return uploaded_file.name

# Global style overrides for text & headings
st.markdown(
    f"""
    <style>
    /* Global text styles */
    body, .block-container {{
        color: {DEHN_DARK_GREY};
        font-family: "Arial", sans-serif;
    }}
    h1, h2, h3, h4, h5, h6 {{
        color: {DEHN_RED};
        font-weight: bold;
    }}
    label, .stTextInput>div>div>input, .stFileUploader label {{
        color: {DEHN_DARK_GREY} !important;
        font-weight: 500;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Custom DEHN heading
st.markdown(f"""
<h1 style='color: {DEHN_DARK_GREY}; font-weight: bold; text-align: center; margin-bottom: 1.5rem;'>
<span style='font-size:2.2rem; vertical-align:middle;'>📕</span> USER MANUAL GENERATOR FOR DEHN PRODUCTS <span style='font-size:2.2rem; vertical-align:middle;'>⚡</span>
</h1>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("Choose Product Information File", type=["json"])

if uploaded_file is not None:
    json_path = save_uploaded_file(uploaded_file)
    
    # Center button
    col1, col2, col3 = st.columns([2, 4, 2])
    with col2:
        generate_clicked = st.button(
            "🛠️ Generate User-Manual",
            key="generate_manual_btn",
            help="Generate the user manual PDF.",
            use_container_width=True
        )

        # Button style
        st.markdown(
            f"""
            <style>
            #generate_manual_btn {{
                background-color: {DEHN_WHITE};
                color: {DEHN_RED};
                border: 2px solid {DEHN_RED};
                border-radius: 30px;
                font-size: 1em;
                font-weight: 500;
                width: 100%;
                min-width: 220px;
                max-width: 400px;
                height: 38px;
                margin: 0 auto 10px auto;
                display: block;
                box-shadow: none;
                transition: background 0.2s, color 0.2s;
            }}
            #generate_manual_btn:hover {{
                background-color: {DEHN_RED};
                color: {DEHN_WHITE};
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

    if 'generate_clicked' not in locals():
        generate_clicked = False

    if generate_clicked:
        spinner_placeholder = st.empty()

        # Spinner with lightning bolt in center
        spinner_html = f'''
        <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 240px;">
            <div style="position: relative; width: 96px; height: 96px;">
                <!-- Outer ring -->
                <div style="border: 12.8px solid #e0e0e0; border-top: 12.8px solid {DEHN_RED};
                            border-right: 12.8px solid #888888; border-bottom: 12.8px solid {DEHN_RED};
                            border-left: 12.8px solid #888888;
                            border-radius: 50%; width: 96px; height: 96px;
                            animation: spin 1s linear infinite;">
                </div>
                <!-- Center icon -->
                <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);
                            font-size: 2rem; color: {DEHN_RED}; animation: pulse 1s infinite;">
                    ⚡
                </div>
                <!-- If you want DEHN logo instead of ⚡, replace above div with this:
                <img src="https://www.dehn.de/sites/default/files/2020-05/dehn-logo.png"
                     style="position:absolute; top:50%; left:50%; transform:translate(-50%, -50%);
                            width:48px; height:auto;" /> -->
            </div>
            <div style="margin-top: 24px; color: {DEHN_DARK_GREY}; font-size: 1.2em; font-weight: bold;">
                Generating User-Manual, please wait...
            </div>
        </div>
        <style>
        @keyframes spin {{
          0% {{ transform: rotate(0deg); }}
          100% {{ transform: rotate(360deg); }}
        }}
        @keyframes pulse {{
          0%, 100% {{ transform: translate(-50%, -50%) scale(1); }}
          50% {{ transform: translate(-50%, -50%) scale(1.2); }}
        }}
        </style>
        '''
        spinner_placeholder.markdown(spinner_html, unsafe_allow_html=True)

        # Generate PDF
        main(json_path)
        spinner_placeholder.empty()

        pdf_name = "CAP-EL-2200uF-16V-RBC_user-manual.pdf"
        if os.path.exists(pdf_name):
            # Download button
            st.markdown(
                f"""
                <style>
                .stDownloadButton>button {{
                    background-color: {DEHN_RED} !important;
                    color: {DEHN_WHITE} !important;
                    font-size: 1.3em !important;
                    font-weight: bold !important;
                    border-radius: 16px !important;
                    padding: 18px 48px !important;
                    min-width: 300px;
                    min-height: 60px;
                    box-shadow: 0 4px 16px rgba(227,0,11,0.15);
                    border: none;
                    display: block;
                    margin: 0 auto;
                }}
                .stDownloadButton>button:hover {{
                    background-color: {DEHN_DARKER_RED} !important;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

            st.markdown("<div style='display: flex; justify-content: center; margin-top: 30px;'>", unsafe_allow_html=True)
            with open(pdf_name, "rb") as f:
                st.download_button(
                    label="⬇️ Download User-Manual",
                    data=f,
                    file_name=pdf_name,
                    mime="application/pdf"
                )
            st.markdown("</div>", unsafe_allow_html=True)
            st.success("User manual generated successfully!")
        else:
            st.error("PDF was not generated.")

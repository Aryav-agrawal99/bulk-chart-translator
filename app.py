import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import pytesseract
import io
import base64

st.set_page_config(page_title="Bulk Size Chart Translator", layout="wide")
st.title("📏 Bulk Size Chart Translator (Chinese to English)")

uploaded_files = st.file_uploader("Upload Size Chart Images (Chinese)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    for uploaded_file in uploaded_files:
        st.subheader(f"📷 Original Image: {uploaded_file.name}")
        image = Image.open(uploaded_file).convert('RGB')
        st.image(image, width=400)

        # Extract text
        extracted_text = pytesseract.image_to_string(image, lang='chi_sim')
        st.markdown("**🈶 Extracted Chinese Text:**")
        st.code(extracted_text)

        # Placeholder translation
        translated_text = "[Translation unavailable in this environment. Please translate manually.]"
        st.markdown("**🌐 Translated Text:**")
        st.code(translated_text)

        # Render translation on image
        new_img = Image.new('RGB', (image.width, image.height), color=(255, 255, 255))
        draw = ImageDraw.Draw(new_img)
        font = ImageFont.load_default()
        draw.multiline_text((10, 10), translated_text, font=font, fill=(0, 0, 0))

        st.markdown("**🖼️ Translated Image:**")
        st.image(new_img, width=400)

        # JPEG Download
        buffered = io.BytesIO()
        new_img.save(buffered, format="JPEG")
        img_bytes = buffered.getvalue()
        b64 = base64.b64encode(img_bytes).decode()
        href = f'<a href="data:image/jpeg;base64,{b64}" download="translated_{uploaded_file.name}">📥 Download Translated Image (JPEG)</a>'
        st.markdown(href, unsafe_allow_html=True)

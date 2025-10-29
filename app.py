import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

st.set_page_config(page_title="Resim Üzerine Yazı Ekle", page_icon="🖋️", layout="centered")

st.title("🖋️ Resim Üzerine Yazı Ekleme Aracı")
st.write("Bir resim yükle, metni yaz ve 1080x1920 boyutunda ortalanmış sonucu al.")

def wrap_text_by_width(draw, text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + ("" if current_line == "" else " ") + word
        w = draw.textlength(test_line, font=font)
        if w <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)
    return "\n".join(lines)

uploaded_image = st.file_uploader("📸 Bir resim yükle", type=["jpg", "jpeg", "png"])
input_text = st.text_area("✏️ Yazılacak metni gir", height=150, placeholder="Metnini buraya yaz...")

if st.button("🖼️ Görseli Oluştur"):
    if not uploaded_image or not input_text:
        st.warning("⚠️ Lütfen hem resim yükleyip hem metin girin.")
    else:
        # 1080x1920 boyutunda yeni bir resim oluştur
        target_width = 1080
        target_height = 1920

        image = Image.open(uploaded_image).convert("RGBA")
        # Resmi hedef boyuta resize
        image = image.resize((target_width, target_height))

        txt_layer = Image.new("RGBA", image.size, (255,255,255,0))
        draw = ImageDraw.Draw(txt_layer)

        font = ImageFont.truetype("arial.ttf", 40)  # Sabit font boyutu
        max_width = image.width - 100

        wrapped_text = wrap_text_by_width(draw, input_text, font, max_width)
        bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font, spacing=10)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        # Resmin ortasında konum
        x = (image.width - text_w) / 2
        y = (image.height - text_h) / 2

        # Hafif koyu kutu
        draw.rectangle((x-20, y-10, x + text_w + 20, y + text_h + 10), fill=(0,0,0,128))

        # Yazıyı ekle
        draw.multiline_text((x, y), wrapped_text, font=font, fill=(255,255,255,255), spacing=10)

        combined = Image.alpha_composite(image, txt_layer).convert("RGB")

        # Görseli göster
        st.image(combined, caption="📷 1080x1920 Ortalanmış yazılı resim")

        # Kaydetme / indirme
        buf = io.BytesIO()
        combined.save(buf, format="JPEG")
        st.download_button(
            label="📥 Görseli indir",
            data=buf.getvalue(),
            file_name="sonuc_1080x1920.jpg",
            mime="image/jpeg"
        )
else:
    st.info("👆 Bir resim yükle, metni yaz ve ardından '🖼️ Görseli Oluştur' butonuna bas.")

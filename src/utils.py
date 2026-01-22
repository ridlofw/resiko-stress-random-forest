from PIL import Image, ImageDraw, ImageFont
import io
from datetime import datetime

def generate_certificate_image(name, result, proba_sehat, proba_stres, input_data):
    # Chart colors
    BG_COLOR = (240, 242, 246)
    HEADER_COLOR = (102, 126, 234)
    TEXT_COLOR = (38, 39, 48)
    CARD_BG = (255, 255, 255)
    SUCCESS_COLOR = (40, 167, 69)
    DANGER_COLOR = (220, 53, 69)
    
    # Create canvas (1200x800)
    img = Image.new('RGB', (1200, 800), color=BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Draw main card
    draw.rounded_rectangle([50, 50, 1150, 750], fill=CARD_BG, outline=HEADER_COLOR, width=5, radius=30)
    
    # Draw Header box
    draw.rounded_rectangle([50, 50, 1150, 150], fill=HEADER_COLOR, radius=30)
    
    # Try to load fonts
    try:
        title_font = ImageFont.truetype("arial.ttf", 45)
        name_font = ImageFont.truetype("arial.ttf", 35)
        label_font = ImageFont.truetype("arial.ttf", 25)
        result_font = ImageFont.truetype("arialbd.ttf", 60)
        footer_font = ImageFont.truetype("arial.ttf", 20)
    except:
        title_font = ImageFont.load_default()
        name_font = ImageFont.load_default()
        label_font = ImageFont.load_default()
        result_font = ImageFont.load_default()
        footer_font = ImageFont.load_default()

    # Draw Title
    draw.text((600, 100), "HASIL PREDIKSI RISIKO STRES", fill=(255, 255, 255), font=title_font, anchor="mm")
    
    # Student Info
    draw.text((100, 200), f"Nama Mahasiswa: {name.upper()}", fill=TEXT_COLOR, font=name_font)
    draw.line([100, 240, 600, 240], fill=HEADER_COLOR, width=2)
    
    # Result Box
    result_color = SUCCESS_COLOR if result == "Sehat" else DANGER_COLOR
    draw.text((600, 350), result.upper(), fill=result_color, font=result_font, anchor="mm")
    
    # Probability
    draw.text((300, 450), f"Probabilitas Sehat: {proba_sehat:.1f}%", fill=SUCCESS_COLOR, font=label_font, anchor="mm")
    draw.text((900, 450), f"Probabilitas Risiko Stres: {proba_stres:.1f}%", fill=DANGER_COLOR, font=label_font, anchor="mm")
    
    # Data summary
    draw.text((100, 520), "Ringkasan Data:", fill=TEXT_COLOR, font=label_font)
    y_pos = 560
    summary_text = [
        f"• Umur: {input_data['Umur']} Tahun",
        f"• IPK: {input_data['IPK']:.2f}",
        f"• Belajar: {input_data['Jam Belajar']} Jam/Hari",
        f"• Tidur: {input_data['Jam Tidur']} Jam/Hari",
        f"• Tugas: {input_data['Jumlah Tugas']} per Minggu"
    ]
    
    cols = [100, 400, 700]
    for idx, text in enumerate(summary_text):
        col_idx = idx % 3
        row_idx = idx // 3
        draw.text((cols[col_idx], y_pos + (row_idx * 40)), text, fill=TEXT_COLOR, font=label_font)

    # Footer
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    draw.text((600, 720), f"Digenerate otomatis oleh Sistem AI Prediksi Stres | {timestamp}", fill=(150, 150, 150), font=footer_font, anchor="mm")
    
    # Save to bytes
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    return byte_im


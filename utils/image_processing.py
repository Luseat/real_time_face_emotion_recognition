import cv2
import numpy as np
from PIL import Image
from io import BytesIO

def create_report_image(frame_rgb, details_text):
    """
    Menggabungkan gambar frame webcam dengan teks detail persentase emosi
    di sebelah kanannya untuk keperluan laporan (PNG/PDF).
    """
    h, w, _ = frame_rgb.shape
    canvas = np.ones((h, w + 300, 3), dtype=np.uint8) * 255
    canvas[:, :w] = frame_rgb
    
    y0 = 40
    cv2.putText(canvas, "Hasil Analisis Emosi:", (w + 20, y0), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)
    y0 += 40
    
    for line in details_text.split('\n'):
        if line.strip():
            clean_line = line.replace('**', '')
            cv2.putText(canvas, clean_line, (w + 20, y0), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
            y0 += 35
            
    return canvas

def get_download_bytes(img_array, file_format='PNG'):
    """
    Mengubah array NumPy gambar menjadi bytes untuk siap di-download via Streamlit.
    """
    img = Image.fromarray(img_array)
    buf = BytesIO()
    img.save(buf, format=file_format)
    return buf.getvalue()

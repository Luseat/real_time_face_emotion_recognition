import cv2
import numpy as np
from PIL import Image
from io import BytesIO
from deepface import DeepFace

def create_report_image(frame_rgb, details_text):
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
    img = Image.fromarray(img_array)
    buf = BytesIO()
    img.save(buf, format=file_format)
    return buf.getvalue()

def process_and_draw_face(frame):
    """
    Memproses frame secara mandiri (Dipakai oleh Upload Foto & Video)
    """
    data_semua_wajah = cari_muka_pake_AI(frame)
    if data_semua_wajah is not None:
        return gambar_kotak_hijau(frame, data_semua_wajah)
    else:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame_rgb, "Tidak ada wajah yang terdeteksi", None
    

def cari_muka_pake_AI(frame):
    """Fungsi 1: Nyari letak muka dan emosi untuk semua wajah di layar"""
    try:
        results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False, detector_backend='mtcnn')
        if isinstance(results, dict):
            results = [results]

        wajah_valid = []
        for face_info in results:
            if face_info['region']['w'] > 0 and face_info['region']['h'] > 0:
                wajah_valid.append(face_info) # Kumpulin semua muka
            
        if len(wajah_valid) > 0:
            return wajah_valid # Kirim semua muka
    except Exception as e:
        print(f"Error AI: {e}")
        
    return None

def gambar_kotak_hijau(frame, daftar_wajah): 
    """Fungsi 2: Gambar kotak dan ngatur teks UI (Beda buat 1 muka vs Banyak muka)"""
    details = ""
    emotions_dict_utama = None
    
    jumlah_wajah = len(daftar_wajah) # Berapa muka yang kedeteksi
    
    # Looping gambar kotak sebanyak muka yang ketemu
    for i, face_info in enumerate(daftar_wajah):
        emotions_dict = face_info['emotion']
    
        # Pake emosi Wajah ke-1 buat Grafik Line Chart
        if i == 0:
            emotions_dict_utama = emotions_dict
        
        if jumlah_wajah == 1:
            for em_name, em_score in emotions_dict.items():
                details += f"**{em_name.capitalize()}**: {em_score:.2f}%\n\n"
        else:
            details += f"### Wajah {i+1}\n" 
            for em_name, em_score in emotions_dict.items():
                details += f"**{em_name.capitalize()}**: {em_score:.2f}%  \n"
            details += "\n---\n\n"
            
            
        region = face_info['region']
        x,y,w,h = region['x'], region['y'], region['w'], region['h']
        
        emotion = face_info['dominant_emotion']
        score = face_info['emotion'][emotion]
        
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
        if jumlah_wajah == 1:
            text = f"{emotion}: {score:.1f}%"
        else:
            text = f"Wajah {i+1}: {emotion}"
        cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame_rgb, details, emotions_dict_utama
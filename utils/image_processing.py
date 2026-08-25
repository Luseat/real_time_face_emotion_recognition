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
    Memproses frame gambar (BGR), mendeteksi emosi, dan menggambar bounding box.
    Mengembalikan frame RGB, teks detail, dan dictionary emosi mentah.
    """
    details = "Tidak ada wajah terdeteksi."
    emotions_dict = None
    
    try:
        results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False, detector_backend='mtcnn')
        if isinstance(results, dict):
            results = [results]
            
        for face_info in results:
            region = face_info['region']
            x, y, w, h = region['x'], region['y'], region['w'], region['h']
            
            if w > 0 and h > 0:
                emotions_dict = face_info['emotion']
                
                details = ""
                for em_name, em_score in emotions_dict.items():
                    details += f"**{em_name.capitalize()}**: {em_score:.2f}%\n\n"
                    
                emotion = face_info['dominant_emotion']
                score = face_info['emotion'][emotion]
                
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                text = f"{emotion}: {score:.1f}%"
                cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                break 
                
    except Exception as e:
        print(f"Error dari DeepFace: {e}")
        
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame_rgb, details, emotions_dict

def cari_muka_pake_AI(frame):
    """Fungsi 1: Mikir pake AI, nyari data letak muka dan emosi"""
    try:
        results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False, detector_backend='mtcnn')
        if isinstance(results, dict):
            results = [results]
    
        for face_info in results:
            if face_info['region']['w']> 0 and face_info['region']['h']>0:
                return face_info
    except Exception as e:
        print(f"Error AI: {e}")
        
    return None

def gambar_kotak_hijau(frame, face_info):
    """Fungsi 2: Cuma nggambar kotak di atas foto pakai data simpanan"""
    emotions_dict = face_info['emotion']
    
    
    details = ""
    for em_name, em_score in emotions_dict.items():
        details += f"**{em_name.capitalize()}**: {em_score:.2f}%\n\n"
        
    
    region = face_info['region']
    x,y,w,h = region['x'], region['y'], region['w'], region['h']
    
    emotion = face_info['dominant_emotion']
    score = face_info['emotion'][emotion]
    
    cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)
    text = f"{emotion}: {score:.1f}%"
    cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
    
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    return frame_rgb, details, emotions_dict
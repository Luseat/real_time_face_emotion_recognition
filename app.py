import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
from PIL import Image

st.set_page_config(page_title="Face Emotion Recognition", page_icon="🎭")
st.title("🎭 Real-time Face Emotion Recognition")
st.write("Aplikasi ini mendeteksi ekspresi wajah menggunakan webcam. Centang kotak di bawah untuk memulai.")

run = st.checkbox('Mulai Kamera')

col1, col2 = st.columns([2, 1])
with col1:
    FRAME_WINDOW = st.image([])
with col2:
    st.markdown("### Detail Emosi")
    emotion_text_placeholder = st.empty()

camera = None

if run:
    # Buka webcam
    camera = cv2.VideoCapture(0)
    
while run:
    ret, frame = camera.read()
    if not ret:
        st.error("Gagal mengakses webcam!")
        break
    
    # DeepFace dapat memproses gambar dalam format BGR (format default OpenCV)
    try:
        # enforce_detection=False agar tidak crash jika tidak ada wajah
        # Kita gunakan detector_backend='mtcnn' yang lebih pintar dan tidak error masalah path file
        results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False, detector_backend='mtcnn')
        
        # DeepFace mengembalikan list jika mendeteksi banyak wajah, atau dict jika 1 wajah
        if isinstance(results, dict):
            results = [results]
            
        for face_info in results:
            # Dapatkan koordinat bounding box
            region = face_info['region']
            x, y, w, h = region['x'], region['y'], region['w'], region['h']
            
            # Jika x, y, w, h ada nilainya (wajah terdeteksi)
            if w > 0 and h > 0:
                # Update detail emosi di samping video
                all_emotions = face_info['emotion']
                details = ""
                for em_name, em_score in all_emotions.items():
                    details += f"**{em_name.capitalize()}**: {em_score:.2f}%\n\n"
                emotion_text_placeholder.markdown(details)
                
                # Dapatkan emosi dominan
                emotion = face_info['dominant_emotion']
                score = face_info['emotion'][emotion]
                
                # Gambar kotak di wajah
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Tulis label emosi
                text = f"{emotion}: {score:.1f}%"
                cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                
    except Exception as e:
        # Tampilkan pesan error di terminal agar kita tahu penyebabnya
        print(f"Error dari DeepFace: {e}")
        
    # Konversi BGR (OpenCV) ke RGB (Streamlit/Pillow)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Update gambar di Streamlit
    FRAME_WINDOW.image(frame_rgb)
    
else:
    if camera is not None:
        camera.release()
    st.info("Kamera sedang dimatikan.")

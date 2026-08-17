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
    camera = cv2.VideoCapture(0)
    
while run:
    ret, frame = camera.read()
    if not ret:
        st.error("Gagal mengakses webcam!")
        break
    

    try:
        results = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False, detector_backend='mtcnn')
        
        if isinstance(results, dict):
            results = [results]
            
        for face_info in results:
            region = face_info['region']
            x, y, w, h = region['x'], region['y'], region['w'], region['h']
            
            
            if w > 0 and h > 0:
                
                all_emotions = face_info['emotion']
                details = ""
                for em_name, em_score in all_emotions.items():
                    details += f"**{em_name.capitalize()}**: {em_score:.2f}%\n\n"
                emotion_text_placeholder.markdown(details)
                
                
                emotion = face_info['dominant_emotion']
                score = face_info['emotion'][emotion]
                
                # Gambar kotak RGB
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Tulis label emosi
                text = f"{emotion}: {score:.1f}%"
                cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                
    except Exception as e:
        # Tampilkan error 
        print(f"Error dari DeepFace: {e}")
        
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    FRAME_WINDOW.image(frame_rgb)
    
else:
    if camera is not None:
        camera.release()
    st.info("Kamera sedang dimatikan.")

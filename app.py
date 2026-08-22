import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
import pandas as pd
from utils.image_processing import create_report_image, get_download_bytes

st.set_page_config(page_title="Face Emotion Recognition", page_icon="🎭")
st.title("🎭 Real-time Face Emotion Recognition")
st.write("Aplikasi ini mendeteksi ekspresi wajah menggunakan webcam. Centang kotak di bawah untuk memulai.")

# INISIALISASI STATE
if 'screenshots' not in st.session_state:
    st.session_state.screenshots = []
if 'current_frame' not in st.session_state:
    st.session_state.current_frame = None
if 'current_details' not in st.session_state:
    st.session_state.current_details = "Menunggu deteksi wajah..."
if 'emotion_history' not in st.session_state:
    st.session_state.emotion_history = {
        'happy': [], 'sad': [], 'angry': [], 'fear': [], 'surprise': [], 'disgust': [], 'neutral': []
    }

# LAYOUT ATAS 
ctrl1, ctrl2 = st.columns([1, 4])
with ctrl1:
    run = st.checkbox('Mulai Kamera')
with ctrl2:
    if st.button('📸 Ambil Screenshot'):
        if st.session_state.current_frame is not None:
            st.session_state.screenshots.append({
                'image': st.session_state.current_frame,
                'details': st.session_state.current_details
            })
            st.success("Berhasil mengambil screenshot!")
        else:
            st.warning("Nyalakan kamera dan tunggu wajah terdeteksi dulu!")

col1, col2 = st.columns([2, 1])
with col1:
    FRAME_WINDOW = st.image([])
with col2:
    st.markdown("### Detail Emosi")
    emotion_text_placeholder = st.empty()

st.markdown("---")
st.markdown("### 📈 Grafik Fluktuasi Emosi (Real-time)")
chart_placeholder = st.empty()

camera = None

if run:
    camera = cv2.VideoCapture(0)
    
while run:
    ret, frame = camera.read()
    if not ret:
        st.error("Gagal mengakses webcam!")
        break
    
    details = "Tidak ada wajah terdeteksi."

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
                
                for em in st.session_state.emotion_history.keys():
                    # Skor emosi, default 0 jika tidak ada
                    score_val = all_emotions.get(em, 0.0)
                    st.session_state.emotion_history[em].append(score_val)
                    # riwayat maksimal 50 frame terakhir
                    if len(st.session_state.emotion_history[em]) > 50:
                        st.session_state.emotion_history[em].pop(0)
                

                df_chart = pd.DataFrame(st.session_state.emotion_history)
                chart_placeholder.line_chart(df_chart)
                
                # Warna Kotak dan Teks Emosi
                emotion = face_info['dominant_emotion']
                score = face_info['emotion'][emotion]
                
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                text = f"{emotion}: {score:.1f}%"
                cv2.putText(frame, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                
                break
                
    except Exception as e:
        print(f"Error dari DeepFace: {e}")  # Tampilkan error
        
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    st.session_state.current_frame = frame_rgb
    st.session_state.current_details = details
    
    FRAME_WINDOW.image(frame_rgb)
    
else:
    if camera is not None:
        camera.release()
    st.info("Kamera sedang dimatikan.")


# SCREENSHOT & DOWNLOAD 
if len(st.session_state.screenshots) > 0:
    st.markdown("---")
    st.subheader("📸 Riwayat Screenshot")
    
    cols = st.columns(3)
    recent_shots = list(reversed(st.session_state.screenshots))[:9] # maks 9 SS terakhir
    
    for idx, ss in enumerate(recent_shots):
        with cols[idx % 3]:
            st.image(ss['image'], use_container_width=True)
            st.markdown(ss['details'])
            
            report_img = create_report_image(ss['image'], ss['details'])
            
            png_bytes = get_download_bytes(report_img, file_format='PNG')
            pdf_bytes = get_download_bytes(report_img, file_format='PDF')
            
            dl_col1, dl_col2 = st.columns(2)
            with dl_col1:
                st.download_button(
                    label="⬇️ .PNG",
                    data=png_bytes,
                    file_name=f"hasil_emosi_{idx}.png",
                    mime="image/png",
                    key=f"dl_png_{idx}"
                )
            with dl_col2:
                st.download_button(
                    label="⬇️ .PDF",
                    data=pdf_bytes,
                    file_name=f"hasil_emosi_{idx}.pdf",
                    mime="application/pdf",
                    key=f"dl_pdf_{idx}"
                )

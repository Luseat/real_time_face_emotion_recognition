import streamlit as st
import cv2
import numpy as np
import pandas as pd
from PIL import Image
import tempfile
import os
from utils.image_processing import create_report_image, get_download_bytes, process_and_draw_face, cari_muka_pake_AI, gambar_kotak_hijau

st.set_page_config(page_title="Face Emotion Recognition", page_icon="🎭")
st.title("🎭 Real-time Face Emotion Recognition")
st.write("Aplikasi ini mendeteksi ekspresi wajah. Pilih mode input dari menu di samping (Webcam, Foto, atau Video).")


st.sidebar.title("Pengaturan Input")
input_mode = st.sidebar.radio("Pilih Mode:", ["📸 Webcam Live","🛜 Kamera HP", "🖼️ Upload Foto", "🎥 Upload Video"])

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

# Meminimalisir kode berulang 
def update_ui_and_chart(details, emotions_dict, text_placeholder, chart_placeholder):
    # text_placeholder.markdown(details)
    
    text_placeholder.empty()
    with text_placeholder.container():
        parts = [p.strip() for p in details.split('---') if p.strip()]
        
        if len(parts) > 0:
            st.markdown(parts[0])
            
            if len(parts) > 1:
                with st.expander("Lihat lainnya..."):
                    for extra in parts[1:]:
                        st.markdown(extra)
                        st.markdown("---")
    
    if emotions_dict:
        
        for em in st.session_state.emotion_history.keys():
            score_val = emotions_dict.get(em, 0.0)
            st.session_state.emotion_history[em].append(score_val)
            
            if len(st.session_state.emotion_history[em]) > 50:
                st.session_state.emotion_history[em].pop(0)
    
        df_chart = pd.DataFrame(st.session_state.emotion_history)
        chart_placeholder.line_chart(df_chart)


# LAYOUT ATAS 
if st.button('📸 Ambil Screenshot Laporan'):
    
    if st.session_state.current_frame is not None:
        st.session_state.screenshots.append({
            'image': st.session_state.current_frame,
            'details': st.session_state.current_details
        })
        st.success("Berhasil mengambil screenshot! Lihat hasilnya di bawah.")
    else:
        st.warning("Pilih mode dan tunggu wajah terdeteksi dulu!")

col1, col2 = st.columns([2, 1])
with col1:
    FRAME_WINDOW = st.image([])
with col2:
    st.markdown("### Detail Emosi")
    emotion_text_placeholder = st.empty()

st.markdown("---")
st.markdown("### Grafik Fluktuasi Emosi")
chart_placeholder = st.empty()


if input_mode == "📸 Webcam Live":
    run = st.checkbox('Mulai Kamera')
    
    if run:
        camera = cv2.VideoCapture(0)
        
        frame_count = 0
        data_simpanan = None
        
        while run:
            ret, frame = camera.read()
            
            if not ret:
                st.error("Gagal mengakses webcam!")
                break
            frame_count += 1
            
            if frame_count % 5 == 0:
                data_simpanan = cari_muka_pake_AI(frame)
            
            if data_simpanan is not None:
                frame_rgb, details, emotions_dict = gambar_kotak_hijau(frame, data_simpanan)
            else:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                details = "Menunggu deteksi wajah..."
                emotions_dict = None
                
            
            st.session_state.current_frame = frame_rgb
            st.session_state.current_details = details
            
            # Render ke layar
            FRAME_WINDOW.image(frame_rgb)
            update_ui_and_chart(details, emotions_dict, emotion_text_placeholder, chart_placeholder)
            
        camera.release()
        st.info("Kamera dimatikan.")
        
elif input_mode == "🛜 Kamera HP":
    st.info("Pastikan HP dan Laptop terhubung di jaringan WiFi yang sama. Gunakan aplikasi 'IP Webcam' di HP Android")
    
    ip_url = st.text_input("Masukkan IP Camera URL", "http://192.168.1.5:8080/video")
    
    if ip_url != "":
        run = st.checkbox("Mulai kamera HP")
        
        if run:
            camera = cv2.VideoCapture(ip_url)
            frame_count = 0
            data_simpanan = None
            
            while run:
                ret, frame = camera.read()
                
                if not ret:
                    st.error("Gagal terhubung! Pastikan IP URL benar, pakai akhiran /video, dan aplikasi HP menyala.")
                    break
                
                tinggi, lebar = frame.shape[:2]
                if lebar > 720: #klo lebih 720px auto resize
                    skala = 720 / lebar
                    dimensi_baru = (720, int(tinggi * skala))
                    frame = cv2.resize(frame, dimensi_baru, interpolation=cv2.INTER_AREA)
                
                frame_count += 1
                
                if frame_count % 5 == 0:
                    data_simpanan = cari_muka_pake_AI(frame)
                    
                if data_simpanan is not None:
                    frame_rgb, details, emotions_dict = gambar_kotak_hijau(frame, data_simpanan)
                else:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    details = "Menunggu deteksi wajah..."
                    emotions_dict = None
                    
                st.session_state.current_frame = frame_rgb
                st.session_state.current_details = details
                
                FRAME_WINDOW.image(frame_rgb)
                update_ui_and_chart(details, emotions_dict, emotion_text_placeholder, chart_placeholder)
                
            camera.release()
            st.info("Kamera HP dimatikan")

elif input_mode == "🖼️ Upload Foto":
    uploaded_file = st.file_uploader("Upload foto mu di sini...", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        # Konversi hasil ke array OpenCV (BGR)
        image = Image.open(uploaded_file)
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        
        tinggi, lebar = frame.shape[:2]
        if lebar > 1200: # Resize foto berpixel besar
            skala = 1200 / lebar
            dimensi_baru = (1200, int(tinggi * skala))
            frame = cv2.resize(frame, dimensi_baru, interpolation=cv2.INTER_AREA)
        
        
        st.info("Memproses gambar...")
        frame_rgb, details, emotions_dict = process_and_draw_face(frame)
        
        st.session_state.current_frame = frame_rgb
        st.session_state.current_details = details
        
        FRAME_WINDOW.image(frame_rgb)
        update_ui_and_chart(details, emotions_dict, emotion_text_placeholder, chart_placeholder)

elif input_mode == "🎥 Upload Video":
    uploaded_video = st.file_uploader("Upload video mu di sini...", type=['mp4', 'mov', 'avi'])
    
    if uploaded_video is not None:
        run_video = st.checkbox('Putar & Analisis Video')
        
        if run_video:
            tfile = tempfile.NamedTemporaryFile(delete=False) 
            tfile.write(uploaded_video.read())
            
            camera = cv2.VideoCapture(tfile.name)
            
            frame_count = 0
            data_simpanan = None
            
            while run_video:
                ret, frame = camera.read()
                
                if not ret:
                    st.success("Pemutaran video selesai!")
                    break
                
                tinggi, lebar = frame.shape[:2]
                if lebar > 1200: # Resize foto berpixel besar
                    skala = 1200 / lebar
                    dimensi_baru = (1200, int(tinggi * skala))
                    frame = cv2.resize(frame, dimensi_baru, interpolation=cv2.INTER_AREA)
                
                frame_count += 1
                
                # FRAME SKIPING (5frame/second)
                if frame_count % 5 == 0:
                    data_simpanan = cari_muka_pake_AI(frame)
                if data_simpanan is not None:
                    frame_rgb, details, emotions_dict = gambar_kotak_hijau(frame, data_simpanan)
                else:
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    details = "Menunggu deteksi wajah...."
                    emotions_dict = None
                    
                #frame_rgb, details, emotions_dict = process_and_draw_face(frame)
                
                st.session_state.current_frame = frame_rgb
                st.session_state.current_details = details
                
                FRAME_WINDOW.image(frame_rgb)
                update_ui_and_chart(details, emotions_dict, emotion_text_placeholder, chart_placeholder)
                
            camera.release()


# SCREENSHOT & DOWNLOAD 
if len(st.session_state.screenshots) > 0:
    st.markdown("---")
    st.subheader("📸 Riwayat Screenshot Laporan")
    
    cols = st.columns(3)
    recent_shots = list(reversed(st.session_state.screenshots))[:9] # maks 9 SS terakhir
    
    for idx, ss in enumerate(recent_shots):
        
        with cols[idx % 3]:
            st.image(ss['image'], use_container_width=True)
            parts = [p.strip()for p in ss['details'].split('---') if p.strip()]
            
            if len(parts) > 0:
                st.markdown(parts[0])
                
            if len(parts) > 1:
                with st.expander("Lihat lainnya..."):
                    for extra in parts [1:]:
                        st.markdown(extra)
                        st.markdown("---")
            # st.markdown(ss['details'])
            
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


st.markdown("<br><br><br><br>", unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray; margin-bottom: 5px;'>"
    "Copyright &copy; 2026 Hanifudin Robbani | All Rights Reserved."
    "</p>", 
    unsafe_allow_html=True
)
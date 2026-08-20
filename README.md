# 🎭 Real-time Face Emotion Recognition

Aplikasi berbasis antarmuka web (Streamlit) untuk mendeteksi wajah dan menganalisis ekspresi/emosi manusia secara *real-time* langsung dari webcam.

## ✨ Fitur Utama
- **Real-time Face Detection:** Melacak posisi wajah menggunakan algoritma MTCNN yang sangat akurat.
- **Emotion Recognition:** Mengenali 7 jenis emosi dominan (Happy, Sad, Angry, Fear, Surprise, Disgust, Neutral).
- **Live UI Dashboard:** Menampilkan *bounding box* (kotak hijau) di sekitar wajah pada video, beserta daftar lengkap persentase setiap emosi di panel samping.
- **📸 Screenshot & Export Laporan:** 
  - Simpan momen ekspresi secara instan ke dalam Galeri Riwayat.
  - Unduh hasil tangkapan layar yang sudah digabung secara otomatis dengan teks detail persentase emosi.
  - Mendukung format *export* dalam bentuk **.PNG** (Gambar) maupun **.PDF** (Dokumen).

## 🛠️ Tech Stack
- **Python** (Bahasa pemrograman utama)
- **[Streamlit](https://streamlit.io/)** (Framework untuk merender Web UI)
- **[OpenCV](https://opencv.org/)** (Untuk memproses video & membuat kanvas laporan gambar)
- **[Pillow (PIL)](https://python-pillow.org/)** (Untuk konversi format ke PDF/PNG)
- **[DeepFace](https://github.com/serengil/deepface)** (Pustaka AI *Deep Learning* untuk membaca emosi)
- **MTCNN** (Model khusus untuk pendeteksi letak wajah)

---

## 🚀 Panduan Instalasi & Penggunaan

### 1. Prasyarat
- Pastikan sudah menginstal **Python (versi 3.8 atau lebih baru)** di komputer kamu.
- Memiliki perangkat *webcam* yang aktif.

### 2. Langkah-langkah Menjalankan Proyek

**Langkah 1:** *Clone* repository ini ke komputer lokal kamu.
```bash
git clone https://github.com/username-kamu/real_time_face_emotion_recognition.git
cd real_time_face_emotion_recognition
```

**Langkah 2:** Buat *Virtual Environment* agar library proyek ini tidak bentrok dengan proyek lain.
```bash
python -m venv venv
```

**Langkah 3:** Aktifkan *Virtual Environment* tersebut.
- **Windows:**
  ```powershell
  .\venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

**Langkah 4:** Instal seluruh *library* yang dibutuhkan.
```bash
pip install -r requirements.txt
```

**Langkah 5:** Jalankan aplikasinya! 🎉
```bash
streamlit run app.py
```

### 3. Cara Menggunakan
1. Buka browser dan pergi ke tautan `http://localhost:8501` (jika tidak terbuka secara otomatis).
2. Centang kotak **"Mulai Kamera"** dan izinkan akses webcam.
3. Tunjukkan berbagai ekspresi ke kamera, dan persentase emosi akan terus diperbarui secara *real-time*.
4. Klik tombol **"📸 Ambil Screenshot"** untuk menyimpan momen saat ini.
5. Gulir ke bawah ke bagian **Riwayat Screenshot**, lalu klik tombol **⬇️ .PNG** atau **⬇️ .PDF** untuk mengunduh laporan analisis wajah lengkap dengan detail emosinya ke laptop kamu!

> **⚠️ Penting:** Saat pertama kali dijalankan dan mendeteksi wajah, sistem (DeepFace) membutuhkan waktu beberapa detik untuk mengunduh model AI dari internet. Setelah selesai, proses deteksi akan berjalan instan dan mulus.

---

## 🤝 Kontribusi
Jika kamu ingin menambahkan fitur baru atau menemukan *bug*, silakan *fork* repository ini dan buat *Pull Request*. Masukan sangat diapresiasi!


---
<p align="center">Copyright &copy; 2026 Hanifudin Robbani | All Rights Reserved.</p>
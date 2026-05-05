# Face Recognition Attendance System

## 📌 Project Overview
This is a Face Recognition based Attendance System that automatically marks attendance using a webcam. It detects and recognizes faces in real-time and stores attendance records in an Excel file.

---

## 🚀 Features
- Real-time face detection using webcam
- Face recognition using trained dataset
- Automatic attendance marking
- Stores attendance in Excel sheet
- Simple UI for live monitoring

---

## 🛠️ Technologies Used
- Python
- OpenCV (cv2)
- face_recognition library
- NumPy
- Pandas
- OS module

---

## 📂 Project Structure
- `face_app.py` → Main application for face recognition
- `live_attendance.py` → Real-time attendance system
- `camera_test.py` → Camera testing script
- `export_attendance.py` → Export attendance data
- `dataset/` → Stored face images
- `attendance.xlsx` → Attendance records

---

## ▶️ How to Run
```bash
pip install -r requirements.txt
python face_app.py
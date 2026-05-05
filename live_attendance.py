import cv2
import face_recognition
import psycopg2
import os

# =========================
# DATABASE CONNECTION
# =========================
conn = psycopg2.connect(
    host="localhost",
    port="5433",
    database="face_db",
    user="postgres",
    password="your_password"
)
cursor = conn.cursor()

# =========================
# LOAD DATASET FACES (SAFE)
# =========================
known_encodings = []
known_names = []

dataset_path = "dataset"

for file in os.listdir(dataset_path):

    # skip hidden/system files like .DS_Store
    if file.startswith("."):
        continue

    # only allow images
    if not file.lower().endswith((".jpg", ".jpeg", ".png")):
        continue

    image_path = os.path.join(dataset_path, file)

    try:
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)

        if len(encodings) > 0:
            known_encodings.append(encodings[0])
            known_names.append(os.path.splitext(file)[0])
        else:
            print("⚠️ No face found in:", file)

    except Exception as e:
        print("⚠️ Error reading file:", file, e)

print("✅ Loaded faces:", known_names)

# =========================
# CAMERA START
# =========================
video = cv2.VideoCapture(0)

if not video.isOpened():
    print("❌ Camera not opening")
    exit()

print("📸 Attendance system started... Press Q to exit")

# =========================
# MAIN LOOP
# =========================
while True:
    ret, frame = video.read()

    if not ret or frame is None:
        continue

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    for encoding, location in zip(face_encodings, face_locations):

        matches = face_recognition.compare_faces(
            known_encodings,
            encoding,
            tolerance=0.5
        )

        name = "Unknown"

        if True in matches:
            index = matches.index(True)
            name = known_names[index]

            # =========================
            # CHECK ATTENDANCE
            # =========================
            cursor.execute("""
                SELECT * FROM attendance
                WHERE name = %s AND date = CURRENT_DATE
            """, (name,))

            result = cursor.fetchone()

            if not result:
                cursor.execute("""
                    INSERT INTO attendance (name)
                    VALUES (%s)
                """, (name,))
                conn.commit()
                print("✅ Attendance marked:", name)
            else:
                print("⚠️ Already marked today:", name)

        # =========================
        # DRAW BOX
        # =========================
        top, right, bottom, left = location
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Face Attendance System", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# =========================
# CLEAN EXIT
# =========================
video.release()
cv2.destroyAllWindows()
cursor.close()
conn.close()

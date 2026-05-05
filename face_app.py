

import psycopg2
import face_recognition

# 🔹 PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    port="5433",
    database="face_db",
    user="postgres",
    password="your_password"   # change this
)

cursor = conn.cursor()

# 🔹 Load image
image = face_recognition.load_image_file("test.jpg")

# 🔹 Get face encodings
encodings = face_recognition.face_encodings(image)

print("Encodings found:", len(encodings))

if len(encodings) == 0:
    print("❌ No face detected. Use a clear image.")
else:
    encoding = encodings[0]

    # Convert to pgvector format
    encoding_str = "[" + ",".join(map(str, encoding)) + "]"

    name = "Nikhitha"

    # 🔹 Check if already exists (optional but IMPORTANT)
    cursor.execute("""
        SELECT name FROM students
        WHERE name = %s
        LIMIT 1
    """, (name,))

    exists = cursor.fetchone()

    if exists:
        print("Attendance already marked for today")
    else:
        # 🔹 Insert into DB
        cursor.execute("""
            INSERT INTO students (name, encoding)
            VALUES (%s, %s::vector)
        """, (name, encoding_str))

        conn.commit()
        print("✅ Inserted successfully!")

    # 🔹 Find closest match
    cursor.execute("""
        SELECT name
        FROM students
        ORDER BY encoding <-> %s::vector
        LIMIT 1
    """, (encoding_str,))

    result = cursor.fetchone()

    if result:
        print("🎯 Matched person:", result[0])
    else:
        print("No match found")

# 🔹 Close connection
cursor.close()
conn.close()
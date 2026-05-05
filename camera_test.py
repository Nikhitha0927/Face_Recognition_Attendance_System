import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Camera not opening")
    exit()

print("📸 Camera working... Press Q to exit")

while True:
    ret, frame = cap.read()

    if not ret:
        print("❌ No frame received")
        break

    cv2.imshow("Camera Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

import cv2
import time
import HandTrackingModule as htm

pTime = 0
cTime = 0

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
detector = htm.HandDetector()

while cap.isOpened():
    success, img = cap.read()
    if not success:
        break
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img)
    if len(lmList) != 0:
        print(lmList[4])

    # Frames Per Second
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()
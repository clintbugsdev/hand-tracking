import cv2
import time
import HandTrackingModule as htm

# Camera
wCam, hCam = 640, 480

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0

# HandTracking Module
detector = htm.HandDetector(maxHands=1, detectionCon=0.75)

tipIds = [4, 8, 12, 16, 20]

while cap.isOpened():
    success, img = cap.read()
    if not success:
        break
    img = detector.findHands(img)
    lmList, bbox = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        fingers = []

        # Thumb
        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 Fingers
        for id in range(1, 5):
            # Fingers Open
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)

        cv2.rectangle(img, (20, 225), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(totalFingers), (45, 375), cv2.FONT_HERSHEY_PLAIN,
                    10, (255, 0, 0), 25)

    # Compute Frames Per Second
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # Display Frames Per Second
    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                1, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

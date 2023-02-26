import cv2
from HandTracking import HandDetector
import mouse
from pynput.mouse import Button, Controller


class FingerTracking:

    def __init__(self, wCam=1280, hCam=720):
        self.wCam = wCam
        self.hCam = hCam
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, self.wCam)
        self.cap.set(4, self.hCam)
        self.detector = HandDetector()
        self.tipIds = [4, 8, 12, 16, 20]
        self.clicked = False

    def run(self):
        while True:
            success, img = self.cap.read()
            img = self.detector.findHands(img)
            lmList = self.detector.findPosition(img, draw=False)
            visibleFingers = 0

            if len(lmList) != 0:
                fingers = []

                # Thumb
                if lmList[self.tipIds[0]][1] > lmList[self.tipIds[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # 4 Fingers
                for id in range(1, 5):
                    if lmList[self.tipIds[id]][2] < lmList[self.tipIds[id] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                # print(fingers)
                visibleFingers = 5 - fingers.count(0)
                # print(visibleFingers)

            if visibleFingers == 2 and (fingers[1] == 1 and fingers[2] == 1):
                # print("Index  finger : { x : " + str(lmList[self.tipIds[1]][1]) + " ; y : " + str(lmList[self.tipIds[1]][2]) + " }")
                # print("Middle finger : { x : " + str(lmList[self.tipIds[2]][1]) + " ; y : " + str(lmList[self.tipIds[2]][2]) + " }")
                print(lmList[self.tipIds[1]][1], lmList[self.tipIds[1]][2])
                self.clicked = False
                print(lmList[self.tipIds[1]][1])
                mouse.move((self.wCam - lmList[self.tipIds[1]][1]) * 1.5, lmList[self.tipIds[1]][2] * 1.5,
                           absolute=True,
                           duration=0.05)

            if not self.clicked:
                if visibleFingers == 3 and (fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1):
                    m = Controller()
                    m.click(Button.left)
                    self.clicked = True

            cv2.imshow("Image", img)
            cv2.waitKey(1)

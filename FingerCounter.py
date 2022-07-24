from HandsDetector import HandsDetector
import cv2 as cv
import time

class FingerCounter(HandsDetector):

    def __init__(self, device_index=0, max_num_hands=1, min_detection_confidence=0.75, cam_width=1280, cam_height=800):
        super().__init__(
            device_index=device_index,
            min_detection_confidence=min_detection_confidence,
            max_num_hands=max_num_hands,
            cam_width=cam_width,
            cam_height=cam_height
        )

        self.fingers = {
            'index': False,
            'middle': False,
            'ring': False,
            'pinky': False,
            'thumb': False
        }

        self.count = 0


    def putText(self):
        cv.putText(self.img, f'Count: {self.count}', (10,60), cv.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)

    def update_fingers(self, hands):
        if hands:
            for hand in hands:
                self.fingers['index'] = self.get_distance(hand, 8, 0) > 250
                self.fingers['middle'] = self.get_distance(hand, 12, 0) > 250
                self.fingers['ring'] = self.get_distance(hand, 16, 0) > 250
                self.fingers['pinky'] = self.get_distance(hand, 20, 0) > 250
                self.fingers['thumb'] = self.get_distance(hand, 4, 17) > 200

        print(self.fingers)
        self.count = len(list(filter(lambda x:x, self.fingers.values())))

        

if __name__ == '__main__':

    counter = FingerCounter()

    while True:
        previous_time = time.time()
        img, hands = counter.detect()
        img = counter.draw(img, hands)

        counter.update_fingers(hands)
        counter.putText()
        current_time = time.time()
        fps = 1/(current_time-previous_time)
        cv.putText(img, f'FPS: {fps}', (10,90), cv.FONT_HERSHEY_PLAIN, 1, (255,0,0), 2)
        cv.imshow('Video', img)
        cv.waitKey(1)

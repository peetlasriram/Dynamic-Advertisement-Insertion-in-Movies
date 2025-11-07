import cv2, numpy as np

class SimpleTracker:
    """Very basic CSRT tracker per target; placeholder for BYTE/DeepSORT."""
    def __init__(self):
        self.trackers = []

    def init(self, frame, boxes):
        self.trackers = []
        for (x,y,w,h) in boxes:
            tracker = cv2.TrackerCSRT_create()
            tracker.init(frame, (x,y,w,h))
            self.trackers.append(tracker)

    def update(self, frame):
        boxes = []
        for t in self.trackers:
            ok, box = t.update(frame)
            if ok:
                x,y,w,h = box
                boxes.append((int(x),int(y),int(w),int(h)))
        return boxes

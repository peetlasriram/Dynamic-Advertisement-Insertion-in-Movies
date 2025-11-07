import numpy as np, cv2

def _try_import_ultralytics():
    try:
        from ultralytics import YOLO
        return YOLO
    except Exception:
        return None

def _try_import_easyocr():
    try:
        import easyocr
        return easyocr.Reader(['en'], gpu=False)
    except Exception:
        return None

class Detector:
    def __init__(self, mode='auto', min_conf=0.35):
        self.mode = mode
        self.min_conf = min_conf
        self.yolo_cls = _try_import_ultralytics()
        self.ocr = _try_import_easyocr()
        self.yolo = self.yolo_cls('yolov8n.pt') if self.yolo_cls else None

    def detect_regions(self, frame):
        h, w = frame.shape[:2]
        regions = []  # list of (x,y,w,h), label

        if self.mode in ['auto','billboard'] and self.yolo is not None:
            try:
                res = self.yolo.predict(frame, verbose=False)[0]
                for b in res.boxes:
                    conf = float(b.conf.cpu().item())
                    if conf < self.min_conf: continue
                    x1,y1,x2,y2 = map(int, b.xyxy.cpu().numpy()[0])
                    regions.append(((x1,y1,x2-x1,y2-y1), "object"))
            except Exception:
                pass

        # OCR-based text region finder
        if self.mode in ['auto','text'] and self.ocr is not None:
            try:
                ocr_res = self.ocr.readtext(frame)
                for (bx, by, bw, bh) in [cv2.boundingRect(np.array(r[0]).astype(int)) for r in ocr_res]:
                    if bw*bh < 400: continue
                    regions.append(((bx,by,bw,bh), "text"))
            except Exception:
                pass

        # Fallback: center box if nothing detected
        if not regions:
            cw, ch = int(w*0.4), int(h*0.15)
            cx, cy = (w-cw)//2, int(h*0.1)
            regions.append(((cx,cy,cw,ch), "fallback"))

        return regions

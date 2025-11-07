import cv2, numpy as np

def paste_ad(frame, box, ad_img, blend=0.85):
    x,y,w,h = box
    if ad_img is None:
        overlay = frame.copy()
        cv2.rectangle(overlay, (x,y), (x+w,y+h), (0,0,0), -1)
        out = cv2.addWeighted(overlay, blend, frame, 1-blend, 0)
        return out
    ad = cv2.resize(ad_img, (w,h))
    roi = frame[y:y+h, x:x+w].copy()
    blended = cv2.addWeighted(ad, blend, roi, 1-blend, 0)
    frame[y:y+h, x:x+w] = blended
    return frame

def write_text(frame, box, text, blend=0.85):
    x,y,w,h = box
    overlay = frame.copy()
    cv2.rectangle(overlay, (x,y), (x+w,y+h), (0,0,0), -1)
    out = cv2.addWeighted(overlay, blend, frame, 1-blend, 0)
    cv2.putText(out, text, (x+10, y+h-10), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255,255,255), 2, cv2.LINE_AA)
    return out

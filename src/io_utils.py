import cv2, os, numpy as np

def video_reader(path):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise RuntimeError(f"Cannot open video: {path}")
    fps = cap.get(cv2.CAP_PROP_FPS)
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    return cap, fps, (w,h)

def video_writer(path, fps, size):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(path, fourcc, fps, size)
    if not out.isOpened():
        raise RuntimeError(f"Cannot open writer: {path}")
    return out

def ensure_dir(d):
    if d:
        os.makedirs(d, exist_ok=True)

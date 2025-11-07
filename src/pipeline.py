import argparse, os, cv2, numpy as np
from tqdm import tqdm
from .config import PipelineConfig
from .io_utils import video_reader, video_writer, ensure_dir
from .detection import Detector
from .tracking import SimpleTracker
from .overlay import paste_ad, write_text

def run_pipeline(input_path, ad_path=None, out_path="out/output.mp4", mode="text", custom_text="ChatGPT Grand Hotel"):
    ensure_dir(os.path.dirname(out_path))
    cap, fps, (W,H) = video_reader(input_path)
    writer = video_writer(out_path, fps, (W,H))

    cfg = PipelineConfig(detect_mode=mode)
    det = Detector(mode=cfg.detect_mode, min_conf=cfg.min_conf)
    tracker = SimpleTracker()

    ad_img = cv2.imread(ad_path) if ad_path and os.path.exists(ad_path) else None

    init_boxes = None
    frame_idx = 0
    pbar = tqdm(total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or None, desc="Processing")

    while True:
        ok, frame = cap.read()
        if not ok: break

        if init_boxes is None or frame_idx % 15 == 0:
            regs = det.detect_regions(frame)
            init_boxes = [r[0] for r in regs]
            tracker.init(frame, init_boxes)

        boxes = tracker.update(frame)
        if not boxes:
            boxes = init_boxes or []

        for box in boxes:
            if mode == "text":
                frame = write_text(frame, box, custom_text, blend=0.85)
            else:
                frame = paste_ad(frame, box, ad_img, blend=0.85)

        writer.write(frame)
        frame_idx += 1
        pbar.update(1)

    pbar.close()
    cap.release()
    writer.release()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to input video")
    parser.add_argument("--ad", default=None, help="Path to ad image")
    parser.add_argument("--out", default="out/output.mp4", help="Output video file")
    parser.add_argument("--mode", default="text", choices=["text","billboard"])
    parser.add_argument("--custom_text", default="ChatGPT Grand Hotel")
    args = parser.parse_args()
    run_pipeline(args.input, args.ad, args.out, args.mode, args.custom_text)

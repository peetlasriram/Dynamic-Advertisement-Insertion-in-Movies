# Dynamic Advertisement Insertion in Movies Using AI

An end-to-end prototype to detect ad/text regions in movie frames, track them across time, and replace them with custom ads (e.g., change a hotel sign).

## Features
- Frame extraction & recomposition
- Object/Text region detection (YOLO / OCR)
- Robust tracking (BYTETracker/DeepSORT placeholder)
- Perspective-aware overlay & blending
- Simple Streamlit UI for demos
- Configuration-driven pipeline

## Quick Start
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
# (Optional) If you plan to use YOLOv8:
# pip install ultralytics

# Run CLI pipeline
python src/pipeline.py --input data/sample_video.mp4 --ad data/sample_ad.png --out out/output.mp4 --mode text

# Or run the UI
streamlit run app.py
```

## Folder Structure
```
dynamic_ad_insertion/
  app.py
  src/
    pipeline.py
    detection.py
    tracking.py
    overlay.py
    io_utils.py
    config.py
  data/
    sample_video.mp4        (placeholder, add your own)
    sample_ad.png           (placeholder, add your own)
  out/
  requirements.txt
  README.md
```

## Notes
- The code includes fallbacks if YOLO/easyocr are not installed.
- For best results, install GPU-enabled libraries and provide domain-specific fine-tuned models.
- This is a prototype and intended for educational purposes.

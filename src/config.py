from dataclasses import dataclass

@dataclass
class PipelineConfig:
    detect_mode: str = "auto"      # 'auto', 'text', or 'billboard'
    min_conf: float = 0.35
    tracker_type: str = "byte"     # 'byte' or 'deepsort' (placeholder implementations)
    overlay_blend: float = 0.85    # 0..1 overlay strength
    write_debug: bool = True       # save debug frames
    max_frames: int = -1           # -1 for all frames

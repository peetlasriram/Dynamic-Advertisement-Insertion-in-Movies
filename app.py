import os
import streamlit as st
from src.pipeline import run_pipeline

st.set_page_config(page_title="Dynamic Ad Insertion", layout="wide")
st.title("🎬 Dynamic Advertisement Insertion in Movies")

st.sidebar.header("Inputs")
video_file = st.sidebar.file_uploader("Upload input video", type=["mp4","mov","mkv","avi"])
ad_file = st.sidebar.file_uploader("Upload ad image (PNG/JPG)", type=["png","jpg","jpeg"])
mode = st.sidebar.selectbox("Replacement mode", ["text","billboard"])
custom_text = st.sidebar.text_input("Custom text (for 'text' mode)", "ChatGPT Grand Hotel")
run_btn = st.sidebar.button("Run")

if run_btn:
    if not video_file:
        st.error("Please upload an input video.")
    else:
        os.makedirs("out", exist_ok=True)
        inpath = os.path.join("out", "uploaded_video.mp4")
        with open(inpath, "wb") as f:
            f.write(video_file.read())
        adpath = None
        if ad_file:
            adpath = os.path.join("out", "uploaded_ad.png")
            with open(adpath, "wb") as f:
                f.write(ad_file.read())
        outpath = os.path.join("out", "output.mp4")
        st.info("Processing... this may take time on long videos.")
        try:
            run_pipeline(input_path=inpath, ad_path=adpath, out_path=outpath, mode=mode, custom_text=custom_text)
            st.success("Done!")
            st.video(outpath)
        except Exception as e:
            st.error(f"Pipeline failed: {e}")

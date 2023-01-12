import streamlit as st

from style_transfer.image_style_transfer import ImageStyleTransfer
from style_transfer.video_style_transfer import VideoStyleTransfer


image_tab, video_tab = st.tabs(['Image', 'Video'])
with image_tab:
    image_style_transfer = ImageStyleTransfer()
    image_style_transfer.run()
with video_tab:
    video_style_transfer = VideoStyleTransfer()
    video_style_transfer.run()

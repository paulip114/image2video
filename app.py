import gradio as gr
import cv2
import os
import uuid
import shutil
import numpy as np
import ffmpeg
from PIL import Image


host = os.getenv("HOST", "127.0.0.1") 
port = int(os.getenv("PORT", 7860))

# === Dummy Interpolation (replace with AnimateDiff later) ===
def simple_interpolate(img1, img2, num_frames):
    frames = [img1]
    for i in range(1, num_frames + 1):
        alpha = i / (num_frames + 1)
        blended = cv2.addWeighted(img1, 1 - alpha, img2, alpha, 0)
        frames.append(blended)
    frames.append(img2)
    return frames

# === Main function ===
def generate_video(keyframe1, keyframe2, num_inter_frames):
    session_id = str(uuid.uuid4())
    os.makedirs(f"temp/{session_id}", exist_ok=True)

    img1 = np.array(Image.open(keyframe1).convert("RGB"))
    img2 = np.array(Image.open(keyframe2).convert("RGB"))

    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    frames = simple_interpolate(img1, img2, num_inter_frames)

    frame_paths = []
    for i, frame in enumerate(frames):
        path = f"temp/{session_id}/frame_{i:03d}.png"
        cv2.imwrite(path, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
        frame_paths.append(path)

    output_video = f"temp/{session_id}/output.mp4"
    (
        ffmpeg
        .input(f"temp/{session_id}/frame_%03d.png", framerate=30)
        .filter("scale", 1920, 1920)
        .output(output_video, vcodec='libx264', pix_fmt='yuv422p')
        .overwrite_output()
        .run()
    )

    return output_video


# === Gradio Interface ===
with gr.Blocks() as demo:
    gr.Markdown("## 🌀 Keyframe to Video Generator (MVP)")
    with gr.Row():
        keyframe1 = gr.Image(label="Start Frame", type="filepath")
        keyframe2 = gr.Image(label="End Frame", type="filepath")
    num_frames = gr.Slider(1, 30, value=6, step=1, label="Number of Interpolated Frames")
    generate_btn = gr.Button("Generate Video")
    video_output = gr.Video(label="Generated Video")

    generate_btn.click(fn=generate_video, inputs=[keyframe1, keyframe2, num_frames], outputs=video_output)

demo.launch(server_name=host, server_port=port)

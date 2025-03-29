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
    # Purge old sessions if needed
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    sessions = [os.path.join(temp_dir, d) for d in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, d))]
    sessions.sort(key=lambda d: os.path.getctime(d)) 

    while len(sessions) > 2:  # keep only the 3 most recent
        to_delete = sessions.pop(0)
        shutil.rmtree(to_delete)
        print(f"Purged old session: {to_delete}")

    # === Generate new session ===
    session_id = str(uuid.uuid4())
    session_path = os.path.join(temp_dir, session_id)
    os.makedirs(session_path, exist_ok=True)

    img1 = np.array(Image.open(keyframe1).convert("RGB"))
    img2 = np.array(Image.open(keyframe2).convert("RGB"))

    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    frames = simple_interpolate(img1, img2, num_inter_frames)

    for i, frame in enumerate(frames):
        path = f"{session_path}/frame_{i:03d}.png"
        cv2.imwrite(path, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    output_video = os.path.join(session_path, "output.mp4") # f"{session_path}/output.mp4"
    
    try:
        (
        ffmpeg
        .input(f"{session_path}/frame_%03d.png", framerate=30)
        # .filter("scale", 1920, 1920)
        .output(output_video, vcodec='libx264', pix_fmt='yuv420p')
        .overwrite_output()
        .run()
        )
    except ffmpeg.Error as e:
        print("❌ FFmpeg error!")
        print("STDOUT:", e.stdout.decode())
        print("STDERR:", e.stderr.decode())  # This is the important one
        raise e

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

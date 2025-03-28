# 🌀 Keyframe-to-Video Generator (Gradio MVP)

This is a minimal MVP (Minimum Viable Product) for generating short videos by interpolating between two **keyframe images** using a simple linear blending technique.

Built with **Gradio** as a frontend and **FFmpeg + OpenCV** as the backend processing stack.

---

## 📸 Features

- Upload two keyframes (start and end frames)
- Choose number of interpolated frames
- Generate smooth transition video (MP4)
- Gradio-powered UI
- Outputs a `.mp4` file in 1920x1920 resolution using FFmpeg

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/keyframe2video.git
cd keyframe2video
```

### 2. Set Up Python Environment

Using `venv` or `conda`:

```bash
conda create -n keyframe-video python=3.10
conda activate keyframe-video
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` isn't created yet, you can install manually:

```bash
pip install gradio opencv-python ffmpeg-python pillow numpy
```

---

## 🛠️ Usage

```bash
python app.py
```

Then open your browser to:  
`http://127.0.0.1:7860`

---

## 📦 Output

- A video file is saved to `./temp/<session_id>/output.mp4`
- Resolution: `1920x1920`
- Format: `.mp4` (H.264, yuv422p)

---

## 📂 Project Structure

```
├── app.py              # Main Gradio app
├── temp/               # Temporary folder to store frames and output
├── README.md
└── requirements.txt    # Python dependencies (optional)
```

---

## 🔮 Future Plans

- Replace dummy interpolation with **AnimateDiff** or **FILM** for motion-aware generation
- Add **ControlNet + Pose** conditioning
- Integrate **prompt-based animation**
- Optional audio/music generation

---

## ⚠️ Requirements

- Python 3.9 / 3.10
- `ffmpeg` must be installed and added to your system PATH  
  👉 [Download FFmpeg](https://www.gyan.dev/ffmpeg/builds/)

---

## 📄 License

MIT License. Use freely and modify.

---

## ✨ Credits

- [Gradio](https://www.gradio.app/)
- [FFmpeg](https://ffmpeg.org/)
- [OpenCV](https://opencv.org/)
- [Pillow](https://python-pillow.org/)

```

---

Want me to create a `requirements.txt` too? Or generate this `README.md` as a downloadable file for you?
```

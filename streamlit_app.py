<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 49273b9 (New layout and features)
"""
Ceramic Tile Defect Detector
Backend-first Streamlit app
Pipeline: Image/Webcam → Grayscale → (Detect Circle) → Invert → Exposure +30% → Sharpen → Crop (Apply Mask) → DINOv2 → Prediction → Threshold 70% → SQLite
"""

<<<<<<< HEAD
import os
import sqlite3
=======
import os
import sqlite3

from dotenv import load_dotenv
load_dotenv()
import threading
import time
from collections import deque
>>>>>>> 4634d35 (update WebRCT using metered.ca)
=======
import os
import sqlite3
>>>>>>> 49273b9 (New layout and features)
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
import streamlit as st
import timm
import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms

# ── streamlit-webrtc (live webcam) ────────────────────────────────────────────
try:
    import av
    from streamlit_webrtc import RTCConfiguration, VideoProcessorBase, webrtc_streamer
    WEBRTC_AVAILABLE = True
except ImportError:
    WEBRTC_AVAILABLE = False

<<<<<<< HEAD
<<<<<<< HEAD
# ══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════════
=======
════
# CONFIG
════
>>>>>>> 4634d35 (update WebRCT using metered.ca)
=======
# ══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════════
>>>>>>> 49273b9 (New layout and features)
MODEL_PATH = Path("best_model_dinov2.pth")
IMG_SIZE   = 224
DB_PATH    = "predictions.db"
DEVICE     = torch.device("cuda" if torch.cuda.is_available() else "cpu")

<<<<<<< HEAD
<<<<<<< HEAD
# ─────────────────────────────────────────────────────────────────────────────
CLASSES_2 = ["crack", "spot"]
CLASSES_3 = ["crack", "pinhole", "spot"]

# THRESHOLD: Jika prediksi crack/spot di bawah nilai ini, dianggap "normal"
CONFIDENCE_THRESHOLD = 70.0  # Dalam persen (70%)
DEFECT_CLASSES_FOR_THRESHOLD = ["crack", "spot"]
# ─────────────────────────────────────────────────────────────────────────────


# ══════════════════════════════════════════════════════════════════════════════
# DATABASE
# ══════════════════════════════════════════════════════════════════════════════
=======
=======
# ─────────────────────────────────────────────────────────────────────────────
>>>>>>> 49273b9 (New layout and features)
CLASSES_2 = ["crack", "spot"]
CLASSES_3 = ["crack", "pinhole", "spot"]

# THRESHOLD: Jika prediksi crack/spot di bawah nilai ini, dianggap "normal"
CONFIDENCE_THRESHOLD = 70.0  # Dalam persen (70%)
DEFECT_CLASSES_FOR_THRESHOLD = ["crack", "spot"]
# ─────────────────────────────────────────────────────────────────────────────


# ══════════════════════════════════════════════════════════════════════════════
# DATABASE
<<<<<<< HEAD
════
>>>>>>> 4634d35 (update WebRCT using metered.ca)
=======
# ══════════════════════════════════════════════════════════════════════════════
>>>>>>> 49273b9 (New layout and features)
def init_db() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 49273b9 (New layout and features)
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            source      TEXT    NOT NULL,
            filename    TEXT,
            label       TEXT    NOT NULL,
            confidence  REAL    NOT NULL,
<<<<<<< HEAD
            circle_found INTEGER DEFAULT 0,
            created_at  TEXT    NOT NULL
        )
    """)
=======
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            source       TEXT    NOT NULL,
            filename     TEXT,
            label        TEXT    NOT NULL,
            confidence   REAL    NOT NULL,
=======
>>>>>>> 49273b9 (New layout and features)
            circle_found INTEGER DEFAULT 0,
            created_at  TEXT    NOT NULL
        )
    """)
<<<<<<< HEAD
    # Migrasi: tambah kolom baru jika belum ada (backward compat)
    try:
        conn.execute("ALTER TABLE predictions ADD COLUMN exposure REAL DEFAULT 1.3")
        conn.execute("ALTER TABLE predictions ADD COLUMN sharpen  REAL DEFAULT 1.5")
    except Exception:
        pass
>>>>>>> 4634d35 (update WebRCT using metered.ca)
=======
>>>>>>> 49273b9 (New layout and features)
    conn.commit()
    conn.close()


def save_prediction(source: str, filename: str, label: str,
<<<<<<< HEAD
<<<<<<< HEAD
                    confidence: float, circle_found: bool = False) -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO predictions "
        "(source, filename, label, confidence, circle_found, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (source, filename or "-", label, round(confidence, 4),
         int(circle_found), datetime.now().isoformat(timespec="seconds")),
=======
                    confidence: float, circle_found: bool = False,
                    exposure: float = 1.3, sharpen: float = 1.5) -> None:
=======
                    confidence: float, circle_found: bool = False) -> None:
>>>>>>> 49273b9 (New layout and features)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO predictions "
        "(source, filename, label, confidence, circle_found, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (source, filename or "-", label, round(confidence, 4),
<<<<<<< HEAD
         int(circle_found), round(exposure, 2), round(sharpen, 2),
         datetime.now().isoformat(timespec="seconds")),
>>>>>>> 4634d35 (update WebRCT using metered.ca)
=======
         int(circle_found), datetime.now().isoformat(timespec="seconds")),
>>>>>>> 49273b9 (New layout and features)
    )
    conn.commit()
    conn.close()


<<<<<<< HEAD
<<<<<<< HEAD
def get_history(limit: int = 30) -> list:
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT id, source, filename, label, confidence, circle_found, created_at "
=======
def get_history(limit: int = 50) -> list:
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT id, source, filename, label, confidence, circle_found, exposure, sharpen, created_at "
>>>>>>> 4634d35 (update WebRCT using metered.ca)
=======
def get_history(limit: int = 30) -> list:
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT id, source, filename, label, confidence, circle_found, created_at "
>>>>>>> 49273b9 (New layout and features)
        "FROM predictions ORDER BY id DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return rows


<<<<<<< HEAD
<<<<<<< HEAD
=======
def get_stats() -> dict:
    """Ambil statistik agregat dari database."""
    conn = sqlite3.connect(DB_PATH)
    total   = conn.execute("SELECT COUNT(*) FROM predictions").fetchone()[0]
    by_label = conn.execute(
        "SELECT label, COUNT(*) FROM predictions GROUP BY label ORDER BY COUNT(*) DESC"
    ).fetchall()
    avg_conf = conn.execute("SELECT AVG(confidence) FROM predictions").fetchone()[0]
    conn.close()
    return {"total": total, "by_label": by_label, "avg_conf": avg_conf or 0.0}


>>>>>>> 4634d35 (update WebRCT using metered.ca)
=======
>>>>>>> 49273b9 (New layout and features)
def clear_history() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM predictions")
    conn.commit()
    conn.close()


<<<<<<< HEAD
<<<<<<< HEAD
# ══════════════════════════════════════════════════════════════════════════════
# MODEL — auto-detect num_classes dari checkpoint
# ══════════════════════════════════════════════════════════════════════════════
def _get_classes_from_checkpoint(path: Path) -> list[str]:
    sd = torch.load(path, map_location="cpu")
    n  = sd["head.weight"].shape[0]
=======
════
=======
# ══════════════════════════════════════════════════════════════════════════════
>>>>>>> 49273b9 (New layout and features)
# MODEL — auto-detect num_classes dari checkpoint
# ══════════════════════════════════════════════════════════════════════════════
def _get_classes_from_checkpoint(path: Path) -> list[str]:
    sd = torch.load(path, map_location="cpu")
<<<<<<< HEAD
    head_key = None
    for key in sd.keys():
        if key.endswith(".weight") and "head" in key:
            head_key = key
            break
    if head_key is None:
        for key in reversed(list(sd.keys())):
            if key.endswith(".weight") and sd[key].ndim == 2 and sd[key].shape[0] <= 10:
                head_key = key
                break
    if head_key is None:
        st.error("Tidak dapat menentukan jumlah kelas dari checkpoint.")
        st.stop()
    n = sd[head_key].shape[0]
>>>>>>> 4634d35 (update WebRCT using metered.ca)
=======
    n  = sd["head.weight"].shape[0]
>>>>>>> 49273b9 (New layout and features)
    if n == 2:
        return CLASSES_2
    elif n == 3:
        return CLASSES_3
    else:
        return [f"class_{i}" for i in range(n)]


@st.cache_resource(show_spinner="⏳ Memuat model DINOv2…")
def load_model() -> tuple[nn.Module, list[str]]:
    if not MODEL_PATH.exists():
        st.error(f"File model tidak ditemukan: {MODEL_PATH}")
        st.stop()
<<<<<<< HEAD
<<<<<<< HEAD

    classes    = _get_classes_from_checkpoint(MODEL_PATH)
    num_classes = len(classes)

=======
    classes     = _get_classes_from_checkpoint(MODEL_PATH)
    num_classes = len(classes)
>>>>>>> 4634d35 (update WebRCT using metered.ca)
=======

    classes    = _get_classes_from_checkpoint(MODEL_PATH)
    num_classes = len(classes)

>>>>>>> 49273b9 (New layout and features)
    model = timm.create_model(
        "vit_small_patch14_dinov2.lvd142m",
        pretrained=False,
        img_size=IMG_SIZE,
    )
    in_features = getattr(model, "num_features", None) or getattr(model, "embed_dim", None)
    model.head  = nn.Linear(in_features, num_classes)
<<<<<<< HEAD
<<<<<<< HEAD

    state_dict = torch.load(MODEL_PATH, map_location=DEVICE)
=======
    state_dict  = torch.load(MODEL_PATH, map_location=DEVICE)
>>>>>>> 4634d35 (update WebRCT using metered.ca)
=======

    state_dict = torch.load(MODEL_PATH, map_location=DEVICE)
>>>>>>> 49273b9 (New layout and features)
    model.load_state_dict(state_dict)
    model.eval()
    model.to(DEVICE)
    return model, classes


<<<<<<< HEAD
<<<<<<< HEAD
# ══════════════════════════════════════════════════════════════════════════════
# CIRCLE DETECTION (Hanya deteksi & buat mask, tanpa apply crop dulu)
# ══════════════════════════════════════════════════════════════════════════════
def detect_circle_mask(gray: np.ndarray) -> tuple[np.ndarray | None, bool, tuple | None]:
    """
    Deteksi lingkaran terbesar pada gambar grayscale menggunakan HoughCircles.
    Menghasilkan mask biner, tetapi BELUM meng-aplikasikannya ke gambar.
    """
    h, w    = gray.shape
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp       = 1.2,
        minDist  = min(h, w) * 0.4,
        param1   = 100,
        param2   = 40,
        minRadius= int(min(h, w) * 0.2),
        maxRadius= int(min(h, w) * 0.55),
    )

    if circles is None:
        return None, False, None

    circles = np.round(circles[0]).astype(int)
    cx, cy, r = max(circles, key=lambda c: c[2])

    # Buat circular mask
    mask = np.zeros_like(gray)
    cv2.circle(mask, (cx, cy), r, 255, thickness=-1)

    return mask, True, (cx, cy, r)


def draw_circle_overlay(img_rgb: np.ndarray, cx: int, cy: int, r: int) -> np.ndarray:
    overlay = img_rgb.copy()
    cv2.circle(overlay, (cx, cy), r, (0, 220, 0), 3)
    cv2.circle(overlay, (cx, cy), 4, (0, 220, 0), -1)
    return overlay


# ══════════════════════════════════════════════════════════════════════════════
# PREPROCESSING PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
=======
════
# CIRCLE DETECTION
════
=======
# ══════════════════════════════════════════════════════════════════════════════
# CIRCLE DETECTION (Hanya deteksi & buat mask, tanpa apply crop dulu)
# ══════════════════════════════════════════════════════════════════════════════
>>>>>>> 49273b9 (New layout and features)
def detect_circle_mask(gray: np.ndarray) -> tuple[np.ndarray | None, bool, tuple | None]:
    """
    Deteksi lingkaran terbesar pada gambar grayscale menggunakan HoughCircles.
    Menghasilkan mask biner, tetapi BELUM meng-aplikasikannya ke gambar.
    """
    h, w    = gray.shape
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp       = 1.2,
        minDist  = min(h, w) * 0.4,
        param1   = 100,
        param2   = 40,
        minRadius= int(min(h, w) * 0.2),
        maxRadius= int(min(h, w) * 0.55),
    )

    if circles is None:
        return None, False, None

    circles = np.round(circles[0]).astype(int)
    cx, cy, r = max(circles, key=lambda c: c[2])

    # Buat circular mask
    mask = np.zeros_like(gray)
    cv2.circle(mask, (cx, cy), r, 255, thickness=-1)

    return mask, True, (cx, cy, r)


def draw_circle_overlay(img_rgb: np.ndarray, cx: int, cy: int, r: int) -> np.ndarray:
    overlay = img_rgb.copy()
    cv2.circle(overlay, (cx, cy), r, (0, 220, 0), 3)
    cv2.circle(overlay, (cx, cy), 4, (0, 220, 0), -1)
    return overlay


<<<<<<< HEAD
════
# PREPROCESSING PIPELINE (exposure & sharpen bisa dikontrol)
════
>>>>>>> 4634d35 (update WebRCT using metered.ca)
=======
# ══════════════════════════════════════════════════════════════════════════════
# PREPROCESSING PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
>>>>>>> 49273b9 (New layout and features)
_transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


<<<<<<< HEAD
<<<<<<< HEAD
def preprocess(img_rgb: np.ndarray) -> dict:
    """
    Pipeline lengkap:
        RGB
         → Grayscale
         → (Deteksi Lingkaran & Buat Mask)
         → Inversi Warna (Seluruh gambar)
         → Exposure +30% (Seluruh gambar)
         → Unsharp Mask / Sharpen (Seluruh gambar)
         → Crop / Terapkan Mask (Luar lingkaran jadi hitam)
         → 3-channel replicate
         → Resize + Normalize (tensor)
=======
def preprocess(img_rgb: np.ndarray,
               exposure: float = DEFAULT_EXPOSURE,
               sharpen_amt: float = DEFAULT_SHARPEN_AMT) -> dict:
    """
    Pipeline lengkap dengan exposure & sharpen yang dapat dikonfigurasi.
>>>>>>> 4634d35 (update WebRCT using metered.ca)
=======
def preprocess(img_rgb: np.ndarray) -> dict:
    """
    Pipeline lengkap:
        RGB
         → Grayscale
         → (Deteksi Lingkaran & Buat Mask)
         → Inversi Warna (Seluruh gambar)
         → Exposure +30% (Seluruh gambar)
         → Unsharp Mask / Sharpen (Seluruh gambar)
         → Crop / Terapkan Mask (Luar lingkaran jadi hitam)
         → 3-channel replicate
         → Resize + Normalize (tensor)
>>>>>>> 49273b9 (New layout and features)
    """
    # 1. Grayscale
    gray = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2GRAY)

<<<<<<< HEAD
<<<<<<< HEAD
    # 2. Deteksi lingkaran (hanya dapatkan mask & info, gambar belum di-crop)
=======
    # 2. Deteksi lingkaran
>>>>>>> 4634d35 (update WebRCT using metered.ca)
=======
    # 2. Deteksi lingkaran (hanya dapatkan mask & info, gambar belum di-crop)
>>>>>>> 49273b9 (New layout and features)
    mask, circle_found, circle_info = detect_circle_mask(gray)

    # 3. Inversi Warna
    inverted = cv2.bitwise_not(gray)

<<<<<<< HEAD
<<<<<<< HEAD
    # 4. Exposure +30%
    exposed = cv2.convertScaleAbs(inverted, alpha=1.3, beta=0)

    # 5. Sharpen via Unsharp Mask
    blurred   = cv2.GaussianBlur(exposed, (0, 0), sigmaX=3)
    sharpened = cv2.addWeighted(exposed, 1.5, blurred, -0.5, 0)

    # 6. Crop (Terapkan mask setelah sharpen)
=======
    # 4. Exposure (alpha = exposure factor)
    exposed = cv2.convertScaleAbs(inverted, alpha=exposure, beta=0)
=======
    # 4. Exposure +30%
    exposed = cv2.convertScaleAbs(inverted, alpha=1.3, beta=0)
>>>>>>> 49273b9 (New layout and features)

    # 5. Sharpen via Unsharp Mask
    blurred   = cv2.GaussianBlur(exposed, (0, 0), sigmaX=3)
    sharpened = cv2.addWeighted(exposed, 1.5, blurred, -0.5, 0)

<<<<<<< HEAD
    # 6. Crop (apply mask setelah sharpen)
>>>>>>> 4634d35 (update WebRCT using metered.ca)
=======
    # 6. Crop (Terapkan mask setelah sharpen)
>>>>>>> 49273b9 (New layout and features)
    if circle_found and mask is not None:
        cropped = cv2.bitwise_and(sharpened, sharpened, mask=mask)
    else:
        cropped = sharpened.copy()

<<<<<<< HEAD
<<<<<<< HEAD
    # 7. 3-channel untuk model
=======
    # 7. 3-channel
>>>>>>> 4634d35 (update WebRCT using metered.ca)
=======
    # 7. 3-channel untuk model
>>>>>>> 49273b9 (New layout and features)
    rgb_3ch = cv2.merge([cropped, cropped, cropped])

    # 8. Transform ke tensor
    tensor = _transform(rgb_3ch).unsqueeze(0).to(DEVICE)

<<<<<<< HEAD
<<<<<<< HEAD
    # 9. Overlay lingkaran di gambar asli (display saja)
=======
    # 9. Overlay lingkaran di gambar asli (display)
>>>>>>> 4634d35 (update WebRCT using metered.ca)
=======
    # 9. Overlay lingkaran di gambar asli (display saja)
>>>>>>> 49273b9 (New layout and features)
    annotated = img_rgb.copy()
    if circle_found and circle_info:
        cx, cy, r = circle_info
        annotated = draw_circle_overlay(img_rgb, cx, cy, r)

    return {
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 49273b9 (New layout and features)
        "tensor"        : tensor,
        "gray"          : gray,
        "inverted"      : inverted,
        "exposed"       : exposed,
        "sharpened"     : sharpened,
        "cropped"       : cropped,
        "annotated_rgb" : annotated,
        "circle_found"  : circle_found,
        "circle_info"   : circle_info,
<<<<<<< HEAD
    }


# ══════════════════════════════════════════════════════════════════════════════
# INFERENCE
# ══════════════════════════════════════════════════════════════════════════════
=======
        "tensor"       : tensor,
        "gray"         : gray,
        "inverted"     : inverted,
        "exposed"      : exposed,
        "sharpened"    : sharpened,
        "cropped"      : cropped,
        "annotated_rgb": annotated,
        "circle_found" : circle_found,
        "circle_info"  : circle_info,
=======
>>>>>>> 49273b9 (New layout and features)
    }


# ══════════════════════════════════════════════════════════════════════════════
# INFERENCE
<<<<<<< HEAD
════
>>>>>>> 4634d35 (update WebRCT using metered.ca)
=======
# ══════════════════════════════════════════════════════════════════════════════
>>>>>>> 49273b9 (New layout and features)
@torch.no_grad()
def predict(model: nn.Module, tensor: torch.Tensor,
            classes: list[str]) -> tuple[str, float, np.ndarray]:
    logits = model(tensor)
    probs  = torch.softmax(logits, dim=1)[0]
    idx    = probs.argmax().item()
    return classes[idx], float(probs[idx]) * 100, probs.cpu().numpy()


<<<<<<< HEAD
<<<<<<< HEAD
# ══════════════════════════════════════════════════════════════════════════════
# UI HELPERS
# ══════════════════════════════════════════════════════════════════════════════
ICONS = {"crack": "🔴", "spot": "🟡", "pinhole": "🔵", "normal": "🟢"}

def apply_threshold(label: str, conf: float) -> tuple[str, str | None]:
    if label in DEFECT_CLASSES_FOR_THRESHOLD and conf < CONFIDENCE_THRESHOLD:
=======
════
=======
# ══════════════════════════════════════════════════════════════════════════════
>>>>>>> 49273b9 (New layout and features)
# UI HELPERS
# ══════════════════════════════════════════════════════════════════════════════
ICONS = {"crack": "🔴", "spot": "🟡", "pinhole": "🔵", "normal": "🟢"}

<<<<<<< HEAD

def apply_threshold(label: str, conf: float,
                    threshold: float = DEFAULT_CONF_THRESH) -> tuple[str, str | None]:
    if label in DEFECT_CLASSES_FOR_THRESHOLD and conf < threshold:
>>>>>>> 4634d35 (update WebRCT using metered.ca)
=======
def apply_threshold(label: str, conf: float) -> tuple[str, str | None]:
    if label in DEFECT_CLASSES_FOR_THRESHOLD and conf < CONFIDENCE_THRESHOLD:
>>>>>>> 49273b9 (New layout and features)
        return "normal", label
    return label, None


def show_result(label: str, conf: float, probs: np.ndarray,
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 49273b9 (New layout and features)
                classes: list[str], circle_found: bool, 
                original_label: str | None = None) -> None:
    
    # Pesan khusus jika lingkaran tidak terdeteksi
<<<<<<< HEAD
    if not circle_found:
        st.error("⚠️ **Lingkaran piring tidak terdeteksi.** Kemungkinan: Piring tidak berbentuk lingkaran, piring terlalu rusak, atau objek bukanlah piring.")
        st.info("ℹ️ Model tetap dijalankan pada gambar penuh, namun hasil prediksi mungkin tidak akurat.")
    
    icon = ICONS.get(label, "⚪")
    
    if label == "normal" and original_label:
        st.markdown(f"### {icon} Prediksi: `NORMAL (TIDAK ADA DEFEK)`")
        st.info(
            f"ℹ️ Model mendeteksi indikasi **'{original_label}'** dengan confidence **{conf:.1f}%**, "
            f"namun karena di bawah threshold ({CONFIDENCE_THRESHOLD}%), piring dinyatakan **NORMAL**."
        )
    else:
        st.markdown(f"### {icon} Prediksi: `{label.upper()}` — {conf:.1f}%")
        
    for i, cls in enumerate(classes):
        st.progress(float(probs[i]), text=f"{cls}: {probs[i]*100:.1f}%")


def show_pipeline_images(orig_rgb: np.ndarray, result: dict) -> None:
    st.markdown("#### 🖼️ Pipeline Gambar")

    # Baris 1: Original, Grayscale, Inversi Warna
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(result["annotated_rgb"],
                 caption="① Original + Deteksi Lingkaran",
                 use_container_width=True)
    with col2:
        st.image(result["gray"],
                 caption="② Grayscale",
                 use_container_width=True, clamp=True)
    with col3:
        st.image(result["inverted"],
                 caption="③ Inversi Warna (Seluruh Gambar)",
                 use_container_width=True, clamp=True)

    # Baris 2: Exposure, Sharpened, Crop
    col4, col5, col6 = st.columns(3)
    with col4:
        st.image(result["exposed"],
                 caption="④ Exposure +30%",
                 use_container_width=True, clamp=True)
    with col5:
        st.image(result["sharpened"],
                 caption="⑤ Sharpened (Seluruh Gambar)",
                 use_container_width=True, clamp=True)
    with col6:
        label_crop = ("⑥ Crop (Luar Lingkaran Hitam)" if result["circle_found"] 
                      else "⑥ Crop Gagal (Lingkaran Tidak Terdeteksi)")
        st.image(result["cropped"],
                 caption=label_crop,
                 use_container_width=True, clamp=True)


# ══════════════════════════════════════════════════════════════════════════════
# STREAMLIT APP
# ══════════════════════════════════════════════════════════════════════════════
def main() -> None:
    st.set_page_config(page_title="Ceramic Defect Detector", layout="centered")
    st.title("🔍 Ceramic Tile Defect Detector")
=======
                classes: list[str], circle_found: bool,
                original_label: str | None = None,
                threshold: float = DEFAULT_CONF_THRESH) -> None:
=======
>>>>>>> 49273b9 (New layout and features)
    if not circle_found:
        st.error("⚠️ **Lingkaran piring tidak terdeteksi.** Kemungkinan: Piring tidak berbentuk lingkaran, piring terlalu rusak, atau objek bukanlah piring.")
        st.info("ℹ️ Model tetap dijalankan pada gambar penuh, namun hasil prediksi mungkin tidak akurat.")
    
    icon = ICONS.get(label, "⚪")
    
    if label == "normal" and original_label:
        st.markdown(f"### {icon} Prediksi: `NORMAL (TIDAK ADA DEFEK)`")
        st.info(
            f"ℹ️ Model mendeteksi indikasi **'{original_label}'** dengan confidence **{conf:.1f}%**, "
            f"namun karena di bawah threshold ({CONFIDENCE_THRESHOLD}%), piring dinyatakan **NORMAL**."
        )
    else:
        st.markdown(f"### {icon} Prediksi: `{label.upper()}` — {conf:.1f}%")
        
    for i, cls in enumerate(classes):
        st.progress(float(probs[i]), text=f"{cls}: {probs[i]*100:.1f}%")


def show_pipeline_images(orig_rgb: np.ndarray, result: dict) -> None:
    st.markdown("#### 🖼️ Pipeline Gambar")

    # Baris 1: Original, Grayscale, Inversi Warna
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(result["annotated_rgb"],
                 caption="① Original + Deteksi Lingkaran",
                 use_container_width=True)
    with col2:
        st.image(result["gray"],
                 caption="② Grayscale",
                 use_container_width=True, clamp=True)
    with col3:
        st.image(result["inverted"],
                 caption="③ Inversi Warna (Seluruh Gambar)",
                 use_container_width=True, clamp=True)

    # Baris 2: Exposure, Sharpened, Crop
    col4, col5, col6 = st.columns(3)
    with col4:
        st.image(result["exposed"],
                 caption="④ Exposure +30%",
                 use_container_width=True, clamp=True)
    with col5:
        st.image(result["sharpened"],
                 caption="⑤ Sharpened (Seluruh Gambar)",
                 use_container_width=True, clamp=True)
    with col6:
        label_crop = ("⑥ Crop (Luar Lingkaran Hitam)" if result["circle_found"] 
                      else "⑥ Crop Gagal (Lingkaran Tidak Terdeteksi)")
        st.image(result["cropped"],
                 caption=label_crop,
                 use_container_width=True, clamp=True)


# ══════════════════════════════════════════════════════════════════════════════
# STREAMLIT APP
# ══════════════════════════════════════════════════════════════════════════════
def main() -> None:
<<<<<<< HEAD
    st.set_page_config(
        page_title="Ceramic Defect Detector",
        page_icon="",
        layout="centered",
    )

    st.title("Ceramic Tile Defect Detector")
>>>>>>> 4634d35 (update WebRCT using metered.ca)
=======
    st.set_page_config(page_title="Ceramic Defect Detector", layout="centered")
    st.title("🔍 Ceramic Tile Defect Detector")
>>>>>>> 49273b9 (New layout and features)

    init_db()
    model, classes = load_model()

    st.caption(
        f"Model: DINOv2 ViT-Small · Device: {DEVICE} · "
<<<<<<< HEAD
<<<<<<< HEAD
        f"Classes ({len(classes)}): {', '.join(classes)} · "
        f"Threshold Defek: {CONFIDENCE_THRESHOLD}%"
    )

    tab_upload, tab_webcam, tab_history = st.tabs([
        "📤 Upload Gambar",
        "📷 Webcam Live",
        "📋 Riwayat Prediksi",
    ])

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 1 — UPLOAD
    # ══════════════════════════════════════════════════════════════════════════
    with tab_upload:
        st.subheader("Upload Gambar Keramik")
=======
        f"Kelas ({len(classes)}): {', '.join(classes)}"
=======
        f"Classes ({len(classes)}): {', '.join(classes)} · "
        f"Threshold Defek: {CONFIDENCE_THRESHOLD}%"
>>>>>>> 49273b9 (New layout and features)
    )

    tab_upload, tab_webcam, tab_history = st.tabs([
        "📤 Upload Gambar",
        "📷 Webcam Live",
        "📋 Riwayat Prediksi",
    ])

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 1 — UPLOAD
    # ══════════════════════════════════════════════════════════════════════════
    with tab_upload:
        st.subheader("Upload Gambar Keramik")
<<<<<<< HEAD

        # ── Pipeline Controls (inline) ─────────────────────────────────────────
        with st.expander("Pipeline Controls", expanded=False):
            uc1, uc2, uc3 = st.columns(3)
            with uc1:
                up_exposure = st.slider(
                    "Exposure (alpha)", min_value=0.5, max_value=3.0,
                    value=DEFAULT_EXPOSURE, step=0.05, key="up_exposure",
                    help="Kecerahan setelah inversi. >1 = terang, <1 = gelap.",
                )
            with uc2:
                up_sharpen = st.slider(
                    "Sharpening", min_value=1.0, max_value=5.0,
                    value=DEFAULT_SHARPEN_AMT, step=0.1, key="up_sharpen",
                    help="Intensitas Unsharp Mask.",
                )
            with uc3:
                up_threshold = st.slider(
                    "Threshold Defek (%)", min_value=30.0, max_value=99.0,
                    value=DEFAULT_CONF_THRESH, step=1.0, key="up_threshold",
                    help="Confidence di bawah ini → dianggap NORMAL.",
                )
            st.caption(
                f"Aktif: Exposure **×{up_exposure:.2f}** · "
                f"Sharpen **×{up_sharpen:.1f}** · "
                f"Threshold **{up_threshold:.0f}%**"
            )

>>>>>>> 4634d35 (update WebRCT using metered.ca)
=======
>>>>>>> 49273b9 (New layout and features)
        uploaded = st.file_uploader(
            "Pilih gambar (.jpg / .jpeg / .png)",
            type=["jpg", "jpeg", "png"],
        )

        if uploaded is not None:
            pil_img   = Image.open(uploaded).convert("RGB")
            img_array = np.array(pil_img)

<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 49273b9 (New layout and features)
            result             = preprocess(img_array)
            raw_label, conf, probs = predict(model, result["tensor"], classes)
            
            # Terapkan Threshold
            final_label, original_label = apply_threshold(raw_label, conf)
<<<<<<< HEAD

            st.divider()
            show_pipeline_images(img_array, result)

            st.divider()
            show_result(final_label, conf, probs, classes, 
                        result["circle_found"], original_label)

            save_prediction("upload", uploaded.name, final_label, conf, result["circle_found"])
            st.success("✅ Prediksi disimpan ke database.")

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 2 — WEBCAM LIVE
    # ══════════════════════════════════════════════════════════════════════════
=======
            with st.spinner("Memproses gambar…"):
                result             = preprocess(img_array, exposure=up_exposure, sharpen_amt=up_sharpen)
                raw_label, conf, probs = predict(model, result["tensor"], classes)
                final_label, original_label = apply_threshold(raw_label, conf, up_threshold)
=======
>>>>>>> 49273b9 (New layout and features)

            st.divider()
            show_pipeline_images(img_array, result)

            st.divider()
            show_result(final_label, conf, probs, classes, 
                        result["circle_found"], original_label)

            save_prediction("upload", uploaded.name, final_label, conf, result["circle_found"])
            st.success("✅ Prediksi disimpan ke database.")

<<<<<<< HEAD
    
    # TAB 2 — WEBCAM LIVE (UPGRADED)
    
>>>>>>> 4634d35 (update WebRCT using metered.ca)
=======
    # ══════════════════════════════════════════════════════════════════════════
    # TAB 2 — WEBCAM LIVE
    # ══════════════════════════════════════════════════════════════════════════
>>>>>>> 49273b9 (New layout and features)
    with tab_webcam:
        st.subheader("Live Webcam Detection")

        if not WEBRTC_AVAILABLE:
            st.error(
                "Paket `streamlit-webrtc` dan `av` belum terinstall.\n\n"
                "Jalankan: `pip install streamlit-webrtc av`"
            )
        else:
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> 49273b9 (New layout and features)
            st.info(
                "Pipeline per frame: **BGR → RGB → Grayscale → Inversi Warna → "
                "Exposure +30% → Sharpen → Crop → Model → Threshold**\n\n"
                "Overlay hijau = piring normal (di bawah threshold defek)."
            )
<<<<<<< HEAD

            class DefectProcessor(VideoProcessorBase):
                def __init__(self) -> None:
                    self._model   = model
                    self._classes = classes
                    self.result   = {"label": "-", "conf": 0.0, "circle": False, "original_label": None}

                def recv(self, frame: "av.VideoFrame") -> "av.VideoFrame":
                    img_bgr = frame.to_ndarray(format="bgr24")
                    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

                    res               = preprocess(img_rgb)
                    raw_label, conf, _ = predict(self._model, res["tensor"], self._classes)
                    
                    # Terapkan Threshold
                    final_label, original_label = apply_threshold(raw_label, conf)
                    
                    self.result = {
                        "label": final_label, 
                        "conf": conf, 
                        "circle": res["circle_found"],
                        "original_label": original_label
                    }

                    # Gunakan gambar yang sudah di-crop untuk ditampilkan di webcam
                    out_bgr = cv2.cvtColor(res["cropped"], cv2.COLOR_GRAY2BGR)

                    # Tampilan teks dan lingkaran pada Webcam
                    if res["circle_found"] and res["circle_info"]:
                        cx, cy, r = res["circle_info"]
                        h0, w0 = img_bgr.shape[:2]
                        h1, w1 = res["cropped"].shape[:2]
                        sx, sy = w1 / w0, h1 / h0
                        cx2, cy2, r2 = int(cx * sx), int(cy * sy), int(r * min(sx, sy))
                        cv2.circle(out_bgr, (cx2, cy2), r2, (0, 220, 0), 2)
                        
                        if final_label == "normal":
                            text = f"NORMAL ({raw_label}: {conf:.1f}%)"
                            text_color = (0, 255, 0)  # Hijau
                        else:
                            text = f"{final_label.upper()}: {conf:.1f}%"
                            text_color = (0, 0, 255)  # Merah untuk defek
                    else:
                        text = "BUKAN PIRING / RUSAK"
                        text_color = (0, 165, 255)  # Oranye

                    cv2.putText(out_bgr, text, (10, 35),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, text_color, 2, cv2.LINE_AA)

                    return av.VideoFrame.from_ndarray(out_bgr, format="bgr24")

            RTC_CONFIG = RTCConfiguration(
                {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
            )
=======
            # ── Pipeline Controls (inline) ─────────────────────────────────────
            with st.expander("Pipeline Controls", expanded=True):
                wc1, wc2, wc3 = st.columns(3)
                with wc1:
                    wc_exposure = st.slider(
                        "Exposure (alpha)", min_value=0.5, max_value=3.0,
                        value=DEFAULT_EXPOSURE, step=0.05, key="wc_exposure",
                        help="Kecerahan setelah inversi. >1 = terang, <1 = gelap.",
                    )
                with wc2:
                    wc_sharpen = st.slider(
                        "Sharpening", min_value=1.0, max_value=5.0,
                        value=DEFAULT_SHARPEN_AMT, step=0.1, key="wc_sharpen",
                        help="Intensitas Unsharp Mask.",
                    )
                with wc3:
                    wc_threshold = st.slider(
                        "Threshold Defek (%)", min_value=30.0, max_value=99.0,
                        value=DEFAULT_CONF_THRESH, step=1.0, key="wc_threshold",
                        help="Confidence di bawah ini → dianggap NORMAL.",
                    )
                st.caption(
                    f"Pipeline aktif: BGR → Grayscale → Inversi → "
                    f"Exposure x{wc_exposure:.2f} → "
                    f"Sharpen x{wc_sharpen:.1f} → "
                    f"Crop → Model → Threshold {wc_threshold:.0f}%"
                )
=======
>>>>>>> 49273b9 (New layout and features)

            class DefectProcessor(VideoProcessorBase):
                def __init__(self) -> None:
                    self._model   = model
                    self._classes = classes
                    self.result   = {"label": "-", "conf": 0.0, "circle": False, "original_label": None}

                def recv(self, frame: "av.VideoFrame") -> "av.VideoFrame":
                    img_bgr = frame.to_ndarray(format="bgr24")
                    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

                    res               = preprocess(img_rgb)
                    raw_label, conf, _ = predict(self._model, res["tensor"], self._classes)
                    
                    # Terapkan Threshold
                    final_label, original_label = apply_threshold(raw_label, conf)
                    
                    self.result = {
                        "label": final_label, 
                        "conf": conf, 
                        "circle": res["circle_found"],
                        "original_label": original_label
                    }

                    # Gunakan gambar yang sudah di-crop untuk ditampilkan di webcam
                    out_bgr = cv2.cvtColor(res["cropped"], cv2.COLOR_GRAY2BGR)

                    # Tampilan teks dan lingkaran pada Webcam
                    if res["circle_found"] and res["circle_info"]:
                        cx, cy, r = res["circle_info"]
                        h0, w0 = img_bgr.shape[:2]
                        h1, w1 = res["cropped"].shape[:2]
                        sx, sy = w1 / w0, h1 / h0
                        cx2, cy2, r2 = int(cx * sx), int(cy * sy), int(r * min(sx, sy))
                        cv2.circle(out_bgr, (cx2, cy2), r2, (0, 220, 0), 2)
                        
                        if final_label == "normal":
                            text = f"NORMAL ({raw_label}: {conf:.1f}%)"
                            text_color = (0, 255, 0)  # Hijau
                        else:
                            text = f"{final_label.upper()}: {conf:.1f}%"
                            text_color = (0, 0, 255)  # Merah untuk defek
                    else:
                        text = "BUKAN PIRING / RUSAK"
                        text_color = (0, 165, 255)  # Oranye

                    cv2.putText(out_bgr, text, (10, 35),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.0, text_color, 2, cv2.LINE_AA)

                    return av.VideoFrame.from_ndarray(out_bgr, format="bgr24")

<<<<<<< HEAD
                def get_fps(self) -> float:
                    ft = self._frame_times
                    if len(ft) < 2:
                        return 0.0
                    elapsed = ft[-1] - ft[0]
                    return (len(ft) - 1) / elapsed if elapsed > 0 else 0.0

            # ── WebRTC streamer 
            _METERED_USERNAME = os.environ.get("METERED_USERNAME", "")
            _METERED_PASSWORD = os.environ.get("METERED_PASSWORD", "")

            RTC_CONFIG = RTCConfiguration({
                "iceServers": [
                    {"urls": ["stun:stun.relay.metered.ca:80"]},
                    {
                        "urls": ["turn:standard.relay.metered.ca:80"],
                        "username": _METERED_USERNAME,
                        "credential": _METERED_PASSWORD,
                    },
                    {
                        "urls": ["turn:standard.relay.metered.ca:80?transport=tcp"],
                        "username": _METERED_USERNAME,
                        "credential": _METERED_PASSWORD,
                    },
                    {
                        "urls": ["turn:standard.relay.metered.ca:443"],
                        "username": _METERED_USERNAME,
                        "credential": _METERED_PASSWORD,
                    },
                    {
                        "urls": ["turns:standard.relay.metered.ca:443?transport=tcp"],
                        "username": _METERED_USERNAME,
                        "credential": _METERED_PASSWORD,
                    },
                ]
            })
>>>>>>> 4634d35 (update WebRCT using metered.ca)
=======
            RTC_CONFIG = RTCConfiguration(
                {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
            )
>>>>>>> 49273b9 (New layout and features)

            ctx = webrtc_streamer(
                key="ceramic-defect-live",
                video_processor_factory=DefectProcessor,
                rtc_configuration=RTC_CONFIG,
<<<<<<< HEAD
<<<<<<< HEAD
                media_stream_constraints={"video": True, "audio": False},
                async_processing=True,
            )

            if ctx.video_processor:
                res = ctx.video_processor.result
                
                # Tampilan status di bawah webcam
                if not res["circle"]:
                    st.error("⚠️ **Lingkaran piring tidak terdeteksi.** Kemungkinan: Piring tidak berbentuk lingkaran, piring terlalu rusak, atau objek bukanlah piring.")
                else:
                    circle_txt = "✅ terdeteksi"
                    if res["label"] == "normal":
                        st.markdown(
                            f"**Live →** 🟢 `NORMAL` — Deteksi {res['original_label']} ({res['conf']:.1f}%) "
                            f"dibawah threshold | Lingkaran: {circle_txt}"
                        )
                    else:
                        st.markdown(
                            f"**Live →** `{res['label'].upper()}` — {res['conf']:.1f}%  "
                            f"| Lingkaran: {circle_txt}"
                        )
                    
                if st.button("💾 Simpan Prediksi Sekarang"):
                    save_prediction("webcam", "live_frame",
                                    res["label"], res["conf"], res["circle"])
                    st.success(f"Disimpan: {res['label']} ({res['conf']:.1f}%)")

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 3 — HISTORY
    # ══════════════════════════════════════════════════════════════════════════
    with tab_history:
        st.subheader("Riwayat Prediksi (30 terakhir)")

        col_r, col_c = st.columns(2)
        with col_r:
            if st.button("🔄 Refresh"):
                st.rerun()
        with col_c:
            if st.button("🗑️ Hapus Semua"):
=======
                media_stream_constraints={
                    "video": {
                        "width": {"ideal": 640},
                        "height": {"ideal": 480},
                        "frameRate": {"ideal": 15},
                    },
                    "audio": False,
                },
=======
                media_stream_constraints={"video": True, "audio": False},
>>>>>>> 49273b9 (New layout and features)
                async_processing=True,
            )

            if ctx.video_processor:
                res = ctx.video_processor.result
                
                # Tampilan status di bawah webcam
                if not res["circle"]:
                    st.error("⚠️ **Lingkaran piring tidak terdeteksi.** Kemungkinan: Piring tidak berbentuk lingkaran, piring terlalu rusak, atau objek bukanlah piring.")
                else:
                    circle_txt = "✅ terdeteksi"
                    if res["label"] == "normal":
                        st.markdown(
                            f"**Live →** 🟢 `NORMAL` — Deteksi {res['original_label']} ({res['conf']:.1f}%) "
                            f"dibawah threshold | Lingkaran: {circle_txt}"
                        )
                    else:
                        st.markdown(
                            f"**Live →** `{res['label'].upper()}` — {res['conf']:.1f}%  "
                            f"| Lingkaran: {circle_txt}"
                        )
                    
                if st.button("💾 Simpan Prediksi Sekarang"):
                    save_prediction("webcam", "live_frame",
                                    res["label"], res["conf"], res["circle"])
                    st.success(f"Disimpan: {res['label']} ({res['conf']:.1f}%)")

    # ══════════════════════════════════════════════════════════════════════════
    # TAB 3 — HISTORY
    # ══════════════════════════════════════════════════════════════════════════
    with tab_history:
        st.subheader("Riwayat Prediksi (30 terakhir)")

        col_r, col_c = st.columns(2)
        with col_r:
            if st.button("🔄 Refresh"):
                st.rerun()
        with col_c:
<<<<<<< HEAD
            if st.button("Hapus Semua"):
>>>>>>> 4634d35 (update WebRCT using metered.ca)
=======
            if st.button("🗑️ Hapus Semua"):
>>>>>>> 49273b9 (New layout and features)
                clear_history()
                st.success("Riwayat dihapus.")
                st.rerun()

        rows = get_history()
        if rows:
<<<<<<< HEAD
<<<<<<< HEAD
=======
            # Filter
            all_labels = sorted({r[3] for r in rows})
            filter_label = st.multiselect("Filter Label", options=all_labels, default=all_labels)
            filtered = [r for r in rows if r[3] in filter_label]

>>>>>>> 4634d35 (update WebRCT using metered.ca)
=======
>>>>>>> 49273b9 (New layout and features)
            st.table([
                {
                    "ID"           : r[0],
                    "Source"       : r[1],
                    "File"         : r[2],
                    "Label"        : r[3],
                    "Conf (%)"     : f"{r[4]:.2f}",
<<<<<<< HEAD
<<<<<<< HEAD
                    "Circle Found" : "✅" if r[5] else "❌",
                    "Waktu"        : r[6],
                }
                for r in rows
=======
                    "Circle"       : "Ya" if r[5] else "Tidak",
                    "Exposure"     : f"x{r[6]:.2f}" if r[6] else "-",
                    "Sharpen"      : f"x{r[7]:.1f}" if r[7] else "-",
                    "Waktu"        : r[8],
                }
                for r in filtered
>>>>>>> 4634d35 (update WebRCT using metered.ca)
=======
                    "Circle Found" : "✅" if r[5] else "❌",
                    "Waktu"        : r[6],
                }
                for r in rows
>>>>>>> 49273b9 (New layout and features)
            ])
        else:
            st.info("Belum ada prediksi tersimpan.")

<<<<<<< HEAD
<<<<<<< HEAD

if __name__ == "__main__":
    main()

    #BDCIHBHIVBOEUFBVIERBCI
=======
    
    # TAB 4 — ANALITIK
    
    with tab_analytics:
        st.subheader("Analitik Prediksi")

        if st.button("Refresh Analitik"):
            st.rerun()

        stats = get_stats()

        # Summary metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Prediksi", stats["total"])
        m2.metric("Rata-rata Confidence", f"{stats['avg_conf']:.1f}%")
        m3.metric("Jumlah Kelas Terdeteksi", len(stats["by_label"]))

        if stats["by_label"]:
            st.divider()
            st.markdown("#### Distribusi Label")

            # Bar chart sederhana via st.bar_chart
            label_data = {row[0]: row[1] for row in stats["by_label"]}
            st.bar_chart(label_data)

            st.markdown("#### Detail per Label")
            total = stats["total"] or 1
            for lbl, cnt in stats["by_label"]:
                pct = cnt / total * 100
                st.progress(pct / 100, text=f"{lbl}: {cnt} prediksi ({pct:.1f}%)")
        else:
            st.info("Belum ada data untuk dianalisis. Jalankan beberapa prediksi terlebih dahulu.")

        # Tabel confidence per label dari riwayat
        rows = get_history(limit=200)
        if rows:
            st.divider()
            st.markdown("#### Statistik Confidence per Label")
            from collections import defaultdict
            label_confs: dict[str, list[float]] = defaultdict(list)
            for r in rows:
                label_confs[r[3]].append(r[4])

            stat_rows = []
            for lbl, confs in sorted(label_confs.items()):
                stat_rows.append({
                    "Label"  : lbl,
                    "Count"  : len(confs),
                    "Min %"  : f"{min(confs):.1f}",
                    "Max %"  : f"{max(confs):.1f}",
                    "Avg %"  : f"{sum(confs)/len(confs):.1f}",
                })
            st.table(stat_rows)


if __name__ == "__main__":
    main()
>>>>>>> 4634d35 (update WebRCT using metered.ca)
=======

if __name__ == "__main__":
    main()

    #BDCIHBHIVBOEUFBVIERBCI
>>>>>>> 49273b9 (New layout and features)

# AI_Model/demo_app_zeroshot.py
# Sama tiedosto toimii sekä:
# 1) Streamlit-demon ajamiseen (kun suoritetaan tämä tiedosto)
# 2) Backendin importoitavana mallimoduulina (classify_pil, save_upload)

import io
import os
import uuid
import requests
from typing import Tuple, Dict, List

import torch
import open_clip
from PIL import Image

# Streamlit tuodaan, mutta UI ajetaan vain if __name__ == "__main__" -haaran alla
import streamlit as st  # ok myös backendissä, kunhan emme kutsu st.* importissa

# Käytä samaa label-kirjastoa kuin muualla
from AI_Model.label_packs import LABEL_PACKS

# ---------------------------
#   Backend-moodi (importoitava)
# ---------------------------
DEVICE = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")

_MODEL = None
_PREPROCESS = None
_TOKENIZER = None
_ALL_LABELS: List[str] = []
_LABEL_TO_PACK: Dict[str, str] = {}
_TEXT_FEATS = None

def _all_labels_and_mapping(packs: Dict[str, List[str]]):
    labels, mapping = [], {}
    for pack, items in packs.items():
        for it in items:
            if it not in mapping:   # ensimmäinen osuma jää voimaan
                mapping[it] = pack
            labels.append(it)
    labels = sorted(set(labels))
    return labels, mapping

def _load_backend_model_once():
    """Ladataan malli & tekstivektorit laiskasti 1. kutsulla."""
    global _MODEL, _PREPROCESS, _TOKENIZER, _TEXT_FEATS, _ALL_LABELS, _LABEL_TO_PACK
    if _MODEL is not None:
        return
    _MODEL, _, _PREPROCESS = open_clip.create_model_and_transforms("ViT-L-14", pretrained="openai")
    _MODEL = _MODEL.eval().to(DEVICE)
    _TOKENIZER = open_clip.get_tokenizer("ViT-L-14")
    _ALL_LABELS, _LABEL_TO_PACK = _all_labels_and_mapping(LABEL_PACKS)
    with torch.no_grad(), torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):
        prompts = [f"a photo of a {lbl}" for lbl in _ALL_LABELS]
        tokens = _TOKENIZER(prompts).to(DEVICE)
        _TEXT_FEATS = _MODEL.encode_text(tokens)
        _TEXT_FEATS = _TEXT_FEATS / _TEXT_FEATS.norm(dim=-1, keepdim=True)

def classify_pil(img: Image.Image, topk: int = 5) -> Tuple[str, float, str, List[Tuple[str, float, str]]]:
    """
    Backend-käyttö: luokittelee PIL.Image-kuvan.
    Palauttaa: (paras_label, todennäköisyys, paketin_nimi, topk-lista(label, prob, pack))
    """
    _load_backend_model_once()
    with torch.no_grad(), torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):
        x = _PREPROCESS(img).unsqueeze(0).to(DEVICE)
        f = _MODEL.encode_image(x)
        f = f / f.norm(dim=-1, keepdim=True)
        logits = (100.0 * f @ _TEXT_FEATS.T).softmax(dim=-1)[0]
        k = min(topk, logits.numel())
        vals, idxs = logits.topk(k)

    results = []
    for v, i in zip(vals.tolist(), idxs.tolist()):
        lbl = _ALL_LABELS[i]
        pack = _LABEL_TO_PACK.get(lbl, "Unknown")
        results.append((lbl, float(v), pack))

    best_lbl, best_p, best_pack = results[0]
    return best_lbl, best_p, best_pack, results

def save_upload(file_bytes: bytes, upload_dir: str = "uploads") -> str:
    """
    Backend-käyttö: tallentaa ladatun kuvan JPEG:nä ja palauttaa polun (esim. 'uploads/xxxx.jpg').
    """
    os.makedirs(upload_dir, exist_ok=True)
    fid = f"{uuid.uuid4().hex}.jpg"
    path = os.path.join(upload_dir, fid)
    Image.open(io.BytesIO(file_bytes)).convert("RGB").save(path, format="JPEG", quality=92)
    return path

# ---------------------------
#   Streamlit-demo (vain kun suoritat tämän tiedoston)
# ---------------------------

def _read_image(file) -> Image.Image:
    if isinstance(file, str):
        if file.startswith("http"):
            b = requests.get(file, timeout=20).content
            return Image.open(io.BytesIO(b)).convert("RGB")
        else:
            return Image.open(file).convert("RGB")
    else:
        return Image.open(file).convert("RGB")

def _topk_chunked(image_features, text_features, k=5, chunk_size=2048):
    """Top-k haku suurille label-määrille muistitehokkaasti (chunkit)."""
    best_scores = torch.empty(0, device=image_features.device)
    best_idxs = torch.empty(0, dtype=torch.long, device=image_features.device)

    n = text_features.shape[0]
    for i in range(0, n, chunk_size):
        tf = text_features[i:i+chunk_size]
        logits = (100.0 * image_features @ tf.T).softmax(dim=-1)[0]
        scores, idxs = logits.topk(min(k, logits.numel()), largest=True)
        idxs = idxs + i  # kompensoi chunk-offsetin
        # Yhdistä globaaliksi top-k:ksi
        all_scores = torch.cat([best_scores, scores])
        all_idxs = torch.cat([best_idxs, idxs])
        gk = min(k, all_scores.numel())
        g_scores, order = torch.topk(all_scores, gk)
        g_idxs = all_idxs[order]
        best_scores, best_idxs = g_scores, g_idxs
    return best_scores, best_idxs

def run_streamlit_app():
    st.set_page_config(page_title="Varustevahti (Zero-Shot CLIP)", layout="centered")
    st.title("Varustevahti – Zero-Shot CLIP (Automaattinen)")
    st.write("Malli käy läpi **kaikki** luokat label pack -kirjastosta. Lataa kuva tai syötä URL.")

    # Lataa backend-malli ja tekstivektorit
    _load_backend_model_once()
    st.caption(f"Luokkia: {len(_ALL_LABELS)} (paketteja: {len(LABEL_PACKS)})")

    # Syöte
    col1, col2 = st.columns(2)
    uploaded = col1.file_uploader("Kuva (jpg/png)", type=["jpg","jpeg","png"])
    url = col2.text_input("tai kuvan URL (https://...)")

    top_k = st.slider("Näytä Top-K", min_value=1, max_value=10, value=5, step=1)
    min_conf = st.slider("Vähimmäisvarmuus (%)", 0, 100, 40, step=1) / 100.0

    img = None
    if uploaded is not None:
        img = _read_image(uploaded)
    elif url:
        try:
            img = _read_image(url)
        except Exception as e:
            st.error(f"URL-virhe: {e}")

    if img:
        st.image(img, caption="Syöte", use_column_width=True)
        with torch.no_grad(), torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):
            image = _PREPROCESS(img).unsqueeze(0).to(DEVICE)
            image_features = _MODEL.encode_image(image)
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)

        use_chunking = len(_ALL_LABELS) > 2000
        if use_chunking:
            scores, idxs = _topk_chunked(image_features, _TEXT_FEATS, k=top_k, chunk_size=2048)
            top_indices = idxs.tolist()
            top_scores = scores.tolist()
        else:
            logits = (100.0 * image_features @ _TEXT_FEATS.T).softmax(dim=-1)
            top = logits.topk(k=min(top_k, logits.shape[-1]), dim=-1)
            top_indices = top.indices[0].tolist()
            top_scores = top.values[0].tolist()

        # Paras osuma
        best_idx = top_indices[0]
        best_prob = top_scores[0]
        best_label = _ALL_LABELS[best_idx]
        best_pack = _LABEL_TO_PACK.get(best_label, "Unknown")
        st.subheader("Paras osuma")
        st.markdown(f"**{best_label}** — {best_prob*100:.1f}%  \nLuokkapaketti: *{best_pack}*")

        st.subheader("Top-osumat")
        shown = False
        for rank, (i, prob) in enumerate(zip(top_indices, top_scores), start=1):
            if prob >= min_conf:
                lbl = _ALL_LABELS[i]
                pack = _LABEL_TO_PACK.get(lbl, "Unknown")
                st.write(f"{rank}. **{lbl}** — {prob*100:.1f}%  *(paketti: {pack})*")
                shown = True
        if not shown:
            st.warning("Epävarmaa – säädä luottamusrajaa tai kokeile toista kuvaa.")

if __name__ == "__main__":
    run_streamlit_app()
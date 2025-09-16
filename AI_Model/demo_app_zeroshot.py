import streamlit as st
import torch, open_clip, requests, io
from PIL import Image

st.set_page_config(page_title="Jääkiekko-varusteiden tunnistin (Zero‑Shot CLIP)", layout="centered")

@st.cache_resource
def load_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, _, preprocess = open_clip.create_model_and_transforms(
        "ViT-L-14", pretrained="openai"
    )
    model = model.eval().to(device)
    tokenizer = open_clip.get_tokenizer("ViT-L-14")
    return model, preprocess, tokenizer, device

CLASSES = [
    "blocker (goalie blocker)",
    "gloves (player gloves)",
    "helmet (player helmet)",
    "mask (goalie mask)",
    "mitt (goalie catch glove, trapper)",
    "pads (goalie leg pads)",
    "pants (hockey pants/breezers)",
    "skates (ice hockey skates)",
    "stick (ice hockey stick)",
    "visor (helmet visor)",
]

PROMPTS = [f"a photo of a {c}" for c in CLASSES]

@st.cache_resource
def build_text_encodings(_model, _tokenizer, _device):
    with torch.no_grad(), torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):
        tokens = _tokenizer(PROMPTS).to(_device)
        text_features = _model.encode_text(tokens)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)
    return text_features

def read_image(file) -> Image.Image:
    if isinstance(file, str):
        if file.startswith("http"):
            b = requests.get(file, timeout=20).content
            return Image.open(io.BytesIO(b)).convert("RGB")
        else:
            return Image.open(file).convert("RGB")
    else:
        return Image.open(file).convert("RGB")

st.title("Jääkiekko-varusteiden tunnistin – Zero‑Shot CLIP")
st.write("Ei tarvetta treenaukselle. Lataa kuva tai anna URL.")

model, preprocess, tokenizer, device = load_model()
text_features = build_text_encodings(model, tokenizer, device)

col1, col2 = st.columns(2)
uploaded = col1.file_uploader("Kuva (jpg/png)", type=["jpg","jpeg","png"])
url = col2.text_input("tai kuvan URL (https://...)")

img = None
if uploaded is not None:
    img = read_image(uploaded)
elif url:
    try:
        img = read_image(url)
    except Exception as e:
        st.error(f"URL-virhe: {e}")

if img:
    st.image(img, caption="Syöte", use_column_width=True)
    with torch.no_grad(), torch.cuda.amp.autocast(enabled=torch.cuda.is_available()):
        image = preprocess(img).unsqueeze(0).to(device)
        image_features = model.encode_image(image)
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        logits = (100.0 * image_features @ text_features.T).softmax(dim=-1)
        topk = logits.topk(k=min(5, logits.shape[-1]), dim=-1)
    st.subheader("Tulokset")
    for i in range(topk.indices.shape[-1]):
        cls = CLASSES[topk.indices[0, i].item()]
        prob = topk.values[0, i].item()
        st.write(f"{i+1}. **{cls}** — {prob*100:.1f}%")

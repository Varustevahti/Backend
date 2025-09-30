# AI_Model — Zero-Shot CLIP (OpenCLIP) kuvien luokitteluun

Tämä kansio sisältää **zero-shot**-pohjaisen kuvien luokittelijan, joka käyttää **OpenCLIP ViT-L/14** -mallia. Samaa koodia voi käyttää:

- **Streamlit-demona** (UI testaukseen)
- **FastAPI-backendistä** importoitavana moduulina, joka luokittelee ladatut kuvat ja tallettaa ne oikeaan kategoriaan/ryhmään.

Luokittelu perustuu laajaan **label pack** -kirjastoon (`label_packs.py`), jossa on vaatteita, urheiluvälineitä, työkaluja, elektroniikkaa, keittiötarvikkeita jne. → ei tarvetta erilliselle treenaukselle.

## Vaatimukset

- **Python** 3.10–3.12 suositeltu  
  (3.13 toimii usein, mutta osa kirjastoista voi vielä päivittyä)
- **Virtuaaliympäristö** (venv)
- Paketit:
  - `torch`, `torchvision`, `open_clip_torch`
  - `pillow`, `requests`
  - (Streamlit-demon ajamiseen) `streamlit`

### Asennus (venv)

```bash
python -m venv .venv
source .venv/bin/activate                
 # Windows: .venv\Scripts\activate
python -m pip install -U pip
pip install torch torchvision open_clip_torch pillow requests
# Demon UI: 
pip install streamlit
Apple Silicon (M1/M2/M3) CPU-fallback
Jos Torch-asennus tökkii tai haluat varman CPU-version:

bash
Copy code
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
pip install open_clip_torch pillow requests
Streamlit-demo
Aja demo, joka käyttää samaa mallia ja samoja labeleita kuin backend:

bash
Copy code
python -m streamlit run AI_Model/demo_app_zeroshot.py
Lataa kuva tai anna kuvan URL.

Sovellus käy läpi kaikki labelit label_packs.py-tiedostosta ja näyttää Top-K todennäköisyyksineen.

Laite valitaan automaattisesti: CUDA → MPS (Apple) → CPU.

Mallin käyttö backendistä
FastAPI-backend voi kutsua samoja funktioita:

python
Copy code
from AI_Model.demo_app_zeroshot import classify_pil, save_upload
Funktiot
classify_pil(img: PIL.Image, topk: int = 5) -> (best_label, prob, pack_name, topk_list)
Palauttaa:

best_label: top-1 label (str)

prob: todennäköisyys 0..1 (float)

pack_name: label packin nimi (esim. "Sports - General")

topk_list: lista tupleja (label, prob, pack_name) (Top-K)

save_upload(file_bytes: bytes, upload_dir: str = "uploads") -> str
Tallentaa kuvan JPEG-muotoon uploads/-kansioon ja palauttaa suhteellisen polun, esim. uploads/xxxx.jpg.

Malli ja kaikkien labelien tekstivektorit ladataan laiskasti ensimmäisessä kutsussa ja pidetään muistissa → seuraavat pyynnöt ovat nopeita.

Esimerkkireitti (valmiiksi integroituna)
Backendin reitti (tiedostossa app/routers.py) odottaa multipart-lomaketta:

vbnet
Copy code
POST /items/auto
  file:      (image) pakollinen
  location:  (string) vapaaehtoinen
  owner:     (string) vapaaehtoinen
Palvelin tekee:

save_upload → tallentaa kuvan uploads/-hakemistoon

classify_pil → saa (label, prob, pack)

hakee/luo Category ja Group packin nimellä

luo Item-rivin:

desc = label,

category_id & group_id = packista,

image = tallennetun tiedoston polku

Staattiset kuvat: app/main.py mounttaa /uploads → selaimella:
http://127.0.0.1:8080/uploads/<tiedosto>.jpg
Luo hakemisto valmiiksi: mkdir -p uploads (tai käytä StaticFiles(..., check_dir=False)).

Pikatestaus
Käynnistä backend

bash
Copy code
uvicorn app.main:app --reload --port 8080
Avaa Swagger: http://127.0.0.1:8080/docs

Lataa & luokittele

Swaggerissa POST /items/auto → Try it out → valitse kuva → Execute

cURL:

bash
Copy code
IMAGE="/ABS/PATH/kuva.jpg"
curl -X POST "http://127.0.0.1:8080/items/auto" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@${IMAGE}" \
  -F "location=Varasto A" \
  -F "owner=Nico"
Avaa palautettu kuva

Kopioi JSON-vastauksen image-arvo ja avaa selaimessa:
http://127.0.0.1:8080/<image>

Listaukset

bash
Copy code
curl "http://127.0.0.1:8080/items/"
curl "http://127.0.0.1:8080/categories/"
curl "http://127.0.0.1:8080/groups/"
Streamlit-demo (valinnainen)

bash
Copy code
python -m streamlit run AI_Model/demo_app_zeroshot.py
Konfigurointi
Labelit & packit: muokkaa AI_Model/label_packs.py.
Uusien labelien lisääminen vaatii vain backendin uudelleenkäynnistyksen; tekstivektorit lasketaan automaattisesti ensimmäisessä pyynnössä.

Laitevalinta: automaattinen (cuda → mps → cpu). Voit yliajaa polun demo_app_zeroshot.py:stä.

Suorituskyky: ensimmäinen pyyntö lämmittää mallin ja tekstivektorit. Sen jälkeen nopeaa.
Erittäin suurille label-joukoille Streamlit-demo sisältää chunkatun Top-K-haun.
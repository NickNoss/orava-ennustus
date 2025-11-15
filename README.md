
# Eläinten liikerata-analyysi ja karttavisualisointi

Tämä projekti lukee kuvista tai CSV-tiedostosta eläinhavaintoja, linkittää ne liikeradoiksi, laskee piirteitä ja ennustaa tulevia sijainteja.  
Lopputuloksena syntyy interaktiivinen kartta (`outputs/map.html`), jossa näkyvät radat ja ennustepisteet.

---

## Projektin rakenne

```

project_root/
│
├── main.py                 # pääohjelma (ajetaan tästä)
├── requirements.txt
├── data/
│   ├── images/             # kuvat (valinnainen)
│   └── detections.csv      # havaintodata CSV
│
├── outputs/                # tulostiedostot
│   ├── track_points.csv
│   ├── track_features.csv
│   ├── predictions.csv
│   └── map.html
│
└── modules/
├── **init**.py
├── config.py
├── io_utils.py
├── linking.py
├── features.py
├── predict.py
├── projection.py
└── visualize.py

````

> Jos et halua käyttää `modules/`-kansiota, voit pitää moduulit suoraan juuritasolla — importit täytyy silloin muuttaa sen mukaisesti.

---

## Asennus

1. Luo virtuaaliympäristö:

```bash
python -m venv venv
# Linux / macOS
source venv/bin/activate
# Windows (PowerShell)
venv\Scripts\Activate.ps1
````

2. Asenna riippuvuudet:

```bash
pip install -r requirements.txt
```

**requirements.txt** voi sisältää esimerkiksi:

```
pandas
numpy
pyproj
folium
```

---

## Havaintodatan valmistelu

Ohjelma tarvitsee `data/detections.csv` -tiedoston, jossa on seuraavat sarakkeet:

| Sarake       | Kuvaus                                         |
| ------------ | ---------------------------------------------- |
| `image_path` | Polku kuvaan (esim. `data/images/img_001.jpg`) |
| `timestamp`  | Aikaleima (`YYYY-MM-DDTHH:MM:SS`)              |
| `species`    | Laji                                           |
| `confidence` | (valinnainen) Luottamusarvo                    |
| `latitude`   | Leveysaste (desimaali)                         |
| `longitude`  | Pituusaste (desimaali)                         |

**Esimerkki:**

```
image_path,timestamp,species,confidence,latitude,longitude
data/images/img_0001.jpg,2025-11-13T08:12:00,hirvi,0.95,60.192059,24.945831
```

---

## Kuinka ajaa ohjelma

1. Varmista, että `data/detections.csv` on valmis.
2. Aktivoi virtuaaliympäristö (ks. yllä).
3. Aja pääohjelma:

```bash
python main.py
```

Ohjelma suorittaa seuraavat vaiheet:

1. Lukee `data/detections.csv`
2. Linkittää havainnot liikeradoiksi (`outputs/track_points.csv`)
3. Laskee piirteet (`outputs/track_features.csv`)
4. Ennustaa tulevat sijainnit (`outputs/predictions.csv`)
5. Luo kartan (`outputs/map.html`)

Tulosteen lopuksi saat viestin:

```
 Valmis! Avaa outputs/map.html selaimessa.
```

---

##  Tulostiedostot

| Tiedosto             | Kuvaus                                    |
| -------------------- | ----------------------------------------- |
| `track_points.csv`   | Linkitetyt havainnot ja niiden `track_id` |
| `track_features.csv` | Piirteet kuten nopeus, kulma ja etäisyys  |
| `predictions.csv`    | Ennustetut tulevat sijainnit              |
| `map.html`           | Interaktiivinen kartta visualisoinnista   |

Avaa `outputs/map.html` selaimessa nähdäksesi liikeradat ja ennustepisteet.

---

##  Konfigurointi

Asetukset löytyvät tiedostosta `modules/config.py`.
Tärkeimmät parametrit:

```python
LINK_MAX_DIST_M = 1500      # suurin sallittu etäisyys (m) kahden pisteen välillä
LINK_MAX_DT_S = 2 * 3600    # suurin aikaväli (s) kahden pisteen välillä
PRED_HORIZON_S = 30 * 60    # ennustehorisontti (s)
```

---

##  Yleisimmät ongelmat

| Virhe                                              | Syy ja ratkaisu                                                                             |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `ModuleNotFoundError: No module named 'modules'`   | Aja `python main.py` projektin juuressa tai varmista, että `modules` sisältää `__init__.py` |
| `FileNotFoundError: data/detections.csv`           | CSV-tiedostoa ei löytynyt – tarkista polku                                                  |
| `ValueError: detections CSV must contain columns:` | CSV:stä puuttuu pakollinen sarake                                                           |
| Tyhjä tai väärin sijoittuva kartta                 | Tarkista, että `latitude` ja `longitude` ovat desimaaleina                                  |

---

##  Vinkki EXIF-kuvien käsittelyyn

Jos sinulla on vain kuvat, joista haluat muodostaa `detections.csv`:

* Lue EXIF-data kirjastolla kuten `Pillow` tai `exifread`
* Poimi `DateTimeOriginal` ja `GPSLatitude` / `GPSLongitude`
* Tallenna arvot CSV-tiedostoon samaan formaattiin kuin yllä

**Esimerkki (idea):**

```python
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
# lue EXIF ja kirjoita CSV havainnoista
```

---

##  Yhteenveto

```bash
# Aktivoi ympäristö
source venv/bin/activate

# Aja ohjelma
python main.py

# Katso tulos selaimessa
open outputs/map.html
```

Ohjelma linkittää eläinhavainnot liikeradoiksi, laskee piirteitä, ennustaa tulevaa liikettä ja näyttää kaiken kartalla.


## Update 15/11/2025

Lisätty kuvasetti ja liittyvä predictions.csv testausta varten kansioon "data"
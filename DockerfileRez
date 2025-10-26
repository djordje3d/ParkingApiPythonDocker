FROM python:3.11-slim
# Koristi zvaničnu Python 3.11 slim sliku kao osnovu
# slim verzija je manja (bez nepotrebnih paketa) i efikasnija za deployment

# Postavi radni direktorijum u /app
WORKDIR /app

# Kopiraj requirements.txt iz lokalnog foldera parking-dashboard
COPY parking-dashboard/requirements.txt .

# Instaliraj zavisnosti
RUN pip install --no-cache-dir -r requirements.txt
# --no-cache-dir opcija sprečava keširanje preuzetih paketa, čime se smanjuje veličina image-a

# Kopiraj ceo app folder u /app u kontejneru
# COPY parking-dashboard/app/ ./ 
COPY parking-dashboard/app ./app

# Otvori port
EXPOSE 8000


# Pokreni aplikaciju
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Run app - bind to Render's assigned $PORT
#  CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]

# Local fallback to 8000 if $PORT is not defined
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]

# ["sh", "-c", "..."] - koristi shell i izvrši komandu koja sledi nakon -c unutar kontejnera.
# Ovo omogućava korišćenje promenljivih okruženja i složenijih komandi unutar kontejnera.

# app.main:app znači: u folderu app/ otvori fajl main.py i u njemu koristi promenljivu (objekat) app — to je FastAPI aplikacija.

# --host 0.0.0.0 : kaže uvicornserveru da sluša na svim mrežnim interfejsima unutar kontejnera, ne samo na localhost 
# kontejner je izolovan od host mašine, pa je potrebno eksplicitno navesti da sluša na svim interfejsima.
# to znači da aplikacija u kontejneru može primati zahteve koji dolaze spolja (npr. sa host mašine ili drugih kontejnera u istoj mreži).

# --port ${PORT:-8000} : koristi vrednost promenljive okruženja PORT ako je definisana, a ako nije, koristi podrazumevani port 8000.
# Npr. Ako je u docker-compose.yml definisano enviroment: PORT=5000, aplikacija će slušati na portu 5000. Ako nije definisano, slušaće na portu 8000.
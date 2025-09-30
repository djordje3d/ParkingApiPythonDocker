FROM python:3.11-slim

# Postavi radni direktorijum u /app
WORKDIR /app

# Kopiraj requirements.txt iz parking-dashboard
COPY parking-dashboard/requirements.txt .

# Instaliraj zavisnosti
RUN pip install --no-cache-dir -r requirements.txt

# Kopiraj ceo app folder u /app
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
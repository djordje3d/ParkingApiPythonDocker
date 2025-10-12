# 🚗 Parking Service API

A modular FastAPI-based system for simulating and managing smart parking operations — complete with a dashboard, API, and simulation tools.

# 📄 License & Credits
This demo was developed by **Djordje Bogdanovic** for client presentation and educational purposes. 
Feel free to adapt or extend for production use.

---

# 🧑‍💻 `README_DEV.md` – Developer Documentation & Onboarding Guide

```markdown
# 🧑‍💻 Parking Service API – Developer Documentation

This document provides technical guidance for developers working on the Parking Service API project.  
It covers architecture, setup, simulation, deployment, and extensibility.

---

## 🧱 Architecture Overview

- **Backend**: FastAPI (Python 3.11+)
- **Frontend**: Static HTML + Chart.js
- **Simulation**: Python script using `requests`
- **Deployment**: Docker image (local or cloud via Render)

---

## 📦 Folder Structure

parking-dashboard/
├── app/
│   ├── main.py               # FastAPI entry point 
│   ├── routers.py            # API route definitions 
│   ├── services.py           # Business logic and cache 
│   ├── ParkingService.py     # Core parking logic 
│   ├── Ticket.py             # Ticket model and barcode logic 
│   ├── VehicleType.py        # Enum for vehicle types 
│   ├── static/               # HTML dashboard with charts 
│   │   ├── index.html 
│   │   ├── indexVue.html 
│   │   └── dashboard.html 
│   └── simulate_apict.py     # Simulation script 
├── requirements.txt          # Python dependencies 
├── Dockerfile                # Container configuration 
├── README.md                 
└── README_DEV.md             # This file

---


## ⚙️ Setup Instructions

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the server locally

```bash
uvicorn app.main:app --reload
```
### 3. Run the simulation

```bash
python app/simulate_apict.py
```

### Docker Deployment
Build and run locally

```bash
docker build -t parking-app .
docker run -p 8000:8000 parking-app
```
### Push to Docker Hub

```bash
docker tag parking-app djolebg/parking-app:latest
docker push djolebg/parking-app:latest
```
### Deploy on Render
Choose “Deploy an existing image from Docker registry”

```bash
Use image: djolebg/parking-app:latest

Set port to 8000
```

## 🌐 Environment Variables
Optional: set BASE_URL for simulation script

```bash
export BASE_URL=http://localhost:8000
```
Or modify simulate_apict.py to read from 

```bash
os.getenv("BASE_URL")
```

## 🧪 Simulation Module
Uses requests to hit API endpoints

Randomly generates vehicle entries and exits

Displays occupancy and vehicle state in terminal

Useful for testing backend logic and dashboard refresh

## 🧩 Extensibility
This system is modular and ready for expansion. Future features may include:

Reservation system

User authentication

Historical analytics

Mobile-friendly dashboard

Persistent database (PostgreSQL, SQLite)

## 🧑‍🏫 Developer Tips
Use VS Code with Python extension

Enable auto-formatting and linting (e.g. Black, Flake8)

Use uvicorn --reload for hot-reloading during development

Keep simulation script decoupled from core logic

Use @cache decorators carefully — disable for real-time data

## 🧪 Testing
Manual testing via dashboard and simulation

API testing via Postman or curl

Add unit tests for ParkingService, Ticket, and routers

## 📄 License & Credits
Developed by **Djordje Bogdanovic** For educational, demo, and client-facing use. 
Feel free to fork, extend, or integrate into larger systems.
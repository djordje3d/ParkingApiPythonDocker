# 🚗 Parking Service API – Demo Setup & Usage

This project simulates a **smart parking garage system** with live API endpoints, terminal feedback, and a visual dashboard.  
It’s designed for **demo purposes and client presentations**.

---

## 🧭 Project Overview

Commissioned by a client managing private parking facilities, this app digitizes manual vehicle tracking and revenue calculation.  
It provides:

- Real-time occupancy monitoring  
- Vehicle entry/exit logging  
- Daily revenue analytics  
- A visual dashboard for operators  
- A simulation module for testing and demonstration

---

## 📦 Project Structure

```
parking-dashboard/ 
├── app/ 
│ ├── main.py               # FastAPI entry point 
│ ├── routers.py            # API route definitions 
│ ├── services.py           # Business logic and cache 
│ ├── ParkingService.py     # Core parking logic 
│ ├── Ticket.py             # Ticket model and barcode logic 
│ ├── VehicleType.py        # Enum for vehicle types 
│ ├── static/               # HTML dashboard with charts 
│ │ ├── index.html 
│ │ ├── indexVue.html 
│ │ └── dashboard.html 
│ └── simulate_apict.py     # Simulation script 
├── requirements.txt        # Python dependencies 
├── Dockerfile              # Container configuration 
└── README.md               # This file
---
```
## 🚀 How to Run the Demo Locally
```
```
### 1. Install dependencies

```bash
pip install -r requirements.txt
```
### 2. Start the backend server

```bash
uvicorn app.main:app --reload
```

- Runs FastAPI server at: [http://127.0.0.1:8000]
- Mounts dashboard (if present) at `/static`  
- Initializes cache and logs startup events  

---

### 3. Run the simulation script

```bash
python app/simulate_apict.py
```

- Simulates **vehicle entries and exits** with randomized data  
- Interacts with **API endpoints** to mimic real garage behavior  
- Displays **occupancy, active vehicles, and exit logs** in terminal  

---

## 📊 Visual Dashboard

Open in your browser:

```
http://127.0.0.1:8000/static/index.html
http://127.0.0.1:8000/static/indexVue.html
http://127.0.0.1:8000/static/dashboard.html

```

### Features
- 🟢 **Donut chart** – occupancy (free vs occupied)  
- 📊 **Bar chart** – daily revenue  
- 🚘 **Bar chart** – vehicle type distribution  
- 📋 **Live table** – active parked vehicles (auto-refresh every 10s)  
- 🔄 **Simulation trigger** – via dashboard button
---

## 🔌 API Endpoints Overview

| Method | Endpoint                  | Description                               |
|--------|---------------------------|-------------------------------------------|
| POST   | `/vehicles/enter`        | Register vehicle entry, returns barcode    |
| POST   | `/vehicles/exit/{barcode}` | Process exit, calculate duration & revenue |
| GET    | `/occupancy`             | Show total capacity and current occupancy  |
| GET    | `/spaces/free`           | Return number of free parking spaces       |
| GET    | `/vehicles/active`       | List all currently parked vehicles         |
| GET    | `/revenue/today`         | Return total revenue for the current day   |
| GET    | `/health`                | Check service status                       |
| POST   | `/simulate`              | Trigger simulation from frontend           |

---

## 🧪 Notes

- All data is **in-memory** and resets on server restart  
- Simulation generates **random Serbian-style license plates**  
- Dashboard **Refresh after click on button** for live feedback  
- No database required — ideal for demos and testing

---

## 📄 License & Credits

This demo was developed by **Djordje Bogdanovic** for client presentation purposes.  
Feel free to adapt or extend for production use.  

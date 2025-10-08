import requests
import random
import sys
import os

# Dodaj parent folder (parking-dashboard) u sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from enum import Enum
from app.VehicleType import VehicleType

BASE_URL = "http://127.0.0.1:8000"
# BASE_URL = "http://localhost:8000" # for request from the same container
# BASE_URL = "http://render.internal:8000"  # for request from another container

# Prefixes and suffixes for registration numbers
prefixes = ["BG", "NS", "NI", "CA", "KG", "SU", "ZR", "VA"]
suffixes = ["JL", "UG", "HG", "SD", "ZH", "ED", "RT"]


def generate_registration() -> str:
    return f"{random.choice(prefixes)}-{random.randint(100, 999)}-{random.choice(suffixes)}"


def show_occupancy():
    print("📡 Fetching occupancy data...")
    # occ = requests.get(f"{BASE_URL}/occupancy").json()
    # free = requests.get(f"{BASE_URL}/spaces/free").json()
    occ = requests.get(f"{BASE_URL}/occupancy", timeout=5).json()
    free = requests.get(f"{BASE_URL}/spaces/free", timeout=5).json()

    occupied = occ["capacity"] - free["free_spaces"]
    print(f"\n📊 Occupancy: {occupied}/{occ['capacity']} ({occ['percent']:.1f}%)")
    print(f"🅿️ FREE parking spaces: {free['free_spaces']}")


def show_vehicles():
    vehicles = requests.get(f"{BASE_URL}/vehicles/active").json()
    if not vehicles:
        print("🅿 Parking is empty.")
        return
    print(f"\n📋 Parked Vehicles: {len(vehicles)}")
    print("-" * 70)
    for v in vehicles:
        print(
            f"Type: {v['type']:<5} | Reg: {v['registration']:<10} "
            f"| Entry: {v['entry_time']} | Barcode: {v['barcode']}"
        )
    print("-" * 70)


def simulate_entry():
    vehicle_count = random.randint(1, 10)
    print(f"\n🅿️ Entering {vehicle_count} vehicles...")

    barcodes = []
    for _ in range(vehicle_count):
        registration = generate_registration()
        vehicle_type = random.choice(list(VehicleType))
        res = requests.post(
            f"{BASE_URL}/vehicles/enter",
            json={"registration": registration, "vehicle_type": vehicle_type},
        ).json()
        if "barcode" in res:
            barcodes.append(res["barcode"])
            print(
                f"✅ Entered {registration} ({vehicle_type}) → Barcode: {res['barcode']}"
            )
        else:
            print("❌ Entry failed:", res)
    return barcodes


# barcodes iz simulate_entry se prosledjuju kao argument
# Ne koristi se vise
# def simulate_exit(barcodes):
#     if not barcodes:
#         print("\n⚠️ No vehicles to exit.")
#         return

#     number_to_exit = random.randint(
#         1, min(6, len(barcodes))
#     )  # Exit up to 5 or available
#     print(f"\n🚗 Exiting {number_to_exit} vehicles...")
#     for barcode in barcodes[:number_to_exit]:
#         res = requests.post(f"{BASE_URL}/vehicles/exit/{barcode}").json()
#         print("🚗 Exit response:", res)


# Pozivanje aktivnih barkodova direktno iz API-ja


def simulate_exit():
    vehicles = requests.get(f"{BASE_URL}/vehicles/active", timeout=5).json()
    if not vehicles:
        print("\n⚠️ No vehicles to exit.")
        return

    barcodes = [v["barcode"] for v in vehicles]
    number_to_exit = random.randint(1, min(6, len(barcodes)))
    print(f"\n🚗 Exiting {number_to_exit} vehicles...")
    for barcode in random.sample(barcodes, number_to_exit):
        res = requests.post(f"{BASE_URL}/vehicles/exit/{barcode}").json()
        print("🚗 Exit response:", res)


def run_simulation():
    print("\n" + "*" * 60)
    print("🚗 Parking Service API Simulation Started")

    print("🔍 Checking server health...")
    try:
        res = requests.get(f"{BASE_URL}/health", timeout=5)
        print("✅ Server response:", res.json())
    except Exception as e:
        print("❌ Server     unreachable:", e)
        return

    print("➡️ Calling show_occupancy()")

    show_occupancy()
    simulate_entry()

    show_vehicles()
    show_occupancy()

    simulate_exit()

    show_occupancy()
    show_vehicles()

    print("*" * 60)

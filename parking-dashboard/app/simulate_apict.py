import requests
import random
import sys
import os

# from enum import Enum
from app.VehicleType import VehicleType

# Dodaj parent folder (parking-dashboard) u sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


#  BASE_URL = "http://127.0.0.1:8000"
# BASE_URL = "http://localhost:8000" # for request from the same container
# BASE_URL = "http://render.internal:8000"  # for request from another container
# Dinamički BASE_URL — lokalno ili produkcija
BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

# Prefixes and suffixes for registration numbers
prefixes = ["BG", "NS", "NI", "CA", "KG", "SU", "ZR", "VA"]
suffixes = ["JL", "UG", "HG", "SD", "ZH", "ED", "RT"]


def generate_registration() -> str:
    return f"{random.choice(prefixes)}-{random.randint(100, 999)}-{random.choice(suffixes)}"


def show_occupancy():
    print("📡 Fetching occupancy data...")

    occ_response = requests.get(f"{BASE_URL}/api/occupancy", timeout=5)
    free_response = requests.get(f"{BASE_URL}/api/spaces/free", timeout=5)

    occ = safe_json(occ_response)
    free = safe_json(free_response)

    if occ and free:
        occupied = occ["capacity"] - free["free_spaces"]
        print(f"\n📊 Occupancy: {occupied}/{occ['capacity']} ({occ['percent']:.1f}%)")
        print(f"🅿️ FREE parking spaces: {free['free_spaces']}")
    else:
        print("❌ Failed to fetch occupancy data.")


def show_vehicles():
    response = requests.get(f"{BASE_URL}/api/vehicles/active", timeout=5)
    vehicles = safe_json(response)

    if not vehicles:
        print("🅿 Parking is empty or data unavailable.")
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

        response = requests.post(
            f"{BASE_URL}/api/vehicles/enter",
            json={"registration": registration, "vehicle_type": vehicle_type},
        )

        res = safe_json(response)
        if res and "barcode" in res:
            barcodes.append(res["barcode"])
            print(
                f"✅ Entered {registration} ({vehicle_type}) → Barcode: {res['barcode']}"
            )
        else:
            print("❌ Entry failed:", res if res else response.text)

    return barcodes


def safe_json(response):
    if response.status_code == 200 and response.content:
        try:
            return response.json()
        except Exception as e:
            print("❌ JSON parsing error:", e)
    else:
        print("❌ Invalid response:", response.status_code, response.text)
    return None


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
    response = requests.get(f"{BASE_URL}/api/vehicles/active", timeout=5)
    vehicles = safe_json(response)

    if not vehicles:
        print("\n⚠️ No vehicles to exit.")
        return

    barcodes = [v["barcode"] for v in vehicles]
    number_to_exit = random.randint(1, min(6, len(barcodes)))
    print(f"\n🚗 Exiting {number_to_exit} vehicles...")

    for barcode in random.sample(barcodes, number_to_exit):
        res = safe_json(requests.post(f"{BASE_URL}/api/vehicles/exit/{barcode}"))
        if res:
            print("🚗 Exit response:", res)
        else:
            print(f"❌ Exit failed for barcode {barcode}")


def run_simulation():
    print("\n" + "*" * 60)
    print("🚗 Parking Service API Simulation Started")

    print("🔍 Checking server health...")
    try:
        res = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if res.status_code == 200 and res.content:
            print("✅ Server response:", res.json())
        else:
            print("❌ Invalid server response:", res.status_code, res.content)
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


if __name__ == "__main__":
    run_simulation()

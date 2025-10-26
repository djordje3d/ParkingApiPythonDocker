import requests
import time


def check_url(name, url, expected_text=None):
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            if expected_text and expected_text not in response.text:
                print(f"⚠️  {name}: running, but content mismatch")
                return False
            print(f"✅  {name}: OK ({response.status_code})")
            return True
        else:
            print(f"❌  {name}: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌  {name}: {e}")
        return False


def main():
    print("🔍 Checking containers (please wait)...")
    time.sleep(3)

    backend_ok = check_url(
        "Backend (FastAPI)", "http://localhost:8000/api/hello", "Hello"
    )
    frontend_ok = check_url("Frontend (Vue app)", "http://localhost:3000")

    if backend_ok and frontend_ok:
        print("\n🎉 All containers are running correctly!")
    elif not backend_ok and not frontend_ok:
        print("\n❌ Neither backend nor frontend are reachable.")
    elif not backend_ok:
        print("\n⚠️ Backend not responding, but frontend works.")
    else:
        print("\n⚠️ Frontend not responding, but backend works.")


if __name__ == "__main__":
    main()

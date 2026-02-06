from src.main import app

def list_routes():
    print("\n--- Registered FastAPI Routes ---")
    for route in app.routes:
        methods = ", ".join(route.methods) if hasattr(route, "methods") else "N/A"
        print(f"Path: {route.path:40} | Methods: {methods}")
    print("---------------------------------\n")

if __name__ == "__main__":
    list_routes()

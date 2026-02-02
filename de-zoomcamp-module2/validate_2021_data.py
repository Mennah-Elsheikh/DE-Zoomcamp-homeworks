import os

DATA_DIR = "./data"

def validate_2021():
    print("=== 2021 NYC Taxi Data Validation Report ===")
    print(f"Checking directory: {os.path.abspath(DATA_DIR)}")
    print("-" * 45)
    
    taxis = ["yellow", "green"]
    months = range(1, 8)  # Jan to Jul
    
    total_expected = len(taxis) * len(months)
    found_count = 0
    missing_files = []
    
    for taxi in taxis:
        for month in months:
            file_name = f"{taxi}_tripdata_2021-{month:02d}.csv"
            file_path = os.path.join(DATA_DIR, file_name)
            
            exists = os.path.exists(file_path)
            size = os.path.getsize(file_path) if exists else 0
            
            status = "✅ OK" if exists and size > 0 else "❌ MISSING/EMPTY"
            if exists and size > 0:
                found_count += 1
                size_mb = size / (1024 * 1024)
                print(f"{file_name:<35} | {size_mb:>7.2f} MB | {status}")
            else:
                missing_files.append(file_name)
                print(f"{file_name:<35} | {'N/A':>10} | {status}")

    print("-" * 45)
    print(f"Summary: {found_count}/{total_expected} files validated.")
    
    if found_count == total_expected:
        print("\n🎉 SUCCESS: All 2021 files are present and valid!")
    else:
        print(f"\n⚠️ WARNING: {len(missing_files)} files are missing or invalid.")
        for f in missing_files:
            print(f"  - {f}")

if __name__ == "__main__":
    if not os.path.exists(DATA_DIR):
        print(f"Error: {DATA_DIR} not found. Did you run the DAG?")
    else:
        validate_2021()

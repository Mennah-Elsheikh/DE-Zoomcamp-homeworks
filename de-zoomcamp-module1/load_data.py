import pandas as pd
from sqlalchemy import create_engine
import os

def main():
    # Database connection details for running INSIDE the Postgres container
    # When inside the container, use localhost:5432 (internal port)
    # When outside the container, use localhost:5433 (mapped port)
    user = os.getenv('POSTGRES_USER', 'postgres')
    password = os.getenv('POSTGRES_PASSWORD', 'postgres')
    host = os.getenv('POSTGRES_HOST', 'localhost')  # localhost when inside container
    port = os.getenv('POSTGRES_PORT', '5432')  # 5432 inside container, 5433 from outside
    db = os.getenv('POSTGRES_DB', 'ny_taxi')
    
    connection_string = f'postgresql://{user}:{password}@{host}:{port}/{db}'
    print(f"Connecting to database: {db} at {host}:{port}")
    
    try:
        engine = create_engine(connection_string)
        # Test connection
        with engine.connect() as conn:
            print("✓ Database connection successful!")
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return

    # 1. Ingest Green Taxi Data (Parquet)
    parquet_file = 'green_tripdata_2025-11.parquet'
    if os.path.exists(parquet_file):
        print(f"\nLoading {parquet_file}...")
        df_green = pd.read_parquet(parquet_file)
        print(f"  Rows: {len(df_green):,}")
        print(f"  Columns: {list(df_green.columns)}")
        
        # Write to Postgres in chunks for better performance
        print("  Writing to database...")
        df_green.head(n=0).to_sql(name='green_tripdata', con=engine, if_exists='replace', index=False)
        df_green.to_sql(name='green_tripdata', con=engine, if_exists='append', index=False, chunksize=10000)
        print(f"✓ Green taxi data ingested successfully ({len(df_green):,} rows)")
    else:
        print(f"✗ File {parquet_file} not found.")

    # 2. Ingest Taxi Zone Lookup (CSV)
    csv_file = 'taxi_zone_lookup.csv'
    if os.path.exists(csv_file):
        print(f"\nLoading {csv_file}...")
        df_zones = pd.read_csv(csv_file)
        print(f"  Rows: {len(df_zones):,}")
        print(f"  Columns: {list(df_zones.columns)}")
        
        # Write to Postgres
        print("  Writing to database...")
        df_zones.to_sql(name='taxi_zone_lookup', con=engine, if_exists='replace', index=False)
        print(f"✓ Taxi zone lookup data ingested successfully ({len(df_zones):,} rows)")
    else:
        print(f"✗ File {csv_file} not found.")
    
    print("\n" + "="*50)
    print("Data loading complete!")
    print("="*50)

if __name__ == '__main__':
    main()

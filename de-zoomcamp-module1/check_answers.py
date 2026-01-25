import psycopg2
from decimal import Decimal

# Connect to database
conn = psycopg2.connect('postgresql://postgres:postgres@localhost:5433/ny_taxi')
cur = conn.cursor()

print("=" * 60)
print("DE ZOOMCAMP MODULE 1 - HOMEWORK ANSWERS")
print("=" * 60)

# Q3
print("\nQ3: Short trips (≤ 1 mile) in November 2025")
cur.execute("""
    SELECT COUNT(*)
    FROM green_tripdata
    WHERE lpep_pickup_datetime >= '2025-11-01'
      AND lpep_pickup_datetime < '2025-12-01'
      AND trip_distance <= 1;
""")
result = cur.fetchone()[0]
print(f"Answer: {result:,}")

# Q4
print("\nQ4: Longest trip pickup day")
cur.execute("""
    SELECT DATE(lpep_pickup_datetime) AS day, trip_distance
    FROM green_tripdata
    WHERE trip_distance < 100
    ORDER BY trip_distance DESC
    LIMIT 1;
""")
day, distance = cur.fetchone()
print(f"Answer: {day} (distance: {distance} miles)")

# Q5
print("\nQ5: Biggest pickup zone on Nov 18, 2025")
cur.execute("""
    SELECT z."Zone", SUM(g."total_amount") AS total
    FROM green_tripdata g
    JOIN taxi_zone_lookup z ON g."PULocationID" = z."LocationID"
    WHERE DATE(g.lpep_pickup_datetime) = '2025-11-18'
    GROUP BY z."Zone"
    ORDER BY total DESC
    LIMIT 1;
""")
zone, total = cur.fetchone()
print(f"Answer: {zone} (${total:.2f})")

# Q6
print("\nQ6: Largest tip from East Harlem North")
cur.execute("""
    SELECT dz."Zone", g.tip_amount
    FROM green_tripdata g
    JOIN taxi_zone_lookup pz ON g."PULocationID" = pz."LocationID"
    JOIN taxi_zone_lookup dz ON g."DOLocationID" = dz."LocationID"
    WHERE pz."Zone" = 'East Harlem North'
    ORDER BY g.tip_amount DESC
    LIMIT 1;
""")
result = cur.fetchone()
if result:
    zone, tip = result
    print(f"Answer: {zone} (tip: ${tip:.2f})")
else:
    print("No results found")

print("\n" + "=" * 60)
print("Q7: Terraform Workflow")
print("Answer: terraform init, terraform apply -auto-approve, terraform destroy")
print("=" * 60)

conn.close()

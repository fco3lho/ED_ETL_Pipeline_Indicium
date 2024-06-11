import os
from datetime import datetime
import yaml

current_date = datetime.now().strftime('%Y-%m-%d')

tables = [
    "employee_territories",
    "orders",
    "customers",
    "products",
    "shippers",
    "suppliers",
    "territories",
    "us_states",
    "region",
    "employees"
]

with open("meltano.yml", "r") as file:
    config = yaml.safe_load(file)

# PostgreSQL to JSONL
for table in tables:
    print(f"Running ETL for table: {table}")

    config["plugins"]["extractors"][0]["select"] = [f"public-{table}.*"]

    with open("meltano.yml", "w") as file:
        yaml.safe_dump(config, file)

    destination_path = f"../data/postgres/{table}/"
    os.system(f"meltano config target-jsonl set destination_path {destination_path}")
    os.system(f"meltano config target-jsonl set custom_name {current_date}")
    os.system("meltano run tap-postgres target-jsonl")

# CSV to JSONL
destination_path = f"../data/csv/order_details/"
os.system(f"meltano config target-jsonl set destination_path {destination_path}")
os.system(f"meltano config target-jsonl set custom_name {current_date}")
os.system("meltano run tap-csv target-jsonl")
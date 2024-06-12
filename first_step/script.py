from datetime import datetime
import pandas as pd
import os
import yaml

def script(tables, date):
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
        os.system(f"meltano config target-jsonl set custom_name {date}")
        os.system("meltano run tap-postgres target-jsonl")

    # CSV to JSONL
    destination_path = f"../data/csv/order_details/"
    os.system(f"meltano config target-jsonl set destination_path {destination_path}")
    os.system(f"meltano config target-jsonl set custom_name {date}")
    os.system("meltano run tap-csv target-jsonl")

def convert_jsonl_to_csv(tables, date):
    for table in tables:
        jsonl_file = f"../data/postgres/{table}/{date}.jsonl"
        csv_file = f"../data/postgres/{table}/{date}.csv"

        if os.path.exists(jsonl_file):
            df = pd.read_json(jsonl_file, lines=True)
            df.to_csv(csv_file, index=False)
            os.remove(jsonl_file)
    
    jsonl_file = f"../data/csv/order_details/{date}.jsonl"
    csv_file = f"../data/csv/order_details/{date}.csv"

    if os.path.exists(jsonl_file):
        df = pd.read_json(jsonl_file, lines=True)
        df.to_csv(csv_file, index=False)
        os.remove(jsonl_file)

current_date = datetime.now().strftime('%Y-%m-%d')
tables = ["employee_territories", "orders", "customers", "products", "shippers", "suppliers", "territories", "us_states", "region", "employees"]

script(tables, current_date)
convert_jsonl_to_csv(tables, current_date)
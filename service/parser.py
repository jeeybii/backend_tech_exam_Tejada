import pandas as pd
import chardet
import asyncio
import os
import io
from datetime import datetime
from api.db import insert_medalists_bulk

async def process_csv(file_path):
    """ Reads a CSV file, auto-detects encoding, and processes data. """
    try:
        # Detect file encoding
        with open(file_path, "rb") as f:
            raw_data = f.read(50000)  # Read first 50KB
            result = chardet.detect(raw_data)
            detected_encoding = result["encoding"]

        print(f"🔍 Detected encoding: {detected_encoding}")

        # Read file as text to handle encoding issues
        with open(file_path, "r", encoding=detected_encoding, errors="replace") as f:
            text = f.read()

        # Convert text back to a file-like object and load into pandas
        df = pd.read_csv(io.StringIO(text))

        # ✅ Convert `medal_date` to ISO format
        def convert_date(date_str):
            try:
                return datetime.strptime(date_str, "%Y-%m-%d")  # Ensure YYYY-MM-DD format
            except ValueError:
                return None  # If conversion fails, store as None

        df["medal_date"] = df["medal_date"].astype(str).apply(convert_date)  # Convert to datetime

        # ✅ Convert numeric fields that might contain NaN
        df["medal_code"] = pd.to_numeric(df["medal_code"], errors="coerce").fillna(0).astype(int)
        df["code_athlete"] = pd.to_numeric(df["code_athlete"], errors="coerce").fillna(0).astype(int)
        df["code_team"] = pd.to_numeric(df["code_team"], errors="coerce").fillna(0).astype(int)

        # ✅ Convert `NaN` values in team-related fields to None
        df["team"] = df["team"].replace({pd.NA: None, "NaN": None})
        df["team_gender"] = df["team_gender"].replace({pd.NA: None, "NaN": None})

        # Convert DataFrame to List of Dicts
        medalists_data = df.where(pd.notna(df), None).to_dict(orient="records")  # ✅ Convert all NaN to None

        # Use bulk insert i
        inserted_ids = await insert_medalists_bulk(medalists_data)
        print(f"✅ Processed {file_path} - Inserted {len(inserted_ids)} new records.")

        # Move processed file to archive
        archive_path = file_path.replace("medalists", "medalists_archive")
        os.makedirs(os.path.dirname(archive_path), exist_ok=True)
        os.rename(file_path, archive_path)

    except Exception as e:
        print(f"❌ Error processing {file_path}: {str(e)}")

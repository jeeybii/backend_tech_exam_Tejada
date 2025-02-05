import os
import time
import asyncio
from service.parser import process_csv

# Directory to scan for new CSV files
WATCH_FOLDER = "storage/app/medalists"

# Ensure the folder exists
os.makedirs(WATCH_FOLDER, exist_ok=True)

async def scan_and_process():
    """ Scans the folder periodically and processes any new CSV files. """
    while True:
        try:
            files = [f for f in os.listdir(WATCH_FOLDER) if f.endswith(".csv")]

            if files:
                for file in files:
                    file_path = os.path.join(WATCH_FOLDER, file)
                    print(f"📄 Processing file: {file_path}")
                    await process_csv(file_path)  # Call parser

            await asyncio.sleep(10)  # Wait before scanning again

        except Exception as e:
            print(f"❌ Error in worker: {str(e)}")

if __name__ == "__main__":
    print("🔄 Worker started... Scanning for new files.")
    asyncio.run(scan_and_process())

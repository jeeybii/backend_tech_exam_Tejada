import os
import time
import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from service.parser import process_csv

# Directory to watch
WATCH_FOLDER = "storage/app/medalists"
os.makedirs(WATCH_FOLDER, exist_ok=True)

# ✅ Async queue for handling multiple file uploads in parallel
file_queue = asyncio.Queue()

class CSVFileHandler(FileSystemEventHandler):
    """ Watches for new CSV files and adds them to the processing queue. """
    
    def on_created(self, event):
        """ Called when a new CSV file is detected. """
        if event.is_directory:
            return
        if event.src_path.endswith(".csv"):
            print(f"📥 New CSV file detected: {event.src_path}")
            asyncio.run_coroutine_threadsafe(file_queue.put(event.src_path), loop)  # ✅ Add file to async queue

async def worker():
    """ Worker task that continuously processes files from the queue in parallel. """
    while True:
        file_path = await file_queue.get()
        print(f"🚀 Processing file: {file_path}")
        await process_csv(file_path)  # ✅ Process each file asynchronously
        file_queue.task_done()  # ✅ Mark as done

async def scan_existing_files():
    """ Scan the directory for existing CSV files on startup and add them to the queue. """
    print("🔍 Scanning for existing CSV files...")
    for filename in os.listdir(WATCH_FOLDER):
        file_path = os.path.join(WATCH_FOLDER, filename)
        if file_path.endswith(".csv"):
            print(f"📌 Found existing CSV file: {file_path} - Adding to queue...")
            await file_queue.put(file_path)

def start_monitor():
    """ Start monitoring the folder for new CSV files and process them in parallel. """
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    try:
        loop.run_until_complete(scan_existing_files())  # ✅ Scan for existing files first

        # ✅ Start multiple worker tasks to process files concurrently
        for _ in range(3):  # Adjust number of workers as needed
            loop.create_task(worker())

        observer = Observer()
        event_handler = CSVFileHandler()
        observer.schedule(event_handler, WATCH_FOLDER, recursive=False)

        print(f"📂 Monitoring folder: {WATCH_FOLDER}")
        observer.start()
        
        loop.run_forever()  # ✅ Keep event loop running

    except Exception as e:
        print(f"🚨 Critical error in monitor service: {str(e)}")
        print("🔄 Restarting service in 5 seconds...")
        time.sleep(5)
        start_monitor()  # ✅ Restart the service on failure

if __name__ == "__main__":
    start_monitor()

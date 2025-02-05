# backend_tech_exam_Tejada

🏅 FastAPI Medalists API

This project is a FastAPI-based service that processes medalists' data from CSV files, stores them in MongoDB, and provides aggregated event statistics via a REST API.

📌 Features

Upload CSV files containing medalist information

Background service that monitors the folder for new files

Stores data in MongoDB efficiently

Retrieves aggregated event statistics with pagination

Runs continuously as a background process

Uses FastAPI for a modern and high-performance API

🚀 Getting Started

Follow these steps to set up and run the application.

1️⃣ Prerequisites

Ensure you have the following installed:

Python 3.8+

MongoDB (Local or Cloud)

Git

FastAPI & Uvicorn

You can install MongoDB locally or use MongoDB Atlas.

2️⃣ Clone the Repository

git clone https://github.com/YOUR-USERNAME/backend_tech_exam.git
cd backend_tech_exam

Replace YOUR-USERNAME with your actual GitHub username.

3️⃣ Create a Virtual Environment

python -m venv venv  # Create a virtual environment
source venv/bin/activate  # Activate it (Mac/Linux)
venv\Scripts\activate  # Activate it (Windows)

4️⃣ Install Dependencies

pip install -r requirements.txt

If you don’t have requirements.txt, install manually:

pip install fastapi uvicorn motor pandas chardet watchdog

5️⃣ Configure Environment Variables

Create a .env file in the project root:

MONGO_URL=mongodb://localhost:27017
DATABASE_NAME=medalists_db

Modify the MONGO_URL if using a remote MongoDB.

6️⃣ Start MongoDB

If MongoDB is installed locally, start it:

mongod --dbpath /path/to/mongodb/data

For MongoDB Atlas, replace MONGO_URL in .env with your connection string.

7️⃣ Run the FastAPI Server

uvicorn api.main:app --reload

This starts the API at:

http://127.0.0.1:8000

API Docs (Swagger UI):

http://127.0.0.1:8000/docs

8️⃣ Start the Background CSV Monitoring Service

python -m service.monitor

This service watches for new CSV files and automatically processes them.

📌 API Endpoints

1️⃣ Upload CSV File

POST /upload

curl -X 'POST' \
  'http://127.0.0.1:8000/upload' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@medalists.csv'

📌 Functionality:

Accepts CSV file uploads.

Saves the file in storage/app/medalists/.

2️⃣ Get Aggregated Event Stats

GET /aggregated_stats/event?page=1&limit=10

curl -X 'GET' 'http://127.0.0.1:8000/aggregated_stats/event?page=1&limit=10'

📌 Functionality:

Fetches aggregated medalists by event.

Supports pagination.

Example JSON Response:

{
    "data": [
        {
            "discipline": "Athletics",
            "event": "Men's 100m Final",
            "event_date": "2024-08-02",
            "medalists": [
                {"name": "John Doe", "medal_type": "Gold", "country": "USA"}
            ]
        }
    ],
    "paginate": {
        "current_page": 1,
        "total_pages": 5
    }
}

📌 Running the Service in Background (Optional)

If you want to run the monitoring service continuously, use:

nohup python -m service.monitor > monitor.log 2>&1 &

To stop it, find the process ID:

ps aux | grep monitor.py
kill -9 PROCESS_ID

Alternatively, use Supervisor or Systemd to manage the service.

🚀 Deployment (Optional)

For production:

uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4

🛠️ Troubleshooting

1️⃣ MongoDB Connection Issues

Ensure MongoDB is running locally or remotely.

Check if MONGO_URL is correct in .env.

2️⃣ API Not Running

Ensure dependencies are installed.

Check logs: monitor.log





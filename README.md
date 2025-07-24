# 🏠 Room Sensor Query Agent

A full-stack AI-powered query agent for analyzing room sensor data like temperature, CO2, and humidity over time. Built with **FastAPI (Python)** as the backend, **OpenAI API** as the LLM, and a **React + Tailwind CSS** frontend for querying and visualization.

---

## ⚙️ Features

- 📈 Analyze room sensor data across multiple text files.
- 🤖 Ask natural language questions (e.g., *“How does CO2 change by day of week?”*).
- 📊 Get tabular + summary answers powered by Anthropic AI.
- 🌐 Clean, interactive frontend UI (React + Tailwind).
- 🔗 Fully decoupled backend and frontend with CORS configured.

---

## 🧱 Project Structure

room-sensor-query/
├── backend/ # FastAPI app
│ ├── main.py # Core backend logic
│ ├── data/ # Folder with sensor data in .txt files
│ └── .env # Environment file with ANTHROPIC_API_KEY
│
├── frontend/ # React + Tailwind UI
│ ├── index.html
│ ├── src/
│ │ ├── App.tsx # Main UI logic
│ │ └── index.css # Tailwind CSS import
│ ├── tailwind.config.js
│ ├── postcss.config.js
│ ├── package.json
│ └── vite.config.js

---

## 🚀 Getting Started

### 1️⃣ Backend Setup (FastAPI + Anthropic)

```bash
cd backend
python -m venv venv
source venv/bin/activate     # on Windows: venv\Scripts\activate
pip install -r requirements.txt

🧪 Sample Queries
“How does the temperature in Room A change by hour of the day?”

“What is the average humidity on Sundays?”

“Compare CO2 levels in Room B throughout the week.”

The response will contain:

json
Copy
Edit
{
  "summary": "CO2 peaks on weekends.",
  "table": {
    "key_label": "Day of Week",
    "value_label": "Average CO2",
    "data": {
      "Monday": 330.2,
      "Tuesday": 400.1,
      ...
    }
  }
}

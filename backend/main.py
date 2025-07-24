import os
import json
import glob
import pandas as pd
from datetime import datetime
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import List
from openai import OpenAI

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

data_dir = "data"

class QueryRequest(BaseModel):
    query: str

def read_all_data():
    all_records = []
    for file_path in glob.glob(os.path.join(data_dir, "*.ndjson")):
        filename = os.path.basename(file_path)
        room_name = filename.replace("sensor_data_", "").replace(".ndjson", "")
        with open(file_path, "r") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    obj["room"] = room_name
                    all_records.append(obj)
                except json.JSONDecodeError:
                    continue
    return all_records

def standardize_fields(records):
    field_mapping = {
        "co2": ["CO2 (ppm)","CO2","co2"],
        "temperature": ["Temperature (\u00b0C)", "temp","Temp"],
        "humidity": ["Relative Humidity (%)","rh","RH"],
        "timestamp": ["timestamp"]
    }

    standardized = []
    for r in records:
        new_r = {"room": r.get("room")}
        for std_key, aliases in field_mapping.items():
            for alias in aliases:
                if alias in r:
                    new_r[std_key] = r[alias]
                    break
        standardized.append(new_r)
    return standardized

def prepare_dataframe():
    records = read_all_data()
    records = standardize_fields(records)
    df = pd.DataFrame(records)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
    df = df.dropna(subset=["timestamp"])
    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.day_name()
    df["date"] = df["timestamp"].dt.date
    return df

def analyze_with_llm(query: str, df: pd.DataFrame):
    sample_data = df.sample(n=min(100, len(df))).to_csv(index=False)

    system_prompt = (
        "You are a data analysis assistant expert. You will be given a user query and a sample of a data table.\n"
        "Analyze the given data and respond with appropriate details.\n"
        "If the query is about breakdown by hour, day, or similar category, respond with a JSON object like:\n"
        "{\n"
        "  \"summary\": str, //  Use around 100 words to summary \n"
        "  \"table\": {\n"
        "    \"key_label\": str,    // label for the grouping key (e.g. 'Day', 'Hour')\n"
        "    \"value_label\": str,  // label for the metric (e.g. 'Average CO2')\n"
        "    \"data\": { key: value, ... }\n"
        "  }\n"
        "}\n"
        "If a table is not applicable, set \"table\": null or an empty object and write about 300 words to the summary in point form\n"
        "Response include only the said formatted data And don't return any reading data from raw files.\n"
        "Avoid returning null value for table data.\n"
        "Avoid returning markdown table format or any other information; use key-value pairs when showing summarized data."
    )

    user_prompt = f"""
    Query: {query}

    Data Sample (CSV):
    {sample_data}
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.5,
        max_tokens=1024
    )
    result = response.choices[0].message.content.strip()
    return result

@app.get("/connection/health")
async def health_check():
    return {"status": "Connection Successful!"}

@app.post("/v1/roomdata/query")
async def query_agent(request: QueryRequest):
    df = prepare_dataframe()
    result = analyze_with_llm(request.query, df)
    return {"result": result}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os

app = FastAPI()

# 允许跨域（前端能访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

EXCEL_FILE = "data.xlsx"

# 读取 Excel
def get_data():
    df = pd.read_excel(EXCEL_FILE)
    return df.to_dict(orient="records")

# 接口1：获取所有数据
@app.get("/api/data")
def read_data():
    return get_data()

if __name__ == "__main__":
    import uvicorn
    # 这里我改正确了！
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
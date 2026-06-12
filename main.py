from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
from datetime import datetime
import numpy as np

app = FastAPI()

# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

EXCEL_FILE = "data.xlsx"

def get_data():
    try:
        if not os.path.exists(EXCEL_FILE):
            print(f"❌ 文件不存在: {os.path.abspath(EXCEL_FILE)}")
            return []
        
        # 读取Excel
        df = pd.read_excel(EXCEL_FILE, engine="openpyxl")
        # 统一清理列名首尾空格
        df.columns = [col.strip() for col in df.columns]

        print(f"✅ 读取成功，共 {len(df)} 条数据")
        print(f"📋 列名：{list(df.columns)}")

        # ========== 修复1：和你Excel真实列名对齐填充空值 ==========
        fill_rule = {
            "年份": 0,
            "月份": 0,
            "一级分类": "未知分类",
            "二级分类": "未知分类",
            "三级分类": "未知分类",
            "品名": "未知品名",
            "店铺": "未知店铺",
            "颜色": "未知颜色",
            "国家": "未知国家",
            "尺码": "未知尺码",
            "销售数量": 0,
            "退货数量": 0,
            "退货原因": "未知原因",
            "退货备注": "无"
        }
        df = df.fillna(fill_rule)

        # ========== 修复2：安全转数字，非法内容强制置0 ==========
        num_cols = ["年份", "月份", "销售数量", "退货数量"]
        for col in num_cols:
            # 转为数值，失败变为NaN，再填充0，最后转整型
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

        # 文本列统一去除首尾空格
        text_cols = df.select_dtypes(include=["object"]).columns
        for col in text_cols:
            df[col] = df[col].astype(str).str.strip()

        # 转为字典列表返回
        result = df.to_dict(orient="records")
        return result

    except Exception as e:
        print(f"❌ 读取Excel失败：{str(e)}")
        return []

# 接口：获取所有数据
@app.get("/api/data")
def read_data():
    return get_data()

# 健康检查接口
@app.get("/api/health")
def health_check():
    if os.path.exists(EXCEL_FILE):
        file_mtime = os.path.getmtime(EXCEL_FILE)
        return {
            "status": "ok",
            "file_path": os.path.abspath(EXCEL_FILE),
            "last_modified": datetime.fromtimestamp(file_mtime).strftime('%Y-%m-%d %H:%M:%S')
        }
    else:
        return {"status": "error", "message": "文件不存在"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 服务器启动中...")
    print(f"📁 Excel文件路径: {os.path.abspath(EXCEL_FILE)}")
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
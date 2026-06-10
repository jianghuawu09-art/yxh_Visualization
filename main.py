from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
from datetime import datetime

app = FastAPI()

# 跨域配置（前端能正常访问）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 你的Excel文件路径
EXCEL_FILE = "data.xlsx"

def get_data():
    try:
        # 1. 检查文件是否存在
        if not os.path.exists(EXCEL_FILE):
            print(f"❌ 文件不存在: {os.path.abspath(EXCEL_FILE)}")
            return []
        
        # 2. 实时读取Excel（每次请求都重新读取，保证数据最新）
        df = pd.read_excel(EXCEL_FILE, engine="openpyxl")
        
        print(f"✅ 读取成功，共 {len(df)} 条数据")
        print(f"📋 列名：{list(df.columns)}")

        # 3. 空值处理（防止前端报错）
        df = df.fillna({
            "年份": 0,
            "月份": 0,
            "分类": "未知分类",
            "品名": "未知品名",
            "店铺": "未知店铺",
            "颜色": "未知颜色",
            "国家": "未知国家",
            "尺码": "未知尺码",
            "销售数量": 0,
            "退货数量": 0,
            "退货原因": "未知原因",
            "退货备注": "无"
        })

        # 4. 强制数据类型转换（防止数字和字符串混合）
        df["年份"] = df["年份"].astype(int)
        df["月份"] = df["月份"].astype(int)
        df["销售数量"] = df["销售数量"].astype(int)
        df["退货数量"] = df["退货数量"].astype(int)

        # 5. 转换为前端可识别的格式
        result = df.to_dict(orient="records")
        return result

    except Exception as e:
        print(f"❌ 读取Excel失败：{str(e)}")
        return []

# 接口：获取所有数据
@app.get("/api/data")
def read_data():
    return get_data()

# 健康检查接口（调试用）
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
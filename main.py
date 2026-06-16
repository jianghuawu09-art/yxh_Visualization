from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
from datetime import datetime
import openpyxl

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
all_data = []
# 新增：记录Excel上次修改时间，实现自动热更新
file_mtime = 0

def get_data():
    global all_data, file_mtime
    # 判断文件是否存在
    if not os.path.exists(EXCEL_FILE):
        print(f"❌ 文件不存在: {os.path.abspath(EXCEL_FILE)}")
        all_data = []
        file_mtime = 0
        return []
    
    # 获取当前文件修改时间
    current_mtime = os.path.getmtime(EXCEL_FILE)
    # 缓存存在 且 文件未修改 → 直接返回缓存
    if all_data and current_mtime == file_mtime:
        return all_data

    # 文件改动/无缓存，重新读取Excel
    try:
        with pd.ExcelFile(EXCEL_FILE, engine="openpyxl") as xls:
            df = pd.read_excel(xls)
            
        df.columns = [col.strip() for col in df.columns]
        print(f"✅ 重新读取Excel，共 {len(df)} 条数据")
        print(f"📋 列名：{list(df.columns)}")

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

        for col, default_val in fill_rule.items():
            if col in df.columns:
                df[col] = df[col].fillna(default_val)
            else:
                print(f"⚠️  警告：Excel中不存在列 [{col}]，已跳过填充")

        num_cols = ["年份", "月份", "销售数量", "退货数量"]
        for col in num_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0).astype(int)

        text_cols = ["一级分类", "二级分类", "三级分类", "品名", "店铺", "颜色", "国家", "尺码", "退货原因", "退货备注"]
        for col in text_cols:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()

        all_data = df.to_dict(orient="records")
        file_mtime = current_mtime # 更新文件修改时间标记
        print(f"✅ 数据处理完成，共 {len(all_data)} 条有效数据")
        return all_data

    except Exception as e:
        print(f"❌ 读取Excel失败：{str(e)}")
        all_data = []
        file_mtime = 0
        return []

# 分页接口 完全匹配前端分页逻辑
@app.get("/api/data")
def read_data(
    page: int = Query(1, ge=1),
    size: int = Query(2000, ge=10, le=2000) # 前端单次2000，这里上限同步2000
):
    data = get_data()
    start = (page - 1) * size
    end = start + size
    return {
        "total": len(data),
        "page": page,
        "size": size,
        "data": data[start:end]
    }

# 手动强制刷新缓存接口
@app.get("/api/refresh")
def refresh_cache():
    global all_data, file_mtime
    all_data = []
    file_mtime = 0
    get_data()
    return {"code": 200, "msg": "缓存刷新成功，已加载最新Excel数据"}

# 健康检查
@app.get("/api/health")
def health_check():
    if os.path.exists(EXCEL_FILE):
        file_mtime_now = os.path.getmtime(EXCEL_FILE)
        return {
            "status": "ok",
            "file_path": os.path.abspath(EXCEL_FILE),
            "last_modified": datetime.fromtimestamp(file_mtime_now).strftime('%Y-%m-%d %H:%M:%S'),
            "cache_total": len(all_data)
        }
    else:
        return {"status": "error", "message": "文件不存在"}

# 启动事件，替代main主线程预加载，适配uvicorn热重载
@app.on_event("startup")
async def startup_load_data():
    print("🔧 服务启动，初始化Excel缓存...")
    get_data()

if __name__ == "__main__":
    import uvicorn
    print("🚀 服务器启动中...")
    print(f"📁 Excel文件路径: {os.path.abspath(EXCEL_FILE)}")
    # 移除主线程get_data，交给startup事件处理
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
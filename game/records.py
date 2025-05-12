import os
import json

RECORDS_FILE = "records.json"

def load_records():
    """加载记录数据"""
    if os.path.exists(RECORDS_FILE):
        with open(RECORDS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    else:
        # 初始化记录数据
        return {
            "初级": {"time": 999, "name": "匿名"},
            "中级": {"time": 999, "name": "匿名"},
            "高级": {"time": 999, "name": "匿名"}
        }

def save_records(records):
    """保存记录数据"""
    with open(RECORDS_FILE, "w", encoding="utf-8") as file:
        json.dump(records, file, ensure_ascii=False, indent=4)

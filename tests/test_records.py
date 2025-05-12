import os
import json
import unittest
from game.records import load_records, save_records, RECORDS_FILE

class TestRecords(unittest.TestCase):
    def setUp(self):
        """在每个测试前运行，确保测试环境干净"""
        if os.path.exists(RECORDS_FILE):
            os.remove(RECORDS_FILE)

    def tearDown(self):
        """在每个测试后运行，清理测试文件"""
        if os.path.exists(RECORDS_FILE):
            os.remove(RECORDS_FILE)

    def test_load_records_initial(self):
        """测试加载初始记录"""
        records = load_records()
        self.assertEqual(records, {
            "初级": {"time": 999, "name": "匿名"},
            "中级": {"time": 999, "name": "匿名"},
            "高级": {"time": 999, "name": "匿名"}
        })

    def test_save_and_load_records(self):
        """测试保存和加载记录"""
        records = {
            "初级": {"time": 100, "name": "Alice"},
            "中级": {"time": 200, "name": "Bob"},
            "高级": {"time": 300, "name": "Charlie"}
        }
        save_records(records)
        loaded_records = load_records()
        self.assertEqual(loaded_records, records)

    def test_load_records_existing_file(self):
        """测试从已有文件加载记录"""
        records = {
            "初级": {"time": 150, "name": "TestUser"},
            "中级": {"time": 250, "name": "TestUser2"},
            "高级": {"time": 350, "name": "TestUser3"}
        }
        with open(RECORDS_FILE, "w", encoding="utf-8") as file:
            json.dump(records, file, ensure_ascii=False, indent=4)
        loaded_records = load_records()
        self.assertEqual(loaded_records, records)

if __name__ == "__main__":
    unittest.main()

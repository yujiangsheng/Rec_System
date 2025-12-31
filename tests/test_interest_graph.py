"""
单元测试 - 兴趣图谱测试

测试InterestGraph的核心功能
"""

import unittest
import json
from datetime import datetime, timedelta
from src.interest_graph import InterestGraph


class TestInterestGraph(unittest.TestCase):
    """测试兴趣图谱"""
    
    def setUp(self):
        """每个测试前的初始化"""
        self.graph = InterestGraph()
    
    def test_add_interest(self):
        """测试添加兴趣"""
        self.graph.add_interest("Python编程", weight=0.8)
        self.assertIn("Python编程", self.graph.graph.nodes())
        
    def test_get_top_interests(self):
        """测试获取top兴趣"""
        self.graph.add_interest("Python", 0.9)
        self.graph.add_interest("JavaScript", 0.7)
        self.graph.add_interest("Java", 0.5)
        
        top = self.graph.get_top_interests(k=2)
        self.assertEqual(len(top), 2)
        self.assertEqual(top[0][0], "Python")
    
    def test_interest_decay(self):
        """测试兴趣衰减"""
        self.graph.add_interest("初始兴趣", weight=1.0)
        original_weight = self.graph.graph.nodes["初始兴趣"]["weight"]
        
        # 模拟时间衰减
        self.graph.decay_interests(days=7)
        decayed_weight = self.graph.graph.nodes["初始兴趣"]["weight"]
        
        self.assertLess(decayed_weight, original_weight)
    
    def test_serialization(self):
        """测试序列化和反序列化"""
        self.graph.add_interest("兴趣1", 0.8)
        self.graph.add_interest("兴趣2", 0.6)
        self.graph.add_edge("兴趣1", "兴趣2", weight=0.5)
        
        # 保存
        data = self.graph.serialize()
        
        # 加载
        new_graph = InterestGraph()
        new_graph.deserialize(data)
        
        self.assertEqual(len(new_graph.graph.nodes()), 2)
        self.assertTrue(new_graph.graph.has_edge("兴趣1", "兴趣2"))


if __name__ == "__main__":
    unittest.main()

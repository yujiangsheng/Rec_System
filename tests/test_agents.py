"""
单元测试 - 智能体测试

测试AgentA和AgentB的基本功能
"""

import unittest
from src.agents import AgentA, AgentB
from src.interest_graph import InterestGraph


class TestAgentA(unittest.TestCase):
    """测试推荐智能体"""
    
    def setUp(self):
        """每个测试前的初始化"""
        self.agent_a = AgentA()
        self.graph = InterestGraph()
        self.graph.add_interest("Python编程", weight=0.8)
        self.graph.add_interest("数据分析", weight=0.7)
    
    def test_recommend_returns_list(self):
        """测试推荐返回列表"""
        recommendations = self.agent_a.recommend(self.graph)
        self.assertIsInstance(recommendations, list)
        self.assertGreater(len(recommendations), 0)
    
    def test_recommendation_structure(self):
        """测试推荐结构"""
        recommendations = self.agent_a.recommend(self.graph)
        rec = recommendations[0]
        
        # 检查必要字段
        self.assertIn("id", rec)
        self.assertIn("title", rec)
        self.assertIn("reason", rec)
        self.assertIn("confidence", rec)


class TestAgentB(unittest.TestCase):
    """测试评估智能体"""
    
    def setUp(self):
        """每个测试前的初始化"""
        self.agent_b = AgentB()
    
    def test_evaluate_returns_dict(self):
        """测试评估返回字典"""
        recommendations = [
            {"id": 1, "title": "推荐1"},
            {"id": 2, "title": "推荐2"}
        ]
        feedback = {
            "clicked_indices": [0],
            "browse_times": [50.0],
            "conversion": True,
            "satisfaction": 0.8
        }
        
        result = self.agent_b.evaluate(recommendations, feedback)
        self.assertIsInstance(result, dict)
        self.assertIn("quality_score", result)
        self.assertIn("suggestions", result)
    
    def test_quality_score_range(self):
        """测试质量评分范围"""
        recommendations = [{"id": 1, "title": "推荐1"}]
        feedback = {
            "clicked_indices": [0],
            "browse_times": [50.0],
            "satisfaction": 0.8
        }
        
        result = self.agent_b.evaluate(recommendations, feedback)
        score = result["quality_score"]
        
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 1)


if __name__ == "__main__":
    unittest.main()

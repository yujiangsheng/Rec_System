"""
单元测试：验证系统各个模块的功能
"""
import unittest
from interest_graph import InterestGraph
from agent_a import AgentA
from agent_b import AgentB, FeedbackMetrics
from evolution_manager import SessionManager, EvolutionManager


class TestInterestGraph(unittest.TestCase):
    \"\"\"测试兴趣图谱\"\"\"
    
    def setUp(self):
        self.graph = InterestGraph(\"test_user\")
    
    def test_add_interest(self):
        \"\"\"测试添加兴趣\"\"\"
        self.graph.add_interest(\"机器学习\", \"AI\", weight=0.8)
        self.assertIn(\"AI:机器学习\", self.graph.graph)
        self.assertEqual(self.graph.node_weights[\"AI:机器学习\"], 0.8)
    
    def test_add_relation(self):
        \"\"\"测试添加关系\"\"\"
        self.graph.add_relation(\"Python\", \"机器学习\", \"编程\", \"AI\", strength=0.7)
        self.assertTrue(self.graph.graph.has_edge(\"编程:Python\", \"AI:机器学习\"))\n    \n    def test_get_top_interests(self):
        \"\"\"测试获取排名前k的兴趣\"\"\"
        self.graph.add_interest(\"Python\", \"编程\", weight=0.9)
        self.graph.add_interest(\"Java\", \"编程\", weight=0.7)
        self.graph.add_interest(\"深度学习\", \"AI\", weight=0.85)
        
        top = self.graph.get_top_interests(top_k=2)
        self.assertEqual(len(top), 2)\n        self.assertEqual(top[0][0], \"编程:Python\")\n    \n    def test_graph_serialization(self):
        \"\"\"测试图谱的序列化和反序列化\"\"\"
        self.graph.add_interest(\"机器学习\", \"AI\", weight=0.8)\n        self.graph.add_interest(\"深度学习\", \"AI\", weight=0.75)\n        \n        # 序列化\n        data = self.graph.to_dict()\n        \n        # 反序列化\n        graph2 = InterestGraph.from_dict(data)\n        self.assertEqual(graph2.user_id, \"test_user\")\n        self.assertEqual(len(graph2.graph), len(self.graph.graph))\n\n\nclass TestAgentB(unittest.TestCase):\n    \"\"\"测试评估智能体B\"\"\"\n    \n    def setUp(self):\n        self.agent_b = AgentB()\n    \n    def test_feedback_metrics(self):\n        \"\"\"测试反馈指标计算\"\"\"  \n        metrics = FeedbackMetrics(\n            click_count=2,\n            total_recommendations=5,\n            browse_time=120,\n            conversion=True,\n            satisfaction=0.8\n        )\n        \n        self.assertEqual(metrics.click_ratio(), 0.4)\n        quality = metrics.quality_score()\n        self.assertGreater(quality, 0.5)\n        self.assertLessEqual(quality, 1.0)\n    \n    def test_evaluate_recommendations(self):\n        \"\"\"测试推荐评估\"\"\"  \n        recs = [\n            {\"title\": \"推荐1\", \"description\": \"描述1\"},\n            {\"title\": \"推荐2\", \"description\": \"描述2\"},\n        ]\n        \n        feedback = {\n            \"clicked_indices\": [0],\n            \"browse_times\": [60],\n            \"conversion\": False,\n            \"satisfaction\": 0.6,\n            \"user_comment\": \"还可以\"\n        }\n        \n        report = self.agent_b.evaluate_recommendations(recs, feedback)\n        \n        self.assertIn(\"quality_score\", report)\n        self.assertIn(\"click_ratio\", report)\n        self.assertIn(\"issues\", report)\n    \n    def test_self_improve(self):\n        \"\"\"测试自我改进\"\"\"  \n        # 添加反馈记录\n        for i in range(5):\n            recs = [{\"title\": f\"rec{j}\"} for j in range(5)]\n            feedback = {\n                \"clicked_indices\": [0, 1, 2] if i < 3 else [0, 1],\n                \"browse_times\": [60, 70, 80] if i < 3 else [40, 50],\n                \"conversion\": i < 3,\n                \"satisfaction\": 0.8 if i < 3 else 0.5\n            }\n            self.agent_b.evaluate_recommendations(recs, feedback)\n        \n        result = self.agent_b.self_improve()\n        self.assertTrue(result[\"improved\"])\n        self.assertGreater(len(result[\"new_rules\"]), 0)\n\n\nclass TestEvolutionManager(unittest.TestCase):\n    \"\"\"测试演化管理器\"\"\"  \n    \n    def setUp(self):\n        self.evo_mgr = EvolutionManager()\n        self.interest_graph = InterestGraph(\"test_user\")\n    \n    def test_user_interaction(self):\n        \"\"\"测试完整的用户交互流程\"\"\"  \n        recommendations = [\n            {\"title\": \"推荐1\", \"description\": \"描述1\"},\n            {\"title\": \"推荐2\", \"description\": \"描述2\"},\n        ]\n        \n        feedback = {\n            \"clicked_indices\": [0],\n            \"browse_times\": [60],\n            \"conversion\": False,\n            \"satisfaction\": 0.7\n        }\n        \n        result = self.evo_mgr.process_user_interaction(\n            \"user_001\",\n            \"测试查询\",\n            self.interest_graph,\n            feedback\n        )\n        \n        self.assertIn(\"recommendations\", result)\n        self.assertIn(\"evaluation\", result)\n        self.assertIn(\"guidance\", result)\n\n\nclass TestSessionManager(unittest.TestCase):\n    \"\"\"测试会话管理器\"\"\"  \n    \n    def setUp(self):\n        self.session_mgr = SessionManager()\n    \n    def test_user_creation(self):\n        \"\"\"测试用户创建\"\"\"  \n        graph, evo_mgr = self.session_mgr.get_or_create_user(\"user_001\")\n        \n        self.assertIsNotNone(graph)\n        self.assertIsNotNone(evo_mgr)\n        self.assertIn(\"user_001\", self.session_mgr.users)\n    \n    def test_get_user_profile(self):\n        \"\"\"测试获取用户档案\"\"\"  \n        user_id = \"user_001\"\n        self.session_mgr.get_or_create_user(user_id)\n        \n        profile = self.session_mgr.get_user_profile(user_id)\n        \n        self.assertEqual(profile[\"user_id\"], user_id)\n        self.assertIn(\"interests\", profile)\n        self.assertIn(\"system_health\", profile)\n\n\nclass TestIntegration(unittest.TestCase):\n    \"\"\"集成测试：完整工作流程\"\"\"  \n    \n    def test_complete_workflow(self):\n        \"\"\"测试完整的推荐-反馈-改进流程\"\"\"  \n        session = SessionManager()\n        user_id = \"integration_test_user\"\n        \n        # 模拟3次交互\n        for i in range(3):\n            feedback = {\n                \"clicked_indices\": [0, 1],\n                \"browse_times\": [60, 70],\n                \"conversion\": i == 2,  # 最后一次转化\n                \"satisfaction\": 0.6 + i*0.1\n            }\n            \n            result = session.process_interaction(\n                user_id,\n                f\"查询主题{i+1}\",\n                feedback\n            )\n            \n            # 验证结果\n            self.assertIn(\"recommendations\", result)\n            self.assertGreater(len(result[\"recommendations\"]), 0)\n            self.assertIn(\"evaluation\", result)\n        \n        # 验证用户档案\n        profile = session.get_user_profile(user_id)\n        self.assertEqual(profile[\"interaction_count\"], 3)\n        self.assertGreater(profile[\"graph_size\"], 0)\n\n\nif __name__ == \"__main__\":\n    unittest.main(verbosity=2)\n
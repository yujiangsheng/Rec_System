"""
演化管理系统

管理智能体A和B的协作、用户交互流程和演化过程。
"""

from typing import Dict, List, Tuple
from datetime import datetime
from src.agents.agent_a import AgentA
from src.agents.agent_b import AgentB
from src.interest_graph import InterestGraph


class EvolutionManager:
    """管理两个智能体的演化过程"""
    
    def __init__(self):
        self.agent_a = AgentA()
        self.agent_b = AgentB()
        self.evolution_history = []
        self.total_iterations = 0
        self.mutual_benefit_score = 0.0
        
    def process_user_interaction(self, user_id: str, user_query: str,
                                 interest_graph: InterestGraph,
                                 feedback_data: Dict) -> Dict:
        """处理完整的用户交互循环"""
        self.total_iterations += 1
        
        # 智能体A生成推荐
        recommendations = self.agent_a.generate_recommendations(
            user_query,
            interest_graph
        )
        
        # 智能体B评估推荐
        evaluation_report = self.agent_b.evaluate_recommendations(
            recommendations,
            feedback_data
        )
        
        # 智能体B生成改进建议
        guidance = self.agent_b.generate_guidance(self.agent_a.get_stats())
        
        # 更新兴趣图谱
        self._update_interest_graph(
            interest_graph,
            user_query,
            recommendations,
            feedback_data
        )
        
        # 判断是否触发演化
        should_evolve = self.agent_b.should_trigger_evolution()
        
        result = {
            "iteration": self.total_iterations,
            "user_id": user_id,
            "query": user_query,
            "recommendations": recommendations,
            "evaluation": evaluation_report,
            "guidance": guidance,
            "graph_version": interest_graph.version,
            "evolved": False,
            "evolution_info": None
        }
        
        # 执行演化
        if should_evolve:
            evolution_info = self._trigger_evolution()
            result["evolved"] = True
            result["evolution_info"] = evolution_info
            self.evolution_history.append(evolution_info)
        
        # 更新互惠受益分数
        self._update_mutual_benefit_score(evaluation_report)
        result["mutual_benefit_score"] = self.mutual_benefit_score
        
        return result
    
    def _update_interest_graph(self, interest_graph: InterestGraph,
                              user_query: str, recommendations: List[Dict],
                              feedback_data: Dict):
        """根据反馈更新兴趣图谱"""
        # 添加查询作为兴趣
        interest_graph.add_interest(user_query, "query", weight=0.6)
        
        # 为点击的推荐添加兴趣关系
        clicked_indices = feedback_data.get("clicked_indices", [])
        for idx in clicked_indices:
            if idx < len(recommendations):
                title = recommendations[idx].get("title", "")
                if title:
                    interest_graph.add_interest(title, "clicked", weight=0.8)
                    # 添加查询和推荐的关联
                    interest_graph.add_relation(
                        user_query, title, "query", "clicked", strength=0.7
                    )
    
    def _trigger_evolution(self) -> Dict:
        """触发两个智能体的版本演化"""
        b_improvement = self.agent_b.self_improve()
        
        # 智能体A应用改进
        improvements = self.agent_b.improvement_rules[-3:] if self.agent_b.improvement_rules else []
        improvements_dict = {
            "adjust_ranking": any(r.get("priority") == "high" for r in improvements),
            "add_filters": len(improvements) > 1
        }
        self.agent_a.set_improvements(improvements_dict)
        
        evolution_record = {
            "timestamp": datetime.now().isoformat(),
            "iteration": self.total_iterations,
            "agent_a_version_before": self.agent_a.version - 1,
            "agent_a_version_after": self.agent_a.version,
            "agent_b_version_before": self.agent_b.version - 1,
            "agent_b_version_after": self.agent_b.version,
            "evolution_stage": self.agent_b.evolution_stages,
            "improvements_applied": improvements_dict,
            "new_rules": b_improvement.get("new_rules", [])
        }
        
        return evolution_record
    
    def _update_mutual_benefit_score(self, evaluation_report: Dict):
        """更新互惠受益分数"""
        quality = evaluation_report.get("quality_score", 0)
        
        # 使用指数移动平均
        self.mutual_benefit_score = (
            0.7 * self.mutual_benefit_score +
            0.3 * quality
        )
    
    def get_system_health(self) -> Dict:
        """获取系统整体健康状态"""
        return {
            "total_iterations": self.total_iterations,
            "evolution_stages": self.agent_b.evolution_stages,
            "total_evolutions": len(self.evolution_history),
            "mutual_benefit_score": self.mutual_benefit_score,
            "agent_a_stats": self.agent_a.get_stats(),
            "agent_b_stats": self.agent_b.get_stats(),
            "evolution_history": self.evolution_history[-5:]
        }


class SessionManager:
    """会话管理"""
    
    def __init__(self):
        self.users = {}
        self.evolution_managers = {}
        self.session_history = {}
        
    def get_or_create_user(self, user_id: str) -> Tuple[InterestGraph, EvolutionManager]:
        """获取或创建用户的兴趣图谱和演化管理器"""
        if user_id not in self.users:
            self.users[user_id] = InterestGraph(user_id)
            self.evolution_managers[user_id] = EvolutionManager()
            self.session_history[user_id] = []
        
        return (
            self.users[user_id],
            self.evolution_managers[user_id]
        )
    
    def process_interaction(self, user_id: str, user_query: str,
                           feedback_data: Dict) -> Dict:
        """处理用户交互"""
        interest_graph, evo_manager = self.get_or_create_user(user_id)
        
        result = evo_manager.process_user_interaction(
            user_id,
            user_query,
            interest_graph,
            feedback_data
        )
        
        # 记录交互历史
        self.session_history[user_id].append({
            "query": user_query,
            "timestamp": datetime.now().isoformat(),
            "result": result
        })
        
        return result
    
    def get_user_profile(self, user_id: str) -> Dict:
        """获取用户档案"""
        if user_id not in self.users:
            return {"user_id": user_id, "error": "用户不存在"}
        
        interest_graph = self.users[user_id]
        evo_manager = self.evolution_managers[user_id]
        
        return {
            "user_id": user_id,
            "interests": interest_graph.get_top_interests(top_k=10),
            "graph_version": interest_graph.version,
            "graph_size": len(interest_graph.graph),
            "system_health": evo_manager.get_system_health(),
            "interaction_count": len(self.session_history.get(user_id, []))
        }

"""
评估智能体 (Agent B)

根据用户反馈评估推荐质量，提供改进建议。
支持自我改进和版本演化。
"""

from typing import Dict, List
from dataclasses import dataclass
from datetime import datetime
import json
from src.config import EVOLUTION_THRESHOLD, MIN_CLICK_RATIO


@dataclass
class FeedbackMetrics:
    """反馈度量指标"""
    click_count: int = 0
    total_recommendations: int = 0
    browse_time: float = 0.0
    conversion: bool = False
    satisfaction: float = 0.0
    
    def click_ratio(self) -> float:
        """计算点击率"""
        return self.click_count / max(self.total_recommendations, 1)
    
    def quality_score(self) -> float:
        """计算综合质量评分"""
        score = (
            self.click_ratio() * 0.4 +
            min(self.browse_time / 300, 1.0) * 0.3 +
            (1.0 if self.conversion else 0) * 0.2 +
            self.satisfaction * 0.1
        )
        return min(score, 1.0)


class AgentB:
    """评估和改进智能体"""
    
    def __init__(self):
        self.version = 0
        self.feedback_history = []
        self.performance_metrics = {
            "quality_scores": [],
            "click_ratios": [],
            "satisfaction_scores": []
        }
        self.improvement_rules = []
        self.evolution_stages = 0
        
    def evaluate_recommendations(self, recommendations: List[Dict], 
                                 feedback_data: Dict) -> Dict:
        """评估推荐质量"""
        metrics = FeedbackMetrics(
            click_count=len(feedback_data.get("clicked_indices", [])),
            total_recommendations=len(recommendations),
            browse_time=sum(feedback_data.get("browse_times", [])),
            conversion=feedback_data.get("conversion", False),
            satisfaction=feedback_data.get("satisfaction", 0.5)
        )
        
        feedback_record = {
            "timestamp": datetime.now().isoformat(),
            "metrics": {
                "click_ratio": metrics.click_ratio(),
                "quality_score": metrics.quality_score(),
                "browse_time": metrics.browse_time,
                "conversion": metrics.conversion,
                "satisfaction": metrics.satisfaction
            },
            "user_comment": feedback_data.get("user_comment", ""),
            "recommendation_titles": [r.get("title") for r in recommendations]
        }
        self.feedback_history.append(feedback_record)
        
        self.performance_metrics["quality_scores"].append(metrics.quality_score())
        self.performance_metrics["click_ratios"].append(metrics.click_ratio())
        self.performance_metrics["satisfaction_scores"].append(metrics.satisfaction)
        
        report = {
            "quality_score": metrics.quality_score(),
            "click_ratio": metrics.click_ratio(),
            "satisfaction": metrics.satisfaction,
            "is_acceptable": metrics.quality_score() >= 0.5,
            "needs_improvement": metrics.quality_score() < EVOLUTION_THRESHOLD,
            "issues": self._identify_issues(metrics, feedback_data),
            "improvements": []
        }
        
        if report["needs_improvement"]:
            report["improvements"] = self._generate_improvements(
                metrics, recommendations, feedback_data
            )
        
        return report
    
    def _identify_issues(self, metrics: FeedbackMetrics, 
                        feedback_data: Dict) -> List[str]:
        """识别问题"""
        issues = []
        
        if metrics.click_ratio() < MIN_CLICK_RATIO:
            issues.append("点击率过低，推荐相关性不足")
        
        if metrics.browse_time < 10:
            issues.append("浏览时间短，推荐缺乏吸引力")
        
        if not metrics.conversion:
            issues.append("未产生转化，推荐未能满足用户需求")
        
        if metrics.satisfaction < 0.5:
            issues.append("用户满意度不足")
        
        user_comment = feedback_data.get("user_comment", "")
        if "缺少" in user_comment or "不够" in user_comment:
            issues.append(f"用户反馈: {user_comment}")
        
        return issues
    
    def _generate_improvements(self, metrics: FeedbackMetrics,
                              recommendations: List[Dict],
                              feedback_data: Dict) -> List[Dict]:
        """生成改进建议"""
        improvements = []
        
        if metrics.click_ratio() < MIN_CLICK_RATIO:
            improvements.append({
                "type": "improve_relevance",
                "action": "增强查询-推荐的相关性匹配",
                "priority": "high",
                "details": "使用更精细的兴趣图谱匹配"
            })
        
        if metrics.browse_time < 10:
            improvements.append({
                "type": "improve_description",
                "action": "优化推荐描述，增强吸引力",
                "priority": "high",
                "details": "推荐描述应更具体、更吸引人"
            })
        
        if not metrics.conversion:
            improvements.append({
                "type": "expand_diversity",
                "action": "扩大推荐的多样性",
                "priority": "medium",
                "details": "减少重复推荐，增加新颖选项"
            })
        
        user_comment = feedback_data.get("user_comment", "")
        if user_comment:
            improvements.append({
                "type": "incorporate_feedback",
                "action": f"理解反馈: {user_comment}",
                "priority": "high",
                "details": "将用户反馈作为改进信号"
            })
        
        return improvements
    
    def should_trigger_evolution(self) -> bool:
        """判断是否应该触发演化"""
        if len(self.performance_metrics["quality_scores"]) < 5:
            return False
        
        recent_scores = self.performance_metrics["quality_scores"][-5:]
        avg_score = sum(recent_scores) / len(recent_scores)
        
        return avg_score < EVOLUTION_THRESHOLD or self._detect_improvement_trend()
    
    def _detect_improvement_trend(self) -> bool:
        """检测改进趋势"""
        if len(self.performance_metrics["quality_scores"]) < 10:
            return False
        
        recent = self.performance_metrics["quality_scores"][-5:]
        older = self.performance_metrics["quality_scores"][-10:-5]
        
        recent_avg = sum(recent) / len(recent)
        older_avg = sum(older) / len(older)
        
        return recent_avg > older_avg + 0.15
    
    def self_improve(self) -> Dict:
        """自我改进"""
        if len(self.feedback_history) < 3:
            return {"improved": False, "reason": "反馈数据不足"}
        
        successful_patterns = []
        failed_patterns = []
        
        for feedback in self.feedback_history:
            score = feedback["metrics"]["quality_score"]
            if score > 0.7:
                successful_patterns.append(feedback)
            elif score < 0.4:
                failed_patterns.append(feedback)
        
        new_rules = []
        if successful_patterns:
            new_rules.append({
                "rule_id": f"rule_{self.version}_success",
                "description": "基于成功反馈学习的规则",
                "success_rate": len(successful_patterns) / len(self.feedback_history),
                "priority": "high"
            })
        
        if failed_patterns:
            new_rules.append({
                "rule_id": f"rule_{self.version}_avoid",
                "description": "基于失败反馈学习的避免规则",
                "failure_rate": len(failed_patterns) / len(self.feedback_history),
                "priority": "high"
            })
        
        self.improvement_rules.extend(new_rules)
        self.version += 1
        self.evolution_stages += 1
        
        return {
            "improved": True,
            "new_rules": new_rules,
            "evolution_stage": self.evolution_stages,
            "average_quality": sum(self.performance_metrics["quality_scores"]) / len(self.performance_metrics["quality_scores"])
        }
    
    def generate_guidance(self, agent_a_stats: Dict) -> Dict:
        """生成对智能体A的指导"""
        guidance = {
            "version": self.version,
            "suggestions": [],
            "priority_actions": []
        }
        
        if len(self.performance_metrics["quality_scores"]) >= 5:
            recent_scores = self.performance_metrics["quality_scores"][-5:]
            avg_score = sum(recent_scores) / len(recent_scores)
            
            if avg_score < EVOLUTION_THRESHOLD:
                guidance["priority_actions"].append({
                    "action": "adjust_ranking_strategy",
                    "reason": "整体质量偏低",
                    "target": "提升质量到0.6以上"
                })
            
            if sum(self.performance_metrics["click_ratios"]) / len(self.performance_metrics["click_ratios"]) < 0.3:
                guidance["priority_actions"].append({
                    "action": "improve_relevance",
                    "reason": "平均点击率过低",
                    "target": "点击率目标0.4+"
                })
        
        if self.improvement_rules:
            guidance["suggestions"].append({
                "type": "apply_learned_rules",
                "rules": self.improvement_rules[-3:],
                "reason": "应用最近学习的改进规则"
            })
        
        return guidance
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        if not self.performance_metrics["quality_scores"]:
            return {
                "version": self.version,
                "evolution_stages": self.evolution_stages,
                "feedback_count": len(self.feedback_history)
            }
        
        return {
            "version": self.version,
            "evolution_stages": self.evolution_stages,
            "feedback_count": len(self.feedback_history),
            "avg_quality_score": sum(self.performance_metrics["quality_scores"]) / len(self.performance_metrics["quality_scores"]),
            "avg_click_ratio": sum(self.performance_metrics["click_ratios"]) / len(self.performance_metrics["click_ratios"]),
            "avg_satisfaction": sum(self.performance_metrics["satisfaction_scores"]) / len(self.performance_metrics["satisfaction_scores"]),
            "total_improvement_rules": len(self.improvement_rules),
            "recent_feedback": self.feedback_history[-3:] if self.feedback_history else []
        }

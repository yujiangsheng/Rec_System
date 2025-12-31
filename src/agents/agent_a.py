"""
推荐智能体 (Agent A)

基于用户兴趣图谱和查询生成个性化推荐。
使用Qwen2.5-0.5B-Instruct LLM生成自然语言推荐。
"""

from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from typing import List, Dict
from src.interest_graph import InterestGraph
from src.config import DEVICE, MODEL_NAME, RECOMMENDATION_NUM
import json


class AgentA:
    """推荐智能体"""
    
    def __init__(self):
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            self.model = AutoModelForCausalLM.from_pretrained(
                MODEL_NAME,
                torch_dtype=torch.float16 if DEVICE.type == "cuda" else torch.float32,
                device_map=DEVICE
            )
        except Exception as e:
            print(f"⚠️  模型加载失败: {e}，使用模拟模式")
            self.tokenizer = None
            self.model = None
        
        self.version = 0
        self.total_recommendations = 0
        self.recommendation_history = []
        
    def generate_recommendations(self, user_query: str, interest_graph: InterestGraph) -> List[Dict]:
        """生成推荐"""
        interest_context = interest_graph.get_recommendations_context(top_k=8)
        top_interests = interest_graph.get_top_interests(top_k=5)
        
        prompt = self._build_prompt(user_query, interest_context, top_interests)
        
        if self.model is not None:
            recommendations = self._generate_with_model(prompt, user_query)
        else:
            recommendations = self._generate_mock_recommendations(user_query, top_interests)
        
        recommendations = self._rank_recommendations(recommendations, user_query, top_interests)
        
        self.total_recommendations += len(recommendations)
        self.recommendation_history.append({
            "query": user_query,
            "recommendations": [r["title"] for r in recommendations],
            "timestamp": __import__('datetime').datetime.now().isoformat()
        })
        
        return recommendations[:RECOMMENDATION_NUM]
    
    def _build_prompt(self, user_query: str, interest_context: str, top_interests) -> str:
        """构造提示词"""
        # top_interests 是 List[Tuple[str, float]] 格式
        if isinstance(top_interests, list):
            interests_str = ", ".join([t[0].split(":")[-1] for t in top_interests[:5]])
        else:
            interests_str = ", ".join(list(top_interests.keys())[:5])
        
        prompt = f"""你是一个专业的个性化推荐系统。
用户的主要兴趣包括: {interest_context}
用户最重视的兴趣领域: {interests_str}

用户当前的需求是: {user_query}

请根据用户的兴趣和需求，生成5条有针对性的推荐。
每条推荐需要包含:
1. 标题 (title)
2. 简短描述 (description, 20字以内)
3. 推荐理由 (reason, 30字以内)

输出格式为JSON数组。"""
        return prompt
    
    def _generate_with_model(self, prompt: str, user_query: str) -> List[Dict]:
        """使用模型生成推荐"""
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt").to(DEVICE)
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=512,
                    temperature=0.7,
                    top_p=0.95,
                    do_sample=True
                )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            try:
                start = response.find('[')
                end = response.rfind(']')
                if start != -1 and end != -1:
                    json_str = response[start:end+1]
                    recommendations = json.loads(json_str)
                else:
                    recommendations = self._generate_mock_recommendations(user_query, {})
            except json.JSONDecodeError:
                recommendations = self._generate_mock_recommendations(user_query, {})
            
            return recommendations
        except Exception as e:
            print(f"⚠️  模型生成失败: {e}")
            return self._generate_mock_recommendations(user_query, {})
    
    def _generate_mock_recommendations(self, user_query: str, top_interests: Dict) -> List[Dict]:
        """生成模拟推荐"""
        recommendation_templates = {
            "机器学习": [
                {"title": "吴恩达机器学习课程", "description": "经典ML入门课程", "reason": "您对AI感兴趣"},
                {"title": "深度学习专项课程", "description": "神经网络和深度学习", "reason": "进阶学习内容"},
                {"title": "竞赛实战项目", "description": "Kaggle竞赛指南", "reason": "巩固实践能力"}
            ],
            "数据分析": [
                {"title": "Pandas数据处理指南", "description": "数据清洗和分析", "reason": "核心数据工具"},
                {"title": "SQL数据库优化", "description": "数据库性能调优", "reason": "提升查询效率"},
                {"title": "可视化仪表板", "description": "Tableau/PowerBI教程", "reason": "数据展现"}
            ]
        }
        
        recommendations = []
        for key, recs in recommendation_templates.items():
            if key.lower() in user_query.lower():
                recommendations = recs[:5]
                break
        
        if not recommendations:
            recommendations = [
                {"title": f"关于{user_query}的完整指南", "description": "综合教程", "reason": "直接匹配需求"},
                {"title": f"{user_query}进阶实战", "description": "项目实战", "reason": "应用练习"},
                {"title": f"{user_query}社区资源", "description": "学习社区", "reason": "共同学习"}
            ]
        
        return recommendations
    
    def _rank_recommendations(self, recommendations: List[Dict], 
                             user_query: str, top_interests: Dict) -> List[Dict]:
        """排序推荐"""
        for rec in recommendations:
            relevance = 0.5
            query_words = set(user_query.lower().split())
            title_words = set(rec.get("title", "").lower().split())
            match_ratio = len(query_words & title_words) / max(len(query_words), 1)
            relevance += match_ratio * 0.3
            
            if top_interests:
                rec["relevance"] = min(relevance + 0.2, 1.0)
            else:
                rec["relevance"] = relevance
            
            rec["score"] = min(relevance, 1.0)
        
        return sorted(recommendations, key=lambda x: x.get("score", 0), reverse=True)
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return {
            "version": self.version,
            "total_recommendations": self.total_recommendations,
            "recent_history": self.recommendation_history[-10:]
        }
    
    def update_version(self):
        """更新版本号"""
        self.version += 1
    
    def set_improvements(self, improvements: Dict):
        """应用改进"""
        if improvements.get("adjust_ranking"):
            pass
        if improvements.get("add_filters"):
            pass
        self.version += 1

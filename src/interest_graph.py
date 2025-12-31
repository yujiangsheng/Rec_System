"""
用户兴趣图谱管理模块

本模块实现一个动态的用户兴趣知识图谱，支持：
  1. 兴趣节点的动态添加和权重更新
  2. 兴趣之间关系的建立和加强
  3. 权重衰减机制 (长期未访问的兴趣自动衰减)
  4. 图谱自动修剪 (当节点数超限时)
  5. 完整的序列化和反序列化

图谱结构：
  - 节点类型：query(查询), clicked(被点击), feedback(反馈)
  - 节点权重：0-1的范围，表示兴趣强度
  - 边权重：表示两个兴趣之间的关联强度
"""
import networkx as nx
from datetime import datetime
from typing import Dict, List, Set, Tuple
import json
import math
from src.config import INTEREST_DECAY_FACTOR, NEW_INTEREST_WEIGHT, MAX_GRAPH_SIZE, INTEREST_UPDATE_ALPHA


class InterestGraph:
    """
    用户兴趣知识图谱 - 使用有向图表示用户的多维兴趣模型。
    
    核心思想：
      - 将用户的兴趣表示为图节点
      - 用边表示兴趣之间的关联
      - 通过权重追踪兴趣强度
      - 自动衰减长期未访问的兴趣
      - 持续演化以适应用户变化
    
    Attributes:
        user_id (str): 用户唯一标识
        graph (nx.DiGraph): 有向图结构，节点为兴趣项，边为关联关系
        node_weights (dict): 每个节点的权重 (0-1), 表示兴趣强度
        edge_weights (dict): 每条边的权重，表示关联强度
        last_update (dict): 每个节点的最后更新时间 (ISO格式)
        access_count (dict): 每个节点的访问次数
        version (int): 图谱版本号，每次修改递增
    """
    
    def __init__(self, user_id: str):
        """
        初始化空的兴趣图谱。
        
        Args:
            user_id (str): 用户唯一标识，用于持久化和多用户支持
        """
        self.user_id = user_id
        self.graph = nx.DiGraph()  # 有向图：节点=兴趣, 边=关联关系
        self.node_weights = {}  # 节点权重 (兴趣强度)
        self.edge_weights = {}  # 边权重 (关联强度)
        self.last_update = {}  # 每个节点的最后更新时间
        self.access_count = {}  # 访问计数 (用于分析热门兴趣)
        self.version = 0  # 版本号，每次修改递增
        
    def add_interest(self, topic: str, category: str = "general", weight: float = None):
        """
        添加或更新一个兴趣节点。
        
        如果节点已存在，使用指数移动平均更新权重，保留历史信息同时响应最新反馈。
        如果节点不存在，添加新节点并设置初始权重。
        
        Args:
            topic (str): 兴趣主题名称
            category (str): 兴趣类别，默认为general
            weight (float, optional): 权重值 (0-1)
        
        Examples:
            graph = InterestGraph("user_001")
            graph.add_interest("机器学习", "AI", weight=0.8)
            graph.add_interest("Python", "编程", weight=0.9)
        """
        # 如果图谱已满，先进行修剪
        if len(self.graph) >= MAX_GRAPH_SIZE:
            self._prune_graph()
        
        # 构造节点ID (category:topic格式)
        node_id = f"{category}:{topic}"
        
        if node_id in self.graph:
            # ===== 更新现有节点 =====
            old_weight = self.node_weights.get(node_id, 0)
            # 使用指数移动平均更新权重
            # 新权重 = INTEREST_UPDATE_ALPHA(0.3) × 当前权重 + (1-INTEREST_UPDATE_ALPHA) × 历史权重
            # 这样既保留历史记忆(70%)，又响应最新反馈(30%)
            new_weight = 0.7 * old_weight + 0.3 * (weight or 1.0)
            self.node_weights[node_id] = min(new_weight, 1.0)  # 限制在0-1范围
        else:
            # ===== 添加新节点 =====
            self.graph.add_node(node_id, category=category, topic=topic)
            self.node_weights[node_id] = weight or NEW_INTEREST_WEIGHT
        
        # 更新时间戳和访问计数
        self.last_update[node_id] = datetime.now().isoformat()
        self.access_count[node_id] = self.access_count.get(node_id, 0) + 1
        self.version += 1
        
    def add_relation(self, source_topic: str, target_topic: str, 
                     source_cat: str = "general", target_cat: str = "general", 
                     strength: float = 1.0):
        """
        添加兴趣之间的关系。
        
        Args:
            source_topic (str): 源兴趣主题
            target_topic (str): 目标兴趣主题
            source_cat (str): 源兴趣类别
            target_cat (str): 目标兴趣类别
            strength (float): 关系强度 (0-1)
        """
        source_id = f"{source_cat}:{source_topic}"
        target_id = f"{target_cat}:{target_topic}"
        
        # 确保节点存在
        if source_id not in self.graph:
            self.add_interest(source_topic, source_cat)
        if target_id not in self.graph:
            self.add_interest(target_topic, target_cat)
        
        # 添加边
        if self.graph.has_edge(source_id, target_id):
            old_strength = self.edge_weights.get((source_id, target_id), 0)
            self.edge_weights[(source_id, target_id)] = 0.6 * old_strength + 0.4 * strength
        else:
            self.edge_weights[(source_id, target_id)] = strength
            self.graph.add_edge(source_id, target_id, weight=strength)
        
        self.version += 1
        
    def decay_interests(self):
        """衰减长期未访问的兴趣"""
        now = datetime.now()
        decayed_nodes = []
        
        for node_id in self.graph.nodes():
            if node_id in self.last_update:
                last_time = datetime.fromisoformat(self.last_update[node_id])
                days_since = (now - last_time).days
                
                # 指数衰减
                decay_factor = INTEREST_DECAY_FACTOR ** (days_since / 7.0)
                self.node_weights[node_id] *= decay_factor
                
                # 如果权重过低则移除
                if self.node_weights[node_id] < 0.01:
                    decayed_nodes.append(node_id)
        
        for node_id in decayed_nodes:
            self._remove_node(node_id)
        
        self.version += 1
        return len(decayed_nodes)
    
    def get_recommendations_context(self, top_k: int = 10) -> str:
        """生成推荐上下文"""
        self.decay_interests()
        
        # 获取权重最高的节点
        sorted_nodes = sorted(
            self.node_weights.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:top_k]
        
        context = f"用户{self.user_id}的兴趣图谱:\n"
        context += "主要兴趣: " + ", ".join([node[0].split(":")[-1] for node in sorted_nodes]) + "\n"
        
        # 添加关联信息
        if sorted_nodes:
            top_node = sorted_nodes[0][0]
            successors = list(self.graph.successors(top_node))
            if successors:
                context += f"相关兴趣: " + ", ".join(successors[:5]) + "\n"
        
        context += f"(版本: {self.version})"
        return context
    
    def get_top_interests(self, top_k: int = 5) -> List[Tuple[str, float]]:
        """获取排名前k的兴趣"""
        self.decay_interests()
        return sorted(
            self.node_weights.items(),
            key=lambda x: x[1],
            reverse=True
        )[:top_k]
    
    def _prune_graph(self):
        """修剪图谱，保留权重最高的节点"""
        if len(self.graph) <= MAX_GRAPH_SIZE * 0.8:
            return
        
        # 删除权重最低的节点
        nodes_to_remove = len(self.graph) - int(MAX_GRAPH_SIZE * 0.7)
        weak_nodes = sorted(self.node_weights.items(), key=lambda x: x[1])[:nodes_to_remove]
        
        for node_id, _ in weak_nodes:
            self._remove_node(node_id)
    
    def _remove_node(self, node_id: str):
        """移除节点及其相关数据"""
        if node_id in self.graph:
            self.graph.remove_node(node_id)
            self.node_weights.pop(node_id, None)
            self.last_update.pop(node_id, None)
            self.access_count.pop(node_id, None)
            self.version += 1
    
    def to_dict(self) -> Dict:
        """序列化为字典"""
        return {
            "user_id": self.user_id,
            "nodes": dict(self.graph.nodes()),
            "edges": list(self.graph.edges()),
            "node_weights": self.node_weights,
            "edge_weights": self.edge_weights,
            "last_update": self.last_update,
            "access_count": self.access_count,
            "version": self.version
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """从字典反序列化"""
        graph = cls(data["user_id"])
        graph.version = data["version"]
        graph.node_weights = data["node_weights"]
        graph.edge_weights = data["edge_weights"]
        graph.last_update = data["last_update"]
        graph.access_count = data["access_count"]
        
        for node in data["nodes"]:
            graph.graph.add_node(node, **data["nodes"][node])
        
        for source, target in data["edges"]:
            graph.graph.add_edge(source, target)
        
        return graph

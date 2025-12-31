"""
RecSystem - 源代码包

包含所有核心模块：
  - config: 系统配置
  - interest_graph: 用户兴趣图谱
  - agents: 推荐和评估智能体
  - managers: 演化管理器
"""
from .interest_graph import InterestGraph
from .agents import AgentA, AgentB
from .managers import EvolutionManager, SessionManager

__all__ = [
    "InterestGraph",
    "AgentA",
    "AgentB",
    "EvolutionManager",
    "SessionManager",
]
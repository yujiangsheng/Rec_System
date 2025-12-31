"""
RecSystem - 双智能体自适应推荐系统

一个具有自学习和自演化能力的智能推荐系统。

主要功能：
  - 推荐生成 (AgentA)
  - 质量评估 (AgentB)
  - 兴趣建模 (InterestGraph)
  - 自动演化 (EvolutionManager)

快速开始：
  from examples.evolution_demo import EvolutionDemo
  demo = EvolutionDemo()
  demo.run_full_demo()
"""

__version__ = "1.0.0"
__author__ = "RecSystem Team"

# 导出主要类和函数
from src.config import DEVICE, MODEL_NAME, RECOMMENDATION_NUM, EVOLUTION_THRESHOLD
from src.interest_graph import InterestGraph
from src.agents.agent_a import AgentA
from src.agents.agent_b import AgentB
from src.managers.evolution_manager import EvolutionManager, SessionManager

__all__ = [
    'DEVICE',
    'MODEL_NAME',
    'RECOMMENDATION_NUM',
    'EVOLUTION_THRESHOLD',
    'InterestGraph',
    'AgentA',
    'AgentB',
    'EvolutionManager',
    'SessionManager',
]

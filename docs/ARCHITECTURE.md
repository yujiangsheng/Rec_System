# RecSystem 推荐系统架构文档

## 项目概述

RecSystem 是一个高级的双智能体推荐系统，支持：
- 🤖 **双智能体协作**：Agent A（推荐）+ Agent B（评估）
- 📚 **动态兴趣建模**：基于NetworkX图谱的用户兴趣表示
- 🧠 **LLM集成**：使用Qwen2.5-0.5B-Instruct进行自然语言推荐
- ⚡ **持续演化**：根据用户反馈自动版本升级
- 🎯 **多设备支持**：GPU (CUDA/HIP) / Apple Silicon (MPS) / CPU

## 项目目录结构

```
RecSystem/
├── src/                      # 核心源代码目录
│   ├── __init__.py          # 主包初始化，导出关键类
│   ├── config.py            # 全局配置 (设备、模型、超参数)
│   ├── interest_graph.py    # 用户兴趣知识图谱
│   ├── agents/              # 智能体模块
│   │   ├── __init__.py      # 导出 AgentA, AgentB
│   │   ├── agent_a.py       # 推荐智能体 (生成推荐)
│   │   └── agent_b.py       # 评估智能体 (评估质量)
│   └── managers/            # 管理器模块
│       ├── __init__.py      # 导出 EvolutionManager, SessionManager
│       └── evolution_manager.py  # 演化和会话管理
│
├── examples/                 # 示例和演示程序
│   ├── __init__.py
│   ├── evolution_demo.py    # 完整的智能体演化演示
│   └── quick_start.py       # 快速开始指南 (可选)
│
├── tests/                    # 单元测试 (可选)
│   ├── __init__.py
│   ├── test_interest_graph.py
│   ├── test_agents.py
│   └── test_evolution.py
│
├── docs/                     # 文档 (可选)
│   ├── ARCHITECTURE.md      # 项目架构详解
│   ├── API_REFERENCE.md     # API参考文档
│   └── DEVELOPMENT.md       # 开发指南
│
├── scripts/                  # 工具脚本 (可选)
│   ├── train.py            # 模型训练脚本
│   └── evaluate.py         # 模型评估脚本
│
├── setup.py                 # 包安装配置
├── requirements.txt         # 依赖列表
├── README.md               # 项目说明
├── .gitignore              # Git忽略文件
└── __init__.py            # 项目根包初始化
```

## 模块说明

### 1. `src/config.py` - 全局配置
定义系统的全局参数：
- **计算设备**：自动检测GPU/MPS/CPU
- **模型参数**：LLM模型名称、路径
- **系统超参数**：推荐数量、演化阈值、图衰减因子等

```python
from src.config import DEVICE, MODEL_NAME, RECOMMENDATION_NUM
```

### 2. `src/interest_graph.py` - 兴趣图谱
用户兴趣的动态知识图谱实现：
- **图节点**：query、clicked、feedback三类兴趣
- **图边**：兴趣之间的关联强度
- **权重衰减**：长期未访问的兴趣自动衰减
- **自动修剪**：节点数超限时自动清理低权重节点

```python
from src.interest_graph import InterestGraph

graph = InterestGraph()
graph.add_interest("Python编程", weight=0.8)
recommendations = graph.get_top_interests(k=5)
```

### 3. `src/agents/` - 智能体模块

#### `agent_a.py` - 推荐智能体
职责：生成个性化推荐
- 输入：用户兴趣图谱
- 处理：使用LLM生成自然语言推荐
- 输出：推荐列表 + 解释文本
- 演化：版本升级时修改生成策略

```python
from src.agents import AgentA

agent_a = AgentA()
recommendations = agent_a.recommend(interest_graph)
# 返回: [{id, title, reason, confidence, ...}, ...]
```

#### `agent_b.py` - 评估智能体
职责：评估推荐质量并提供改进建议
- 输入：推荐列表 + 用户反馈
- 处理：计算满意度、点击率、转化率等指标
- 输出：质量评分 + 改进建议
- 演化：版本升级时调整评分权重

```python
from src.agents import AgentB

agent_b = AgentB()
evaluation = agent_b.evaluate(recommendations, user_feedback)
# 返回: {quality_score, suggestions, metrics, ...}
```

### 4. `src/managers/` - 管理器模块

#### `evolution_manager.py` - 演化和会话管理
职责：协调双智能体，管理系统演化
- **SessionManager**：管理用户会话和交互历史
- **EvolutionManager**：监控性能，触发版本升级

```python
from src.managers import SessionManager, EvolutionManager

session = SessionManager(user_id="user123")
session.add_interaction(query, recommendations, feedback)

# 检查是否需要演化
if session.should_evolve():
    session.evolve()
```

## 导入方式

### 方式1：从主包导入（推荐用于上层应用）
```python
from recsys import AgentA, AgentB, InterestGraph, SessionManager

agent_a = AgentA()
agent_b = AgentB()
graph = InterestGraph()
session = SessionManager()
```

### 方式2：直接导入（推荐用于开发）
```python
from src.agents import AgentA, AgentB
from src.interest_graph import InterestGraph
from src.managers import SessionManager, EvolutionManager
```

### 方式3：具体导入
```python
from src.agents.agent_a import AgentA
from src.agents.agent_b import AgentB
from src.interest_graph import InterestGraph
from src.managers.evolution_manager import SessionManager
```

## 系统工作流

```
用户查询
   ↓
Agent A 生成推荐
   ↓
用户反馈 (点击、浏览时间、评价)
   ↓
Agent B 评估质量
   ↓
更新用户兴趣图谱
   ↓
判断是否演化
   ├─ YES → Agent A/B 升级版本 → 继续循环
   └─ NO → 继续学习 → 继续循环
```

## 数据流

```
InterestGraph (用户兴趣建模)
    ↓
AgentA.recommend() → 推荐列表
    ↓
用户交互 → 反馈数据
    ↓
AgentB.evaluate() → 质量评分
    ↓
EvolutionManager.should_evolve()
    ├─ YES → 双智能体版本升级
    └─ NO → 继续优化
```

## 关键参数说明

| 参数 | 类型 | 说明 |
|------|------|------|
| `DEVICE` | str | 计算设备 (cuda/mps/cpu) |
| `MODEL_NAME` | str | LLM模型名称 |
| `RECOMMENDATION_NUM` | int | 每次推荐数量 |
| `EVOLUTION_THRESHOLD` | float | 演化触发的质量评分阈值 |
| `INTEREST_DECAY_FACTOR` | float | 兴趣衰减速度 (0-1) |
| `NEW_INTEREST_WEIGHT` | float | 新兴趣的初始权重 |
| `MAX_GRAPH_SIZE` | int | 兴趣图谱的最大节点数 |

## 版本演化机制

系统支持多版本并存：

```
Agent A: v0 (初始) → v1 (第一次演化) → v2 (第二次演化)
Agent B: v0 (初始) → v1 (第一次演化) → v2 (第二次演化)
```

每个版本改进不同方面：
- **v0**：基础策略，学习用户偏好
- **v1**：优化推荐，提高点击率
- **v2**：精细化排序，最大化用户满意度

## 扩展建议

### 1. 添加新的智能体
```python
# src/agents/agent_c.py
class AgentC:
    """新的智能体（如排序智能体）"""
    def rank(self, recommendations, context):
        # 实现排序逻辑
        pass
```

### 2. 替换LLM模型
在 `src/config.py` 中修改：
```python
MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"  # 更大的模型
```

### 3. 添加新的反馈类型
在 `src/interest_graph.py` 中扩展 `add_feedback()` 方法

### 4. 实现自定义评估指标
在 `src/agents/agent_b.py` 中添加新的评分函数

## 生产部署

### 本地开发安装
```bash
pip install -e .
```

### 生产打包
```bash
python setup.py sdist bdist_wheel
```

### 依赖管理
```bash
pip install -r requirements.txt
```

## 常见问题

**Q: 推荐为空？**  
A: 用户兴趣图谱为空，需要先添加初始兴趣

**Q: 如何加速推理？**  
A: 在 `src/config.py` 中启用GPU或使用更小的模型

**Q: 如何自定义演化阈值？**  
A: 修改 `src/config.py` 中的 `EVOLUTION_THRESHOLD`

## 许可证
MIT License

## 联系方式
RecSystem Developer Team

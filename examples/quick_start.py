# 快速开始指南

## 安装

### 方法1：开发安装（推荐）
```bash
cd RecSystem
pip install -e .
```

### 方法2：使用requirements.txt
```bash
pip install -r requirements.txt
```

## 基本用法

### 1. 简单推荐
```python
from src import InterestGraph, AgentA, AgentB

# 创建用户兴趣图谱
graph = InterestGraph()
graph.add_interest("Python编程", weight=0.8)
graph.add_interest("数据分析", weight=0.7)

# Agent A 生成推荐
agent_a = AgentA()
recommendations = agent_a.recommend(graph)

print("推荐结果：")
for rec in recommendations:
    print(f"  - {rec['title']}: {rec['reason']}")

# Agent B 评估质量
agent_b = AgentB()
feedback = {
    "clicked_indices": [0, 1],
    "browse_times": [45.0, 50.0],
    "satisfaction": 0.8
}
evaluation = agent_b.evaluate(recommendations, feedback)
print(f"\n推荐质量评分: {evaluation['quality_score']:.2f}")
```

### 2. 完整会话管理
```python
from src.managers import SessionManager

# 创建会话
session = SessionManager(user_id="user_001")

# 第一次交互
query = "我想学习数据分析"
recommendations = session.get_recommendations(query)
feedback = {
    "clicked_indices": [0, 2],
    "browse_times": [50.0, 45.0],
    "satisfaction": 0.7
}
session.add_interaction(query, recommendations, feedback)

# 检查系统是否需要演化
if session.should_evolve():
    print("系统正在演化...")
    session.evolve()
```

### 3. 运行完整演示
```bash
python examples/evolution_demo.py
```

## 项目结构快速导航

```
RecSystem/
├── src/
│   ├── config.py              # 修改全局参数（设备、模型等）
│   ├── interest_graph.py      # 修改兴趣图谱算法
│   ├── agents/
│   │   ├── agent_a.py         # 修改推荐生成逻辑
│   │   └── agent_b.py         # 修改评估逻辑
│   └── managers/
│       └── evolution_manager.py  # 修改演化策略
│
├── examples/
│   └── evolution_demo.py      # 运行演示
│
└── docs/
    └── ARCHITECTURE.md        # 了解详细架构
```

## 常用代码片段

### 查看设备配置
```python
from src.config import DEVICE, MODEL_NAME
print(f"计算设备: {DEVICE}")
print(f"模型: {MODEL_NAME}")
```

### 自定义配置
```python
# 注意：修改前需要编辑 src/config.py
from src.config import RECOMMENDATION_NUM, EVOLUTION_THRESHOLD

print(f"推荐数量: {RECOMMENDATION_NUM}")
print(f"演化阈值: {EVOLUTION_THRESHOLD}")
```

### 保存和加载兴趣图谱
```python
from src.interest_graph import InterestGraph

# 保存
graph = InterestGraph()
graph.add_interest("Python", 0.8)
graph.save("user_graph.json")

# 加载
graph2 = InterestGraph()
graph2.load("user_graph.json")
```

## 故障排除

### 问题：模型加载缓慢
**解决**：首次加载需要下载模型（1-2GB）。后续自动使用缓存。

### 问题：推荐为空
**解决**：确保兴趣图谱已添加内容
```python
if not graph.graph.nodes():
    graph.add_interest("初始兴趣", weight=0.5)
```

### 问题：GPU内存不足
**解决**：在 `src/config.py` 中改用更小的模型或 CPU

## 下一步

1. 阅读 [架构文档](docs/ARCHITECTURE.md) 了解系统设计
2. 查看 [examples/evolution_demo.py](examples/evolution_demo.py) 学习高级用法
3. 修改 `src/config.py` 自定义系统参数
4. 扩展代码实现自己的需求

## 联系支持
遇到问题？提交 Issue 或 Pull Request！

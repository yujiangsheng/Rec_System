# 双智能体推荐系统 (Dual-Agent Recommendation System)

**作者**: Jiangsheng Yu  
**维护者**: Jiangsheng Yu

## 系统概述

这是一个基于 **Qwen2.5-0.5B-Instruct** 的高级推荐系统，采用双智能体架构，具有演化能力和自我改进机制。

### 核心特性

- 🤖 **智能体A (推荐系统)**: 基于用户兴趣图谱和LLM的个性化推荐引擎
- 🔍 **智能体B (评估系统)**: 实时评估推荐质量，并指导智能体A改进
- 📊 **动态兴趣图谱**: 构建和维护用户的知识图谱，支持持续演化
- 🔄 **双向演化机制**: 两个智能体相互促进，不断改进
- 🧠 **自我学习**: 智能体B具有从反馈中学习的能力
- ⚡ **设备自适应**: 自动选择最优计算设备 (GPU > MPS > CPU)

## 系统架构

```
┌─────────────────────────────────────────────────┐
│         用户交互与反馈系统                        │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌────────────────┐         ┌────────────────┐  │
│  │  智能体A       │         │  智能体B       │  │
│  │  推荐系统      │◄───────►│  评估系统      │  │
│  │  v1 → v2 ...  │         │  v1 → v2 ...  │  │
│  └────────────────┘         └────────────────┘  │
│         ▲                            │            │
│         │ 提供上下文                │ 生成指导    │
│         │                           ▼            │
│  ┌─────────────────────────────────────────┐   │
│  │      用户兴趣图谱                        │   │
│  │   (动态增长、衰减、修剪)                │   │
│  └─────────────────────────────────────────┘   │
│         ▲                           ▲            │
│         └─ 从反馈学习更新 ─────────┘            │
└─────────────────────────────────────────────────┘
```

## 工作流程

### 1. 推荐生成阶段
```
用户查询 → 智能体A获取兴趣图谱 → 构建提示词 → Qwen2.5生成推荐 → 排序和过滤 → 返回Top-5推荐
```

### 2. 反馈评估阶段
```
用户反馈(点击、浏览时间、满意度) 
  ↓
智能体B计算质量评分 = 点击率×0.4 + 浏览时间×0.3 + 转化×0.2 + 满意度×0.1
  ↓
识别问题(相关性不足、吸引力不够、多样性差等)
  ↓
生成改进建议(优化排序、改进描述、扩大多样性)
```

### 3. 兴趣图谱更新
```
用户查询词 → 添加为"query"类型节点
被点击的推荐 → 添加相关词为"clicked"类型节点
用户评论 → 提取词为"feedback"类型节点
关系建立 → 查询词指向被点击推荐词(权重0.7)
衰减机制 → 长期未访问的兴趣指数衰减(周期衰减因子0.95)
```

### 4. 演化触发条件
- 最近5次评估的平均质量评分 < 0.6, 或
- 检测到显著改进趋势(最近5次vs前5次，差异>0.15)

### 5. 演化执行
```
智能体B进化:
  ├─ 分析成功/失败反馈模式
  ├─ 生成新的改进规则
  └─ 版本号递增

智能体A进化:
  ├─ 接收来自B的改进指导
  ├─ 应用新的排序策略
  ├─ 添加过滤规则
  └─ 版本号递增

共同进化:
  └─ 互惠受益分数更新 = 0.7×历史分 + 0.3×当前质量
```

## 快速开始

### 安装依赖

```bash
cd /Users/jiangshengyu/Documents/program/python/RecSystem
pip install -r requirements.txt
```

### 运行演示

```bash
# 演示模式：自动运行完整工作流程
python main.py

# 交互模式：与系统实时交互
python main.py --interactive
```

### 在交互模式中的命令

```
查询词        - 输入任何查询词以获取推荐
profile       - 查看用户兴趣档案
history       - 查看交互历史
exit          - 退出程序
```

## 核心模块说明

### 1. config.py
系统配置和设备选择
```python
# 设备优先级: GPU > MPS > CPU
DEVICE = get_device()
MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

# 关键参数
RECOMMENDATION_NUM = 5          # 推荐数量
EVOLUTION_THRESHOLD = 0.6       # 演化触发阈值
INTEREST_DECAY_FACTOR = 0.95    # 兴趣衰减因子
```

### 2. interest_graph.py
用户兴趣知识图谱
```python
class InterestGraph:
    add_interest(topic, category, weight)      # 添加兴趣节点
    add_relation(source, target, strength)     # 建立兴趣关系
    decay_interests()                          # 衰减长期未访问的兴趣
    get_top_interests(top_k)                   # 获取排名前k的兴趣
    get_recommendations_context()              # 生成推荐上下文
```

### 3. agent_a.py
推荐智能体（基于Qwen2.5）
```python
class AgentA:
    generate_recommendations(query, interest_graph)  # 生成推荐
    _rank_recommendations(...)                       # 排序推荐
    set_improvements(improvements)                   # 应用改进
    get_stats()                                      # 获取统计信息
```

### 4. agent_b.py
评估和改进智能体
```python
class AgentB:
    evaluate_recommendations(recs, feedback)        # 评估推荐
    self_improve()                                  # 自我改进
    should_trigger_evolution()                      # 判断是否演化
    generate_guidance(agent_a_stats)                # 生成改进指导
```

### 5. evolution_manager.py
演化和交互管理
```python
class EvolutionManager:
    process_user_interaction(...)                   # 完整交互循环
    _trigger_evolution()                           # 触发演化

class SessionManager:
    get_or_create_user(user_id)                     # 用户会话管理
    process_interaction(...)                        # 处理交互
    get_user_profile()                              # 获取用户档案
    save_session() / load_session()                 # 持久化
```

## 关键算法

### 兴趣权重更新
```
新权重 = 0.7 × 旧权重 + 0.3 × 当前权重
（使用指数移动平均保持历史记忆）
```

### 质量评分公式
```
Quality = 点击率×0.4 + 浏览时间×0.3 + 转化×0.2 + 满意度×0.1
```

### 兴趣衰减公式
```
衰减后权重 = 原权重 × (0.95 ^ (天数/7))
（周周期衰减，7天衰减到0.95倍）
```

### 互惠受益分数
```
MBS = 0.7 × 历史分 + 0.3 × 当前质量
（追踪双智能体的协作效果）
```

## 使用场景

### 场景1：新用户推荐
1. 用户首次查询"机器学习"
2. 智能体A基于初始权重生成5个推荐
3. 用户浏览并反馈（点击2个，浏览120秒）
4. 智能体B评估质量(0.65)，认为可接受
5. 兴趣图谱添加查询词和被点击推荐

### 场景2：推荐质量低
1. 用户查询"深度学习"
2. 智能体A生成推荐，但用户只点击1个，浏览30秒
3. 智能体B评估质量(0.35)，识别"相关性不足"
4. 生成改进建议：增强匹配度、改进描述
5. 触发演化（如果满足条件），双智能体版本升级

### 场景3：长期交互
1. 经过10次交互，用户的兴趣图谱扩展到50个节点
2. 关键节点权重不断更新，弱关系逐渐衰减
3. 系统发现用户从"ML"转向"医疗AI"
4. 推荐逐渐过渡，兴趣图谱自动优化
5. 多次演化后，系统对该用户形成精准模型

## 数据格式示例

### 用户反馈
```json
{
  "clicked_indices": [0, 2],
  "browse_times": [45.5, 120.3],
  "conversion": false,
  "satisfaction": 0.7,
  "user_comment": "不错，但缺少案例"
}
```

### 推荐项目
```json
{
  "title": "深度学习入门指南",
  "description": "从零开始学习DL",
  "reason": "与您的兴趣匹配度高",
  "score": 0.87,
  "relevance": 0.85
}
```

### 用户档案
```json
{
  "user_id": "user_001",
  "interests": [
    ["AI:机器学习", 0.95],
    ["AI:深度学习", 0.88],
    ["AI:医疗AI", 0.76]
  ],
  "graph_version": 5,
  "graph_size": 42,
  "interaction_count": 15,
  "system_mutual_benefit_score": 0.72
}
```

## 性能指标监测

系统持续监测以下KPI:

| 指标 | 计算方式 | 目标 | 说明 |
|------|--------|------|------|
| 质量评分 | 见上文 | > 0.7 | 综合用户反馈 |
| 点击率 | 点击/推荐数 | > 0.4 | 推荐相关性 |
| 浏览时长 | 累计秒数 | > 60s | 吸引力度量 |
| 转化率 | 完成动作/推荐 | > 0.2 | 最终效果 |
| 满意度 | 用户评分 | > 0.7 | 主观体验 |
| 互惠受益 | 动态加权平均 | > 0.7 | 演化效果 |

## 演化记录示例

```json
{
  "timestamp": "2024-12-28T10:30:45",
  "iteration": 8,
  "evolution_stage": 2,
  "agent_a_version": "1 → 2",
  "agent_b_version": "1 → 2",
  "improvements_applied": {
    "adjust_ranking": true,
    "add_filters": true
  },
  "new_rules": [
    {
      "rule_id": "rule_1_success",
      "description": "基于成功反馈学习的规则",
      "success_rate": 0.67
    }
  ]
}
```

## 扩展开发

### 添加新的反馈维度
编辑 `agent_b.py` 中的 `FeedbackMetrics` 类：
```python
@dataclass
class FeedbackMetrics:
    click_count: int = 0
    total_recommendations: int = 0
    # 添加新维度
    share_count: int = 0  # 分享数
    saved_count: int = 0  # 收藏数
```

### 自定义改进规则
在 `agent_b.py` 中扩展 `_generate_improvements()` 方法。

### 使用不同的LLM
更新 `config.py` 中的 `MODEL_NAME`：
```python
MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"  # 使用更大的模型
```

## 文件结构

```
RecSystem/
├── config.py                  # 系统配置
├── interest_graph.py          # 兴趣图谱
├── agent_a.py                 # 推荐智能体
├── agent_b.py                 # 评估智能体
├── evolution_manager.py       # 演化管理
├── main.py                    # 主程序
├── requirements.txt           # 依赖
└── README.md                  # 本文档
```

## 故障排除

### 问题1: CUDA内存不足
```python
# 在 config.py 中改用float32或CPU
torch_dtype=torch.float32
# 或改用更小的模型
MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"
```

### 问题2: 模型加载失败
系统会自动切换到模拟模式，提供测试数据用于演示演化逻辑。

### 问题3: 性能缓慢
- 检查设备选择是否正确（运行 `python config.py`）
- 减少 `RECOMMENDATION_NUM` 或使用更小的 `top_k` 参数

## 参考资源

- [Qwen2.5 文档](https://huggingface.co/Qwen/Qwen2.5-0.5B-Instruct)
- [Transformers 库](https://huggingface.co/docs/transformers)
- [NetworkX 图论库](https://networkx.org/)

## 许可证

MIT License

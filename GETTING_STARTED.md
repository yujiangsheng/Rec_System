# 🚀 双智能体推荐系统 - 完整项目说明

## 📋 项目概览

这是一个**基于Qwen2.5-0.5B-Instruct**的高级推荐系统，采用双智能体架构，具有演化能力和自我改进机制。

### 🎯 核心创新

| 特性 | 传统系统 | 本系统 |
|------|--------|--------|
| 推荐生成 | 协同过滤/内容 | LLM + 动态图谱 |
| 反馈处理 | 简单统计 | 多维度评估 |
| 自我改进 | 无（需人工调参） | 自动学习 |
| 兴趣模型 | 静态向量 | 动态演化图谱 |
| 系统演化 | 版本发布 | 连续自动演化 |

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────┐
│     用户交互与反馈系统                        │
├─────────────────────────────────────────────┤
│  ┌────────────────┐    ┌────────────────┐  │
│  │  智能体A       │◄──►│  智能体B       │  │
│  │  推荐系统      │    │  评估系统      │  │
│  │  v1→v2...     │    │  v1→v2...     │  │
│  └────────────────┘    └────────────────┘  │
│         ▲                     │             │
│    图谱上下文            改进指导           │
│         │                     ▼             │
│  ┌─────────────────────────────────────┐  │
│  │  用户兴趣图谱                        │  │
│  │  (动态增长、衰减、演化)             │  │
│  └─────────────────────────────────────┘  │
│         ▲                     ▲            │
│    反馈学习                反馈学习        │
└─────────────────────────────────────────────┘
```

---

## 📁 项目结构

```
RecSystem/
├── 📄 README.md                    # 完整使用说明
├── 📄 requirements.txt             # 项目依赖
├── 📄 QUICKSTART.py               # 快速开始指南（本文档）
├── 📄 ARCHITECTURE.py              # 系统架构详解
├── 📄 PROJECT_SUMMARY.py           # 项目总结
│
├── 🔧 配置层
│   └── config.py                   # 系统配置和设备选择
│
├── 📊 数据层
│   └── interest_graph.py           # 用户兴趣知识图谱
│
├── 🤖 智能体层
│   ├── agent_a.py                  # 推荐智能体（基于Qwen2.5）
│   └── agent_b.py                  # 评估改进智能体
│
├── 🔄 演化层
│   └── evolution_manager.py        # 演化和会话管理
│
├── 🚀 应用层
│   ├── main.py                     # 主程序和交互界面
│   ├── advanced_examples.py        # 高级示例
│   └── launcher.py                 # 交互式启动器
│
└── 🧪 测试层
    └── test_system.py              # 单元测试和集成测试
```

---

## ⚡ 快速开始

### 1️⃣ 安装依赖
```bash
cd /Users/jiangshengyu/Documents/program/python/RecSystem
pip install -r requirements.txt
```

### 2️⃣ 选择运行方式

#### 自动演示（推荐首选）
```bash
python main.py
```
✓ 自动展示完整工作流程  
✓ 演示推荐生成、反馈评估、演化过程  
✓ 显示最终系统状态  

#### 交互模式
```bash
python main.py --interactive
```
✓ 输入查询词获取推荐  
✓ 实时查看系统响应  
✓ 输入 `profile` 查看用户档案  

#### 高级示例
```bash
python advanced_examples.py
```
✓ 3个完整场景演示  
✓ 展示系统的演化能力  

#### 单元测试
```bash
python -m unittest test_system.py -v
```
✓ 验证系统功能  

#### 交互式启动器
```bash
python launcher.py
```
✓ 菜单式导航  
✓ 环境检查  

---

## 🔄 工作流程

### 完整循环（9个步骤）

```
1️⃣  用户输入查询
      ↓
2️⃣  智能体A生成推荐
    ├─ 获取兴趣图谱上下文
    ├─ 调用Qwen2.5模型
    └─ 返回排序后的推荐
      ↓
3️⃣  用户提供反馈
    ├─ 点击推荐（记录索引）
    ├─ 浏览时长（秒数）
    ├─ 转化（布尔值）
    └─ 满意度评分（0-1）
      ↓
4️⃣  智能体B评估
    ├─ 计算质量评分（0-1）
    ├─ 识别问题
    └─ 生成改进建议
      ↓
5️⃣  更新兴趣图谱
    ├─ 添加查询词节点
    ├─ 添加被点击推荐的词
    ├─ 建立关系边
    └─ 应用衰减因子
      ↓
6️⃣  判断是否演化
    └─ 检查触发条件
      ↓
7️⃣  可选：执行演化
    ├─ 智能体B学习新规则
    ├─ 智能体A应用改进
    └─ 双智能体版本升级
      ↓
8️⃣  更新系统指标
    ├─ 互惠受益分数
    └─ 演化历史
      ↓
9️⃣  返回完整结果
```

---

## 📊 关键指标

### 质量评分公式
```
Q = 点击率×0.4 + 浏览×0.3 + 转化×0.2 + 满意度×0.1
```

| 维度 | 权重 | 范围 | 说明 |
|------|------|------|------|
| 点击率 | 40% | 0-1 | 推荐相关性 |
| 浏览时长 | 30% | 0-100% | 推荐吸引力 |
| 转化 | 20% | 0/1 | 最终效果 |
| 满意度 | 10% | 0-1 | 用户体验 |

### 演化触发条件
- **条件1**：最近5次的平均质量评分 < 0.6
- **条件2**：检测到改进趋势（最近vs历史，差异 > 0.15）

---

## 🎯 核心特性

### 1. 智能体A - 推荐系统
- 基于Qwen2.5-0.5B-Instruct模型
- 利用用户兴趣图谱进行上下文感知
- 自适应排序策略
- 版本管理和演化

### 2. 智能体B - 评估改进系统
- 多维度反馈评估（4个维度）
- 问题自动识别
- 改进建议生成
- **自我改进**：从反馈学习规则

### 3. 动态兴趣图谱
- 有向图数据结构
- 指数移动平均权重更新
- 周期衰减机制（7天周期）
- 自动图修剪

### 4. 双向演化
- 智能体B学习规则
- 智能体A应用改进
- 版本号递增
- 互惠受益分数追踪

---

## 💻 使用示例

### 基本使用
```python
from evolution_manager import SessionManager

session = SessionManager()

# 处理用户交互
result = session.process_interaction(
    user_id="user_001",
    user_query="机器学习教程",
    feedback_data={
        "clicked_indices": [0, 2],
        "browse_times": [60.0, 90.0],
        "conversion": False,
        "satisfaction": 0.8,
        "user_comment": "很好，但想要更多应用案例"
    }
)

# 查看结果
print(f"推荐数: {len(result['recommendations'])}")
print(f"质量评分: {result['evaluation']['quality_score']:.2f}")
print(f"是否演化: {result['evolved']}")
```

### 用户档案查询
```python
profile = session.get_user_profile("user_001")
print("主要兴趣:", profile["interests"][:5])
print("互惠受益分数:", profile["system_health"]["mutual_benefit_score"])
```

---

## 🔌 设备选择

系统自动按优先级选择计算设备：

```
GPU > MPS > CPU
```

在 `config.py` 中配置：
```python
def get_device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    elif torch.backends.mps.is_available():
        return torch.device("mps")
    else:
        return torch.device("cpu")
```

---

## 📈 性能指标

### KPI 追踪

| 指标 | 计算方式 | 目标 | 说明 |
|------|--------|------|------|
| 质量评分 | 见上文 | > 0.7 | 综合推荐效果 |
| 点击率 | 点击/推荐 | > 0.4 | 相关性 |
| 浏览时长 | 累计秒数 | > 60s | 吸引力 |
| 转化率 | 转化/推荐 | > 0.2 | 最终效果 |
| 满意度 | 用户评分 | > 0.7 | 主观体验 |
| 互惠受益 | 加权平均 | > 0.7 | 系统健康度 |

---

## 🎓 应用场景

### 场景1：学术论文推荐
- **用户**：博士研究生
- **初始查询**："深度学习在医学影像中的应用"
- **演化过程**：系统从相关论文逐步拓展到医疗AI生态
- **最终状态**：完全个性化的研究资源推荐

### 场景2：电商产品推荐
- **用户**：家居装修爱好者
- **初始查询**："北欧风格客厅"
- **演化过程**：从单品推荐→完整搭配方案→风格顾问
- **转化提升**：5% → 18%

### 场景3：内容平台推荐
- **用户**：技术博主
- **初始查询**："Python Web开发"
- **演化轨迹**：基础→实战→高深→个性化混合
- **点击率提升**：35% → 65%

---

## 🛠️ 扩展开发

### 添加新的反馈维度
编辑 `agent_b.py` 的 `FeedbackMetrics`：
```python
@dataclass
class FeedbackMetrics:
    click_count: int = 0
    browse_time: float = 0.0
    share_count: int = 0          # 新增
    save_count: int = 0             # 新增
```

### 使用更大的LLM
编辑 `config.py`：
```python
MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"  # 更大的模型
```

### 自定义排序策略
编辑 `agent_a.py` 的 `_rank_recommendations` 方法。

---

## 📚 文档导航

- **README.md** - 完整使用说明（必读）
- **ARCHITECTURE.py** - 系统架构和算法详解
- **PROJECT_SUMMARY.py** - 项目总结和对比
- **QUICKSTART.py** - 本快速开始指南

---

## 🐛 故障排除

| 问题 | 解决方案 |
|------|--------|
| CUDA内存不足 | 改用float32或CPU |
| 模型加载失败 | 自动切换到模拟模式 |
| 性能缓慢 | 检查设备选择，使用GPU |
| 图谱过大 | 自动修剪机制会处理 |

---

## ✅ 验证安装

运行以下命令验证系统正常工作：

```bash
# 检查依赖
python -c "import torch, transformers, networkx; print('✓ 依赖检查通过')"

# 检查设备
python config.py

# 运行测试
python -m unittest test_system.py
```

---

## 🎉 开始使用

推荐的学习路径：

1. **阅读本文档**（5分钟）
2. **运行演示**（`python main.py`，5分钟）
3. **阅读README.md**（15分钟）
4. **尝试交互模式**（`python main.py --interactive`，10分钟）
5. **查看高级示例**（`python advanced_examples.py`，10分钟）
6. **研究源代码**（按需）

---

## 📞 支持

遇到问题？

1. 查看 README.md 的故障排除部分
2. 查看 ARCHITECTURE.py 的架构说明
3. 运行 test_system.py 验证各模块
4. 检查 launcher.py 中的环境检查

---

**祝你使用愉快！🚀**

# RecSystem - 双智能体推荐系统

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)
![Status: Production](https://img.shields.io/badge/Status-Production-green)

> 一个高级的双智能体推荐系统，支持智能体协作、动态学习和自动演化。

## 🎯 核心特性

### 🤖 双智能体架构
- **Agent A（推荐智能体）**：基于LLM生成个性化推荐
- **Agent B（评估智能体）**：评估推荐质量并反馈

### 📚 动态兴趣建模
- 基于NetworkX的知识图谱
- 支持兴趣权重衰减和自动修剪
- 自动建立兴趣间的关联关系

### 🧠 大语言模型集成
- 内置Qwen2.5-0.5B-Instruct模型
- 支持自然语言推荐生成
- 智能解释推荐理由

### ⚡ 自动演化机制
- 根据用户反馈触发版本升级
- 支持多个智能体版本并存
- 逐步改进推荐质量

### 🎮 多设备支持
- NVIDIA GPU (CUDA)
- Apple Silicon (MPS)
- CPU 后备方案

## 🚀 快速开始

### 安装

```bash
# 克隆项目
git clone https://github.com/yourusername/RecSystem.git
cd RecSystem

# 安装依赖
pip install -r requirements.txt

# 本地开发安装（推荐）
pip install -e .
```

### 最简单的示例

```python
from src import SessionManager

# 创建用户会话
session = SessionManager("user_001")

# 获取推荐
recommendations = session.get_recommendations("我想学习Python")

# 用户反馈
feedback = {
    "clicked_indices": [0, 1],
    "browse_times": [45.0, 50.0],
    "satisfaction": 0.8
}

# 添加交互
session.add_interaction("query", recommendations, feedback)

# 系统会自动学习和演化
print(f"系统质量评分: {session.get_latest_score()}")
```

### 运行完整演示

```bash
python3 examples/evolution_demo.py
```

演示会显示：
- 10次用户交互
- 2次系统演化
- 推荐质量逐步提升

## 📁 项目结构

```
RecSystem/
├── src/                    # 核心源代码
│   ├── config.py          # 系统配置
│   ├── interest_graph.py  # 兴趣知识图谱
│   ├── agents/            # 智能体模块
│   │   ├── agent_a.py    # 推荐智能体
│   │   └── agent_b.py    # 评估智能体
│   └── managers/          # 管理器模块
│       └── evolution_manager.py  # 演化管理
├── examples/              # 示例和演示
│   ├── evolution_demo.py # 完整演化演示
│   └── quick_start.py    # 快速开始指南
├── tests/                 # 单元测试
├── docs/                  # 文档
└── setup.py              # 包安装配置
```

## 📖 文档

- [架构设计](docs/ARCHITECTURE.md) - 详细的系统架构说明
- [快速开始](examples/quick_start.py) - 快速入门指南
- [版本历史](CHANGELOG.md) - 更新日志
- [优化报告](OPTIMIZATION_REPORT.md) - 项目优化总结

## 💡 工作原理

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
触发演化?
├─ YES → 双智能体升级版本
└─ NO → 继续学习
```

## 🔧 配置

在 `src/config.py` 中修改：

```python
# 计算设备 (auto/cuda/mps/cpu)
DEVICE = "auto"

# LLM模型
MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"

# 每次推荐数量
RECOMMENDATION_NUM = 5

# 演化触发阈值
EVOLUTION_THRESHOLD = 0.6

# 兴趣衰减速度
INTEREST_DECAY_FACTOR = 0.95

# 兴趣图谱最大节点数
MAX_GRAPH_SIZE = 1000
```

## 🧪 测试

```bash
# 运行单元测试
python -m pytest tests/ -v

# 测试覆盖率
python -m pytest tests/ --cov=src
```

## 📊 系统指标

| 指标 | 值 |
|------|-----|
| Python版本 | 3.8+ |
| 核心模块 | 6个 |
| 核心类 | 6个 |
| 核心方法 | 50+ |
| 代码行数 | 1000+ |
| 中文注释 | 500+ |
| 测试用例 | 10+ |

## 🎓 学习资源

### 核心概念
1. **兴趣图谱** - 用有向图表示用户的多维兴趣
2. **版本演化** - 基于反馈的自动版本升级
3. **双智能体** - 推荐和评估的分离设计

### 扩展方向
- 集成更大的LLM模型
- 实现多用户并发支持
- 添加实时推荐能力
- 集成WebAPI接口

## 🤝 贡献指南

1. Fork 本仓库
2. 创建分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📝 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 👥 作者

- **RecSystem Team** - 核心开发
- 欢迎社区贡献！

## 🔗 相关资源

- [PyTorch 文档](https://pytorch.org)
- [Transformers 库](https://huggingface.co/transformers/)
- [NetworkX 文档](https://networkx.org)
- [Qwen 模型](https://huggingface.co/Qwen)

## ⭐ 致谢

感谢以下开源项目的支持：
- PyTorch
- Hugging Face Transformers
- NetworkX
- 所有贡献者

---

**最后更新**：2024-01-XX  
**版本**：1.0.0  
**状态**：✅ 生产就绪

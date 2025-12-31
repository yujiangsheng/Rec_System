"""
项目架构文档和使用指南
"""

PROJECT_STRUCTURE = \"\"\"
RecSystem/
├── 📄 README.md                      # 项目完整说明
├── 📄 requirements.txt               # Python依赖
│
├── 🔧 配置层 (Configuration)
│   └── config.py                     # 系统配置、设备选择
│
├── 📊 数据层 (Data)
│   └── interest_graph.py             # 用户兴趣知识图谱
│       ├── InterestGraph 类
│       ├── 节点权重管理
│       ├── 边权重关系
│       ├── 衰减机制
│       └── 序列化/反序列化
│
├── 🤖 智能体层 (Agents)
│   ├── agent_a.py                    # 推荐智能体
│   │   ├── AgentA 类
│   │   ├── 基于Qwen2.5的推荐生成
│   │   ├── 推荐排序和过滤
│   │   └── 版本管理
│   │
│   └── agent_b.py                    # 评估改进智能体  
│       ├── AgentB 类
│       ├── FeedbackMetrics 类
│       ├── 推荐质量评估
│       ├── 问题识别
│       ├── 改进建议生成
│       └── 自我学习和改进
│
├── 🔄 演化层 (Evolution)
│   └── evolution_manager.py          # 演化和交互管理
│       ├── EvolutionManager 类
│       │   ├── 完整交互循环
│       │   ├── 兴趣图谱更新
│       │   ├── 演化触发
│       │   └── 版本升级
│       └── SessionManager 类
│           ├── 用户会话管理
│           ├── 多用户支持
│           └── 持久化存储
│
├── 🚀 应用层 (Application)
│   ├── main.py                       # 主程序和交互界面
│   │   ├── 演示工作流程
│   │   ├── 交互模式
│   │   └── 命令行界面
│   │
│   ├── advanced_examples.py          # 高级示例
│   │   ├── 医疗AI用户演化示例
│   │   ├── 跨领域探索示例
│   │   └── 负反馈恢复示例
│   │
│   └── test_system.py                # 单元测试
│       ├── 兴趣图谱测试
│       ├── 智能体测试
│       ├── 演化管理测试
│       └── 集成测试
\"\"\"

WORKFLOW_DESCRIPTION = \"\"\"
【完整工作流程】

1️⃣  用户交互开始
    ↓
2️⃣  智能体A生成推荐
    ├─ 获取用户兴趣图谱
    ├─ 构造Qwen2.5提示词
    ├─ 生成推荐列表
    └─ 排序优化
    ↓
3️⃣  用户提供反馈
    ├─ 点击推荐项（记录索引）
    ├─ 浏览时长（秒数）
    ├─ 是否转化（布尔）
    ├─ 满意度评分（0-1）
    └─ 文字评论（可选）
    ↓
4️⃣  智能体B评估
    ├─ 计算质量评分 = 点击率×0.4 + 浏览×0.3 + 转化×0.2 + 满意度×0.1
    ├─ 识别问题
    ├─ 生成改进建议
    └─ 生成改进指导
    ↓
5️⃣  更新兴趣图谱
    ├─ 添加查询词节点
    ├─ 添加被点击推荐的词
    ├─ 建立关系边
    └─ 应用衰减因子
    ↓
6️⃣  判断是否演化
    └─ 检查触发条件：
        ├─ 最近5次平均质量 < 0.6, 或
        └─ 检测到改进趋势 (+0.15)
    ↓
7️⃣  可选：执行演化
    ├─ 智能体B自我改进
    │  ├─ 分析反馈历史
    │  └─ 生成新规则
    ├─ 智能体A应用改进
    │  ├─ 调整排序策略
    │  └─ 添加过滤规则
    └─ 双智能体版本升级
    ↓
8️⃣  更新系统指标
    ├─ 互惠受益分数
    ├─ 性能曲线
    └─ 演化历史
    ↓
9️⃣  返回结果
    ├─ 推荐列表
    ├─ 评估报告
    ├─ 改进建议
    ├─ 演化信息（如果发生）
    └─ 系统状态
\"\"\"

KEY_ALGORITHMS = \"\"\"
【关键算法】

1. 质量评分算法 (Quality Scoring)
   ──────────────────────────────
   Q = Cr×0.4 + Br×0.3 + Cv×0.2 + Sa×0.1
   
   其中：
   - Cr = 点击率 = 点击数 / 推荐数
   - Br = 浏览归一化 = min(浏览时长 / 300, 1.0)
   - Cv = 转化 = 1 if 用户完成转化 else 0
   - Sa = 满意度 = 用户评分 (0-1)

2. 兴趣权重更新 (Interest Weight Update)
   ──────────────────────────────────
   新权重 = 0.7 × 旧权重 + 0.3 × 当前权重
   
   目的：
   - 0.7系数: 保留历史记忆
   - 0.3系数: 响应最新偏好

3. 兴趣衰减 (Interest Decay)
   ──────────────────────────
   衰减权重 = 原权重 × (0.95 ^ (天数/7))
   
   特点：
   - 周期衰减因子为0.95
   - 7天衰减到原来的95%
   - 约48天衰减到50%

4. 演化触发条件 (Evolution Trigger)
   ────────────────────────────
   触发 if:
   - avg(最后5次质量评分) < 0.6, or
   - (avg(最后5次) - avg(前5次)) > 0.15
   
   含义：
   - 情况1: 质量不足
   - 情况2: 明显改进

5. 互惠受益分数 (Mutual Benefit Score)
   ─────────────────────────────────
   MBS(t) = 0.7 × MBS(t-1) + 0.3 × Q(t)
   
   含义：
   - 追踪双智能体的合作效果
   - 0.7保留历史，0.3响应当前
   - 范围0-1，越高越好

6. 图谱修剪 (Graph Pruning)
   ─────────────
   当节点数 > 1000时：
   - 保留权重最高的700个节点
   - 移除权重<0.01的节点
   - 自动保持图的规模
\"\"\"

USAGE_EXAMPLES = \"\"\"
【使用示例】

示例1：基本使用
──────────────
from evolution_manager import SessionManager

session = SessionManager()

# 处理用户交互
result = session.process_interaction(
    user_id=\"user_001\",
    user_query=\"机器学习教程\",
    feedback_data={
        \"clicked_indices\": [0, 2],
        \"browse_times\": [60.0, 90.0],
        \"conversion\": False,
        \"satisfaction\": 0.8,
        \"user_comment\": \"很好，但想要更多应用案例\"
    }
)

# 获取推荐
recommendations = result[\"recommendations\"]
print(f\"生成了{len(recommendations)}个推荐\")

# 检查是否演化
if result[\"evolved\"]:
    print(f\"系统演化到阶段{result['evolution_info']['evolution_stage']}\")

示例2：用户档案查询
──────────────────
# 获取用户档案
profile = session.get_user_profile(\"user_001\")

# 查看兴趣
print(\"主要兴趣:\", profile[\"interests\"][:5])

# 查看系统健康
health = profile[\"system_health\"]
print(f\"互惠受益分数: {health['mutual_benefit_score']:.2f}\")
print(f\"总演化次数: {health['total_evolutions']}\")

示例3：会话保存和恢复
────────────────────
# 保存会话
session.save_session(\"user_001\", \"./user_001_session.json\")

# 加载会话
new_session = SessionManager()
new_session.load_session(\"user_001\", \"./user_001_session.json\")

# 继续交互
result = new_session.process_interaction(...)

示例4：运行高级示例
──────────────────
python advanced_examples.py

输出：
- 医疗AI研究员的推荐系统演化过程
- 跨领域兴趣探索示例
- 从负反馈恢复的示例
\"\"\"

EXTENSION_POINTS = \"\"\"
【扩展开发点】

1. 扩展反馈维度
   ──────────────
   编辑 agent_b.py 的 FeedbackMetrics:
   
   @dataclass
   class FeedbackMetrics:
       click_count: int = 0
       browse_time: float = 0.0
       conversion: bool = False
       satisfaction: float = 0.0
       share_count: int = 0          # ← 新增
       save_count: int = 0             # ← 新增
       comment_length: int = 0         # ← 新增

2. 自定义LLM模型
   ──────────────
   编辑 config.py:
   
   # 使用更大的模型
   MODEL_NAME = \"Qwen/Qwen2.5-1.5B-Instruct\"
   
   # 或使用其他模型
   MODEL_NAME = \"mistralai/Mistral-7B-Instruct-v0.1\"

3. 添加过滤规则
   ──────────────
   编辑 agent_a.py 的 _rank_recommendations:
   
   def _rank_recommendations(self, ...):
       # 添加自定义过滤
       filtered = [r for r in recommendations 
                   if not self._is_spam(r)]
       return self._rank(filtered)

4. 实现个性化排序
   ────────────────
   编辑 agent_a.py:
   
   def _rank_recommendations(self, recs, query, interests):
       for rec in recs:
           # 用户类型特定排序
           if user_type == \"researcher\":
               rec[\"score\"] *= 1.2 if \"论文\" in rec[\"title\"]
           elif user_type == \"practitioner\":
               rec[\"score\"] *= 1.2 if \"应用\" in rec[\"title\"]

5. 监测和告警
   ───────────
   添加到 evolution_manager.py:
   
   def check_system_health():
       if mutual_benefit_score < 0.5:
           alert(\"质量下降，需要人工干预\")
       if evolution_count > 20:
           alert(\"演化过度，可能过拟合\")

6. A/B测试
   ─────────
   支持并行运行多个推荐算法：
   
   result_a = agent_a_v1.generate(...)
   result_b = agent_a_v2.generate(...)
   
   # 基于反馈比较
   evaluate(result_a) vs evaluate(result_b)
\"\"\"

if __name__ == \"__main__\":
    print(PROJECT_STRUCTURE)
    print(\"\\n\" + \"=\"*70)\n    print(WORKFLOW_DESCRIPTION)
    print(\"\\n\" + \"=\"*70)\n    print(KEY_ALGORITHMS)
    print(\"\\n\" + \"=\"*70)\n    print(USAGE_EXAMPLES)
    print(\"\\n\" + \"=\"*70)\n    print(EXTENSION_POINTS)
"
"""
系统配置模块 - 全局参数管理

本模块集中管理双智能体推荐系统的所有配置参数，包括：
  1. 计算设备选择（GPU/MPS/CPU）
  2. LLM模型配置
  3. 推荐系统参数
  4. 兴趣图谱参数
  5. 权重更新参数

参数说明：
  - DEVICE: 自动选择计算设备，优先级：CUDA > MPS > CPU
  - MODEL_NAME: 使用Qwen2.5-0.5B-Instruct模型
  - RECOMMENDATION_NUM: 每次推荐返回5个结果
  - 质量评分: Q = Cr(40%) + Br(30%) + Cv(20%) + Sa(10%)
  - 权重衰减: w_decay = w × (0.95 ^ (days/7))
  - 演化触发: avg(最近5次质量) < 0.6 或 改进趋势 > 0.15
"""

import torch

# ===== 1. 计算设备配置 =====
if torch.cuda.is_available():
    DEVICE = torch.device("cuda")
    print("✅ 使用CUDA GPU")
elif torch.backends.mps.is_available():
    DEVICE = torch.device("mps")
    print("✅ 使用Apple Silicon MPS")
else:
    DEVICE = torch.device("cpu")
    print("⚠️  使用CPU (推理速度较慢)")

# ===== 2. LLM模型配置 =====
MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"  # 轻量级模型，推荐使用

# ===== 3. 推荐系统参数 =====
RECOMMENDATION_NUM = 5  # 每次推荐返回的数量

# ===== 4. 评估和演化参数 =====
EVOLUTION_THRESHOLD = 0.6  # 演化触发的质量评分阈值
MIN_CLICK_RATIO = 0.3  # 最小点击率 (点击数/推荐数)

# 质量评分公式:
# Q = click_ratio × 0.4 + normalized_browse_time × 0.3 
#     + conversion_rate × 0.2 + satisfaction × 0.1

# ===== 5. 兴趣图谱参数 =====
INTEREST_DECAY_FACTOR = 0.95  # 兴趣衰减因子
NEW_INTEREST_WEIGHT = 0.1  # 新兴趣的初始权重
MAX_GRAPH_SIZE = 1000  # 兴趣图谱的最大节点数

# ===== 6. 权重更新参数 =====
INTEREST_UPDATE_ALPHA = 0.3  # 指数移动平均权重系数

print(f"\n{'='*50}")
print(f"🖥️  计算设备: {DEVICE}")
print(f"🤖 LLM模型: {MODEL_NAME}")
print(f"⚙️  推荐数量: {RECOMMENDATION_NUM}")
print(f"📊 演化阈值: {EVOLUTION_THRESHOLD}")
print(f"{'='*50}\n")

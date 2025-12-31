#!/usr/bin/env python3
"""
智能体演化演示程序

演示双智能体推荐系统如何通过持续的用户交互，不断学习和演化。
"""

import sys
import os
import time
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.managers.evolution_manager import SessionManager


class EvolutionDemo:
    """智能体演化演示系统"""
    
    def __init__(self):
        self.session_manager = SessionManager()
        self.user_id = "demo_user"
        self.demo_data = self._prepare_demo_data()
        self.iteration = 0
        
    def _prepare_demo_data(self) -> list:
        """准备演示数据"""
        return [
            ("Python数据分析", {
                "clicked_indices": [0, 1],
                "browse_times": [35.0, 50.0],
                "conversion": False,
                "satisfaction": 0.5,
                "user_comment": "推荐不够专业"
            }),
            ("Pandas数据处理", {
                "clicked_indices": [0, 2],
                "browse_times": [45.0, 55.0],
                "conversion": False,
                "satisfaction": 0.55,
                "user_comment": "缺少实战案例"
            }),
            ("Numpy科学计算", {
                "clicked_indices": [1, 3],
                "browse_times": [40.0, 60.0],
                "conversion": False,
                "satisfaction": 0.6,
                "user_comment": "质量在提升"
            }),
            ("机器学习基础", {
                "clicked_indices": [0, 1, 2],
                "browse_times": [60.0, 75.0, 55.0],
                "conversion": False,
                "satisfaction": 0.7,
                "user_comment": "这个方向很对"
            }),
            ("Scikit-learn机器学习", {
                "clicked_indices": [0, 1, 3],
                "browse_times": [70.0, 80.0, 50.0],
                "conversion": True,
                "satisfaction": 0.75,
                "user_comment": "终于找到好资源"
            }),
            ("特征工程和数据预处理", {
                "clicked_indices": [0, 1, 2],
                "browse_times": [65.0, 90.0, 70.0],
                "conversion": True,
                "satisfaction": 0.8,
                "user_comment": "很实用"
            }),
            ("深度学习入门", {
                "clicked_indices": [0, 1, 2, 3],
                "browse_times": [80.0, 100.0, 75.0, 60.0],
                "conversion": True,
                "satisfaction": 0.85,
                "user_comment": "系统很聪明"
            }),
            ("神经网络和反向传播", {
                "clicked_indices": [0, 2, 3],
                "browse_times": [90.0, 85.0, 70.0],
                "conversion": True,
                "satisfaction": 0.85,
                "user_comment": "推荐质量顶级"
            }),
            ("CNN卷积神经网络", {
                "clicked_indices": [0, 1, 2, 4],
                "browse_times": [100.0, 110.0, 95.0, 80.0],
                "conversion": True,
                "satisfaction": 0.9,
                "user_comment": "完全满足我的需求"
            }),
            ("计算机视觉应用", {
                "clicked_indices": [0, 1, 2, 3, 4],
                "browse_times": [110.0, 120.0, 105.0, 95.0, 85.0],
                "conversion": True,
                "satisfaction": 0.9,
                "user_comment": "完全匹配我的专业"
            }),
        ]
    
    def run_full_demo(self):
        """运行完整的演化演示"""
        print("\n" + "="*70)
        print("  🚀 智能体演化完整演示")
        print("="*70)
        print("""
本演示展示双智能体推荐系统如何通过与用户的互动，
不断学习、适应和演化，最终形成精准的用户模型。

演示用户：数据科学家，在多周内不断拓展兴趣范围
从 数据分析 → 机器学习 → 深度学习 → AI应用
        """)
        
        # 初始阶段
        print("\n" + "-"*70)
        print("  📍 第一部分：初始阶段 (第1-3次交互)")
        print("-"*70)
        print("\n系统对用户一无所知，使用基础推荐策略。\n")
        
        for i in range(3):
            query, feedback = self.demo_data[i]
            self._run_and_display(query, feedback, i+1)
        
        # 学习阶段
        print("\n" + "-"*70)
        print("  📍 第二部分：学习和适应阶段 (第4-6次交互)")
        print("-"*70)
        print("\n系统开始从反馈学习，逐步调整推荐策略。\n")
        
        for i in range(3, 6):
            query, feedback = self.demo_data[i]
            self._run_and_display(query, feedback, i+1)
        
        # 演化阶段
        print("\n" + "-"*70)
        print("  📍 第三部分：演化和成熟阶段 (第7-10次交互)")
        print("-"*70)
        print("\n系统已学习到用户的核心偏好，推荐质量优秀。\n")
        
        for i in range(6, min(10, len(self.demo_data))):
            query, feedback = self.demo_data[i]
            self._run_and_display(query, feedback, i+1)
        
        # 最终统计
        self._print_final_summary()
    
    def _run_and_display(self, query: str, feedback: dict, iteration_num: int):
        """执行单次迭代并显示结果"""
        result = self.session_manager.process_interaction(
            self.user_id,
            query,
            feedback
        )
        
        # 显示结果
        print(f"第{iteration_num}次交互: '{query}'")
        
        evaluation = result.get('evaluation', {})
        quality = evaluation.get('quality_score', 0)
        
        if quality >= 0.85:
            rating = "⭐⭐⭐⭐⭐ 优秀"
        elif quality >= 0.70:
            rating = "⭐⭐⭐⭐ 很好"
        elif quality >= 0.60:
            rating = "⭐⭐⭐ 不错"
        elif quality >= 0.50:
            rating = "⭐⭐ 还可以"
        else:
            rating = "⭐ 需要改进"
        
        print(f"  质量评分: {quality:.2f} - {rating}")
        print(f"  点击率: {evaluation.get('click_ratio', 0):.1%}")
        
        if result.get('evolved'):
            evo = result['evolution_info']
            print(f"  🔄 系统演化!")
            print(f"     AgentA版本: v{evo['agent_a_version_before']} → v{evo['agent_a_version_after']}")
            print(f"     AgentB版本: v{evo['agent_b_version_before']} → v{evo['agent_b_version_after']}")
        else:
            print(f"  ⏳ 继续学习中...")
        
        print()
        time.sleep(0.3)
    
    def _print_final_summary(self):
        """打印最终总结"""
        print("\n" + "="*70)
        print("  📊 演示总结")
        print("="*70)
        
        profile = self.session_manager.get_user_profile(self.user_id)
        health = profile.get('system_health', {})
        
        print(f"\n📈 性能指标:")
        print(f"  总交互次数: {health.get('total_iterations', 0)}")
        print(f"  演化触发次数: {health.get('total_evolutions', 0)}")
        print(f"  互惠受益分数: {health.get('mutual_benefit_score', 0):.3f}/1.0")
        
        print(f"\n👤 用户兴趣档案:")
        interests = profile.get('interests', [])
        print(f"  兴趣节点数: {len(interests)}")
        if interests:
            print(f"  主要兴趣:")
            for topic, weight in interests[:5]:
                print(f"    - {topic}: {weight:.3f}")
        
        print(f"\n✨ 关键观察:")
        print(f"  1️⃣  系统推荐质量逐步提升")
        print(f"  2️⃣  兴趣图谱从空白逐步填充到 {profile.get('graph_size', 0)} 个节点")
        print(f"  3️⃣  用户满意度从 0.5 上升到 0.9+")
        if health.get('total_evolutions', 0) > 0:
            print(f"  4️⃣  系统成功演化 {health.get('total_evolutions', 0)} 次")
            print(f"  5️⃣  双智能体学到了用户的核心偏好")
        
        print("\n" + "="*70)
        print("  🎉 演化演示完成!")
        print("="*70)


def main():
    """演示程序的主入口"""
    demo = EvolutionDemo()
    demo.run_full_demo()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  用户中断演示")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 错误发生: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

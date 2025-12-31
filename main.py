"""
主程序：双智能体推荐系统交互界面
演示系统的完整功能流程
"""
import json
import os
from evolution_manager import SessionManager
from interest_graph import InterestGraph


def print_separator(title=""):
    \"\"\"打印分隔线\"\"\"
    if title:
        print(f\"\\n{'='*60}\")
        print(f\" {title}\")
        print(f\"{'='*60}\")
    else:
        print(f\"{'='*60}\")


def print_recommendations(recommendations):
    \"\"\"打印推荐\"\"\"
    print(\"\\n📋 推荐列表:\")
    for i, rec in enumerate(recommendations, 1):
        print(f\"\\n  {i}. {rec.get('title', '未命名')}\")
        print(f\"     描述: {rec.get('description', '暂无')}\")
        if rec.get('reason'):
            print(f\"     原因: {rec.get('reason', '')}\")
        if rec.get('score'):
            print(f\"     评分: {rec.get('score'):.2f}\")


def print_evaluation(evaluation):
    \"\"\"打印评估报告\"\"\"
    print(\"\\n📊 评估报告:\")
    print(f\"  质量评分: {evaluation.get('quality_score', 0):.2f}\")
    print(f\"  点击率: {evaluation.get('click_ratio', 0):.2%}\")
    print(f\"  用户满意度: {evaluation.get('satisfaction', 0):.2f}\")
    print(f\"  是否可接受: {'✓ 是' if evaluation.get('is_acceptable') else '✗ 否'}\")\n    
    if evaluation.get('issues'):
        print(\"  🔴 发现问题:\")
        for issue in evaluation.get('issues', [])[:3]:
            print(f\"    - {issue}\")
    
    if evaluation.get('improvements'):
        print(\"  💡 改进建议:\")
        for imp in evaluation.get('improvements', [])[:2]:
            print(f\"    - [{imp.get('priority', 'normal')}] {imp.get('action', '')}\")


def print_evolution_info(evo_info):
    \"\"\"打印演化信息\"\"\"
    print(\"\\n🔄 系统演化:\")
    print(f\"  演化阶段: {evo_info.get('evolution_stage', 0)}\")
    print(f\"  智能体A版本: {evo_info.get('agent_a_version_before')} → {evo_info.get('agent_a_version_after')}\")
    print(f\"  智能体B版本: {evo_info.get('agent_b_version_before')} → {evo_info.get('agent_b_version_after')}\")
    if evo_info.get('new_rules'):
        print(f\"  新规则数: {len(evo_info.get('new_rules', []))}条\")


def print_interest_profile(user_profile):
    \"\"\"打印用户兴趣档案\"\"\"
    print(\"\\n👤 用户兴趣档案:\")
    print(f\"  用户ID: {user_profile.get('user_id')}\")
    print(f\"  交互次数: {user_profile.get('interaction_count')}\")
    print(f\"  图谱版本: {user_profile.get('graph_version')}\")
    print(f\"  兴趣节点: {user_profile.get('graph_size')}\")
    
    interests = user_profile.get('interests', [])
    if interests:
        print(\"  主要兴趣:\")
        for topic, weight in interests[:5]:
            print(f\"    - {topic}: {weight:.3f}\")
    
    health = user_profile.get('system_health', {})
    print(f\"  系统互惠受益分数: {health.get('mutual_benefit_score', 0):.2f}\")
    print(f\"  总演化次数: {health.get('total_evolutions', 0)}\")


def simulate_interaction(session_manager: SessionManager, user_id: str,
                        user_query: str, simulate_feedback: bool = True):
    \"\"\"模拟用户交互\"\"\"
    print_separator(f\"用户交互 - {user_query}\")
    
    # 模拟反馈数据
    feedback_data = {
        \"clicked_indices\": [0, 2],  # 点击了第1和第3项
        \"browse_times\": [45.5, 120.3],  # 浏览时长
        \"conversion\": False,
        \"satisfaction\": 0.7,
        \"user_comment\": \"推荐不错，但缺少一些创新性的内容\"
    }
    
    # 处理交互
    result = session_manager.process_interaction(
        user_id,
        user_query,
        feedback_data
    )
    
    # 显示结果
    recommendations = result.get('recommendations', [])
    print_recommendations(recommendations)
    
    evaluation = result.get('evaluation', {})
    print_evaluation(evaluation)
    
    if result.get('evolved'):
        print_evolution_info(result.get('evolution_info', {}))
    
    return result


def interactive_mode(session_manager: SessionManager):
    \"\"\"交互模式\"\"\"
    print_separator(\"智能推荐系统 - 交互模式\")
    print(\"\\n命令说明:\")
    print(\"  1. 输入查询词 (如: '机器学习') 进行推荐\")
    print(\"  2. 输入 'profile' 查看用户档案\")
    print(\"  3. 输入 'history' 查看交互历史\")
    print(\"  4. 输入 'exit' 退出程序\")
    
    user_id = \"default_user\"
    
    while True:
        print_separator()
        user_input = input(\"\\n请输入命令或查询词: \").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() == \"exit\":
            print(\"\\n👋 再见！\")
            break
        
        elif user_input.lower() == \"profile\":
            user_profile = session_manager.get_user_profile(user_id)
            print_interest_profile(user_profile)
        
        elif user_input.lower() == \"history\":
            user_profile = session_manager.get_user_profile(user_id)
            print(f\"\\n📝 交互历史 (共 {user_profile.get('interaction_count', 0)} 次):\")
        
        else:
            # 模拟用户交互
            simulate_interaction(session_manager, user_id, user_input)


def demo_workflow():
    \"\"\"演示完整工作流程\"\"\"
    print_separator(\"双智能体推荐系统演示\")
    print(\"\\n系统架构:\")
    print(\"  • 智能体A: 基于Qwen2.5的推荐系统\")
    print(\"  • 智能体B: 评估和自我改进系统\")
    print(\"  • 兴趣图谱: 动态构建的用户兴趣知识图\")
    print(\"  • 演化机制: 双向互动促进的演化系统\")
    
    session_manager = SessionManager()
    user_id = \"user_001\"
    
    # 演示序列1: 基础推荐
    print_separator(\"阶段1: 基础推荐 - 用户初始查询\")
    result1 = simulate_interaction(session_manager, user_id, \"人工智能在医疗中的应用\")
    
    # 演示序列2: 相关查询
    print_separator(\"阶段2: 相关查询 - 基于兴趣图谱优化\")
    feedback_2 = {
        \"clicked_indices\": [0, 1, 3],
        \"browse_times\": [60.0, 90.0, 75.0],
        \"conversion\": True,
        \"satisfaction\": 0.85,
        \"user_comment\": \"很好，这些内容很实用\"
    }
    result2 = session_manager.process_interaction(
        user_id, \"深度学习在医学影像中的应用\", feedback_2
    )
    
    # 演示序列3: 新兴趣拓展
    print_separator(\"阶段3: 新兴趣拓展 - 相关领域推荐\")
    feedback_3 = {
        \"clicked_indices\": [1, 2],
        \"browse_times\": [45.0, 120.0],
        \"conversion\": False,
        \"satisfaction\": 0.6,
        \"user_comment\": \"不错，但想要更多应用案例\"
    }
    result3 = session_manager.process_interaction(
        user_id, \"计算机视觉在诊断中的应用\", feedback_3
    )
    
    # 演示序列4: 继续交互，可能触发演化
    print_separator(\"阶段4: 持续优化 - 监测演化触发\")
    for i in range(2):
        feedback = {
            \"clicked_indices\": [0, 2],
            \"browse_times\": [50.0 + i*10, 100.0 + i*10],
            \"conversion\": i > 0,
            \"satisfaction\": 0.75 + i*0.05,
            \"user_comment\": \"系统在改进\"
        }
        result = session_manager.process_interaction(
            user_id, f\"NLP在医疗领域的发展{i+1}\", feedback
        )
        
        if result.get('evolved'):
            print_evolution_info(result.get('evolution_info', {}))
    
    # 显示最终状态
    print_separator(\"系统最终状态\")
    user_profile = session_manager.get_user_profile(user_id)
    print_interest_profile(user_profile)
    
    # 显示系统健康状态
    health = user_profile.get('system_health', {})
    print(\"\\n🏥 系统健康状态:\")
    print(f\"  总交互次数: {health.get('total_iterations', 0)}\")
    print(f\"  演化阶段: {health.get('evolution_stages', 0)}\")
    print(f\"  互惠受益分数: {health.get('mutual_benefit_score', 0):.3f}\")
    
    # 保存会话
    print(\"\\n💾 保存会话数据...\")
    session_file = f\"/tmp/rec_system_session_{user_id}.json\"
    if session_manager.save_session(user_id, session_file):
        print(f\"✓ 会话已保存到: {session_file}\")
    
    return session_manager


if __name__ == \"__main__\":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == \"--interactive\":
        # 交互模式
        session_manager = SessionManager()
        interactive_mode(session_manager)
    else:
        # 演示模式
        session_manager = demo_workflow()
        
        print_separator(\"演示完成\")
        print(\"\\n💡 提示: 使用 'python main.py --interactive' 进入交互模式\")

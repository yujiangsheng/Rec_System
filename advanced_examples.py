"""
高级示例：展示系统的演化和自我改进能力
模拟真实的用户交互场景
"""
import json
from evolution_manager import SessionManager
from datetime import datetime


def example_medical_ai_user():
    \"\"\"
    示例场景：医疗AI研究人员的推荐系统演化
    展示系统如何随着用户交互不断改进
    \"\"\"
    print(\"\\n\" + \"=\"*70)
    print(\" 示例场景: 医疗AI研究人员的个性化推荐系统演化\")
    print(\"=\"*70)
    
    session = SessionManager()
    user_id = \"medical_researcher_001\"
    
    # 模拟用户的查询序列
    user_queries = [
        \"医学影像深度学习\",
        \"CNN在肿瘤检测中的应用\",
        \"医疗数据隐私保护\",
        \"联邦学习在医疗中的应用\",
        \"医学NLP自然语言处理\"
    ]
    
    # 对应的反馈数据（逐步改善）
    feedback_sequence = [
        # 第1次查询：点击率低
        {
            \"clicked_indices\": [0, 3],
            \"browse_times\": [30.0, 45.0],
            \"conversion\": False,
            \"satisfaction\": 0.5,
            \"user_comment\": \"相关性不足，缺少最新研究\"
        },
        # 第2次查询：有所改善
        {
            \"clicked_indices\": [0, 1, 3],
            \"browse_times\": [60.0, 75.0, 50.0],
            \"conversion\": False,
            \"satisfaction\": 0.65,
            \"user_comment\": \"好些了，但还需要更多应用案例\"
        },
        # 第3次查询：品质提升
        {
            \"clicked_indices\": [0, 2, 4],
            \"browse_times\": [90.0, 120.0, 60.0],
            \"conversion\": True,
            \"satisfaction\": 0.8,
            \"user_comment\": \"很不错，找到了有用的资源\"
        },
        # 第4次查询：接近完美
        {
            \"clicked_indices\": [0, 1, 2],
            \"browse_times\": [100.0, 110.0, 95.0],
            \"conversion\": True,
            \"satisfaction\": 0.85,
            \"user_comment\": \"推荐质量很高，正是我需要的\"
        },
        # 第5次查询：继续高质量
        {
            \"clicked_indices\": [0, 1, 2, 3],\n            \"browse_times\": [120.0, 100.0, 110.0, 85.0],
            \"conversion\": True,
            \"satisfaction\": 0.9,
            \"user_comment\": \"系统已经充分了解我的需求\"
        }
    ]
    
    evolution_events = []
    
    for iteration, (query, feedback) in enumerate(zip(user_queries, feedback_sequence), 1):
        print(f\"\\n{'─'*70}\")
        print(f\" 第{iteration}次交互: \\\"{query}\\\"\")
        print(f\"{'─'*70}\")
        
        # 处理交互
        result = session.process_interaction(user_id, query, feedback)
        
        # 显示关键指标
        evaluation = result.get(\"evaluation\", {})
        print(f\"\\n  推荐数量: {len(result.get('recommendations', []))} 项\")
        print(f\"  质量评分: {evaluation.get('quality_score', 0):.2f}\")
        print(f\"  点击率:   {evaluation.get('click_ratio', 0):.2%}\")
        print(f\"  用户满意度: {evaluation.get('satisfaction', 0):.2f}\")
        
        # 显示兴趣图谱信息
        interest_graph = session.users[user_id]
        print(f\"\\n  📊 兴趣图谱:\")
        print(f\"    节点数: {len(interest_graph.graph)}\")
        print(f\"    版本号: {interest_graph.version}\")
        
        top_interests = interest_graph.get_top_interests(top_k=3)
        if top_interests:
            print(f\"    主要兴趣: {', '.join([t[0] for t in top_interests])}\")\n        \n        # 检查是否发生演化\n        if result.get('evolved'):\n            evo_info = result.get('evolution_info', {})\n            evolution_events.append(evo_info)\n            \n            print(f\"\\n  🔄 系统演化!\")  \n            print(f\"    演化阶段: {evo_info.get('evolution_stage', 0)}\")  \n            print(f\"    智能体A版本: {evo_info.get('agent_a_version_before')} → {evo_info.get('agent_a_version_after')}\")  \n            print(f\"    智能体B版本: {evo_info.get('agent_b_version_before')} → {evo_info.get('agent_b_version_after')}\")  \n            \n            if evo_info.get('new_rules'):\n                print(f\"    新规则: {len(evo_info.get('new_rules', []))} 条\")\n        \n        # 显示改进建议\n        guidance = result.get('guidance', {})\n        if guidance.get('priority_actions'):\n            print(f\"\\n  💡 改进建议:\")\n            for action in guidance.get('priority_actions', [])[:2]:\n                print(f\"    - {action.get('action', '')}: {action.get('reason', '')}\")\n    \n    # 显示最终的系统状态\n    print(f\"\\n{'═'*70}\")\n    print(\" 演化总结\")  \n    print(f\"{'═'*70}\")\n    \n    user_profile = session.get_user_profile(user_id)\n    health = user_profile.get('system_health', {})\n    \n    print(f\"\\n📈 整体改进:\")  \n    print(f\"  总交互次数: {health.get('total_iterations', 0)}\")  \n    print(f\"  演化触发次数: {len(evolution_events)}\")  \n    print(f\"  互惠受益分数: {health.get('mutual_benefit_score', 0):.3f}\")  \n    \n    print(f\"\\n👤 用户兴趣档案:\")  \n    interests = user_profile.get('interests', [])\n    for topic, weight in interests[:5]:\n        print(f\"  {topic:30} → {weight:.3f}\")\n    \n    print(f\"\\n📊 性能曲线:\")  \n    agent_b_stats = health.get('agent_b_stats', {})\n    quality_scores = agent_b_stats.get('avg_quality_score', 0)\n    click_ratios = agent_b_stats.get('avg_click_ratio', 0)\n    satisfaction = agent_b_stats.get('avg_satisfaction', 0)\n    print(f\"  平均质量评分: {quality_scores:.2f}\")  \n    print(f\"  平均点击率: {click_ratios:.2%}\")  \n    print(f\"  平均满意度: {satisfaction:.2f}\")  \n    \n    if evolution_events:\n        print(f\"\\n🔄 演化历程:\")\n        for event in evolution_events:\n            print(f\"  阶段{event.get('evolution_stage', '?')} @iter{event.get('iteration', '?')}:\")  \n            print(f\"    AgentA: {event.get('agent_a_version_before')}→{event.get('agent_a_version_after')}, \"\n                  f\"AgentB: {event.get('agent_b_version_before')}→{event.get('agent_b_version_after')}\")\n    \n    return session, user_profile\n\n\ndef example_cross_domain_exploration():\n    \"\"\"  \n    示例场景：跨领域探索\n    用户从一个领域逐渐拓展到相关领域\n    \"\"\"  \n    print(\"\\n\" + \"=\"*70)\n    print(\" 示例场景: 跨领域探索与兴趣演化\")\n    print(\"=\"*70)\n    \n    session = SessionManager()\n    user_id = \"explorer_user\"\n    \n    # 第1阶段：初始兴趣 - Python编程\n    print(f\"\\n\\n【第1阶段】初始兴趣领域\")\n    result1 = session.process_interaction(\n        user_id, \"Python编程教程\",\n        {\n            \"clicked_indices\": [0, 1],\n            \"browse_times\": [50, 60],\n            \"conversion\": False,\n            \"satisfaction\": 0.7,\n            \"user_comment\": \"不错的基础教程\"\n        }\n    )\n    print(f\"推荐内容涉及: {[r.get('title', '')[:20] for r in result1.get('recommendations', [])[:3]]}...\")\n    \n    # 第2阶段：相邻领域 - 数据分析\n    print(f\"\\n【第2阶段】拓展到相邻领域\")\n    result2 = session.process_interaction(\n        user_id, \"Python数据分析Pandas\",\n        {\n            \"clicked_indices\": [0, 2, 3],\n            \"browse_times\": [70, 90, 50],\n            \"conversion\": True,\n            \"satisfaction\": 0.8,\n            \"user_comment\": \"很实用，正是我需要的\"\n        }\n    )\n    print(f\"推荐内容涉及: {[r.get('title', '')[:20] for r in result2.get('recommendations', [])[:3]]}...\")\n    \n    # 第3阶段：进一步扩展 - 机器学习\n    print(f\"\\n【第3阶段】进入AI领域\")\n    result3 = session.process_interaction(\n        user_id, \"Python机器学习Scikit-learn\",\n        {\n            \"clicked_indices\": [0, 1, 2],\n            \"browse_times\": [100, 120, 85],\n            \"conversion\": True,\n            \"satisfaction\": 0.85,\n            \"user_comment\": \"完美的进阶方向\"\n        }\n    )\n    print(f\"推荐内容涉及: {[r.get('title', '')[:20] for r in result3.get('recommendations', [])[:3]]}...\")\n    \n    # 显示兴趣图谱的演化\n    interest_graph = session.users[user_id]\n    print(f\"\\n\\n📈 兴趣图谱的演化:\")\n    print(f\"  节点数增长: 0 → {len(interest_graph.graph)}\")\n    print(f\"  版本号: {interest_graph.version}\")\n    \n    top_interests = interest_graph.get_top_interests(top_k=8)\n    print(f\"\\n  当前主要兴趣路径:\")\n    for i, (topic, weight) in enumerate(top_interests, 1):\n        print(f\"    {i}. {topic:30} (权重: {weight:.3f})\")\n    \n    return session\n\n\ndef example_negative_feedback_recovery():\n    \"\"\"  \n    示例场景：从负反馈恢复\n    展示智能体B的自我改进如何帮助系统从低质量推荐中恢复\n    \"\"\"  \n    print(\"\\n\" + \"=\"*70)\n    print(\" 示例场景: 从负反馈中恢复与改进\")\n    print(\"=\"*70)\n    \n    session = SessionManager()\n    user_id = \"recovery_user\"\n    \n    # 初始良好表现\n    print(f\"\\n【初期】系统表现良好\")\n    for i in range(2):\n        result = session.process_interaction(\n            user_id, f\"推荐主题{i+1}\",\n            {\n                \"clicked_indices\": [0, 1, 2],\n                \"browse_times\": [80, 100, 90],\n                \"conversion\": True,\n                \"satisfaction\": 0.85,\n                \"user_comment\": \"很好\"\n            }\n        )\n        print(f\"  第{i+1}次查询: 质量评分 {result['evaluation']['quality_score']:.2f}\")\n    \n    # 突然的质量下降\n    print(f\"\\n【质量下降】系统表现恶化\")\n    for i in range(3):\n        result = session.process_interaction(\n            user_id, f\"新查询主题{i+1}\",\n            {\n                \"clicked_indices\": [0],  # 只点击1个\n                \"browse_times\": [15],    # 浏览时间短\n                \"conversion\": False,\n                \"satisfaction\": 0.3,\n                \"user_comment\": \"推荐不相关，质量下降了\"\n            }\n        )\n        print(f\"  第{i+3}次查询: 质量评分 {result['evaluation']['quality_score']:.2f}\")\n        \n        if result.get('evolved'):\n            print(f\"  → 触发演化! 智能体开始自我改进\")\n    \n    # 恢复和改善\n    print(f\"\\n【恢复】系统逐步改进\")\n    for i in range(2):\n        result = session.process_interaction(\n            user_id, f\"恢复查询{i+1}\",\n            {\n                \"clicked_indices\": [0, 1, 2],\n                \"browse_times\": [70, 85, 75],\n                \"conversion\": True,\n                \"satisfaction\": 0.8,\n                \"user_comment\": \"改进了不少\"\n            }\n        )\n        print(f\"  第{i+6}次查询: 质量评分 {result['evaluation']['quality_score']:.2f}\")\n    \n    # 显示系统的自我改进数据\n    profile = session.get_user_profile(user_id)\n    health = profile.get('system_health', {})\n    \n    print(f\"\\n📊 系统恢复统计:\")\n    print(f\"  总交互次数: {health.get('total_iterations', 0)}\")  \n    print(f\"  演化次数: {health.get('total_evolutions', 0)}\")  \n    print(f\"  最终互惠受益分数: {health.get('mutual_benefit_score', 0):.3f}\")  \n    print(f\"  最后5次反馈质量: {[f['metrics']['quality_score'] for f in health.get('agent_b_stats', {}).get('recent_feedback', [])]}\")\n    \n    return session\n\n\nif __name__ == \"__main__\":\n    print(\"\\n\" + \"#\"*70)\n    print(\"#\" + \" \"*68 + \"#\")\n    print(\"#\" + \"  高级示例: 双智能体推荐系统的演化演示\".center(68) + \"#\")\n    print(\"#\" + \" \"*68 + \"#\")\n    print(\"#\"*70)\n    \n    # 运行示例1\n    session1, profile1 = example_medical_ai_user()\n    \n    # 运行示例2\n    session2 = example_cross_domain_exploration()\n    \n    # 运行示例3\n    session3 = example_negative_feedback_recovery()\n    \n    print(\"\\n\" + \"#\"*70)\n    print(\"#\" + \" \"*68 + \"#\")\n    print(\"#\" + \"  所有示例执行完成\".center(68) + \"#\")\n    print(\"#\" + \" \"*68 + \"#\")\n    print(\"#\"*70)\n
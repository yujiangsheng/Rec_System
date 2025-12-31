#!/usr/bin/env python3
"""
快速启动脚本
用于快速验证系统和运行演示
"""

import subprocess
import sys
import os


def print_banner():
    \"\"\"打印欢迎横幅\"\"\"
    banner = \"\"\"
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║       🤖 双智能体推荐系统 (Dual-Agent Recommendation System)         ║
║                                                                      ║
║  基于Qwen2.5的演化型推荐引擎，具备自我改进和知识图谱能力          ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
\"\"\"
    print(banner)


def check_environment():
    \"\"\"检查环境\"\"\"
    print(\"\\n📋 环境检查:\")
    print(f\"  Python版本: {sys.version.split()[0]}\")
    print(f\"  工作目录: {os.getcwd()}\")
    
    # 检查依赖
    dependencies = [\"torch\", \"transformers\", \"networkx\"]
    missing = []
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f\"  ✓ {dep} 已安装\")
        except ImportError:
            print(f\"  ✗ {dep} 未安装\")\n            missing.append(dep)
    
    if missing:
        print(f\"\\n⚠️  需要安装缺失的依赖: {', '.join(missing)}\")
        print(\"   运行: pip install -r requirements.txt\")\n        return False
    
    return True


def run_demo():
    \"\"\"运行演示\"\"\"
    print(\"\\n🚀 启动演示...\\n\")\n    subprocess.run([sys.executable, \"main.py\"])\n\n\ndef run_interactive():\n    \"\"\"运行交互模式\"\"\"
    print(\"\\n💬 启动交互模式...\\n\")\n    subprocess.run([sys.executable, \"main.py\", \"--interactive\"])\n\n\ndef run_advanced_examples():\n    \"\"\"运行高级示例\"\"\"
    print(\"\\n📚 运行高级示例...\\n\")\n    subprocess.run([sys.executable, \"advanced_examples.py\"])\n\n\ndef run_tests():\n    \"\"\"运行单元测试\"\"\"
    print(\"\\n✅ 运行单元测试...\\n\")\n    subprocess.run([sys.executable, \"-m\", \"unittest\", \"test_system.py\", \"-v\"])\n\n\ndef show_architecture():\n    \"\"\"显示架构文档\"\"\"
    print(\"\\n📐 项目架构...\\n\")\n    subprocess.run([sys.executable, \"ARCHITECTURE.py\"])\n\n\ndef main():\n    \"\"\"主菜单\"\"\"
    print_banner()\n    \n    if not check_environment():\n        return 1\n    \n    while True:\n        print(\"\\n\" + \"=\"*70)\n        print(\"主菜单\")\n        print(\"=\"*70)\n        print(\"\\n请选择操作:\")\n        print(\"  1. 🎬 运行演示 (自动演示完整工作流程)\")\n        print(\"  2. 💬 交互模式 (与系统实时交互)\")\n        print(\"  3. 📚 高级示例 (多个场景演示)\")\n        print(\"  4. ✅ 运行测试 (单元测试和集成测试)\")\n        print(\"  5. 📐 查看架构 (项目架构和设计文档)\")\n        print(\"  6. 📖 查看README (完整使用说明)\")\n        print(\"  0. 🚪 退出\")\n        print(\"\\n\" + \"=\"*70)\n        \n        choice = input(\"\\n请输入选择 (0-6): \").strip()\n        \n        if choice == \"1\":\n            run_demo()\n        elif choice == \"2\":\n            run_interactive()\n        elif choice == \"3\":\n            run_advanced_examples()\n        elif choice == \"4\":\n            run_tests()\n        elif choice == \"5\":\n            show_architecture()\n        elif choice == \"6\":\n            print(\"\\n📖 打开README.md...\\n\")\n            try:\n                import os\n                os.system(\"cat README.md | less\" if sys.platform != \"win32\" else \"more README.md\")\n            except:\n                print(\"请手动打开 README.md 文件\")\n        elif choice == \"0\":\n            print(\"\\n👋 感谢使用！再见！\\n\")\n            return 0\n        else:\n            print(\"\\n❌ 无效选择，请重试\")\n\n\nif __name__ == \"__main__\":\n    try:\n        sys.exit(main())\n    except KeyboardInterrupt:\n        print(\"\\n\\n👋 用户中断程序执行\")\n        sys.exit(0)\n"
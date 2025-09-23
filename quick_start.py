#!/usr/bin/env python3
"""
快速启动脚本 - 增强版学术论文分析系统
提供预设配置的快速启动选项
"""

import os
import sys
import argparse
from datetime import datetime, timedelta

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from user_config import UserConfig, save_user_config
from loguru import logger


def get_preset_configs():
    """获取预设配置"""
    now = datetime.now()
    past_year = (now - timedelta(days=365)).strftime("%Y-%m-%d")
    current_date = now.strftime("%Y-%m-%d")
    
    return {
        "1": {
            "name": "具身智能研究 (Embodied AI)",
            "description": "搜索具身智能、机器人学相关论文",
            "config": UserConfig(
                search_keywords=["embodied", "embodied AI", "robotics", "embodied intelligence"],
                research_categories=["cs.AI", "cs.RO", "cs.CV", "cs.LG"],
                start_date="2024-01-01",
                end_date="2024-12-31",
                max_papers=50,
                custom_task_categories={},
                use_default_categories=True,
                include_author_affiliations=True,
                output_format="csv"
            )
        },
        "2": {
            "name": "多模态学习 (Multimodal Learning)",
            "description": "搜索多模态、视觉-语言模型相关论文",
            "config": UserConfig(
                search_keywords=["multimodal", "vision-language", "CLIP", "cross-modal", "VLM"],
                research_categories=["cs.CV", "cs.CL", "cs.LG", "cs.AI"],
                start_date="2024-01-01",
                end_date="2024-12-31",
                max_papers=50,
                custom_task_categories={},
                use_default_categories=True,
                include_author_affiliations=True,
                output_format="csv"
            )
        },
        "3": {
            "name": "大语言模型 (Large Language Models)",
            "description": "搜索大语言模型、Transformer相关论文",
            "config": UserConfig(
                search_keywords=["large language model", "LLM", "transformer", "GPT", "BERT"],
                research_categories=["cs.CL", "cs.AI", "cs.LG"],
                start_date="2024-01-01",
                end_date="2024-12-31",
                max_papers=50,
                custom_task_categories={},
                use_default_categories=True,
                include_author_affiliations=True,
                output_format="csv"
            )
        },
        "4": {
            "name": "计算机视觉 (Computer Vision)",
            "description": "搜索计算机视觉、图像处理相关论文",
            "config": UserConfig(
                search_keywords=["computer vision", "image processing", "object detection", "segmentation"],
                research_categories=["cs.CV", "cs.AI", "cs.LG"],
                start_date="2024-01-01",
                end_date="2024-12-31",
                max_papers=50,
                custom_task_categories={},
                use_default_categories=True,
                include_author_affiliations=True,
                output_format="csv"
            )
        },
        "5": {
            "name": "强化学习 (Reinforcement Learning)",
            "description": "搜索强化学习、智能体相关论文",
            "config": UserConfig(
                search_keywords=["reinforcement learning", "RL", "agent", "policy learning"],
                research_categories=["cs.LG", "cs.AI", "cs.RO"],
                start_date="2024-01-01",
                end_date="2024-12-31",
                max_papers=50,
                custom_task_categories={},
                use_default_categories=True,
                include_author_affiliations=True,
                output_format="csv"
            )
        },
        "6": {
            "name": "最新热点 (Recent Trends)",
            "description": "搜索最近3个月的AI热点论文",
            "config": UserConfig(
                search_keywords=["AI", "machine learning", "deep learning", "neural network"],
                research_categories=["cs.AI", "cs.LG", "cs.CV", "cs.CL"],
                start_date=(now - timedelta(days=90)).strftime("%Y-%m-%d"),
                end_date=current_date,
                max_papers=30,
                custom_task_categories={},
                use_default_categories=True,
                include_author_affiliations=True,
                output_format="csv"
            )
        }
    }


def display_presets():
    """显示预设配置选项"""
    presets = get_preset_configs()
    
    print("🚀 增强版学术论文分析系统 - 快速启动")
    print("=" * 60)
    print("请选择预设配置：\n")
    
    for key, preset in presets.items():
        config = preset["config"]
        print(f"{key}. {preset['name']}")
        print(f"   📝 {preset['description']}")
        print(f"   🔍 检索词: {', '.join(config.search_keywords[:3])}{'...' if len(config.search_keywords) > 3 else ''}")
        print(f"   📅 时间范围: {config.start_date} 到 {config.end_date}")
        print(f"   📊 最大论文数: {config.max_papers}")
        print()
    
    print("7. 自定义配置 (进入交互式配置模式)")
    print("0. 退出")
    print("=" * 60)


def get_user_choice():
    """获取用户选择"""
    while True:
        choice = input("请输入选项编号 (0-7): ").strip()
        if choice in ['0', '1', '2', '3', '4', '5', '6', '7']:
            return choice
        print("❌ 无效选择，请输入 0-7 之间的数字")


def confirm_config(preset_name, config):
    """确认配置信息"""
    print(f"\n📋 已选择配置: {preset_name}")
    print("-" * 40)
    print(f"🔍 检索词: {', '.join(config.search_keywords)}")
    print(f"🏷️ 研究领域: {', '.join(config.research_categories)}")
    print(f"📅 时间范围: {config.start_date} 到 {config.end_date}")
    print(f"📊 最大论文数: {config.max_papers}")
    print(f"🎯 任务分类: {'默认分类' if config.use_default_categories else '自定义分类'}")
    print("-" * 40)
    
    confirm = input("确认使用此配置？(y/n): ").lower().strip()
    return confirm in ['y', 'yes', '是', '确认']


def run_analysis(api_key, config, output_dir="output"):
    """运行论文分析"""
    # 保存配置
    save_user_config(config)
    print("✅ 配置已保存")
    
    # 构建命令行参数
    cmd_args = [
        "python", "enhanced_main.py",
        "--openai_api_key", api_key,
        "--output_dir", output_dir,
        "--skip_setup"  # 跳过交互配置
    ]
    
    print(f"\n🚀 开始分析论文...")
    print(f"📁 结果将保存到: {output_dir}")
    print("-" * 40)
    
    # 执行分析
    import subprocess
    try:
        result = subprocess.run(cmd_args, check=True, capture_output=False)
        print("\n✅ 分析完成！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 分析失败: {e}")
        return False
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断分析")
        return False


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='快速启动学术论文分析')
    parser.add_argument('--api_key', type=str, help='OpenAI API密钥')
    parser.add_argument('--output_dir', type=str, default='output', help='输出目录')
    args = parser.parse_args()
    
    # 获取API密钥
    api_key = args.api_key or os.environ.get('OPENAI_API_KEY')
    if not api_key:
        print("❌ 请提供OpenAI API密钥")
        print("方法1: python quick_start.py --api_key YOUR_API_KEY")
        print("方法2: 设置环境变量 OPENAI_API_KEY")
        sys.exit(1)
    
    try:
        while True:
            display_presets()
            choice = get_user_choice()
            
            if choice == '0':
                print("👋 再见！")
                break
            elif choice == '7':
                print("🔧 启动交互式配置模式...")
                # 运行完整的交互式配置
                cmd_args = ["python", "enhanced_main.py", "--openai_api_key", api_key]
                subprocess.run(cmd_args)
                break
            else:
                # 使用预设配置
                presets = get_preset_configs()
                preset = presets[choice]
                
                if confirm_config(preset["name"], preset["config"]):
                    success = run_analysis(api_key, preset["config"], args.output_dir)
                    if success:
                        # 询问是否继续
                        if input("\n是否继续选择其他配置？(y/n): ").lower().strip() not in ['y', 'yes', '是']:
                            break
                    else:
                        print("分析失败，请检查配置和网络连接")
                else:
                    print("❌ 已取消")
    
    except KeyboardInterrupt:
        print("\n👋 用户退出")
    except Exception as e:
        logger.error(f"程序出错: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
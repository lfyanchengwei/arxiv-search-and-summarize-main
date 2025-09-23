#!/usr/bin/env python3
"""
增强版学术论文分析系统使用示例
演示如何使用各种功能
"""

import os
import sys
from datetime import datetime, timedelta

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from user_config import UserConfig, save_user_config
from enhanced_main import main as enhanced_main


def create_embodied_ai_config():
    """创建具身智能研究配置示例"""
    config = UserConfig(
        search_keywords=["embodied", "embodied AI", "robotics", "multimodal"],
        research_categories=["cs.AI", "cs.RO", "cs.CV", "cs.LG"],
        start_date="2024-01-01",
        end_date="2024-12-31",
        max_papers=30,
        custom_task_categories={
            "具身智能规划": {
                "definition": "在物理环境中进行长期任务规划和执行的智能体研究",
                "typical_output": "任务序列、执行计划",
                "datasets_metrics": "成功率、执行时间"
            }
        },
        use_default_categories=True,
        include_author_affiliations=True,
        output_format="csv"
    )
    return config


def create_multimodal_learning_config():
    """创建多模态学习配置示例"""
    config = UserConfig(
        search_keywords=["multimodal", "vision-language", "CLIP", "cross-modal"],
        research_categories=["cs.CV", "cs.CL", "cs.LG", "cs.AI"],
        start_date="2023-06-01",
        end_date="2024-06-01",
        max_papers=50,
        custom_task_categories={
            "跨模态检索": {
                "definition": "在不同模态之间进行信息检索和匹配",
                "typical_output": "检索结果、相似度分数",
                "datasets_metrics": "Recall@K, MRR"
            },
            "多模态生成": {
                "definition": "基于多种输入模态生成目标内容",
                "typical_output": "生成的图像、文本或视频",
                "datasets_metrics": "FID, BLEU, CLIP Score"
            }
        },
        use_default_categories=True,
        include_author_affiliations=True,
        output_format="csv"
    )
    return config


def create_nlp_config():
    """创建自然语言处理配置示例"""
    config = UserConfig(
        search_keywords=["large language model", "LLM", "transformer", "BERT", "GPT"],
        research_categories=["cs.CL", "cs.AI", "cs.LG"],
        start_date="2024-01-01",
        end_date="2024-12-31",
        max_papers=40,
        custom_task_categories={
            "大模型微调": {
                "definition": "针对特定任务对大型语言模型进行微调优化",
                "typical_output": "微调后的模型、性能提升",
                "datasets_metrics": "任务特定指标、参数效率"
            },
            "提示工程": {
                "definition": "设计和优化提示词以提升模型性能",
                "typical_output": "优化的提示模板、性能改进",
                "datasets_metrics": "准确率提升、推理效率"
            }
        },
        use_default_categories=True,
        include_author_affiliations=True,
        output_format="csv"
    )
    return config


def demo_config_creation():
    """演示配置创建和保存"""
    print("=== 配置创建演示 ===\n")
    
    configs = {
        "具身智能研究": create_embodied_ai_config(),
        "多模态学习": create_multimodal_learning_config(),
        "自然语言处理": create_nlp_config()
    }
    
    for name, config in configs.items():
        print(f"📋 {name}配置:")
        print(f"  检索词: {', '.join(config.search_keywords)}")
        print(f"  研究领域: {', '.join(config.research_categories)}")
        print(f"  时间范围: {config.start_date} 到 {config.end_date}")
        print(f"  最大论文数: {config.max_papers}")
        print(f"  自定义分类数: {len(config.custom_task_categories)}")
        print()
    
    # 选择一个配置保存
    selected_config = configs["具身智能研究"]
    save_user_config(selected_config)
    print(f"✅ 已保存'{list(configs.keys())[0]}'配置到 user_config.json")


def demo_time_range_configs():
    """演示不同时间范围的配置"""
    print("=== 时间范围配置演示 ===\n")
    
    now = datetime.now()
    
    time_configs = {
        "最近3个月": {
            "start": (now - timedelta(days=90)).strftime("%Y-%m-%d"),
            "end": now.strftime("%Y-%m-%d")
        },
        "最近6个月": {
            "start": (now - timedelta(days=180)).strftime("%Y-%m-%d"),
            "end": now.strftime("%Y-%m-%d")
        },
        "过去一年": {
            "start": (now - timedelta(days=365)).strftime("%Y-%m-%d"),
            "end": now.strftime("%Y-%m-%d")
        },
        "2024年全年": {
            "start": "2024-01-01",
            "end": "2024-12-31"
        },
        "2023年下半年": {
            "start": "2023-07-01",
            "end": "2023-12-31"
        }
    }
    
    for name, time_range in time_configs.items():
        print(f"📅 {name}: {time_range['start']} 到 {time_range['end']}")
    
    print("\n💡 建议根据研究需要选择合适的时间范围")


def demo_research_categories():
    """演示研究领域分类"""
    print("=== 研究领域分类演示 ===\n")
    
    category_examples = {
        "人工智能核心": ["cs.AI", "cs.LG", "cs.NE"],
        "计算机视觉": ["cs.CV", "cs.GR", "cs.MM"],
        "自然语言处理": ["cs.CL", "cs.IR", "cs.AI"],
        "机器人学": ["cs.RO", "cs.AI", "cs.CV"],
        "人机交互": ["cs.HC", "cs.AI", "cs.MM"],
        "跨学科研究": ["cs.AI", "q-bio.QM", "stat.ML"],
        "理论基础": ["cs.LG", "math.ST", "stat.ML"]
    }
    
    for field, categories in category_examples.items():
        print(f"🔬 {field}: {', '.join(categories)}")
    
    print("\n💡 可以组合多个领域以获得更全面的搜索结果")


def demo_custom_task_categories():
    """演示自定义任务分类"""
    print("=== 自定义任务分类演示 ===\n")
    
    custom_examples = {
        "医疗AI应用": {
            "医学图像分析": "使用AI技术分析医学影像，辅助疾病诊断",
            "药物发现": "利用机器学习加速新药研发过程",
            "临床决策支持": "为医生提供基于数据的诊疗建议"
        },
        "金融科技": {
            "算法交易": "使用AI进行自动化金融交易",
            "风险评估": "基于机器学习的信用风险和市场风险评估",
            "反欺诈检测": "识别和防范金融欺诈行为"
        },
        "教育技术": {
            "个性化学习": "根据学生特点提供定制化教学内容",
            "智能评估": "自动化的学习成果评估和反馈",
            "知识图谱构建": "构建领域知识的结构化表示"
        }
    }
    
    for domain, tasks in custom_examples.items():
        print(f"🏷️ {domain}:")
        for task, description in tasks.items():
            print(f"  • {task}: {description}")
        print()
    
    print("💡 可以根据具体研究领域定义专门的任务分类")


def main():
    """主演示函数"""
    print("🚀 增强版学术论文分析系统使用示例\n")
    
    demos = [
        ("配置创建", demo_config_creation),
        ("时间范围配置", demo_time_range_configs),
        ("研究领域分类", demo_research_categories),
        ("自定义任务分类", demo_custom_task_categories)
    ]
    
    for i, (name, demo_func) in enumerate(demos, 1):
        print(f"{i}. {name}")
    
    print("\n请选择要运行的演示 (1-4), 或按回车查看所有演示:")
    choice = input().strip()
    
    if choice == "":
        # 运行所有演示
        for name, demo_func in demos:
            demo_func()
            print("\n" + "="*60 + "\n")
    elif choice.isdigit() and 1 <= int(choice) <= len(demos):
        # 运行选定的演示
        name, demo_func = demos[int(choice) - 1]
        demo_func()
    else:
        print("❌ 无效选择")
        return
    
    print("✨ 演示完成！")
    print("\n要运行实际的论文分析，请使用:")
    print("python enhanced_main.py --openai_api_key YOUR_API_KEY")


if __name__ == "__main__":
    main()
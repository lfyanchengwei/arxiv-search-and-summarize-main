#!/usr/bin/env python3
"""
为GitHub Actions生成配置文件
"""

import argparse
import json
from datetime import datetime
from user_config import UserConfig, save_user_config


def get_preset_configs():
    """获取预设配置"""
    return {
        "embodied_ai": {
            "search_keywords": ["embodied", "embodied AI", "robotics", "embodied intelligence"],
            "research_categories": ["cs.AI", "cs.RO", "cs.CV", "cs.LG"],
            "description": "具身智能研究"
        },
        "multimodal_learning": {
            "search_keywords": ["multimodal", "vision-language", "CLIP", "cross-modal", "VLM"],
            "research_categories": ["cs.CV", "cs.CL", "cs.LG", "cs.AI"],
            "description": "多模态学习"
        },
        "large_language_models": {
            "search_keywords": ["large language model", "LLM", "transformer", "GPT", "BERT"],
            "research_categories": ["cs.CL", "cs.AI", "cs.LG"],
            "description": "大语言模型"
        },
        "computer_vision": {
            "search_keywords": ["computer vision", "image processing", "object detection", "segmentation"],
            "research_categories": ["cs.CV", "cs.AI", "cs.LG"],
            "description": "计算机视觉"
        },
        "reinforcement_learning": {
            "search_keywords": ["reinforcement learning", "RL", "agent", "policy learning"],
            "research_categories": ["cs.LG", "cs.AI", "cs.RO"],
            "description": "强化学习"
        },
        "recent_trends": {
            "search_keywords": ["AI", "machine learning", "deep learning", "neural network"],
            "research_categories": ["cs.AI", "cs.LG", "cs.CV", "cs.CL"],
            "description": "最新AI趋势"
        }
    }


def parse_list_input(input_str):
    """解析逗号分隔的输入"""
    if not input_str:
        return []
    return [item.strip() for item in input_str.split(',') if item.strip()]


def main():
    parser = argparse.ArgumentParser(description='为GitHub Actions生成配置')
    parser.add_argument('--keywords', type=str, help='检索关键词 (逗号分隔)')
    parser.add_argument('--categories', type=str, help='研究领域 (逗号分隔)')
    parser.add_argument('--start-date', type=str, help='开始日期')
    parser.add_argument('--end-date', type=str, help='结束日期')
    parser.add_argument('--max-papers', type=int, default=50, help='最大论文数量')
    parser.add_argument('--preset', type=str, default='custom', help='预设配置')
    
    args = parser.parse_args()
    
    # 获取预设配置
    presets = get_preset_configs()
    
    if args.preset != 'custom' and args.preset in presets:
        # 使用预设配置
        preset = presets[args.preset]
        config = UserConfig(
            search_keywords=preset["search_keywords"],
            research_categories=preset["research_categories"],
            start_date=args.start_date or "2024-01-01",
            end_date=args.end_date or "2024-12-31",
            max_papers=args.max_papers,
            custom_task_categories={},
            use_default_categories=True,
            include_author_affiliations=True,
            output_format="csv"
        )
        print(f"✅ 使用预设配置: {preset['description']}")
    else:
        # 使用自定义配置
        config = UserConfig(
            search_keywords=parse_list_input(args.keywords),
            research_categories=parse_list_input(args.categories),
            start_date=args.start_date or "2024-01-01",
            end_date=args.end_date or "2024-12-31",
            max_papers=args.max_papers,
            custom_task_categories={},
            use_default_categories=True,
            include_author_affiliations=True,
            output_format="csv"
        )
        print("✅ 使用自定义配置")
    
    # 保存配置
    save_user_config(config)
    
    # 输出配置信息
    print(f"🔍 检索关键词: {', '.join(config.search_keywords)}")
    print(f"🏷️ 研究领域: {', '.join(config.research_categories)}")
    print(f"📅 时间范围: {config.start_date} 到 {config.end_date}")
    print(f"📊 最大论文数: {config.max_papers}")
    
    # 生成运行信息文件
    run_info = {
        "timestamp": datetime.now().isoformat(),
        "config": {
            "search_keywords": config.search_keywords,
            "research_categories": config.research_categories,
            "start_date": config.start_date,
            "end_date": config.end_date,
            "max_papers": config.max_papers
        },
        "preset_used": args.preset if args.preset != 'custom' else None
    }
    
    with open('output/run_info.json', 'w', encoding='utf-8') as f:
        json.dump(run_info, f, ensure_ascii=False, indent=2)
    
    print("✅ 配置生成完成")


if __name__ == "__main__":
    main()
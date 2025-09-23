"""
增强版学术论文分析系统主程序
支持用户自定义检索词、时间区间、研究领域和任务分类
"""

import arxiv
import argparse
import os
import sys
import json
from datetime import datetime, timedelta
from dotenv import load_dotenv
from loguru import logger
from tqdm import tqdm
from typing import List, Dict, Optional

# 加载环境变量
load_dotenv(override=True)
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# 导入自定义模块
from enhanced_paper import EnhancedArxivPaper
from llm import set_global_llm
from enhanced_paper_analyzer import EnhancedPaperAnalyzer
from enhanced_csv_exporter import EnhancedCSVExporter
from user_config import UserConfig, load_user_config, save_user_config

# arXiv主要研究领域分类
ARXIV_CATEGORIES = {
    "cs": "计算机科学 (Computer Science)",
    "math": "数学 (Mathematics)", 
    "physics": "物理学 (Physics)",
    "q-bio": "定量生物学 (Quantitative Biology)",
    "q-fin": "定量金融 (Quantitative Finance)",
    "stat": "统计学 (Statistics)",
    "eess": "电气工程与系统科学 (Electrical Engineering and Systems Science)",
    "econ": "经济学 (Economics)"
}

# 计算机科学子领域
CS_SUBCATEGORIES = {
    "cs.AI": "人工智能 (Artificial Intelligence)",
    "cs.CL": "计算与语言 (Computation and Language)",
    "cs.CV": "计算机视觉与模式识别 (Computer Vision and Pattern Recognition)",
    "cs.LG": "机器学习 (Machine Learning)",
    "cs.RO": "机器人学 (Robotics)",
    "cs.HC": "人机交互 (Human-Computer Interaction)",
    "cs.IR": "信息检索 (Information Retrieval)",
    "cs.MM": "多媒体 (Multimedia)",
    "cs.NE": "神经与进化计算 (Neural and Evolutionary Computing)",
    "cs.SI": "社会与信息网络 (Social and Information Networks)"
}


def interactive_setup() -> UserConfig:
    """交互式设置用户配置"""
    print("\n=== 学术论文分析系统配置 ===\n")
    
    # 尝试加载现有配置
    config = load_user_config()
    
    print("1. 检索词配置")
    print(f"当前检索词: {', '.join(config.search_keywords) if config.search_keywords else '无'}")
    
    if input("是否修改检索词? (y/n): ").lower() == 'y':
        keywords_input = input("请输入检索词（用逗号分隔，如: embodied,robotics,multimodal）: ")
        config.search_keywords = [kw.strip() for kw in keywords_input.split(',') if kw.strip()]
    
    print(f"\n2. 研究领域配置")
    print(f"当前领域: {config.research_categories if config.research_categories else '无'}")
    
    if input("是否修改研究领域? (y/n): ").lower() == 'y':
        print("\n可选的arXiv主要领域:")
        for key, name in ARXIV_CATEGORIES.items():
            print(f"  {key}: {name}")
        
        categories_input = input("请输入领域代码（用逗号分隔，如: cs,math）: ")
        main_categories = [cat.strip() for cat in categories_input.split(',') if cat.strip()]
        
        # 如果选择了cs，询问是否要选择具体子领域
        subcategories = []
        if 'cs' in main_categories:
            if input("是否选择计算机科学的具体子领域? (y/n): ").lower() == 'y':
                print("\n计算机科学子领域:")
                for key, name in CS_SUBCATEGORIES.items():
                    print(f"  {key}: {name}")
                
                sub_input = input("请输入子领域代码（用逗号分隔）: ")
                subcategories = [sub.strip() for sub in sub_input.split(',') if sub.strip()]
        
        config.research_categories = main_categories + subcategories
    
    print(f"\n3. 时间区间配置")
    print(f"当前时间区间: {config.start_date} 到 {config.end_date}")
    
    if input("是否修改时间区间? (y/n): ").lower() == 'y':
        start_date = input("请输入开始日期 (YYYY-MM-DD格式，如: 2024-01-01): ")
        end_date = input("请输入结束日期 (YYYY-MM-DD格式，如: 2024-12-31): ")
        
        try:
            # 验证日期格式
            datetime.strptime(start_date, "%Y-%m-%d")
            datetime.strptime(end_date, "%Y-%m-%d")
            config.start_date = start_date
            config.end_date = end_date
        except ValueError:
            print("日期格式错误，保持原设置")
    
    print(f"\n4. 任务分类配置")
    print(f"当前自定义任务数量: {len(config.custom_task_categories)}")
    
    if input("是否修改任务分类? (y/n): ").lower() == 'y':
        print("选择任务分类模式:")
        print("1. 使用默认分类")
        print("2. 添加自定义分类")
        print("3. 完全自定义分类")
        
        choice = input("请选择 (1/2/3): ")
        
        if choice == '2':
            print("添加自定义任务分类（输入空行结束）:")
            while True:
                task_name = input("任务名称: ").strip()
                if not task_name:
                    break
                task_desc = input("任务描述: ").strip()
                config.custom_task_categories[task_name] = {
                    "definition": task_desc,
                    "typical_output": "",
                    "datasets_metrics": ""
                }
        elif choice == '3':
            config.custom_task_categories = {}
            print("创建完全自定义的任务分类（输入空行结束）:")
            while True:
                task_name = input("任务名称: ").strip()
                if not task_name:
                    break
                task_desc = input("任务描述: ").strip()
                config.custom_task_categories[task_name] = {
                    "definition": task_desc,
                    "typical_output": "",
                    "datasets_metrics": ""
                }
    
    print(f"\n5. 其他配置")
    print(f"最大论文数量: {config.max_papers}")
    
    if input("是否修改最大论文数量? (y/n): ").lower() == 'y':
        try:
            max_papers = int(input(f"请输入最大论文数量 (当前: {config.max_papers}): "))
            config.max_papers = max_papers
        except ValueError:
            print("输入无效，保持原设置")
    
    # 保存配置
    save_user_config(config)
    print(f"\n配置已保存到 {UserConfig.CONFIG_FILE}")
    
    return config


def build_search_query(config: UserConfig) -> str:
    """根据用户配置构建搜索查询"""
    query_parts = []
    
    # 添加关键词查询
    if config.search_keywords:
        keyword_query = " OR ".join([f'all:"{kw}"' for kw in config.search_keywords])
        query_parts.append(f"({keyword_query})")
    
    # 添加领域限制
    if config.research_categories:
        category_query = " OR ".join([f'cat:{cat}' for cat in config.research_categories])
        query_parts.append(f"({category_query})")
    
    # 添加时间限制
    start_date_str = config.start_date.replace('-', '')
    end_date_str = config.end_date.replace('-', '')
    query_parts.append(f'submittedDate:[{start_date_str} TO {end_date_str}]')
    
    return " AND ".join(query_parts)


def search_papers_with_config(config: UserConfig) -> List[EnhancedArxivPaper]:
    """根据用户配置搜索论文"""
    query = build_search_query(config)
    
    logger.info(f"搜索查询: {query}")
    logger.info(f"检索词: {', '.join(config.search_keywords)}")
    logger.info(f"研究领域: {', '.join(config.research_categories)}")
    logger.info(f"时间范围: {config.start_date} 到 {config.end_date}")
    
    client = arxiv.Client(num_retries=10, delay_seconds=3)
    search = arxiv.Search(
        query=query,
        max_results=config.max_papers,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )
    
    papers = []
    logger.info(f"正在检索论文，最大数量: {config.max_papers}")
    
    try:
        with tqdm(desc="检索论文") as pbar:
            for result in client.results(search):
                paper = EnhancedArxivPaper(result)
                papers.append(paper)
                pbar.update(1)
                
                if len(papers) >= config.max_papers:
                    break
                    
    except Exception as e:
        logger.error(f"搜索论文时出错: {str(e)}")
        raise
    
    logger.info(f"搜索完成，找到 {len(papers)} 篇论文")
    
    # 过滤非计算机科学相关论文（如果用户选择了计算机科学领域）
    if any(cat.startswith('cs') for cat in config.research_categories):
        filtered_papers = []
        for paper in papers:
            # 检查论文是否与计算机科学相关
            if paper.is_cs_related():
                filtered_papers.append(paper)
            else:
                logger.debug(f"跳过非计算机科学论文: {paper.title}")
        
        logger.info(f"过滤后剩余 {len(filtered_papers)} 篇计算机科学相关论文")
        return filtered_papers
    
    return papers


def setup_argument_parser():
    """设置命令行参数解析器"""
    parser = argparse.ArgumentParser(description='增强版学术论文分析系统')
    
    def add_argument(*args, **kwargs):
        def get_env(key: str, default=None):
            v = os.environ.get(key)
            if v == '' or v is None:
                return default
            return v
        
        parser.add_argument(*args, **kwargs)
        arg_full_name = kwargs.get('dest', args[-1][2:])
        env_name = arg_full_name.upper()
        env_value = get_env(env_name)
        
        if env_value is not None:
            if kwargs.get('type') == bool:
                env_value = env_value.lower() in ['true', '1']
            elif kwargs.get('type') is not None:
                env_value = kwargs.get('type')(env_value)
            parser.set_defaults(**{arg_full_name: env_value})
    
    # 必需参数
    add_argument('--openai_api_key', type=str, help='OpenAI API密钥', required=False)
    add_argument('--openai_api_base', type=str, help='OpenAI API基础URL', 
                default='https://api.openai.com/v1')
    add_argument('--model_name', type=str, help='LLM模型名称', default='gpt-4o')
    
    # 可选参数
    add_argument('--output_dir', type=str, help='输出目录', default='output')
    add_argument('--debug', action='store_true', help='调试模式')
    add_argument('--skip_setup', action='store_true', help='跳过交互式配置，使用现有配置')
    
    return parser


def main():
    """主函数"""
    # 设置参数解析
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    # 设置日志级别
    if args.debug:
        logger.remove()
        logger.add(sys.stdout, level="DEBUG")
        logger.debug("调试模式已启用")
    else:
        logger.remove()
        logger.add(sys.stdout, level="INFO")
    
    # 验证API密钥
    if not args.openai_api_key:
        logger.error("必须提供OpenAI API密钥")
        sys.exit(1)
    
    try:
        # 交互式配置或加载现有配置
        if args.skip_setup:
            config = load_user_config()
            logger.info("使用现有配置")
        else:
            config = interactive_setup()
        
        # 设置LLM
        logger.info("初始化LLM...")
        logger.info(f"使用API LLM: {args.model_name}")
        set_global_llm(
            api_key=args.openai_api_key,
            base_url=args.openai_api_base,
            model=args.model_name,
            lang="Chinese"
        )
        
        # 搜索论文
        papers = search_papers_with_config(config)
        
        if not papers:
            logger.warning("未找到符合条件的论文")
            return
        
        # 分析论文
        analyzer = EnhancedPaperAnalyzer(config)
        analyses = analyzer.analyze_papers_batch(papers)
        
        if not analyses:
            logger.warning("没有成功分析的论文")
            return
        
        # 导出结果
        exporter = EnhancedCSVExporter()
        
        # 导出详细分析结果
        csv_path = exporter.export_to_csv(analyses, args.output_dir)
        
        # 导出统计摘要
        summary_path = exporter.export_summary_stats(analyses, args.output_dir)
        
        # 打印摘要
        exporter.print_summary(analyses)
        
        logger.success("分析完成！")
        logger.info(f"详细结果文件: {csv_path}")
        if summary_path:
            logger.info(f"统计摘要文件: {summary_path}")
        
    except KeyboardInterrupt:
        logger.warning("用户中断程序执行")
        sys.exit(1)
    except Exception as e:
        logger.error(f"程序执行出错: {str(e)}")
        if args.debug:
            raise
        sys.exit(1)


if __name__ == '__main__':
    main()
"""
学术论文分析系统主程序
搜索包含"embodied"关键词的arXiv论文并进行结构化分析
"""

import arxiv
import argparse
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from loguru import logger
from tqdm import tqdm

# 加载环境变量
load_dotenv(override=True)
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# 导入自定义模块
from paper import ArxivPaper
from llm import set_global_llm
from paper_analyzer import PaperAnalyzer
from csv_exporter import CSVExporter


def search_embodied_papers(max_results: int = 100) -> list[ArxivPaper]:
    """
    搜索包含"embodied"关键词的arXiv论文（2024-2025年）
    
    Args:
        max_results: 最大搜索结果数量
        
    Returns:
        ArxivPaper对象列表
    """
    logger.info("开始搜索包含'embodied'关键词的论文...")
    
    # 构建搜索查询
    # 搜索标题或摘要包含"embodied"的论文，时间范围2024-2025年
    query = 'all:embodied AND submittedDate:[20240101 TO 20251231]'
    
    client = arxiv.Client(num_retries=10, delay_seconds=3)
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending
    )
    
    papers = []
    logger.info(f"正在检索论文，最大数量: {max_results}")
    
    try:
        with tqdm(desc="检索论文") as pbar:
            for result in client.results(search):
                paper = ArxivPaper(result)
                papers.append(paper)
                pbar.update(1)
                
                # 检查是否达到最大数量
                if len(papers) >= max_results:
                    break
                    
    except Exception as e:
        logger.error(f"搜索论文时出错: {str(e)}")
        raise
    
    logger.info(f"搜索完成，找到 {len(papers)} 篇论文")
    
    # 过滤确保标题或摘要确实包含"embodied"（不区分大小写）
    filtered_papers = []
    for paper in papers:
        title_lower = paper.title.lower()
        summary_lower = paper.summary.lower()
        if 'embodied' in title_lower or 'embodied' in summary_lower:
            filtered_papers.append(paper)
    
    logger.info(f"过滤后剩余 {len(filtered_papers)} 篇相关论文")
    return filtered_papers


def setup_argument_parser():
    """设置命令行参数解析器"""
    parser = argparse.ArgumentParser(description='学术论文分析系统 - 分析包含embodied关键词的论文')
    
    def add_argument(*args, **kwargs):
        def get_env(key: str, default=None):
            # 处理运行时生成的环境变量
            # 未设置的环境变量会传递为''，我们应该将其视为None
            v = os.environ.get(key)
            if v == '' or v is None:
                return default
            return v
        
        parser.add_argument(*args, **kwargs)
        arg_full_name = kwargs.get('dest', args[-1][2:])
        env_name = arg_full_name.upper()
        env_value = get_env(env_name)
        
        if env_value is not None:
            # 将env_value转换为指定类型
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
    add_argument('--max_papers', type=int, help='最大分析论文数量', default=50)
    add_argument('--output_dir', type=str, help='输出目录', default='output')
    add_argument('--use_local_llm', type=bool, help='使用本地LLM而非API', default=False)
    add_argument('--debug', action='store_true', help='调试模式')
    
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
    
    # 验证API密钥（如果使用API）
    if not args.use_local_llm and not args.openai_api_key:
        logger.error("使用API模式时必须提供OpenAI API密钥")
        sys.exit(1)
    
    try:
        # 设置LLM
        logger.info("初始化LLM...")
        if args.use_local_llm:
            logger.info("使用本地LLM")
            set_global_llm(lang="Chinese")
        else:
            logger.info(f"使用API LLM: {args.model_name}")
            set_global_llm(
                api_key=args.openai_api_key,
                base_url=args.openai_api_base,
                model=args.model_name,
                lang="Chinese"
            )
        
        # 搜索论文
        papers = search_embodied_papers(max_results=args.max_papers)
        
        if not papers:
            logger.warning("未找到符合条件的论文")
            return
        
        # 分析论文
        analyzer = PaperAnalyzer()
        analyses = analyzer.analyze_papers_batch(papers)
        
        if not analyses:
            logger.warning("没有成功分析的论文")
            return
        
        # 导出结果
        exporter = CSVExporter()
        
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
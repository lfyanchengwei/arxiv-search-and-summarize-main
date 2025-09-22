"""
CSV导出器：将论文分析结果导出为CSV格式
"""

import csv
import os
from typing import List
from datetime import datetime
from loguru import logger
from paper_analyzer import PaperAnalysis


class CSVExporter:
    """CSV导出器类"""
    
    def __init__(self):
        self.csv_headers = [
            "Title",
            "Task_Category", 
            "Methods",
            "Contributions",
            "Training_Dataset",
            "Testing_Dataset", 
            "Evaluation_Metrics",
            "Publication_Date",
            "ArXiv_URL",
            "Classification_Confidence"
        ]
    
    def export_to_csv(self, analyses: List[PaperAnalysis], output_dir: str = "output") -> str:
        """
        将分析结果导出为CSV文件
        
        Args:
            analyses: PaperAnalysis对象列表
            output_dir: 输出目录
            
        Returns:
            生成的CSV文件路径
        """
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"embody_papers_analysis_{timestamp}.csv"
        filepath = os.path.join(output_dir, filename)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # 写入表头
                writer.writerow(self.csv_headers)
                
                # 写入数据
                for analysis in analyses:
                    row = [
                        analysis.title,
                        analysis.task_category,
                        analysis.methods,
                        analysis.contributions,
                        analysis.training_dataset,
                        analysis.testing_dataset,
                        analysis.evaluation_metrics,
                        analysis.publication_date,
                        analysis.arxiv_url,
                        analysis.confidence
                    ]
                    writer.writerow(row)
            
            logger.info(f"CSV文件已生成: {filepath}")
            logger.info(f"共导出 {len(analyses)} 条记录")
            
            return filepath
            
        except Exception as e:
            logger.error(f"导出CSV文件失败: {str(e)}")
            raise
    
    def print_summary(self, analyses: List[PaperAnalysis]):
        """
        打印分析结果摘要
        
        Args:
            analyses: PaperAnalysis对象列表
        """
        if not analyses:
            logger.info("没有找到符合条件的论文")
            return
        
        # 统计任务类别分布
        category_counts = {}
        confidence_sum = 0
        
        for analysis in analyses:
            category = analysis.task_category
            category_counts[category] = category_counts.get(category, 0) + 1
            confidence_sum += analysis.confidence
        
        # 打印统计信息
        logger.info("=" * 50)
        logger.info("论文分析结果摘要")
        logger.info("=" * 50)
        logger.info(f"总论文数量: {len(analyses)}")
        logger.info(f"平均分类置信度: {confidence_sum / len(analyses):.2f}")
        logger.info("")
        logger.info("任务类别分布:")
        
        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(analyses)) * 100
            logger.info(f"  {category}: {count} 篇 ({percentage:.1f}%)")
        
        logger.info("=" * 50)
    
    def export_summary_stats(self, analyses: List[PaperAnalysis], output_dir: str = "output") -> str:
        """
        导出统计摘要到单独的CSV文件
        
        Args:
            analyses: PaperAnalysis对象列表
            output_dir: 输出目录
            
        Returns:
            生成的统计文件路径
        """
        if not analyses:
            return None
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"embody_papers_summary_{timestamp}.csv"
        filepath = os.path.join(output_dir, filename)
        
        # 统计任务类别分布
        category_counts = {}
        for analysis in analyses:
            category = analysis.task_category
            category_counts[category] = category_counts.get(category, 0) + 1
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # 写入表头
                writer.writerow(["Task_Category", "Paper_Count", "Percentage"])
                
                # 写入统计数据
                total = len(analyses)
                for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / total) * 100
                    writer.writerow([category, count, f"{percentage:.1f}%"])
            
            logger.info(f"统计摘要文件已生成: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"导出统计摘要失败: {str(e)}")
            raise
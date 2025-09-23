"""
增强版CSV导出器：支持作者信息和更多统计功能
"""

import csv
import os
from typing import List, Dict
from datetime import datetime
from loguru import logger
from enhanced_paper_analyzer import EnhancedPaperAnalysis


class EnhancedCSVExporter:
    """增强版CSV导出器类"""
    
    def __init__(self):
        self.csv_headers = [
            "Title",
            "Authors",
            "Authors_with_Affiliations", 
            "Primary_Affiliations",
            "Task_Category",
            "Research_Field",
            "Methods",
            "Contributions",
            "Training_Dataset",
            "Testing_Dataset",
            "Evaluation_Metrics",
            "Publication_Date",
            "ArXiv_URL",
            "ArXiv_Categories",
            "Classification_Confidence",
            "Novelty_Score"
        ]
    
    def export_to_csv(self, analyses: List[EnhancedPaperAnalysis], output_dir: str = "output") -> str:
        """
        将分析结果导出为CSV文件
        
        Args:
            analyses: EnhancedPaperAnalysis对象列表
            output_dir: 输出目录
            
        Returns:
            生成的CSV文件路径
        """
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"enhanced_papers_analysis_{timestamp}.csv"
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
                        analysis.authors,
                        analysis.authors_with_affiliations,
                        analysis.primary_affiliations,
                        analysis.task_category,
                        analysis.research_field,
                        analysis.methods,
                        analysis.contributions,
                        analysis.training_dataset,
                        analysis.testing_dataset,
                        analysis.evaluation_metrics,
                        analysis.publication_date,
                        analysis.arxiv_url,
                        analysis.arxiv_categories,
                        analysis.confidence,
                        analysis.novelty_score
                    ]
                    writer.writerow(row)
            
            logger.info(f"CSV文件已生成: {filepath}")
            logger.info(f"共导出 {len(analyses)} 条记录")
            
            return filepath
            
        except Exception as e:
            logger.error(f"导出CSV文件失败: {str(e)}")
            raise
    
    def print_summary(self, analyses: List[EnhancedPaperAnalysis]):
        """
        打印分析结果摘要
        
        Args:
            analyses: EnhancedPaperAnalysis对象列表
        """
        if not analyses:
            logger.info("没有找到符合条件的论文")
            return
        
        # 统计任务类别分布
        category_counts = {}
        field_counts = {}
        confidence_sum = 0
        novelty_sum = 0
        
        for analysis in analyses:
            # 任务类别统计
            category = analysis.task_category
            category_counts[category] = category_counts.get(category, 0) + 1
            
            # 研究领域统计
            field = analysis.research_field
            field_counts[field] = field_counts.get(field, 0) + 1
            
            # 置信度和创新性统计
            confidence_sum += analysis.confidence
            novelty_sum += analysis.novelty_score
        
        # 打印统计信息
        logger.info("=" * 60)
        logger.info("增强版论文分析结果摘要")
        logger.info("=" * 60)
        logger.info(f"总论文数量: {len(analyses)}")
        logger.info(f"平均分类置信度: {confidence_sum / len(analyses):.2f}")
        logger.info(f"平均创新性评分: {novelty_sum / len(analyses):.2f}")
        
        # 高创新性论文统计
        high_novelty_count = sum(1 for analysis in analyses if analysis.novelty_score >= 4)
        logger.info(f"高创新性论文数量(评分>=4): {high_novelty_count} 篇 ({high_novelty_count/len(analyses)*100:.1f}%)")
        
        logger.info("")
        logger.info("任务类别分布:")
        for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(analyses)) * 100
            logger.info(f"  {category}: {count} 篇 ({percentage:.1f}%)")
        
        logger.info("")
        logger.info("研究领域分布:")
        for field, count in sorted(field_counts.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / len(analyses)) * 100
            logger.info(f"  {field}: {count} 篇 ({percentage:.1f}%)")
        
        # 显示最具创新性的论文
        logger.info("")
        logger.info("最具创新性的论文 (评分>=4):")
        high_novelty_papers = [a for a in analyses if a.novelty_score >= 4]
        high_novelty_papers.sort(key=lambda x: x.novelty_score, reverse=True)
        
        for i, paper in enumerate(high_novelty_papers[:5], 1):  # 显示前5篇
            logger.info(f"  {i}. {paper.title[:80]}... (评分: {paper.novelty_score})")
        
        logger.info("=" * 60)
    
    def export_summary_stats(self, analyses: List[EnhancedPaperAnalysis], output_dir: str = "output") -> str:
        """
        导出详细统计摘要到CSV文件
        
        Args:
            analyses: EnhancedPaperAnalysis对象列表
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
        filename = f"enhanced_papers_summary_{timestamp}.csv"
        filepath = os.path.join(output_dir, filename)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # 任务类别统计
                writer.writerow(["=== 任务类别分布 ==="])
                writer.writerow(["Task_Category", "Paper_Count", "Percentage"])
                
                category_counts = {}
                for analysis in analyses:
                    category = analysis.task_category
                    category_counts[category] = category_counts.get(category, 0) + 1
                
                total = len(analyses)
                for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / total) * 100
                    writer.writerow([category, count, f"{percentage:.1f}%"])
                
                writer.writerow([])  # 空行
                
                # 研究领域统计
                writer.writerow(["=== 研究领域分布 ==="])
                writer.writerow(["Research_Field", "Paper_Count", "Percentage"])
                
                field_counts = {}
                for analysis in analyses:
                    field = analysis.research_field
                    field_counts[field] = field_counts.get(field, 0) + 1
                
                for field, count in sorted(field_counts.items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / total) * 100
                    writer.writerow([field, count, f"{percentage:.1f}%"])
                
                writer.writerow([])  # 空行
                
                # 创新性统计
                writer.writerow(["=== 创新性统计 ==="])
                writer.writerow(["Metric", "Value"])
                
                novelty_scores = [analysis.novelty_score for analysis in analyses]
                confidence_scores = [analysis.confidence for analysis in analyses]
                
                writer.writerow(["平均创新性评分", f"{sum(novelty_scores) / len(novelty_scores):.2f}"])
                writer.writerow(["最高创新性评分", max(novelty_scores)])
                writer.writerow(["最低创新性评分", min(novelty_scores)])
                writer.writerow(["高创新性论文数量(评分>=4)", sum(1 for score in novelty_scores if score >= 4)])
                writer.writerow(["平均分类置信度", f"{sum(confidence_scores) / len(confidence_scores):.2f}"])
                
                writer.writerow([])  # 空行
                
                # 机构统计
                writer.writerow(["=== 主要机构分布 ==="])
                writer.writerow(["Institution", "Paper_Count"])
                
                institution_counts = {}
                for analysis in analyses:
                    if analysis.primary_affiliations and analysis.primary_affiliations != "未知机构":
                        institutions = [inst.strip() for inst in analysis.primary_affiliations.split(';')]
                        for inst in institutions:
                            if inst:
                                institution_counts[inst] = institution_counts.get(inst, 0) + 1
                
                # 显示论文数量>=2的机构
                for inst, count in sorted(institution_counts.items(), key=lambda x: x[1], reverse=True):
                    if count >= 2:
                        writer.writerow([inst, count])
            
            logger.info(f"详细统计摘要文件已生成: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"导出统计摘要失败: {str(e)}")
            raise
    
    def export_high_novelty_papers(self, analyses: List[EnhancedPaperAnalysis], 
                                   output_dir: str = "output", min_score: int = 4) -> str:
        """
        导出高创新性论文到单独的CSV文件
        
        Args:
            analyses: EnhancedPaperAnalysis对象列表
            output_dir: 输出目录
            min_score: 最小创新性评分阈值
            
        Returns:
            生成的高创新性论文文件路径
        """
        high_novelty_papers = [a for a in analyses if a.novelty_score >= min_score]
        
        if not high_novelty_papers:
            logger.info(f"没有找到创新性评分>={min_score}的论文")
            return None
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"high_novelty_papers_{timestamp}.csv"
        filepath = os.path.join(output_dir, filename)
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # 写入表头
                writer.writerow(self.csv_headers)
                
                # 按创新性评分排序
                high_novelty_papers.sort(key=lambda x: x.novelty_score, reverse=True)
                
                # 写入数据
                for analysis in high_novelty_papers:
                    row = [
                        analysis.title,
                        analysis.authors,
                        analysis.authors_with_affiliations,
                        analysis.primary_affiliations,
                        analysis.task_category,
                        analysis.research_field,
                        analysis.methods,
                        analysis.contributions,
                        analysis.training_dataset,
                        analysis.testing_dataset,
                        analysis.evaluation_metrics,
                        analysis.publication_date,
                        analysis.arxiv_url,
                        analysis.arxiv_categories,
                        analysis.confidence,
                        analysis.novelty_score
                    ]
                    writer.writerow(row)
            
            logger.info(f"高创新性论文文件已生成: {filepath}")
            logger.info(f"共导出 {len(high_novelty_papers)} 篇高创新性论文")
            
            return filepath
            
        except Exception as e:
            logger.error(f"导出高创新性论文文件失败: {str(e)}")
            raise
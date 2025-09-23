"""
增强版论文分析器：支持自定义任务分类和更详细的分析
"""

import json
import re
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
from loguru import logger
from llm import get_llm
from enhanced_config import ENHANCED_EXTRACTION_PROMPT_TEMPLATE, format_enhanced_classification_table
from user_config import UserConfig, get_effective_task_categories


@dataclass
class EnhancedPaperAnalysis:
    """增强版论文分析结果数据类"""
    title: str
    authors: str
    authors_with_affiliations: str
    primary_affiliations: str
    task_category: str
    methods: str
    contributions: str
    training_dataset: str
    testing_dataset: str
    evaluation_metrics: str
    publication_date: str
    arxiv_url: str
    confidence: float
    research_field: str
    novelty_score: int
    arxiv_categories: str


class EnhancedPaperAnalyzer:
    """增强版论文分析器类"""
    
    def __init__(self, config: UserConfig):
        self.config = config
        self.task_categories = get_effective_task_categories(config)
        self.classification_table = format_enhanced_classification_table(
            self.task_categories if not config.use_default_categories else config.custom_task_categories
        )
    
    def analyze_paper(self, paper) -> Optional[EnhancedPaperAnalysis]:
        """
        分析单篇论文，提取结构化信息
        
        Args:
            paper: EnhancedArxivPaper对象
            
        Returns:
            EnhancedPaperAnalysis对象或None（如果分析失败）
        """
        try:
            # 构建提示词
            prompt = ENHANCED_EXTRACTION_PROMPT_TEMPLATE.format(
                title=paper.title,
                abstract=paper.summary,
                authors=paper.authors_with_affiliations,
                classification_table=self.classification_table
            )
            
            # 调用LLM进行分析
            llm = get_llm()
            response = llm.generate([
                {
                    "role": "system",
                    "content": "你是一个专业的学术论文分析专家。请仔细分析论文内容，准确提取所需信息，并严格按照JSON格式输出结果。所有回复必须使用中文。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ])
            
            # 解析LLM响应
            analysis_data = self._parse_llm_response(response)
            if not analysis_data:
                logger.warning(f"无法解析LLM响应，论文: {paper.title}")
                return None
            
            # 构建分析结果
            return EnhancedPaperAnalysis(
                title=paper.title,
                authors="; ".join(paper.authors),
                authors_with_affiliations=paper.authors_with_affiliations,
                primary_affiliations=paper.primary_affiliations,
                task_category=analysis_data.get("task_category", "未分类"),
                methods=analysis_data.get("methods", "未明确说明"),
                contributions=analysis_data.get("contributions", "未明确说明"),
                training_dataset=analysis_data.get("training_dataset", "未明确说明"),
                testing_dataset=analysis_data.get("testing_dataset", "未明确说明"),
                evaluation_metrics=analysis_data.get("evaluation_metrics", "未明确说明"),
                publication_date=self._format_date(paper._paper.published),
                arxiv_url=paper._paper.entry_id,
                confidence=float(analysis_data.get("confidence", 0.0)),
                research_field=analysis_data.get("research_field", "未明确说明"),
                novelty_score=int(analysis_data.get("novelty_score", 3)),
                arxiv_categories="; ".join(paper.categories)
            )
            
        except Exception as e:
            logger.error(f"分析论文时出错 '{paper.title}': {str(e)}")
            return None
    
    def _parse_llm_response(self, response: str) -> Optional[Dict]:
        """
        解析LLM的JSON响应
        
        Args:
            response: LLM的原始响应文本
            
        Returns:
            解析后的字典或None
        """
        try:
            # 尝试直接解析JSON
            return json.loads(response)
        except json.JSONDecodeError:
            # 如果直接解析失败，尝试提取JSON部分
            try:
                # 查找JSON代码块
                json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group(1))
                
                # 查找花括号包围的内容
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group(0))
                
                logger.warning(f"无法从响应中提取JSON: {response[:200]}...")
                return None
                
            except json.JSONDecodeError as e:
                logger.warning(f"解析提取的JSON失败: {str(e)}")
                return None
    
    def _format_date(self, date_obj) -> str:
        """
        格式化日期
        
        Args:
            date_obj: datetime对象
            
        Returns:
            格式化的日期字符串
        """
        if isinstance(date_obj, datetime):
            return date_obj.strftime("%Y-%m-%d")
        return str(date_obj)
    
    def analyze_papers_batch(self, papers: List) -> List[EnhancedPaperAnalysis]:
        """
        批量分析论文
        
        Args:
            papers: EnhancedArxivPaper对象列表
            
        Returns:
            EnhancedPaperAnalysis对象列表
        """
        results = []
        total = len(papers)
        
        logger.info(f"开始分析 {total} 篇论文...")
        
        for i, paper in enumerate(papers, 1):
            logger.info(f"正在分析第 {i}/{total} 篇论文: {paper.title[:50]}...")
            
            analysis = self.analyze_paper(paper)
            if analysis:
                results.append(analysis)
                logger.info(f"分析完成，分类为: {analysis.task_category}")
            else:
                logger.warning(f"论文分析失败: {paper.title}")
        
        logger.info(f"批量分析完成，成功分析 {len(results)}/{total} 篇论文")
        return results
    
    def get_category_statistics(self, analyses: List[EnhancedPaperAnalysis]) -> Dict[str, int]:
        """获取任务分类统计"""
        stats = {}
        for analysis in analyses:
            category = analysis.task_category
            stats[category] = stats.get(category, 0) + 1
        return stats
    
    def get_research_field_statistics(self, analyses: List[EnhancedPaperAnalysis]) -> Dict[str, int]:
        """获取研究领域统计"""
        stats = {}
        for analysis in analyses:
            field = analysis.research_field
            stats[field] = stats.get(field, 0) + 1
        return stats
    
    def get_novelty_statistics(self, analyses: List[EnhancedPaperAnalysis]) -> Dict[str, float]:
        """获取创新性统计"""
        if not analyses:
            return {}
        
        novelty_scores = [analysis.novelty_score for analysis in analyses]
        return {
            "平均创新性评分": sum(novelty_scores) / len(novelty_scores),
            "最高创新性评分": max(novelty_scores),
            "最低创新性评分": min(novelty_scores),
            "高创新性论文数量(评分>=4)": sum(1 for score in novelty_scores if score >= 4)
        }
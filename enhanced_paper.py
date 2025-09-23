"""
增强版论文类，包含作者信息和学校信息
"""

from typing import Optional, List, Dict
import arxiv
import re
from loguru import logger


class EnhancedArxivPaper:
    """增强版arXiv论文类，包含作者和机构信息"""
    
    def __init__(self, paper: arxiv.Result):
        self._paper = paper
        self.score = None
        self._author_affiliations = self._extract_author_affiliations()
    
    @property
    def title(self) -> str:
        """论文标题"""
        return self._paper.title
    
    @property
    def summary(self) -> str:
        """论文摘要"""
        return self._paper.summary
    
    @property
    def authors(self) -> List[str]:
        """作者列表"""
        return [str(author) for author in self._paper.authors]
    
    @property
    def authors_with_affiliations(self) -> str:
        """带机构信息的作者列表（格式化字符串）"""
        if not self._author_affiliations:
            return "; ".join(self.authors)
        
        formatted_authors = []
        for author_info in self._author_affiliations:
            author_str = author_info['name']
            if author_info['affiliation']:
                author_str += f" ({author_info['affiliation']})"
            formatted_authors.append(author_str)
        
        return "; ".join(formatted_authors)
    
    @property
    def primary_affiliations(self) -> str:
        """主要机构列表"""
        if not self._author_affiliations:
            return "未知机构"
        
        affiliations = set()
        for author_info in self._author_affiliations:
            if author_info['affiliation']:
                affiliations.add(author_info['affiliation'])
        
        return "; ".join(sorted(affiliations)) if affiliations else "未知机构"
    
    @property
    def arxiv_id(self) -> str:
        """arXiv ID"""
        return re.sub(r'v\d+$', '', self._paper.get_short_id())
    
    @property
    def pdf_url(self) -> str:
        """PDF链接"""
        return self._paper.pdf_url
    
    @property
    def published_date(self) -> str:
        """发表日期"""
        return self._paper.published.strftime("%Y-%m-%d")
    
    @property
    def entry_id(self) -> str:
        """arXiv条目ID"""
        return self._paper.entry_id
    
    @property
    def categories(self) -> List[str]:
        """论文分类"""
        return self._paper.categories
    
    @property
    def primary_category(self) -> str:
        """主要分类"""
        return self._paper.primary_category
    
    def is_cs_related(self) -> bool:
        """判断是否为计算机科学相关论文"""
        cs_keywords = [
            'computer', 'computing', 'algorithm', 'machine learning', 'deep learning',
            'neural network', 'artificial intelligence', 'robotics', 'computer vision',
            'natural language processing', 'data mining', 'software', 'programming',
            'database', 'network', 'security', 'optimization', 'simulation'
        ]
        
        # 检查分类
        if any(cat.startswith('cs.') for cat in self.categories):
            return True
        
        # 检查标题和摘要中的关键词
        text = (self.title + " " + self.summary).lower()
        return any(keyword in text for keyword in cs_keywords)
    
    def _extract_author_affiliations(self) -> List[Dict[str, str]]:
        """
        从论文信息中提取作者和机构信息
        注意：arXiv API通常不提供详细的机构信息，这里主要是为了扩展性
        """
        author_info = []
        
        for author in self._paper.authors:
            # arXiv API的作者对象通常只有姓名，没有机构信息
            # 这里为未来可能的API升级或其他数据源预留接口
            author_data = {
                'name': str(author),
                'affiliation': self._guess_affiliation_from_name(str(author))
            }
            author_info.append(author_data)
        
        return author_info
    
    def _guess_affiliation_from_name(self, author_name: str) -> Optional[str]:
        """
        尝试从作者姓名推测机构（这是一个简化的实现）
        在实际应用中，可能需要连接其他数据库或使用更复杂的方法
        """
        # 这里可以实现更复杂的机构识别逻辑
        # 例如：连接学者数据库、使用NLP技术等
        
        # 目前返回None，表示无法确定机构
        return None
    
    def __str__(self) -> str:
        return f"EnhancedArxivPaper(id={self.arxiv_id}, title={self.title[:50]}...)"
    
    def __repr__(self) -> str:
        return self.__str__()
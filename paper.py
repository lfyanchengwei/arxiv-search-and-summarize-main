"""
简化的论文类，只保留基本信息
"""

from typing import Optional
import arxiv
import re
from loguru import logger


class ArxivPaper:
    """arXiv论文类"""
    
    def __init__(self, paper: arxiv.Result):
        self._paper = paper
        self.score = None
    
    @property
    def title(self) -> str:
        """论文标题"""
        return self._paper.title
    
    @property
    def summary(self) -> str:
        """论文摘要"""
        return self._paper.summary
    
    @property
    def authors(self) -> list[str]:
        """作者列表"""
        return [str(author) for author in self._paper.authors]
    
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
    
    def __str__(self) -> str:
        return f"ArxivPaper(id={self.arxiv_id}, title={self.title[:50]}...)"
    
    def __repr__(self) -> str:
        return self.__str__()
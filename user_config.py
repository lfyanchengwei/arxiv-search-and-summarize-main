"""
用户配置管理模块
"""

import json
import os
from dataclasses import dataclass, asdict
from typing import List, Dict, Any
from datetime import datetime, timedelta
from loguru import logger


@dataclass
class UserConfig:
    """用户配置数据类"""
    
    CONFIG_FILE = "user_config.json"
    
    # 检索配置
    search_keywords: List[str]
    research_categories: List[str]
    start_date: str
    end_date: str
    max_papers: int
    
    # 任务分类配置
    custom_task_categories: Dict[str, Dict[str, str]]
    use_default_categories: bool
    
    # 输出配置
    include_author_affiliations: bool
    output_format: str
    
    @classmethod
    def create_default(cls) -> 'UserConfig':
        """创建默认配置"""
        # 默认时间范围：过去一年
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        return cls(
            search_keywords=["embodied", "multimodal", "robotics"],
            research_categories=["cs.AI", "cs.CV", "cs.RO", "cs.LG"],
            start_date=start_date.strftime("%Y-%m-%d"),
            end_date=end_date.strftime("%Y-%m-%d"),
            max_papers=50,
            custom_task_categories={},
            use_default_categories=True,
            include_author_affiliations=True,
            output_format="csv"
        )


def load_user_config() -> UserConfig:
    """加载用户配置"""
    if os.path.exists(UserConfig.CONFIG_FILE):
        try:
            with open(UserConfig.CONFIG_FILE, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            # 验证配置数据完整性
            default_config = UserConfig.create_default()
            for key in asdict(default_config).keys():
                if key not in config_data:
                    config_data[key] = getattr(default_config, key)
            
            return UserConfig(**config_data)
            
        except Exception as e:
            logger.warning(f"加载配置文件失败: {str(e)}，使用默认配置")
            return UserConfig.create_default()
    else:
        logger.info("配置文件不存在，使用默认配置")
        return UserConfig.create_default()


def save_user_config(config: UserConfig) -> None:
    """保存用户配置"""
    try:
        with open(UserConfig.CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(asdict(config), f, ensure_ascii=False, indent=2)
        logger.info(f"配置已保存到 {UserConfig.CONFIG_FILE}")
    except Exception as e:
        logger.error(f"保存配置文件失败: {str(e)}")


def validate_config(config: UserConfig) -> bool:
    """验证配置有效性"""
    try:
        # 验证日期格式
        datetime.strptime(config.start_date, "%Y-%m-%d")
        datetime.strptime(config.end_date, "%Y-%m-%d")
        
        # 验证其他必要字段
        if not config.search_keywords:
            logger.warning("检索词不能为空")
            return False
        
        if config.max_papers <= 0:
            logger.warning("最大论文数量必须大于0")
            return False
        
        return True
        
    except ValueError as e:
        logger.error(f"配置验证失败: {str(e)}")
        return False


def get_effective_task_categories(config: UserConfig) -> Dict[str, Dict[str, str]]:
    """获取有效的任务分类（默认+自定义）"""
    from enhanced_config import ENHANCED_TASK_CATEGORIES
    
    if config.use_default_categories:
        # 合并默认分类和自定义分类
        effective_categories = ENHANCED_TASK_CATEGORIES.copy()
        effective_categories.update(config.custom_task_categories)
        return effective_categories
    else:
        # 只使用自定义分类
        return config.custom_task_categories
from openai import OpenAI
from loguru import logger
from time import sleep

GLOBAL_LLM = None

class LLM:
    def __init__(self, api_key: str, base_url: str = None, model: str = "gpt-4o", lang: str = "Chinese"):
        """
        初始化LLM客户端，只支持OpenAI API格式
        
        Args:
            api_key: OpenAI API密钥
            base_url: API基础URL，默认为OpenAI官方
            model: 模型名称，默认gpt-4o
            lang: 语言设置，默认中文
        """
        if not api_key:
            raise ValueError("API密钥不能为空")
            
        self.llm = OpenAI(
            api_key=api_key, 
            base_url=base_url or "https://api.openai.com/v1"
        )
        self.model = model
        self.lang = lang

    def generate(self, messages: list[dict]) -> str:
        """
        生成回复
        
        Args:
            messages: 对话消息列表
            
        Returns:
            生成的回复文本
        """
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.llm.chat.completions.create(
                    messages=messages, 
                    temperature=0, 
                    model=self.model
                )
                return response.choices[0].message.content
            except Exception as e:
                logger.error(f"API调用失败 (尝试 {attempt + 1}/{max_retries}): {e}")
                if attempt == max_retries - 1:
                    raise
                sleep(3)

def set_global_llm(api_key: str, base_url: str = None, model: str = "gpt-4o", lang: str = "Chinese"):
    """
    设置全局LLM实例
    
    Args:
        api_key: OpenAI API密钥
        base_url: API基础URL
        model: 模型名称
        lang: 语言设置
    """
    global GLOBAL_LLM
    GLOBAL_LLM = LLM(api_key=api_key, base_url=base_url, model=model, lang=lang)

def get_llm() -> LLM:
    """
    获取全局LLM实例
    
    Returns:
        LLM实例
    """
    if GLOBAL_LLM is None:
        raise RuntimeError("请先使用 set_global_llm() 设置API密钥")
    return GLOBAL_LLM
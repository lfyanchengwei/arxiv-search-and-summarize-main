"""
增强版配置文件：包含扩展的任务分类表和提示词模板
"""

# 增强版任务分类表（基于原有分类，增加更多类别）
ENHANCED_TASK_CATEGORIES = {
    "动作识别": {
        "definition": "识别视频或传感器数据中的预定义动作或活动",
        "typical_output": "分类标签（如\"行走\"、\"挥手\"）",
        "datasets_metrics": "UCF101, HMDB51, 准确率 (Accuracy)"
    },
    "手物交互检测 (HOI)": {
        "definition": "检测图像中的人体、物体，并识别其间的交互关系（动词）",
        "typical_output": "<人, 动词, 物体> 三元组",
        "datasets_metrics": "HICO-DET, V-COCO, mAP"
    },
    "主动物体检测": {
        "definition": "在交互场景中主动检测可能发生交互的物体（或\"热点\"区域）",
        "typical_output": "交互物体的边界框或热点图",
        "datasets_metrics": "Epic-Kitchens, EGTEA Gaze+"
    },
    "跨具身模仿学习": {
        "definition": "将人类动作（如从视频中提取的手部姿态）转化为机器人可执行策略，涉及视觉-动作映射、运动重定向和少样本泛化。核心是学习跨形态（如人→人形机器人）的模仿能力，允许机器人通过少量演示适应新任务，无需重新训练。",
        "typical_output": "- **机器人动作序列**：包括关节角度、手腕位姿和抓取信号（如论文中的 at）。\n- **任务执行轨迹**：在测试时生成与人类演示相似的动态行为序列（如抓取→移动→放置物体），输出格式为时间步长的动作向量（如32步预测序列）。",
        "datasets_metrics": "**Real-world GR1 Demonstra**评估指标**：\n任务成功率，轨迹相似度，泛化性能"
    },
    "情景记忆": {
        "definition": "利用情景记忆优化提示中的示例顺序，提升模型在少样本学习场景下的性能",
        "typical_output": "为测试查询选择能产生最高奖励的示例序列",
        "datasets_metrics": ""
    },
    "自然语言查询 (NLQ)": {
        "definition": "根据自然语言问题在视频中定位特定时刻或区域（第一视角）",
        "typical_output": "时间戳或时空边界框",
        "datasets_metrics": "Ego4D-NLQ"
    },
    "VQ2D/VQ3D": {
        "definition": "Visual Query 2D/3D：在（多视角）视频中根据查询（如物体外观）进行检索、定位与跟踪",
        "typical_output": "2D或3D空间中的物体轨迹或姿态",
        "datasets_metrics": "EmbodiedScan"
    },
    "具身3D视觉 grounding": {
        "definition": "从第一人称视角根据自然语言指令在3D环境中定位目标物体",
        "typical_output": "9自由度（9DoF）的3D边界框，包括物体中心坐标（x, y, z）、尺寸（长l、宽w、高h）和方向角（α, β, γ）",
        "datasets_metrics": ""
    },
    "具身问答（EQA）": {
        "definition": "智能体在环境中通过探索（如导航、交互）来回答关于环境的问题",
        "typical_output": "对自然语言问题的答案",
        "datasets_metrics": ""
    },
    "导航": {
        "definition": "在具身环境中，基于自然语言指令规划并执行从起点到目标点的路径，涉及逐步决策（如选择下一个导航点或动作）、处理空间/认知/执行复杂性，并在零样本设置下评估模型对全局意图的理解、临时进度跟踪和局部动作推理能力。",
        "typical_output": "一系列导航动作（如前进、左转、停止）或路径点序列",
        "datasets_metrics": "Room-to-Room (R2R)、RxR、GEL-R2R、FGR2R**Success Rate (SR)**、**Success weighted by Path Length (SPL)**"
    },
    "任务进度估计": {
        "definition": "预测视频中每一帧的任务完成百分比，提供任务进展的实时量化评估",
        "typical_output": "0-100%的进度值（如\"开门进度30%\"）",
        "datasets_metrics": "RoboCasa, OpenX Embodiment；Pearson相关系数、L2距离"
    },
    "视频问答（VQA）": {
        "definition": "根据整个视频内容回答自然语言问题，特别是关于事件发生与否及发生时间",
        "typical_output": "问题答案（如\"是，在第120帧\"）",
        "datasets_metrics": "RoboCasa, OpenX Embodiment；准确率、精确率、召回率、时间定位误差（帧差）"
    },
    "自然语言状态推理": {
        "definition": "为视频的每一帧生成描述当前状态的自然语言文本，并验证其与真实状态的一致性",
        "typical_output": "自然语言描述（如\"机械爪接触门把手\"）",
        "datasets_metrics": "RoboCasa, OpenX Embodiment；错误率、正确率"
    },
    "行为预估": {
        "definition": "预测智能体（如人、车）未来的行为或运动轨迹",
        "typical_output": "未来一段时间内的轨迹点或行为分类（如\"将左转\"）",
        "datasets_metrics": "用户行为数据集，准确率"
    },
    "下一活动物体检测": {
        "definition": "预测下一步最可能与之交互的物体",
        "typical_output": "候选物体的边界框或概率评分",
        "datasets_metrics": "Epic-Kitchens, EGTEA Gaze+"
    },
    "交互预测": {
        "definition": "预测未来可能发生的交互动作或交互类型",
        "typical_output": "交互动词（如\"抓取\"、\"打开\"）",
        "datasets_metrics": "Epic-Kitchens, EGTEA Gaze+"
    },
    "第一视角人体姿态估计": {
        "definition": "从第一人称视角（如头盔相机）估计人体各关节点的2D或3D位置",
        "typical_output": "2D或3D关节点坐标",
        "datasets_metrics": "Human3.6M, MPI-INF-3DHP, MPJPE"
    },
    "文本驱动的交互生成": {
        "definition": "根据文本描述生成与之匹配的人体动作或交互序列",
        "typical_output": "生成的动作序列（如视频、3D姿态序列）",
        "datasets_metrics": "分类要求与示例"
    },
    # 新增任务类别
    "多模态学习": {
        "definition": "结合多种模态（如视觉、语言、音频）进行联合学习和推理",
        "typical_output": "跨模态表示、多模态预测结果",
        "datasets_metrics": "CLIP, ALIGN, 跨模态检索准确率"
    },
    "强化学习": {
        "definition": "通过与环境交互学习最优策略的机器学习方法",
        "typical_output": "策略函数、动作序列、奖励值",
        "datasets_metrics": "累积奖励、成功率、收敛速度"
    },
    "大语言模型应用": {
        "definition": "将大型语言模型应用于特定任务或领域的研究",
        "typical_output": "文本生成、任务完成结果",
        "datasets_metrics": "BLEU, ROUGE, 人工评估"
    },
    "计算机视觉基础": {
        "definition": "图像分类、目标检测、语义分割等基础计算机视觉任务",
        "typical_output": "分类标签、边界框、分割掩码",
        "datasets_metrics": "ImageNet, COCO, mAP, IoU"
    },
    "自然语言处理": {
        "definition": "文本理解、生成、翻译等自然语言处理任务",
        "typical_output": "文本分类、生成文本、翻译结果",
        "datasets_metrics": "GLUE, SuperGLUE, BLEU"
    }
}

# 预设配置
PRESET_CONFIGS = {
    "embodied_ai": {
        "name": "具身智能研究",
        "description": "专注于具身AI、机器人学和人机交互研究，使用原始详细任务分类",
        "keywords": ["embodied", "robotics", "manipulation", "navigation", "embodied AI", "robot learning", "imitation learning", "HOI", "egocentric"],
        "categories": ["cs.AI", "cs.RO", "cs.CV", "cs.LG"],
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "max_papers": 50,
        "use_embodied_tasks": True  # 使用原始具身智能任务分类
    },
    "multimodal_learning": {
        "name": "多模态学习",
        "description": "跨模态学习、视觉语言模型、多模态融合研究",
        "keywords": ["multimodal", "vision-language", "CLIP", "cross-modal", "VLM", "vision transformer"],
        "categories": ["cs.CV", "cs.CL", "cs.LG", "cs.AI"],
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "max_papers": 50,
        "custom_tasks": {
            "视觉语言预训练": {
                "definition": "大规模视觉-语言联合预训练模型",
                "typical_output": "跨模态表示、图文匹配分数",
                "datasets_metrics": "CLIP, ALIGN, 零样本分类准确率"
            },
            "跨模态检索": {
                "definition": "图像-文本相互检索和匹配",
                "typical_output": "检索排序、相似度分数",
                "datasets_metrics": "Flickr30K, MS-COCO, Recall@K"
            },
            "多模态对话": {
                "definition": "结合视觉信息的对话系统",
                "typical_output": "对话回复、视觉问答",
                "datasets_metrics": "VQA, BLEU, CIDEr"
            }
        }
    },
    "large_language_models": {
        "name": "大语言模型",
        "description": "大型语言模型、指令微调、推理能力研究",
        "keywords": ["LLM", "transformer", "GPT", "language model", "instruction tuning", "reasoning", "alignment"],
        "categories": ["cs.CL", "cs.AI", "cs.LG"],
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "max_papers": 50,
        "custom_tasks": {
            "指令微调": {
                "definition": "基于人类反馈的模型对齐和指令跟随",
                "typical_output": "指令跟随回复、对齐评分",
                "datasets_metrics": "Alpaca, Vicuna, 人工评估"
            },
            "思维链推理": {
                "definition": "逐步推理和复杂问题解决",
                "typical_output": "推理步骤、最终答案",
                "datasets_metrics": "GSM8K, MATH, 推理准确率"
            },
            "代码生成": {
                "definition": "自然语言到代码的生成和理解",
                "typical_output": "可执行代码、代码解释",
                "datasets_metrics": "HumanEval, MBPP, Pass@K"
            }
        }
    },
    "computer_vision": {
        "name": "计算机视觉",
        "description": "图像识别、目标检测、图像生成等计算机视觉研究",
        "keywords": ["computer vision", "object detection", "segmentation", "recognition", "image generation", "diffusion"],
        "categories": ["cs.CV", "cs.AI", "cs.LG"],
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "max_papers": 50,
        "custom_tasks": {
            "目标检测": {
                "definition": "图像中物体的定位和识别",
                "typical_output": "边界框、类别标签、置信度",
                "datasets_metrics": "COCO, Pascal VOC, mAP"
            },
            "语义分割": {
                "definition": "像素级的场景理解和分割",
                "typical_output": "分割掩码、像素标签",
                "datasets_metrics": "Cityscapes, ADE20K, mIoU"
            },
            "图像生成": {
                "definition": "基于条件的图像合成和生成",
                "typical_output": "生成图像、编辑结果",
                "datasets_metrics": "FID, IS, LPIPS"
            }
        }
    },
    "reinforcement_learning": {
        "name": "强化学习",
        "description": "强化学习算法、多智能体系统、策略优化研究",
        "keywords": ["reinforcement learning", "RL", "policy", "reward", "agent", "MARL", "offline RL"],
        "categories": ["cs.LG", "cs.AI", "cs.RO", "cs.MA"],
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "max_papers": 50,
        "custom_tasks": {
            "离线强化学习": {
                "definition": "从历史数据学习策略，无需在线交互",
                "typical_output": "离线策略、价值函数",
                "datasets_metrics": "D4RL, 归一化分数"
            },
            "多智能体强化学习": {
                "definition": "多个智能体协作或竞争学习",
                "typical_output": "多智能体策略、协调机制",
                "datasets_metrics": "SMAC, MPE, 胜率"
            },
            "层次化强化学习": {
                "definition": "分层决策和技能学习",
                "typical_output": "层次策略、子目标",
                "datasets_metrics": "成功率、样本效率"
            }
        }
    },
    "recent_trends": {
        "name": "最新趋势",
        "description": "AI领域最新发展趋势和前沿技术",
        "keywords": ["AI", "machine learning", "deep learning", "neural network", "foundation model", "AGI"],
        "categories": ["cs.AI", "cs.LG", "cs.CV", "cs.CL"],
        "start_date": "2024-01-01",
        "end_date": "2024-12-31",
        "max_papers": 50,
        "custom_tasks": {
            "基础模型": {
                "definition": "大规模预训练基础模型研究",
                "typical_output": "预训练模型、下游任务性能",
                "datasets_metrics": "多任务评估、零样本性能"
            },
            "AI安全": {
                "definition": "人工智能的安全性和可靠性研究",
                "typical_output": "安全评估、对抗样本检测",
                "datasets_metrics": "鲁棒性指标、安全评分"
            },
            "联邦学习": {
                "definition": "分布式隐私保护学习",
                "typical_output": "联邦模型、隐私保护机制",
                "datasets_metrics": "通信效率、隐私预算"
            }
        }
    }
}

# arXiv分类映射
ARXIV_CATEGORIES = {
    # 计算机科学
    "cs.AI": "人工智能",
    "cs.CV": "计算机视觉与模式识别", 
    "cs.CL": "计算与语言",
    "cs.LG": "机器学习",
    "cs.RO": "机器人学",
    "cs.HC": "人机交互",
    "cs.MA": "多智能体系统",
    "cs.NE": "神经与进化计算",
    "cs.IR": "信息检索",
    "cs.MM": "多媒体",
    
    # 数学
    "math.ST": "统计理论",
    "math.OC": "优化与控制",
    "math.PR": "概率论",
    
    # 统计学
    "stat.ML": "机器学习统计",
    "stat.AP": "应用统计",
    
    # 物理学
    "physics.data-an": "数据分析统计与概率",
    "physics.comp-ph": "计算物理",
    
    # 定量生物学
    "q-bio.QM": "定量方法",
    "q-bio.NC": "神经元与认知",
    
    # 电气工程
    "eess.IV": "图像与视频处理",
    "eess.AS": "音频与语音处理",
    "eess.SP": "信号处理"
}

# 增强版信息提取提示词模板
ENHANCED_EXTRACTION_PROMPT_TEMPLATE = """你是一个专业的学术论文分析专家。请仔细分析以下论文并提取结构化信息。

论文标题：{title}
论文摘要：{abstract}
作者信息：{authors}

请按照以下JSON格式输出分析结果：
{{
  "task_category": "从给定分类表中选择最匹配的类别，如无法匹配则返回'未分类'",
  "methods": "论文使用的主要方法和技术（简洁描述，不超过200字）",
  "contributions": "论文的主要贡献和创新点（简洁描述，不超过200字）",
  "training_dataset": "训练使用的数据集名称（如果有多个，用逗号分隔）",
  "testing_dataset": "测试/评估使用的数据集名称（如果有多个，用逗号分隔）",
  "evaluation_metrics": "使用的评估指标（如果有多个，用逗号分隔）",
  "confidence": "分类置信度，范围0-1，表示对任务分类的确信程度",
  "research_field": "研究领域（如机器学习、计算机视觉、自然语言处理等）",
  "novelty_score": "创新性评分，范围1-5，5表示非常创新"
}}

任务分类表：
{classification_table}

分析要求：
1. 如果论文涉及多个任务类别，选择最主要的一个
2. 如果无法确定具体的数据集或指标，可以填写"未明确说明"
3. 置信度应该基于论文内容与分类表的匹配程度来判断
4. 创新性评分应考虑方法的新颖性、问题的重要性和解决方案的有效性
5. 请确保输出是有效的JSON格式
6. 所有回复必须使用中文
"""

# 分类表格式化函数
def format_enhanced_classification_table(custom_categories=None):
    """将增强版分类表格式化为字符串"""
    categories = ENHANCED_TASK_CATEGORIES.copy()
    
    # 添加自定义分类
    if custom_categories:
        categories.update(custom_categories)
    
    formatted = ""
    for category, info in categories.items():
        formatted += f"- {category}: {info['definition']}\n"
    return formatted

def get_preset_config(preset_name):
    """获取预设配置"""
    return PRESET_CONFIGS.get(preset_name, None)

def list_preset_configs():
    """列出所有预设配置"""
    return [(key, config["name"], config["description"]) for key, config in PRESET_CONFIGS.items()]
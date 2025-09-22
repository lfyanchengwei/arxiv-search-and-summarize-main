"""
配置文件：包含任务分类表和提示词模板
"""

# 任务分类表
TASK_CATEGORIES = {
    "动作识别": {
        "definition": "识别视频或传感器数据中的预定义动作或活动",
        "typical_output": "分类标签（如"行走"、"挥手"）",
        "datasets_metrics": "UCF101, HMDB51, 准确率 (Accuracy)"
    },
    "手物交互检测 (HOI)": {
        "definition": "检测图像中的人体、物体，并识别其间的交互关系（动词）",
        "typical_output": "<人, 动词, 物体> 三元组",
        "datasets_metrics": "HICO-DET, V-COCO, mAP"
    },
    "主动物体检测": {
        "definition": "在交互场景中主动检测可能发生交互的物体（或"热点"区域）",
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
        "typical_output": "0-100%的进度值（如"开门进度30%"）",
        "datasets_metrics": "RoboCasa, OpenX Embodiment；Pearson相关系数、L2距离"
    },
    "视频问答（VQA）": {
        "definition": "根据整个视频内容回答自然语言问题，特别是关于事件发生与否及发生时间",
        "typical_output": "问题答案（如"是，在第120帧"）",
        "datasets_metrics": "RoboCasa, OpenX Embodiment；准确率、精确率、召回率、时间定位误差（帧差）"
    },
    "自然语言状态推理": {
        "definition": "为视频的每一帧生成描述当前状态的自然语言文本，并验证其与真实状态的一致性",
        "typical_output": "自然语言描述（如"机械爪接触门把手"）",
        "datasets_metrics": "RoboCasa, OpenX Embodiment；错误率、正确率"
    },
    "行为预估": {
        "definition": "预测智能体（如人、车）未来的行为或运动轨迹",
        "typical_output": "未来一段时间内的轨迹点或行为分类（如"将左转"）",
        "datasets_metrics": "用户行为数据集，准确率"
    },
    "下一活动物体检测": {
        "definition": "预测下一步最可能与之交互的物体",
        "typical_output": "候选物体的边界框或概率评分",
        "datasets_metrics": "Epic-Kitchens, EGTEA Gaze+"
    },
    "交互预测": {
        "definition": "预测未来可能发生的交互动作或交互类型",
        "typical_output": "交互动词（如"抓取"、"打开"）",
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
    }
}

# 信息提取提示词模板
EXTRACTION_PROMPT_TEMPLATE = """你是一个学术论文分析专家。请仔细分析以下论文并提取结构化信息。

论文标题：{title}
论文摘要：{abstract}

请按照以下JSON格式输出分析结果：
{{
  "task_category": "从给定分类表中选择最匹配的类别，如无法匹配则返回'未分类'",
  "methods": "论文使用的主要方法和技术（简洁描述，不超过200字）",
  "contributions": "论文的主要贡献和创新点（简洁描述，不超过200字）",
  "training_dataset": "训练使用的数据集名称（如果有多个，用逗号分隔）",
  "testing_dataset": "测试/评估使用的数据集名称（如果有多个，用逗号分隔）",
  "evaluation_metrics": "使用的评估指标（如果有多个，用逗号分隔）",
  "confidence": "分类置信度，范围0-1，表示对任务分类的确信程度"
}}

任务分类表：
{classification_table}

注意事项：
1. 如果论文涉及多个任务类别，选择最主要的一个
2. 如果无法确定具体的数据集或指标，可以填写"未明确说明"
3. 置信度应该基于论文内容与分类表的匹配程度来判断
4. 请确保输出是有效的JSON格式
"""

# 分类表格式化函数
def format_classification_table():
    """将分类表格式化为字符串"""
    formatted = ""
    for category, info in TASK_CATEGORIES.items():
        formatted += f"- {category}: {info['definition']}\n"
    return formatted
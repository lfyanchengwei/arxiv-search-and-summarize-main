# 增强版学术论文分析系统

这是一个功能强大的学术论文分析系统，支持用户自定义检索词、时间区间、研究领域和任务分类。系统能够从arXiv搜索论文并进行智能分析，提取结构化信息。

## 🚀 新增功能

### 1. 作者和机构信息
- ✅ 新增作者列（包括学校/机构信息）
- ✅ 支持作者-机构关联显示
- ✅ 主要机构统计分析

### 2. 用户自定义检索词
- ✅ 支持多个检索词组合搜索
- ✅ 灵活的关键词配置
- ✅ 检索词历史记录

### 3. 研究领域选择
- ✅ 基于arXiv官方分类系统
- ✅ 支持主要领域和子领域选择
- ✅ 计算机科学相关论文过滤

### 4. 自定义任务分类
- ✅ 支持添加自定义任务类别
- ✅ 可选择使用默认分类或完全自定义
- ✅ 任务分类配置持久化

### 5. 时间区间自定义
- ✅ 用户可设置任意时间范围
- ✅ 灵活的日期格式支持
- ✅ 默认过去一年的智能设置

### 6. 增强分析功能
- ✅ 创新性评分（1-5分）
- ✅ 研究领域自动识别
- ✅ 分类置信度评估
- ✅ 高创新性论文单独导出

## 📋 系统要求

- Python 3.8+
- 所需依赖包（见 `pyproject.toml`）
- OpenAI API密钥（如使用API模式）

## 🛠️ 安装和配置

1. **安装依赖**
```bash
pip install -r requirements.txt
# 或使用 uv
uv sync
```

2. **配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，添加你的 OpenAI API 密钥
```

3. **首次运行配置**
```bash
python enhanced_main.py --openai_api_key YOUR_API_KEY
```

## 🎯 使用方法

### 交互式配置模式

运行程序时，系统会引导您完成配置：

```bash
python enhanced_main.py --openai_api_key YOUR_API_KEY
```

系统会依次询问：

1. **检索词配置**
   - 输入感兴趣的关键词（如：embodied,robotics,multimodal）
   - 支持多个关键词用逗号分隔

2. **研究领域选择**
   - 选择arXiv主要领域（如：cs, math, physics）
   - 如选择计算机科学，可进一步选择子领域

3. **时间区间设置**
   - 设置论文发表的时间范围
   - 格式：YYYY-MM-DD

4. **任务分类配置**
   - 选择使用默认分类、添加自定义分类或完全自定义

5. **其他参数**
   - 最大论文数量等

### 命令行参数

```bash
python enhanced_main.py \
  --openai_api_key YOUR_API_KEY \
  --model_name gpt-4o \
  --max_papers 100 \
  --output_dir results \
  --skip_setup  # 跳过交互配置，使用已保存配置
```

### 配置文件

系统会自动保存配置到 `user_config.json`，下次运行时可直接使用：

```json
{
  "search_keywords": ["embodied", "robotics", "multimodal"],
  "research_categories": ["cs.AI", "cs.CV", "cs.RO"],
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "max_papers": 50,
  "custom_task_categories": {},
  "use_default_categories": true
}
```

## 📊 输出文件

系统会生成以下文件：

1. **详细分析结果** (`enhanced_papers_analysis_TIMESTAMP.csv`)
   - 包含所有论文的完整分析信息
   - 作者、机构、任务分类、方法、贡献等

2. **统计摘要** (`enhanced_papers_summary_TIMESTAMP.csv`)
   - 任务类别分布
   - 研究领域分布
   - 创新性统计
   - 主要机构分布

3. **高创新性论文** (`high_novelty_papers_TIMESTAMP.csv`)
   - 创新性评分≥4的论文
   - 按创新性评分排序

## 🔧 arXiv研究领域分类

### 主要领域
- `cs`: 计算机科学
- `math`: 数学
- `physics`: 物理学
- `q-bio`: 定量生物学
- `q-fin`: 定量金融
- `stat`: 统计学
- `eess`: 电气工程与系统科学
- `econ`: 经济学

### 计算机科学子领域
- `cs.AI`: 人工智能
- `cs.CL`: 计算与语言
- `cs.CV`: 计算机视觉与模式识别
- `cs.LG`: 机器学习
- `cs.RO`: 机器人学
- `cs.HC`: 人机交互
- `cs.IR`: 信息检索
- `cs.MM`: 多媒体
- `cs.NE`: 神经与进化计算
- `cs.SI`: 社会与信息网络

## 📈 任务分类系统

系统包含丰富的任务分类，涵盖：

### 具身智能相关
- 动作识别
- 手物交互检测 (HOI)
- 跨具身模仿学习
- 具身问答（EQA）
- 导航
- 第一视角人体姿态估计

### 计算机视觉
- 计算机视觉基础
- VQ2D/VQ3D
- 具身3D视觉 grounding

### 自然语言处理
- 自然语言处理
- 自然语言查询 (NLQ)
- 文本驱动的交互生成

### 机器学习
- 多模态学习
- 强化学习
- 大语言模型应用

## 🎨 使用示例

### 示例1：搜索具身智能相关论文
```python
# 配置示例
search_keywords = ["embodied", "embodied AI", "robotics"]
research_categories = ["cs.AI", "cs.RO", "cs.CV"]
start_date = "2024-01-01"
end_date = "2024-12-31"
```

### 示例2：搜索多模态学习论文
```python
search_keywords = ["multimodal", "vision-language", "CLIP"]
research_categories = ["cs.CV", "cs.CL", "cs.LG"]
start_date = "2023-06-01"
end_date = "2024-06-01"
```

### 示例3：自定义任务分类
```python
custom_task_categories = {
    "医疗AI": {
        "definition": "将AI技术应用于医疗诊断和治疗",
        "typical_output": "诊断结果、治疗建议",
        "datasets_metrics": "医疗数据集、准确率、敏感性"
    }
}
```

## 🔍 高级功能

### 1. 创新性评分
- 系统会为每篇论文评估创新性（1-5分）
- 基于方法新颖性、问题重要性和解决方案有效性

### 2. 机构分析
- 自动提取和统计主要研究机构
- 支持机构合作网络分析

### 3. 研究趋势分析
- 时间序列分析
- 热点话题识别
- 研究领域演进

## 🚨 注意事项

1. **API限制**：请注意OpenAI API的调用限制和费用
2. **数据质量**：arXiv API可能不包含完整的机构信息
3. **分析准确性**：LLM分析结果仅供参考，建议人工验证重要结论
4. **时间范围**：建议设置合理的时间范围以避免检索过多论文

## 🤝 贡献

欢迎提交Issue和Pull Request来改进系统功能！

## 📄 许可证

本项目采用MIT许可证，详见LICENSE文件。
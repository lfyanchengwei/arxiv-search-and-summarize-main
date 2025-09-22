# Embody Papers Analyzer

一个专门用于分析包含"embody"关键词的学术论文的自动化系统。该系统能够从arXiv搜索相关论文，使用LLM进行结构化信息提取和任务分类，并生成CSV格式的分析报告。

## 🎯 功能特性

- **智能搜索**: 自动搜索arXiv中标题或摘要包含"embody"关键词的论文（2024-2025年）
- **结构化分析**: 使用LLM提取论文的关键信息：
  - 任务领域分类（基于预定义分类表）
  - 使用的方法和技术
  - 主要贡献和创新点
  - 训练和测试数据集
  - 评估指标
- **任务分类**: 基于18个具身AI相关任务类别进行自动分类
- **CSV输出**: 生成结构化的CSV报告，便于后续分析
- **GitHub Actions部署**: 支持云端自动化运行

## 📊 支持的任务分类

系统支持以下18个任务类别的自动分类：

1. **动作识别** - 识别视频或传感器数据中的预定义动作或活动
2. **手物交互检测 (HOI)** - 检测图像中的人体、物体，并识别其间的交互关系
3. **主动物体检测** - 在交互场景中主动检测可能发生交互的物体
4. **跨具身模仿学习** - 将人类动作转化为机器人可执行策略
5. **情景记忆** - 利用情景记忆优化提示中的示例顺序
6. **自然语言查询 (NLQ)** - 根据自然语言问题在视频中定位特定时刻
7. **VQ2D/VQ3D** - 在视频中根据查询进行检索、定位与跟踪
8. **具身3D视觉 grounding** - 从第一人称视角在3D环境中定位目标物体
9. **具身问答（EQA）** - 智能体通过探索来回答关于环境的问题
10. **导航** - 基于自然语言指令规划并执行路径
11. **任务进度估计** - 预测视频中每一帧的任务完成百分比
12. **视频问答（VQA）** - 根据视频内容回答自然语言问题
13. **自然语言状态推理** - 为视频的每一帧生成描述当前状态的文本
14. **行为预估** - 预测智能体未来的行为或运动轨迹
15. **下一活动物体检测** - 预测下一步最可能与之交互的物体
16. **交互预测** - 预测未来可能发生的交互动作或交互类型
17. **第一视角人体姿态估计** - 从第一人称视角估计人体各关节点位置
18. **文本驱动的交互生成** - 根据文本描述生成匹配的人体动作序列

## 🚀 快速开始

### 1. Fork 项目
Fork 这个仓库到你的GitHub账户

### 2. 设置GitHub Secrets
在你的仓库设置中添加以下Secrets：

| 变量名 | 必需 | 描述 | 示例 |
|--------|------|------|------|
| `OPENAI_API_KEY` | ✅ | OpenAI API密钥 | sk-xxx |
| `OPENAI_API_BASE` | ❌ | API基础URL | https://api.openai.com/v1 |
| `MODEL_NAME` | ❌ | 模型名称 | gpt-4o |

### 3. 运行分析
1. 进入你的仓库的 Actions 页面
2. 选择 "Analyze Embody Papers" 工作流
3. 点击 "Run workflow"
4. 设置参数：
   - `最大分析论文数量`: 默认50篇
   - `使用本地LLM`: 默认false（使用API）
5. 点击运行

### 4. 下载结果
工作流完成后，在 Artifacts 中下载分析结果文件。

## 📁 输出文件

系统会生成以下文件：

1. **详细分析结果**: `embody_papers_analysis_YYYYMMDD_HHMMSS.csv`
   - 包含每篇论文的完整分析信息
   
2. **统计摘要**: `embody_papers_summary_YYYYMMDD_HHMMSS.csv`
   - 任务类别分布统计

### CSV文件字段说明

| 字段名 | 描述 |
|--------|------|
| Title | 论文标题 |
| Task_Category | 任务领域分类 |
| Methods | 使用的方法和技术 |
| Contributions | 主要贡献和创新点 |
| Training_Dataset | 训练数据集 |
| Testing_Dataset | 测试数据集 |
| Evaluation_Metrics | 评估指标 |
| Publication_Date | 发表日期 |
| ArXiv_URL | arXiv链接 |
| Classification_Confidence | 分类置信度(0-1) |

## 🛠️ 本地运行

如果你想在本地运行系统：

```bash
# 克隆仓库
git clone <your-repo-url>
cd embody-papers-analyzer

# 安装依赖（需要先安装uv）
uv sync

# 设置环境变量
export OPENAI_API_KEY="your-api-key"
export OPENAI_API_BASE="https://api.openai.com/v1"  # 可选
export MODEL_NAME="gpt-4o"  # 可选

# 运行分析
uv run main.py --max_papers 20
```

### 本地运行参数

```bash
uv run main.py --help
```

主要参数：
- `--max_papers`: 最大分析论文数量（默认50）
- `--use_local_llm`: 使用本地LLM而非API
- `--output_dir`: 输出目录（默认output）
- `--debug`: 启用调试模式

## 🔧 配置说明

### API配置
- 支持OpenAI API和兼容的API服务
- 推荐使用 [SiliconFlow](https://cloud.siliconflow.cn/) 等免费API服务
- 本地LLM使用Qwen2.5-3B模型

### 搜索配置
- 搜索范围：2024年1月1日 - 2025年12月31日
- 关键词：标题或摘要包含"embody"
- 排序：按提交日期降序

## 📈 使用场景

1. **学术研究**: 快速了解具身AI领域的最新研究进展
2. **文献综述**: 系统性分析相关论文的方法和贡献
3. **趋势分析**: 统计不同任务类别的研究热度
4. **数据集调研**: 了解常用的训练和测试数据集

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

## 📄 许可证

本项目采用 AGPLv3 许可证。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [arXiv API](https://arxiv.org/help/api) - 论文数据来源
- [OpenAI](https://openai.com/) - LLM API服务
- [uv](https://github.com/astral-sh/uv) - Python包管理器
<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="assets/logo.svg" alt="logo"></a>
</p>

<h3 align="center">Embody Papers Analyzer</h3>

<div align="center">

  [![Status](https://img.shields.io/badge/status-active-success.svg)]()
  [![License](https://img.shields.io/github/license/TideDra/zotero-arxiv-daily)](/LICENSE)

</div>

---

<p align="center"> 智能分析包含"embody"关键词的学术论文，自动提取结构化信息并进行任务分类
    <br> 
</p>

## 🎯 项目简介

**Embody Papers Analyzer** 是一个专门用于分析具身AI相关学术论文的自动化系统。该系统能够：

- 🔍 **智能搜索**: 自动搜索arXiv中包含"embody"关键词的论文（2024-2025年）
- 🤖 **AI分析**: 使用大语言模型提取论文的关键信息和结构化数据
- 📊 **任务分类**: 基于18个具身AI任务类别进行自动分类
- 📈 **CSV输出**: 生成结构化的分析报告，便于后续研究

## ✨ 核心功能

### 📋 信息提取
- **论文标题** - 完整的论文标题
- **任务分类** - 基于预定义分类表的自动分类
- **方法技术** - 论文使用的主要方法和技术
- **主要贡献** - 论文的创新点和贡献
- **数据集信息** - 训练和测试数据集（分开记录）
- **评估指标** - 使用的性能评估指标
- **发表信息** - 发表日期和arXiv链接

### 🏷️ 支持的任务分类（18类）

1. **动作识别** - 识别视频或传感器数据中的预定义动作
2. **手物交互检测 (HOI)** - 检测人体、物体及其交互关系
3. **主动物体检测** - 检测可能发生交互的物体
4. **跨具身模仿学习** - 人类动作到机器人策略的转换
5. **情景记忆** - 优化少样本学习的示例顺序
6. **自然语言查询 (NLQ)** - 基于自然语言的视频检索
7. **VQ2D/VQ3D** - 视觉查询的2D/3D定位跟踪
8. **具身3D视觉 grounding** - 3D环境中的目标定位
9. **具身问答（EQA）** - 通过环境探索回答问题
10. **导航** - 基于自然语言指令的路径规划
11. **任务进度估计** - 实时任务完成度预测
12. **视频问答（VQA）** - 基于视频内容的问答
13. **自然语言状态推理** - 视频状态的文本描述
14. **行为预估** - 智能体未来行为预测
15. **下一活动物体检测** - 预测下一步交互物体
16. **交互预测** - 预测未来交互动作类型
17. **第一视角人体姿态估计** - 第一人称视角的姿态估计
18. **文本驱动的交互生成** - 基于文本的动作序列生成

## 🚀 快速开始

### 1. Fork 项目
点击右上角的 Fork 按钮，将项目复制到你的GitHub账户

### 2. 配置API密钥
在你的仓库设置中添加以下 Secrets：

| 变量名 | 必需 | 描述 | 示例 |
|--------|------|------|------|
| `OPENAI_API_KEY` | ✅ | OpenAI API密钥或兼容API密钥 | sk-xxx |
| `OPENAI_API_BASE` | ❌ | API基础URL（可选） | https://api.openai.com/v1 |
| `MODEL_NAME` | ❌ | 使用的模型名称（可选） | gpt-4o |

> 💡 **推荐**: 使用 [SiliconFlow](https://cloud.siliconflow.cn/) 等免费API服务

### 3. 运行分析
1. 进入你的仓库的 **Actions** 页面
2. 选择 **"Analyze Embody Papers"** 工作流
3. 点击 **"Run workflow"** 按钮
4. 设置参数：
   - `最大分析论文数量`: 默认50篇
   - `使用本地LLM`: 默认false（推荐使用API）
5. 点击 **"Run workflow"** 开始执行

### 4. 下载结果
工作流完成后，在 **Artifacts** 部分下载分析结果文件

## 📊 输出文件

### 主要输出文件
1. **详细分析结果**: `embody_papers_analysis_YYYYMMDD_HHMMSS.csv`
2. **统计摘要**: `embody_papers_summary_YYYYMMDD_HHMMSS.csv`

### CSV字段说明
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

```bash
# 克隆仓库
git clone <your-repo-url>
cd embody-papers-analyzer

# 安装uv包管理器（如果未安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装依赖
uv sync

# 设置环境变量
export OPENAI_API_KEY="your-api-key"

# 运行分析（测试3篇论文）
uv run python test_local.py
```

### 本地运行参数
```bash
uv run main.py --help
```

## 📈 使用场景

- 🔬 **学术研究**: 快速了解具身AI领域最新进展
- 📚 **文献综述**: 系统分析相关论文的方法和贡献  
- 📊 **趋势分析**: 统计不同任务类别的研究热度
- 🗃️ **数据集调研**: 了解常用的训练和测试数据集

## 🔧 技术架构

```
arXiv搜索 → 论文过滤 → LLM分析 → 任务分类 → CSV导出
```

- **搜索引擎**: arXiv API
- **AI分析**: OpenAI API / 本地LLM
- **部署平台**: GitHub Actions
- **输出格式**: CSV文件

## 📃 许可证

本项目采用 AGPLv3 许可证。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [arXiv](https://arxiv.org/) - 学术论文数据源
- [OpenAI](https://openai.com/) - 大语言模型API
- [uv](https://github.com/astral-sh/uv) - Python包管理器
- [GitHub Actions](https://github.com/features/actions) - CI/CD平台

---

<p align="center">
  <strong>🌟 如果这个项目对你有帮助，请给个Star支持一下！</strong>
</p>

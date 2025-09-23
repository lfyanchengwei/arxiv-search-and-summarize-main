<p align="center">
  <a href="" rel="noopener">
 <img width=200px height=200px src="assets/logo.svg" alt="logo"></a>
</p>

<h3 align="center">增强版学术论文分析系统</h3>

<div align="center">

  [![Status](https://img.shields.io/badge/status-active-success.svg)]()
  [![License](https://img.shields.io/github/license/TideDra/zotero-arxiv-daily)](/LICENSE)
  [![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-支持-blue.svg)]()
  [![Docker](https://img.shields.io/badge/Docker-支持-blue.svg)]()

</div>

---

<p align="center"> 🚀 智能分析学术论文的全功能系统，支持自定义检索、多领域分析、GitHub Actions自动化部署
    <br> 
</p>

## 🎯 项目简介

**增强版学术论文分析系统** 是一个功能强大的学术论文自动化分析平台。相比原版，新增了大量实用功能：

### 🆕 增强功能亮点
- ✅ **作者机构信息** - 新增作者和学校/机构列
- ✅ **自定义检索词** - 用户可自定义多个检索关键词
- ✅ **研究领域选择** - 基于arXiv分类的领域筛选
- ✅ **自定义任务分类** - 支持添加和完全自定义任务类别
- ✅ **时间区间设置** - 灵活的论文发表时间范围
- ✅ **GitHub Actions部署** - 一键云端分析，无需本地环境
- ✅ **创新性评分** - AI评估论文创新性（1-5分）
- ✅ **中文全支持** - 完整的中文交互界面

### 🔍 核心功能
- 🤖 **AI智能分析**: 使用大语言模型提取论文关键信息
- 📊 **多维度分类**: 支持20+任务类别，可自定义扩展
- 📈 **丰富输出**: CSV详细结果 + 统计摘要 + 高创新性论文
- 🌐 **多部署方式**: GitHub Actions云端 + 本地运行 + Docker

## 🚀 快速开始

### 方式1: GitHub Actions云端分析（推荐⭐）

**优势**: 无需本地环境，随时随地分析，自动生成报告

1. **Fork项目** 
   - 点击右上角Fork按钮

2. **配置API密钥**
   - 进入仓库 `Settings` → `Secrets and variables` → `Actions`
   - 添加以下Secrets：
   
   | Secret名称 | 必需 | 描述 | 示例值 |
   |-----------|------|------|--------|
   | `OPENAI_API_KEY` | ✅ 必需 | OpenAI API密钥或兼容API密钥 | `sk-xxx` 或 `Bearer xxx` |
   | `OPENAI_API_BASE` | ❌ 可选 | API基础URL，不填默认OpenAI官方 | `https://api.siliconflow.cn/v1` |
   | `MODEL_NAME` | ❌ 可选 | 模型名称，不填默认gpt-4o | `gpt-4o-mini`, `Qwen/Qwen2.5-7B-Instruct` |

3. **运行分析**
   - 进入 `Actions` 标签页
   - 选择 `学术论文分析系统` workflow
   - 点击 `Run workflow`
   - 选择预设配置或自定义参数

4. **下载结果**
   - 分析完成后在 `Artifacts` 下载结果文件

#### 🎯 预设配置选项

| 配置名称 | 研究领域 | 检索词示例 |
|---------|---------|-----------|
| 具身智能研究 | cs.AI, cs.RO, cs.CV | embodied, robotics |
| 多模态学习 | cs.CV, cs.CL, cs.LG | multimodal, vision-language |
| 大语言模型 | cs.CL, cs.AI, cs.LG | LLM, transformer, GPT |
| 计算机视觉 | cs.CV, cs.AI | computer vision, detection |
| 强化学习 | cs.LG, cs.AI, cs.RO | reinforcement learning, RL |
| 最新趋势 | cs.AI, cs.LG, cs.CV | AI, machine learning |

### 方式2: 本地快速启动

```bash
# 1. 克隆仓库
git clone <your-repo-url>
cd zotero-arxiv-daily

# 2. 安装依赖
pip install -r requirements.txt

# 3. 快速启动（交互式配置）
python quick_start.py --api_key YOUR_OPENAI_API_KEY

# 4. 或使用完整配置
python enhanced_main.py --openai_api_key YOUR_OPENAI_API_KEY
```

### 方式3: Docker部署

```bash
# 构建镜像
docker build -f Dockerfile.github -t paper-analyzer .

# 运行分析
docker run --rm \
  -v $(pwd)/output:/app/output \
  -e OPENAI_API_KEY="your-key" \
  paper-analyzer \
  python enhanced_main.py --openai_api_key "$OPENAI_API_KEY" --skip_setup
```

## 📊 功能对比

| 功能 | 原版 | 增强版 |
|------|------|--------|
| 检索词 | 固定"embodied" | ✅ 用户自定义多个关键词 |
| 研究领域 | 无限制 | ✅ arXiv分类筛选 |
| 时间范围 | 固定2024-2025 | ✅ 用户自定义任意时间 |
| 任务分类 | 18个固定分类 | ✅ 20+分类+自定义扩展 |
| 作者信息 | 仅姓名 | ✅ 姓名+机构信息 |
| 创新性评估 | 无 | ✅ 1-5分AI评分 |
| 部署方式 | 仅本地 | ✅ GitHub Actions + 本地 + Docker |
| 界面语言 | 英文 | ✅ 完整中文支持 |
| 配置管理 | 无 | ✅ 配置持久化保存 |

## 🏷️ 支持的任务分类

### 具身智能相关（原有18类+新增）
- 动作识别、手物交互检测(HOI)、跨具身模仿学习
- 具身问答(EQA)、导航、第一视角人体姿态估计
- VQ2D/VQ3D、具身3D视觉grounding等

### 新增通用AI分类
- **多模态学习** - 跨模态表示学习和推理
- **强化学习** - 策略学习和环境交互
- **大语言模型应用** - LLM在特定领域的应用
- **计算机视觉基础** - 图像分类、检测、分割
- **自然语言处理** - 文本理解、生成、翻译

### 自定义分类支持
- ✅ 添加自定义任务类别
- ✅ 完全自定义分类体系
- ✅ 配置持久化保存

## 📈 输出文件详解

### 1. 详细分析结果 (`enhanced_papers_analysis_*.csv`)
包含16个字段的完整论文信息：

| 字段 | 描述 | 示例 |
|------|------|------|
| Title | 论文标题 | "Embodied AI for Robotics..." |
| Authors | 作者列表 | "John Doe; Jane Smith" |
| Authors_with_Affiliations | 带机构的作者 | "John Doe (MIT); Jane Smith (Stanford)" |
| Primary_Affiliations | 主要机构 | "MIT; Stanford University" |
| Task_Category | 任务分类 | "跨具身模仿学习" |
| Research_Field | 研究领域 | "机器人学" |
| Methods | 主要方法 | "深度强化学习，Transformer" |
| Contributions | 主要贡献 | "提出了新的模仿学习框架" |
| Training_Dataset | 训练数据集 | "RoboMimic, D4RL" |
| Testing_Dataset | 测试数据集 | "Meta-World, RLBench" |
| Evaluation_Metrics | 评估指标 | "成功率，样本效率" |
| Publication_Date | 发表日期 | "2024-03-15" |
| ArXiv_URL | 论文链接 | "http://arxiv.org/abs/2403.xxxxx" |
| ArXiv_Categories | arXiv分类 | "cs.RO; cs.AI" |
| Classification_Confidence | 分类置信度 | "0.92" |
| Novelty_Score | 创新性评分 | "4" |

### 2. 统计摘要 (`enhanced_papers_summary_*.csv`)
- 任务类别分布统计
- 研究领域分布统计  
- 创新性统计分析
- 主要机构分布

### 3. 高创新性论文 (`high_novelty_papers_*.csv`)
- 创新性评分≥4的论文
- 按创新性评分排序
- 便于发现突破性研究

### 4. 分析报告 (`analysis_summary.md`)
- Markdown格式的可读性报告
- 包含图表和统计信息
- 适合分享和展示

## 🔧 高级配置

### arXiv研究领域分类

#### 主要领域
- `cs` - 计算机科学
- `math` - 数学  
- `physics` - 物理学
- `q-bio` - 定量生物学
- `stat` - 统计学
- `eess` - 电气工程与系统科学

#### 计算机科学子领域
- `cs.AI` - 人工智能
- `cs.CV` - 计算机视觉与模式识别
- `cs.CL` - 计算与语言
- `cs.LG` - 机器学习
- `cs.RO` - 机器人学
- `cs.HC` - 人机交互

### 自定义任务分类示例

```python
custom_categories = {
    "医疗AI": {
        "definition": "将AI技术应用于医疗诊断和治疗",
        "typical_output": "诊断结果、治疗建议",
        "datasets_metrics": "医疗数据集、准确率、敏感性"
    },
    "金融科技": {
        "definition": "AI在金融领域的应用",
        "typical_output": "风险评估、交易决策",
        "datasets_metrics": "金融数据集、收益率、风险指标"
    }
}
```

## 🛠️ 技术架构

```
用户配置 → arXiv搜索 → 领域过滤 → LLM分析 → 任务分类 → 多格式输出
    ↓
GitHub Actions / 本地运行 / Docker
    ↓
CSV + Markdown + JSON 报告
```

### 技术栈
- **搜索**: arXiv API
- **AI分析**: OpenAI API / 兼容API
- **部署**: GitHub Actions + Docker
- **语言**: Python 3.9+
- **依赖管理**: pip / uv

## 📚 使用场景

### 学术研究
- 🔬 **文献调研**: 快速了解特定领域最新进展
- 📊 **趋势分析**: 统计研究热点和发展趋势
- 🏛️ **机构分析**: 了解主要研究机构和合作网络
- 💡 **创新发现**: 识别高创新性的突破性研究

### 产业应用  
- 📈 **技术跟踪**: 跟踪竞争对手和行业动态
- 🎯 **投资决策**: 评估技术领域的投资价值
- 🔍 **人才招聘**: 识别优秀研究者和团队

## 🚨 注意事项

### API使用
- 💰 **费用控制**: 建议设置合理的论文数量限制
- ⏱️ **速率限制**: 注意API调用频率限制
- 🔑 **密钥安全**: 妥善保管API密钥，不要泄露

### GitHub Actions
- ⏰ **运行时间**: 免费账户有6小时运行时间限制
- 💾 **存储限制**: Artifacts有存储空间限制
- 🔄 **并发限制**: 注意并发job数量限制

## 📖 详细文档

- 📘 [增强功能详细说明](README_ENHANCED.md)
- 🚀 [GitHub Actions部署指南](README_GITHUB_ACTIONS.md)
- 💻 [本地开发指南](example_usage.py)
- 🧪 [系统测试说明](test_enhanced_system.py)

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

### 贡献方向
- 🆕 新增任务分类定义
- 🌐 多语言支持
- 📊 数据可视化功能
- 🔗 更多数据源集成
- 🎨 UI界面改进

## 📃 许可证

本项目采用 AGPLv3 许可证。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [arXiv](https://arxiv.org/) - 学术论文数据源
- [OpenAI](https://openai.com/) - 大语言模型API  
- [GitHub Actions](https://github.com/features/actions) - CI/CD平台
- [Docker](https://www.docker.com/) - 容器化平台
- 所有贡献者和用户的支持 ❤️

---

<p align="center">
  <strong>🌟 如果这个项目对你有帮助，请给个Star支持一下！</strong>
</p>

<p align="center">
  <a href="#快速开始">快速开始</a> •
  <a href="README_GITHUB_ACTIONS.md">GitHub Actions部署</a> •
  <a href="README_ENHANCED.md">功能详解</a> •
  <a href="/issues">问题反馈</a>
</p>
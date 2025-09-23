# 🚀 GitHub Actions 部署指南

本指南将帮助您在GitHub Actions中部署学术论文分析系统，实现自动化的论文分析和报告生成。

## 📋 功能特性

- ✅ **自动化分析**: 通过GitHub Actions自动运行论文分析
- ✅ **手动触发**: 支持手动触发，可自定义参数
- ✅ **定时运行**: 支持定时自动分析（每周一次）
- ✅ **预设配置**: 提供6种研究领域的预设配置
- ✅ **结果下载**: 分析结果自动打包为Artifacts
- ✅ **报告生成**: 自动生成Markdown和JSON格式的分析报告
- ✅ **Issue通知**: 可选择创建Issue来通知分析完成

## 🛠️ 部署步骤

### 1. Fork或Clone仓库

```bash
git clone https://github.com/your-username/zotero-arxiv-daily.git
cd zotero-arxiv-daily
```

### 2. 配置GitHub Secrets

在您的GitHub仓库中设置以下Secrets：

1. 进入仓库设置页面：`Settings` → `Secrets and variables` → `Actions`
2. 点击 `New repository secret`
3. 添加以下Secrets：

| Secret名称 | 描述 | 必需 | 示例值 |
|-----------|------|------|--------|
| `OPENAI_API_KEY` | API密钥 | ✅ 必需 | `sk-xxx` 或 `Bearer xxx` |
| `OPENAI_API_BASE` | API基础URL | ❌ 可选 | `https://api.siliconflow.cn/v1` |
| `MODEL_NAME` | 模型名称 | ❌ 可选 | `gpt-4o-mini`, `Qwen/Qwen2.5-7B-Instruct` |

#### 🔑 API配置说明

**OPENAI_API_KEY (必需)**
- OpenAI官方API密钥格式：`sk-xxxxxxxxxxxxxxxx`
- 兼容API服务密钥格式：`Bearer xxxxxxxx` 或直接填写token

**OPENAI_API_BASE (可选)**
- 不填写：默认使用OpenAI官方API (`https://api.openai.com/v1`)
- 自定义：使用兼容OpenAI格式的API服务

**MODEL_NAME (可选)**
- 不填写：默认使用 `gpt-4o`
- 自定义：根据API服务支持的模型填写

#### 💡 推荐免费API服务

| 服务商 | API地址 | 推荐模型 | 特点 |
|--------|---------|----------|------|
| [SiliconFlow](https://cloud.siliconflow.cn/) | `https://api.siliconflow.cn/v1` | `Qwen/Qwen2.5-7B-Instruct` | 免费额度，多种开源模型 |
| [DeepSeek](https://platform.deepseek.com/) | `https://api.deepseek.com/v1` | `deepseek-chat` | 高性价比，推理能力强 |
| [智谱AI](https://open.bigmodel.cn/) | `https://open.bigmodel.cn/api/paas/v4` | `glm-4-flash` | 国产大模型，免费额度 |
| [月之暗面](https://platform.moonshot.cn/) | `https://api.moonshot.cn/v1` | `moonshot-v1-8k` | 长文本处理能力强 |

#### 🛠️ 配置示例

**使用SiliconFlow免费服务：**
```
OPENAI_API_KEY: Bearer your_siliconflow_token
OPENAI_API_BASE: https://api.siliconflow.cn/v1
MODEL_NAME: Qwen/Qwen2.5-7B-Instruct
```

**使用DeepSeek服务：**
```
OPENAI_API_KEY: Bearer your_deepseek_token
OPENAI_API_BASE: https://api.deepseek.com/v1
MODEL_NAME: deepseek-chat
```

**使用OpenAI官方服务：**
```
OPENAI_API_KEY: sk-your_openai_key
# OPENAI_API_BASE 和 MODEL_NAME 可以不填，使用默认值
```

### 3. 启用GitHub Actions

1. 进入仓库的 `Actions` 标签页
2. 如果Actions被禁用，点击 `I understand my workflows, go ahead and enable them`

## 🎯 使用方法

### 方法1: 手动触发（推荐）

1. 进入仓库的 `Actions` 标签页
2. 选择 `学术论文分析系统` workflow
3. 点击 `Run workflow`
4. 填写参数或选择预设配置：

#### 参数说明

| 参数 | 描述 | 示例 |
|------|------|------|
| 检索关键词 | 用逗号分隔的关键词 | `embodied,robotics,multimodal` |
| 研究领域 | arXiv分类代码 | `cs.AI,cs.RO,cs.CV,cs.LG` |
| 开始日期 | YYYY-MM-DD格式 | `2024-01-01` |
| 结束日期 | YYYY-MM-DD格式 | `2024-12-31` |
| 最大论文数量 | 整数 | `50` |
| 预设配置 | 选择预设或自定义 | `embodied_ai` |

#### 预设配置选项

| 预设名称 | 描述 | 关键词 | 领域 |
|---------|------|--------|------|
| `embodied_ai` | 具身智能研究 | embodied, robotics | cs.AI, cs.RO, cs.CV |
| `multimodal_learning` | 多模态学习 | multimodal, vision-language | cs.CV, cs.CL, cs.LG |
| `large_language_models` | 大语言模型 | LLM, transformer, GPT | cs.CL, cs.AI, cs.LG |
| `computer_vision` | 计算机视觉 | computer vision, detection | cs.CV, cs.AI, cs.LG |
| `reinforcement_learning` | 强化学习 | reinforcement learning, RL | cs.LG, cs.AI, cs.RO |
| `recent_trends` | 最新趋势 | AI, machine learning | cs.AI, cs.LG, cs.CV |

### 方法2: 定时自动运行

系统默认配置为每周一上午9点（UTC时间）自动运行，使用默认的具身智能配置。

要修改定时设置，编辑 `.github/workflows/paper-analysis.yml` 中的 `cron` 表达式：

```yaml
schedule:
  # 每周一上午9点 (UTC)
  - cron: '0 9 * * 1'
```

## 📊 查看结果

### 1. 下载Artifacts

1. 进入 `Actions` 标签页
2. 点击对应的workflow运行记录
3. 在页面底部找到 `Artifacts` 部分
4. 下载 `paper-analysis-results-XXX` 文件

### 2. 查看在线报告

如果启用了Issue创建功能，系统会自动创建一个Issue包含分析摘要。

### 3. 结果文件说明

下载的Artifacts包含以下文件：

| 文件 | 描述 |
|------|------|
| `enhanced_papers_analysis_*.csv` | 详细的论文分析结果 |
| `enhanced_papers_summary_*.csv` | 统计摘要数据 |
| `high_novelty_papers_*.csv` | 高创新性论文 |
| `analysis_summary.md` | Markdown格式的分析报告 |
| `analysis_summary.json` | JSON格式的分析摘要 |
| `run_info.json` | 运行配置信息 |

## 🔧 高级配置

### 自定义Workflow

您可以修改 `.github/workflows/paper-analysis.yml` 来自定义workflow：

```yaml
# 修改运行频率
schedule:
  - cron: '0 9 * * 1'  # 每周一
  - cron: '0 9 1 * *'  # 每月1号

# 添加更多输入参数
inputs:
  custom_categories:
    description: '自定义任务分类 (JSON格式)'
    required: false
    type: string
```

### 添加通知

您可以添加其他通知方式，如Slack、邮件等：

```yaml
- name: 发送Slack通知
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: 论文分析完成！
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### 自定义输出格式

修改 `generate_report.py` 来自定义报告格式：

```python
# 添加更多图表
def generate_charts(papers):
    # 生成趋势图、词云等
    pass

# 自定义报告模板
def custom_report_template():
    # 您的自定义模板
    pass
```

## 🚨 注意事项

### API限制
- OpenAI API有调用频率和费用限制
- 建议设置合理的 `max_papers` 参数
- 监控API使用情况

### 存储限制
- GitHub Actions Artifacts有存储限制
- 大文件可能需要使用外部存储

### 运行时间
- GitHub Actions有运行时间限制（免费账户6小时）
- 大量论文分析可能需要较长时间

## 🔍 故障排除

### 常见问题

1. **API密钥错误**
   ```
   Error: 使用API模式时必须提供OpenAI API密钥
   ```
   解决：检查 `OPENAI_API_KEY` Secret是否正确设置

2. **依赖安装失败**
   ```
   Error: Could not find a version that satisfies the requirement
   ```
   解决：检查 `requirements.txt` 文件是否存在

3. **分析结果为空**
   ```
   Warning: 未找到符合条件的论文
   ```
   解决：调整检索关键词或扩大时间范围

### 调试方法

1. **启用调试模式**
   ```yaml
   - name: 运行论文分析 (调试模式)
     run: |
       python enhanced_main.py \
         --openai_api_key "${{ secrets.OPENAI_API_KEY }}" \
         --debug \
         --skip_setup
   ```

2. **查看详细日志**
   在Actions运行页面查看详细的执行日志

3. **本地测试**
   ```bash
   # 本地运行相同的命令
   python generate_github_config.py --keywords "test" --categories "cs.AI"
   python enhanced_main.py --openai_api_key "your-key" --skip_setup
   ```

## 📈 扩展功能

### 1. 多语言支持
- 添加英文版本的报告生成
- 支持其他语言的关键词搜索

### 2. 数据可视化
- 集成图表生成库
- 创建交互式分析仪表板

### 3. 结果存储
- 集成数据库存储历史结果
- 支持结果对比和趋势分析

### 4. 通知集成
- 支持多种通知渠道
- 自定义通知内容和格式

## 🤝 贡献

欢迎提交Issue和Pull Request来改进GitHub Actions集成！

## 📄 许可证

本项目采用MIT许可证。
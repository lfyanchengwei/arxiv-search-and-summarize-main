# 🔑 API配置详细指南

本指南详细介绍如何配置不同API服务来运行学术论文分析系统。

## 📋 支持的API服务

### 1. OpenAI官方API

**优势**: 模型质量最高，稳定性好
**劣势**: 需要付费，国内访问可能需要代理

```bash
# 配置示例
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# OPENAI_API_BASE 不填，使用默认值
# MODEL_NAME 不填，使用默认 gpt-4o
```

**推荐模型**:
- `gpt-4o` - 最新多模态模型，综合能力强
- `gpt-4o-mini` - 轻量版，性价比高
- `gpt-3.5-turbo` - 经典模型，成本低

### 2. SiliconFlow (推荐⭐)

**优势**: 免费额度丰富，支持多种开源模型，国内访问稳定
**劣势**: 免费额度有限制

**注册地址**: https://cloud.siliconflow.cn/

```bash
# 配置示例
OPENAI_API_KEY=Bearer sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
OPENAI_API_BASE=https://api.siliconflow.cn/v1
MODEL_NAME=Qwen/Qwen2.5-7B-Instruct
```

**推荐模型**:
- `Qwen/Qwen2.5-7B-Instruct` - 通义千问，中文能力强
- `meta-llama/Llama-3.1-8B-Instruct` - Meta开源模型
- `deepseek-ai/DeepSeek-V2.5` - DeepSeek开源版本

### 3. DeepSeek

**优势**: 高性价比，推理能力强，数学和代码能力突出
**劣势**: 需要付费（但价格便宜）

**注册地址**: https://platform.deepseek.com/

```bash
# 配置示例
OPENAI_API_KEY=Bearer your_deepseek_api_key
OPENAI_API_BASE=https://api.deepseek.com/v1
MODEL_NAME=deepseek-chat
```

**推荐模型**:
- `deepseek-chat` - 主力对话模型
- `deepseek-coder` - 代码专用模型

### 4. 智谱AI (GLM)

**优势**: 国产大模型，免费额度，中文理解好
**劣势**: API格式可能需要适配

**注册地址**: https://open.bigmodel.cn/

```bash
# 配置示例
OPENAI_API_KEY=your_zhipu_api_key
OPENAI_API_BASE=https://open.bigmodel.cn/api/paas/v4
MODEL_NAME=glm-4-flash
```

**推荐模型**:
- `glm-4-flash` - 快速版本，免费额度
- `glm-4` - 完整版本，能力更强

### 5. 月之暗面 (Moonshot)

**优势**: 长文本处理能力强，适合分析长论文
**劣势**: 需要付费

**注册地址**: https://platform.moonshot.cn/

```bash
# 配置示例
OPENAI_API_KEY=Bearer your_moonshot_api_key
OPENAI_API_BASE=https://api.moonshot.cn/v1
MODEL_NAME=moonshot-v1-8k
```

**推荐模型**:
- `moonshot-v1-8k` - 8K上下文
- `moonshot-v1-32k` - 32K上下文，适合长文本
- `moonshot-v1-128k` - 128K上下文，超长文本

## 🛠️ 配置步骤

### GitHub Actions配置

1. **进入仓库设置**
   ```
   你的仓库 → Settings → Secrets and variables → Actions
   ```

2. **添加Secrets**
   点击 `New repository secret`，依次添加：
   
   - **OPENAI_API_KEY**: 你的API密钥
   - **OPENAI_API_BASE**: API基础URL（可选）
   - **MODEL_NAME**: 模型名称（可选）

3. **验证配置**
   运行一次workflow，检查是否正常工作

### 本地开发配置

1. **环境变量方式**
   ```bash
   export OPENAI_API_KEY="your_api_key"
   export OPENAI_API_BASE="your_api_base"
   export MODEL_NAME="your_model_name"
   ```

2. **命令行参数方式**
   ```bash
   python enhanced_main.py \
     --openai_api_key "your_api_key" \
     --openai_api_base "your_api_base" \
     --model_name "your_model_name"
   ```

3. **.env文件方式**
   ```bash
   # 创建 .env 文件
   echo "OPENAI_API_KEY=your_api_key" > .env
   echo "OPENAI_API_BASE=your_api_base" >> .env
   echo "MODEL_NAME=your_model_name" >> .env
   ```

## 💰 成本估算

### 免费服务
- **SiliconFlow**: 每月免费额度，适合轻度使用
- **智谱AI**: 每月免费tokens，适合测试

### 付费服务成本对比 (分析50篇论文)

| 服务商 | 模型 | 预估成本 | 特点 |
|--------|------|----------|------|
| OpenAI | gpt-4o-mini | ~$2-5 | 质量高，稳定 |
| OpenAI | gpt-4o | ~$10-20 | 最高质量 |
| DeepSeek | deepseek-chat | ~$0.5-1 | 极高性价比 |
| 月之暗面 | moonshot-v1-8k | ~$1-3 | 长文本能力强 |

## 🔧 故障排除

### 常见错误

1. **API密钥错误**
   ```
   Error: Incorrect API key provided
   ```
   **解决**: 检查API密钥格式和有效性

2. **API地址错误**
   ```
   Error: Connection failed
   ```
   **解决**: 检查OPENAI_API_BASE是否正确

3. **模型不存在**
   ```
   Error: Model not found
   ```
   **解决**: 检查MODEL_NAME是否为该API服务支持的模型

4. **额度不足**
   ```
   Error: Insufficient quota
   ```
   **解决**: 充值或切换到其他API服务

### 调试方法

1. **启用调试模式**
   ```bash
   python enhanced_main.py --debug
   ```

2. **测试API连接**
   ```bash
   curl -X POST "your_api_base/chat/completions" \
     -H "Authorization: Bearer your_api_key" \
     -H "Content-Type: application/json" \
     -d '{"model":"your_model","messages":[{"role":"user","content":"test"}]}'
   ```

3. **检查配置**
   ```bash
   python -c "
   import os
   print('API Key:', os.getenv('OPENAI_API_KEY', 'Not set'))
   print('API Base:', os.getenv('OPENAI_API_BASE', 'Not set'))
   print('Model:', os.getenv('MODEL_NAME', 'Not set'))
   "
   ```

## 📊 性能对比

基于实际测试，不同API服务的性能对比：

| 指标 | OpenAI GPT-4o | SiliconFlow Qwen2.5 | DeepSeek Chat | 智谱 GLM-4 |
|------|---------------|---------------------|---------------|------------|
| 分析准确性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| 中文理解 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| 响应速度 | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| 成本效益 | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| 稳定性 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

## 🎯 推荐配置

### 新手用户
```bash
# 使用SiliconFlow免费服务
OPENAI_API_KEY=Bearer your_siliconflow_token
OPENAI_API_BASE=https://api.siliconflow.cn/v1
MODEL_NAME=Qwen/Qwen2.5-7B-Instruct
```

### 高质量需求
```bash
# 使用OpenAI官方服务
OPENAI_API_KEY=sk-your_openai_key
MODEL_NAME=gpt-4o-mini  # 性价比版本
```

### 高性价比需求
```bash
# 使用DeepSeek服务
OPENAI_API_KEY=Bearer your_deepseek_token
OPENAI_API_BASE=https://api.deepseek.com/v1
MODEL_NAME=deepseek-chat
```

### 长文本分析
```bash
# 使用月之暗面服务
OPENAI_API_KEY=Bearer your_moonshot_token
OPENAI_API_BASE=https://api.moonshot.cn/v1
MODEL_NAME=moonshot-v1-32k
```

---

💡 **提示**: 建议先使用免费服务测试系统功能，确认满足需求后再考虑付费服务。
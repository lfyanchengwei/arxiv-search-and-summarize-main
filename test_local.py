#!/usr/bin/env python3
"""
本地测试脚本 - 用于测试论文分析系统
"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 设置测试参数
os.environ["MAX_PAPERS"] = "3"  # 只测试3篇论文
os.environ["USE_LOCAL_LLM"] = "false"  # 使用API
os.environ["OUTPUT_DIR"] = "test_output"

# 检查API密钥
if not os.environ.get("OPENAI_API_KEY"):
    print("错误: 请设置 OPENAI_API_KEY 环境变量")
    print("示例: export OPENAI_API_KEY='your-api-key'")
    sys.exit(1)

# 导入并运行主程序
if __name__ == "__main__":
    # 添加调试参数
    sys.argv.extend(["--debug", "--max_papers", "3"])
    
    # 导入主程序
    from main import main
    
    print("开始本地测试...")
    print("=" * 50)
    
    try:
        main()
        print("=" * 50)
        print("测试完成！请检查 test_output 目录中的结果文件。")
    except Exception as e:
        print(f"测试失败: {e}")
        sys.exit(1)
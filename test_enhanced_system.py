#!/usr/bin/env python3
"""
增强版系统测试脚本
测试各个模块的基本功能
"""

import os
import sys
import json
from datetime import datetime, timedelta

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_user_config():
    """测试用户配置模块"""
    print("🧪 测试用户配置模块...")
    
    try:
        from user_config import UserConfig, save_user_config, load_user_config, validate_config
        
        # 创建测试配置
        test_config = UserConfig.create_default()
        test_config.search_keywords = ["test", "example"]
        test_config.max_papers = 10
        
        # 测试保存和加载
        save_user_config(test_config)
        loaded_config = load_user_config()
        
        # 验证配置
        is_valid = validate_config(loaded_config)
        
        assert loaded_config.search_keywords == ["test", "example"]
        assert loaded_config.max_papers == 10
        assert is_valid == True
        
        print("✅ 用户配置模块测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 用户配置模块测试失败: {e}")
        return False


def test_enhanced_paper():
    """测试增强版论文类"""
    print("🧪 测试增强版论文类...")
    
    try:
        from enhanced_paper import EnhancedArxivPaper
        import arxiv
        
        # 创建一个模拟的arxiv.Result对象
        class MockArxivResult:
            def __init__(self):
                self.title = "Test Paper: Embodied AI Research"
                self.summary = "This is a test paper about embodied artificial intelligence and robotics."
                self.authors = ["John Doe", "Jane Smith"]
                self.categories = ["cs.AI", "cs.RO"]
                self.primary_category = "cs.AI"
                self.published = datetime.now()
                self.entry_id = "http://arxiv.org/abs/2024.12345v1"
                self.pdf_url = "http://arxiv.org/pdf/2024.12345v1.pdf"
            
            def get_short_id(self):
                return "2024.12345v1"
        
        # 测试EnhancedArxivPaper
        mock_result = MockArxivResult()
        paper = EnhancedArxivPaper(mock_result)
        
        # 测试基本属性
        assert paper.title == "Test Paper: Embodied AI Research"
        assert len(paper.authors) == 2
        assert paper.is_cs_related() == True
        assert "cs.AI" in paper.categories
        
        print("✅ 增强版论文类测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 增强版论文类测试失败: {e}")
        return False


def test_enhanced_config():
    """测试增强版配置"""
    print("🧪 测试增强版配置...")
    
    try:
        from enhanced_config import ENHANCED_TASK_CATEGORIES, format_enhanced_classification_table
        
        # 测试任务分类表
        assert len(ENHANCED_TASK_CATEGORIES) > 0
        assert "动作识别" in ENHANCED_TASK_CATEGORIES
        assert "多模态学习" in ENHANCED_TASK_CATEGORIES
        
        # 测试格式化函数
        formatted_table = format_enhanced_classification_table()
        assert len(formatted_table) > 0
        assert "动作识别" in formatted_table
        
        # 测试自定义分类
        custom_categories = {
            "测试分类": {
                "definition": "这是一个测试分类",
                "typical_output": "测试输出",
                "datasets_metrics": "测试指标"
            }
        }
        
        formatted_with_custom = format_enhanced_classification_table(custom_categories)
        assert "测试分类" in formatted_with_custom
        
        print("✅ 增强版配置测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 增强版配置测试失败: {e}")
        return False


def test_csv_exporter():
    """测试CSV导出器"""
    print("🧪 测试CSV导出器...")
    
    try:
        from enhanced_csv_exporter import EnhancedCSVExporter
        from enhanced_paper_analyzer import EnhancedPaperAnalysis
        
        # 创建测试数据
        test_analyses = [
            EnhancedPaperAnalysis(
                title="Test Paper 1",
                authors="John Doe; Jane Smith",
                authors_with_affiliations="John Doe (MIT); Jane Smith (Stanford)",
                primary_affiliations="MIT; Stanford",
                task_category="动作识别",
                methods="深度学习方法",
                contributions="提出了新的算法",
                training_dataset="UCF101",
                testing_dataset="HMDB51",
                evaluation_metrics="准确率",
                publication_date="2024-01-01",
                arxiv_url="http://arxiv.org/abs/2024.12345",
                confidence=0.9,
                research_field="计算机视觉",
                novelty_score=4,
                arxiv_categories="cs.CV; cs.AI"
            )
        ]
        
        # 测试导出器
        exporter = EnhancedCSVExporter()
        
        # 测试打印摘要（不会实际输出文件）
        exporter.print_summary(test_analyses)
        
        print("✅ CSV导出器测试通过")
        return True
        
    except Exception as e:
        print(f"❌ CSV导出器测试失败: {e}")
        return False


def test_search_query_building():
    """测试搜索查询构建"""
    print("🧪 测试搜索查询构建...")
    
    try:
        from enhanced_main import build_search_query
        from user_config import UserConfig
        
        # 创建测试配置
        config = UserConfig(
            search_keywords=["embodied", "robotics"],
            research_categories=["cs.AI", "cs.RO"],
            start_date="2024-01-01",
            end_date="2024-12-31",
            max_papers=50,
            custom_task_categories={},
            use_default_categories=True,
            include_author_affiliations=True,
            output_format="csv"
        )
        
        # 构建查询
        query = build_search_query(config)
        
        # 验证查询包含必要元素
        assert "embodied" in query
        assert "robotics" in query
        assert "cs.AI" in query
        assert "cs.RO" in query
        assert "20240101" in query
        assert "20241231" in query
        
        print("✅ 搜索查询构建测试通过")
        return True
        
    except Exception as e:
        print(f"❌ 搜索查询构建测试失败: {e}")
        return False


def run_all_tests():
    """运行所有测试"""
    print("🚀 开始运行增强版系统测试\n")
    
    tests = [
        ("用户配置模块", test_user_config),
        ("增强版论文类", test_enhanced_paper),
        ("增强版配置", test_enhanced_config),
        ("CSV导出器", test_csv_exporter),
        ("搜索查询构建", test_search_query_building)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"📋 测试: {test_name}")
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
            failed += 1
        print()
    
    print("=" * 50)
    print(f"📊 测试结果: {passed} 通过, {failed} 失败")
    
    if failed == 0:
        print("🎉 所有测试通过！系统准备就绪。")
    else:
        print("⚠️ 部分测试失败，请检查相关模块。")
    
    return failed == 0


def check_dependencies():
    """检查依赖包"""
    print("🔍 检查依赖包...")
    
    required_packages = [
        "arxiv",
        "loguru", 
        "tqdm",
        "python-dotenv"
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (缺失)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️ 缺失依赖包: {', '.join(missing_packages)}")
        print("请运行: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ 所有依赖包已安装")
        return True


def main():
    """主函数"""
    print("🧪 增强版学术论文分析系统 - 测试套件\n")
    
    # 检查依赖
    if not check_dependencies():
        print("❌ 依赖检查失败，请先安装依赖包")
        sys.exit(1)
    
    print()
    
    # 运行测试
    success = run_all_tests()
    
    if success:
        print("\n🚀 系统测试完成，可以开始使用！")
        print("运行方式:")
        print("1. 快速启动: python quick_start.py --api_key YOUR_API_KEY")
        print("2. 完整配置: python enhanced_main.py --openai_api_key YOUR_API_KEY")
        print("3. 查看示例: python example_usage.py")
    else:
        print("\n❌ 系统测试失败，请修复问题后重试")
        sys.exit(1)


if __name__ == "__main__":
    main()
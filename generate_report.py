#!/usr/bin/env python3
"""
生成GitHub Actions分析报告
"""

import os
import json
import csv
import argparse
from datetime import datetime
from pathlib import Path


def read_csv_results(output_dir):
    """读取CSV分析结果"""
    csv_files = list(Path(output_dir).glob("enhanced_papers_analysis_*.csv"))
    if not csv_files:
        return None, None
    
    # 读取最新的分析文件
    latest_csv = max(csv_files, key=os.path.getctime)
    
    papers = []
    with open(latest_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        papers = list(reader)
    
    return papers, latest_csv


def read_summary_results(output_dir):
    """读取统计摘要结果"""
    summary_files = list(Path(output_dir).glob("enhanced_papers_summary_*.csv"))
    if not summary_files:
        return None
    
    latest_summary = max(summary_files, key=os.path.getctime)
    
    summary_data = {}
    current_section = None
    
    with open(latest_summary, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            if row[0].startswith("==="):
                current_section = row[0].strip("= ")
                summary_data[current_section] = []
            elif current_section and len(row) >= 2:
                summary_data[current_section].append(row)
    
    return summary_data


def read_run_info(output_dir):
    """读取运行信息"""
    run_info_path = Path(output_dir) / "run_info.json"
    if run_info_path.exists():
        with open(run_info_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def generate_markdown_report(papers, summary_data, run_info, output_dir):
    """生成Markdown格式的报告"""
    
    report_lines = []
    
    # 标题和基本信息
    report_lines.append("# 📊 学术论文分析报告")
    report_lines.append("")
    report_lines.append(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if run_info:
        config = run_info.get('config', {})
        report_lines.append(f"**分析时间范围**: {config.get('start_date')} 到 {config.get('end_date')}")
        report_lines.append(f"**检索关键词**: {', '.join(config.get('search_keywords', []))}")
        report_lines.append(f"**研究领域**: {', '.join(config.get('research_categories', []))}")
        report_lines.append(f"**最大论文数**: {config.get('max_papers')}")
        
        if run_info.get('preset_used'):
            report_lines.append(f"**使用预设**: {run_info['preset_used']}")
    
    report_lines.append("")
    
    # 总体统计
    if papers:
        report_lines.append("## 📈 总体统计")
        report_lines.append("")
        report_lines.append(f"- **总论文数量**: {len(papers)}")
        
        # 计算平均置信度和创新性
        confidences = [float(p.get('Classification_Confidence', 0)) for p in papers if p.get('Classification_Confidence')]
        novelty_scores = [int(p.get('Novelty_Score', 0)) for p in papers if p.get('Novelty_Score')]
        
        if confidences:
            avg_confidence = sum(confidences) / len(confidences)
            report_lines.append(f"- **平均分类置信度**: {avg_confidence:.2f}")
        
        if novelty_scores:
            avg_novelty = sum(novelty_scores) / len(novelty_scores)
            high_novelty_count = sum(1 for score in novelty_scores if score >= 4)
            report_lines.append(f"- **平均创新性评分**: {avg_novelty:.2f}")
            report_lines.append(f"- **高创新性论文数量** (评分≥4): {high_novelty_count}")
        
        report_lines.append("")
    
    # 任务分类分布
    if summary_data and "任务类别分布" in summary_data:
        report_lines.append("## 🎯 任务分类分布")
        report_lines.append("")
        report_lines.append("| 任务类别 | 论文数量 | 占比 |")
        report_lines.append("|---------|---------|------|")
        
        for row in summary_data["任务类别分布"]:
            if len(row) >= 3 and row[0] != "Task_Category":
                report_lines.append(f"| {row[0]} | {row[1]} | {row[2]} |")
        
        report_lines.append("")
    
    # 研究领域分布
    if summary_data and "研究领域分布" in summary_data:
        report_lines.append("## 🔬 研究领域分布")
        report_lines.append("")
        report_lines.append("| 研究领域 | 论文数量 | 占比 |")
        report_lines.append("|---------|---------|------|")
        
        for row in summary_data["研究领域分布"]:
            if len(row) >= 3 and row[0] != "Research_Field":
                report_lines.append(f"| {row[0]} | {row[1]} | {row[2]} |")
        
        report_lines.append("")
    
    # 主要机构
    if summary_data and "主要机构分布" in summary_data:
        report_lines.append("## 🏛️ 主要机构分布")
        report_lines.append("")
        report_lines.append("| 机构 | 论文数量 |")
        report_lines.append("|------|---------|")
        
        for row in summary_data["主要机构分布"][:10]:  # 只显示前10个
            if len(row) >= 2 and row[0] != "Institution":
                report_lines.append(f"| {row[0]} | {row[1]} |")
        
        report_lines.append("")
    
    # 高创新性论文
    if papers:
        high_novelty_papers = [p for p in papers if p.get('Novelty_Score') and int(p['Novelty_Score']) >= 4]
        if high_novelty_papers:
            report_lines.append("## 🌟 高创新性论文 (评分≥4)")
            report_lines.append("")
            
            # 按创新性评分排序
            high_novelty_papers.sort(key=lambda x: int(x.get('Novelty_Score', 0)), reverse=True)
            
            for i, paper in enumerate(high_novelty_papers[:10], 1):  # 显示前10篇
                title = paper.get('Title', '未知标题')
                score = paper.get('Novelty_Score', 'N/A')
                category = paper.get('Task_Category', '未分类')
                url = paper.get('ArXiv_URL', '')
                
                report_lines.append(f"### {i}. {title}")
                report_lines.append(f"- **创新性评分**: {score}")
                report_lines.append(f"- **任务类别**: {category}")
                if url:
                    report_lines.append(f"- **论文链接**: [{url}]({url})")
                report_lines.append("")
    
    # 文件下载链接
    report_lines.append("## 📁 详细结果文件")
    report_lines.append("")
    report_lines.append("请在GitHub Actions的Artifacts中下载以下文件：")
    report_lines.append("- 📊 详细分析结果 (CSV)")
    report_lines.append("- 📈 统计摘要 (CSV)")
    report_lines.append("- 🌟 高创新性论文 (CSV)")
    report_lines.append("")
    
    # 保存报告
    report_path = Path(output_dir) / "analysis_summary.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
    
    return report_path


def generate_json_summary(papers, summary_data, run_info, output_dir):
    """生成JSON格式的摘要"""
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "run_info": run_info,
        "statistics": {
            "total_papers": len(papers) if papers else 0
        }
    }
    
    if papers:
        # 计算统计信息
        confidences = [float(p.get('Classification_Confidence', 0)) for p in papers if p.get('Classification_Confidence')]
        novelty_scores = [int(p.get('Novelty_Score', 0)) for p in papers if p.get('Novelty_Score')]
        
        if confidences:
            summary["statistics"]["avg_confidence"] = sum(confidences) / len(confidences)
        
        if novelty_scores:
            summary["statistics"]["avg_novelty"] = sum(novelty_scores) / len(novelty_scores)
            summary["statistics"]["high_novelty_count"] = sum(1 for score in novelty_scores if score >= 4)
        
        # 任务分类统计
        task_categories = {}
        for paper in papers:
            category = paper.get('Task_Category', '未分类')
            task_categories[category] = task_categories.get(category, 0) + 1
        
        summary["task_categories"] = task_categories
        
        # 研究领域统计
        research_fields = {}
        for paper in papers:
            field = paper.get('Research_Field', '未明确说明')
            research_fields[field] = research_fields.get(field, 0) + 1
        
        summary["research_fields"] = research_fields
    
    # 保存JSON摘要
    json_path = Path(output_dir) / "analysis_summary.json"
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    return json_path


def main():
    parser = argparse.ArgumentParser(description='生成分析报告')
    parser.add_argument('--output_dir', type=str, default='output', help='输出目录')
    
    args = parser.parse_args()
    
    print("📊 生成分析报告...")
    
    # 读取分析结果
    papers, csv_file = read_csv_results(args.output_dir)
    summary_data = read_summary_results(args.output_dir)
    run_info = read_run_info(args.output_dir)
    
    if not papers:
        print("❌ 未找到分析结果文件")
        return
    
    print(f"✅ 读取到 {len(papers)} 篇论文的分析结果")
    
    # 生成Markdown报告
    md_path = generate_markdown_report(papers, summary_data, run_info, args.output_dir)
    print(f"✅ Markdown报告已生成: {md_path}")
    
    # 生成JSON摘要
    json_path = generate_json_summary(papers, summary_data, run_info, args.output_dir)
    print(f"✅ JSON摘要已生成: {json_path}")
    
    print("🎉 报告生成完成！")


if __name__ == "__main__":
    main()
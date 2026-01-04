#!/usr/bin/env python3
"""
性能测试脚本 - 测试优化后的性能改进
"""

import time
import json
from pathlib import Path
from scripts.fetch_papers import PaperFetcher
from scripts.generate_html import HTMLGenerator


def test_paper_classification():
    """测试论文分类性能"""
    print("=" * 60)
    print("测试论文分类性能")
    print("=" * 60)
    
    fetcher = PaperFetcher()
    
    # 加载测试数据
    data_file = Path("data/papers.json")
    if not data_file.exists():
        print("未找到测试数据文件")
        return
    
    with open(data_file, 'r', encoding='utf-8') as f:
        papers = json.load(f)
    
    # 测试分类性能（只测试前100篇以节省时间）
    test_papers = papers[:100]
    
    start_time = time.time()
    for paper in test_papers:
        tags = fetcher.classify_paper(paper)
    end_time = time.time()
    
    elapsed = end_time - start_time
    print(f"✅ 分类 {len(test_papers)} 篇论文耗时: {elapsed:.3f} 秒")
    print(f"   平均每篇: {elapsed/len(test_papers)*1000:.2f} 毫秒")


def test_venue_extraction():
    """测试会议期刊提取性能"""
    print("\n" + "=" * 60)
    print("测试会议期刊提取性能")
    print("=" * 60)
    
    fetcher = PaperFetcher()
    
    test_comments = [
        "Accepted to CVPR 2025",
        "ICML 2024",
        "preprint",
        None,
        "IEEE Transactions on Pattern Analysis",
        "To appear in NeurIPS 2024",
        "ICCV 2023 Oral Presentation"
    ] * 100  # 重复100次以获得更准确的计时
    
    start_time = time.time()
    for comment in test_comments:
        venue = fetcher.extract_venue_from_comment(comment)
    end_time = time.time()
    
    elapsed = end_time - start_time
    print(f"✅ 提取 {len(test_comments)} 个会议信息耗时: {elapsed:.3f} 秒")
    print(f"   平均每个: {elapsed/len(test_comments)*1000:.2f} 毫秒")


def test_html_generation():
    """测试HTML生成性能"""
    print("\n" + "=" * 60)
    print("测试HTML生成性能")
    print("=" * 60)
    
    generator = HTMLGenerator()
    generator.load_papers()
    
    if not generator.papers:
        print("未加载到论文数据")
        return
    
    # 测试HTML生成
    start_time = time.time()
    html = generator.generate_papers_html()
    end_time = time.time()
    
    elapsed = end_time - start_time
    print(f"✅ 生成 {len(generator.papers)} 篇论文的HTML耗时: {elapsed:.3f} 秒")
    print(f"   HTML大小: {len(html) / 1024 / 1024:.2f} MB")


def main():
    """主函数"""
    print("\n🚀 开始性能测试\n")
    
    try:
        test_paper_classification()
        test_venue_extraction()
        test_html_generation()
        
        print("\n" + "=" * 60)
        print("✨ 所有性能测试完成！")
        print("=" * 60)
        print("\n主要优化点：")
        print("1. 预编译正则表达式模式，避免重复编译")
        print("2. 缓存小写文本，避免重复字符串操作")
        print("3. 分类时使用早期退出，找到匹配后立即跳过")
        print("4. HTML生成使用join而不是字符串拼接")
        print("5. CSS/JS生成前检查文件是否改变，避免不必要的写入")
        print("6. JavaScript端缓存DOM文本内容，避免重复调用textContent")
        print("7. 搜索输入添加300ms防抖，减少不必要的过滤操作")
        print("8. 使用CSS类隐藏元素而非内联样式，提升渲染性能")
        
    except Exception as e:
        print(f"\n❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

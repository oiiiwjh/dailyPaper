#!/usr/bin/env python3
"""
生成静态网页脚本
将论文数据生成为 HTML 页面
"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HTMLGenerator:
    """HTML 生成器"""
    
    def __init__(self, data_path: str = "data/papers.json", 
                 output_dir: str = "docs"):
        self.data_path = Path(data_path)
        self.output_dir = Path(output_dir)
        self.papers = []
        
    def load_papers(self):
        """加载论文数据"""
        if not self.data_path.exists():
            logger.warning(f"数据文件不存在: {self.data_path}")
            return
        
        with open(self.data_path, 'r', encoding='utf-8') as f:
            self.papers = json.load(f)
        
        logger.info(f"加载了 {len(self.papers)} 篇论文")
    
    def generate_index_html(self):
        """生成主页 HTML"""
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DailyPaper - AI/ML/CV/NLP 最新论文</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <div class="container">
            <h1>📚 DailyPaper</h1>
            <p class="subtitle">每日自动更新 AI/ML/CV/NLP 领域最新论文</p>
            <p class="update-time">最后更新: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} UTC</p>
        </div>
    </header>
    
    <nav class="container">
        <div class="filter-section">
            <div class="filter-group">
                <label class="filter-label">📌 发表状态：</label>
                <div class="filters status-filters">
                    <button class="filter-btn status-btn active" data-status="all">全部 ({len(self.papers)})</button>
                    <button class="filter-btn status-btn" data-status="published">已发表 ({sum(1 for p in self.papers if p.get('conference'))})</button>
                    <button class="filter-btn status-btn" data-status="preprint">预印本 ({sum(1 for p in self.papers if not p.get('conference'))})</button>
                </div>
            </div>
            <div class="filter-group">
                <label class="filter-label">🏷️ 研究领域：</label>
                <div class="filters category-filters">
                    <button class="filter-btn category-btn active" data-category="all">全部</button>
                    <button class="filter-btn category-btn" data-category="Computer Vision">Computer Vision</button>
                    <button class="filter-btn category-btn" data-category="Natural Language Processing">NLP</button>
                    <button class="filter-btn category-btn" data-category="Machine Learning">Machine Learning</button>
                    <button class="filter-btn category-btn" data-category="Robotics">Robotics</button>
                    <button class="filter-btn category-btn" data-category="Multimodal">Multimodal</button>
                </div>
            </div>
        </div>
        <div class="search-box">
            <input type="text" id="searchInput" placeholder="🔍 搜索论文标题、作者、摘要...">
        </div>
    </nav>
    
    <main class="container">
        <div id="papers-container">
            {self.generate_papers_html()}
        </div>
    </main>
    
    <footer>
        <div class="container">
            <p>© 2025 DailyPaper | 数据来源: ArXiv | <a href="https://github.com/yourusername/DailyPaper" target="_blank">GitHub</a></p>
        </div>
    </footer>
    
    <script src="js/main.js"></script>
</body>
</html>
"""
        
        output_file = self.output_dir / "index.html"
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        
        logger.info(f"生成主页: {output_file}")
    
    def get_category_name(self, category: str) -> str:
        """将 ArXiv 类别代码转换为友好的名称"""
        category_map = {
            'cs.AI': 'Artificial Intelligence',
            'cs.CV': 'Computer Vision',
            'cs.CL': 'Computational Linguistics (NLP)',
            'cs.LG': 'Machine Learning',
            'cs.IR': 'Information Retrieval',
            'cs.RO': 'Robotics',
            'cs.NE': 'Neural and Evolutionary Computing',
            'cs.CR': 'Cryptography and Security',
            'cs.HC': 'Human-Computer Interaction',
            'cs.MM': 'Multimedia',
            'stat.ML': 'Machine Learning (Statistics)',
        }
        return category_map.get(category, category)
    
    def generate_papers_html(self) -> str:
        """生成论文列表 HTML"""
        if not self.papers:
            return '<p class="no-results">暂无论文数据</p>'
        
        html_parts = []
        for paper in self.papers:
            tags_html = ''.join([f'<span class="tag">{tag}</span>' for tag in paper.get('tags', [])])
            authors_html = ', '.join(paper['authors'][:5])
            if len(paper['authors']) > 5:
                authors_html += ' et al.'
            
            # 获取友好的类别名称
            primary_category = paper.get('primary_category', paper['venue'])
            category_name = self.get_category_name(primary_category)
            
            # 构建来源信息 - 优先显示会议/期刊
            conference = paper.get('conference')
            if conference:
                # 如果有会议/期刊信息，优先显示
                source_info = f"📍 {conference}"
                source_class = "conference"
            else:
                # 否则显示 ArXiv 预印本
                source_info = f"📄 ArXiv Preprint ({category_name})"
                source_class = "preprint"
            
            # 确定发表状态
            is_published = 'published' if conference else 'preprint'
            
            paper_html = f"""
            <article class="paper-card" data-tags="{','.join(paper.get('tags', []))}" data-status="{is_published}">
                <h2 class="paper-title">
                    <a href="{paper['arxiv_url']}" target="_blank">{paper['title']}</a>
                </h2>
                <div class="paper-meta">
                    <span class="meta-item">📅 {paper['published']}</span>
                    <span class="meta-item venue-{source_class}">{source_info}</span>
                </div>
                <div class="paper-authors">
                    👥 {authors_html}
                </div>
                <div class="paper-tags">
                    {tags_html}
                </div>
                <div class="paper-abstract">
                    <details>
                        <summary>查看摘要</summary>
                        <p>{paper['abstract']}</p>
                    </details>
                </div>
                <div class="paper-links">
                    <a href="{paper['pdf_url']}" target="_blank" class="btn-link">📄 PDF</a>
                    <a href="{paper['arxiv_url']}" target="_blank" class="btn-link">🔗 ArXiv</a>
                </div>
            </article>
            """
            html_parts.append(paper_html)
        
        return '\n'.join(html_parts)
    
    def generate_css(self):
        """生成 CSS 样式"""
        css = """/* 全局样式 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    line-height: 1.6;
    color: #333;
    background-color: #f5f5f5;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* 头部样式 */
header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2rem 0;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

header h1 {
    font-size: 2.5rem;
    margin-bottom: 0.5rem;
}

.subtitle {
    font-size: 1.1rem;
    opacity: 0.9;
}

.update-time {
    font-size: 0.9rem;
    opacity: 0.8;
    margin-top: 0.5rem;
}

/* 导航和筛选 */
nav {
    background: white;
    padding: 1.5rem 20px;
    margin: 2rem auto;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.filter-section {
    margin-bottom: 1rem;
}

.filter-group {
    margin-bottom: 1rem;
}

.filter-label {
    display: inline-block;
    font-weight: 600;
    color: #333;
    margin-bottom: 0.5rem;
    font-size: 0.95rem;
}

.filters {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.filter-btn {
    padding: 0.5rem 1rem;
    border: 2px solid #667eea;
    background: white;
    color: #667eea;
    border-radius: 20px;
    cursor: pointer;
    transition: all 0.3s;
    font-size: 0.9rem;
}

.filter-btn:hover {
    background: #f0f0f0;
}

.filter-btn.active {
    background: #667eea;
    color: white;
}

.search-box {
    margin-top: 1.5rem;
}

.search-box input {
    width: 100%;
    padding: 0.8rem;
    border: 2px solid #ddd;
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.3s;
}

.search-box input:focus {
    outline: none;
    border-color: #667eea;
}

/* 主内容区域 */
main {
    margin-top: 0;
}

#papers-container {
    margin-top: 1rem;
}

/* 论文卡片 */
.paper-card {
    background: white;
    padding: 1.5rem;
    margin-bottom: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    transition: transform 0.3s, box-shadow 0.3s;
}

.paper-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.paper-title {
    font-size: 1.3rem;
    margin-bottom: 0.8rem;
}

.paper-title a {
    color: #333;
    text-decoration: none;
    transition: color 0.3s;
}

.paper-title a:hover {
    color: #667eea;
}

.paper-meta {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 0.8rem;
    font-size: 0.9rem;
    color: #666;
}

.meta-item.venue-conference {
    color: #2e7d32;
    font-weight: 600;
    background: #e8f5e9;
    padding: 0.2rem 0.6rem;
    border-radius: 4px;
}

.meta-item.venue-preprint {
    color: #666;
}

.paper-authors {
    margin-bottom: 0.8rem;
    color: #555;
    font-size: 0.95rem;
}

.paper-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

.tag {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    background: #e3f2fd;
    color: #1976d2;
    border-radius: 15px;
    font-size: 0.85rem;
}

.paper-abstract {
    margin-bottom: 1rem;
}

.paper-abstract details summary {
    cursor: pointer;
    color: #667eea;
    font-weight: 500;
    user-select: none;
}

.paper-abstract details[open] summary {
    margin-bottom: 0.5rem;
}

.paper-abstract p {
    color: #555;
    line-height: 1.8;
    text-align: justify;
}

.paper-links {
    display: flex;
    gap: 1rem;
}

.btn-link {
    padding: 0.5rem 1rem;
    background: #667eea;
    color: white;
    text-decoration: none;
    border-radius: 5px;
    font-size: 0.9rem;
    transition: background 0.3s;
}

.btn-link:hover {
    background: #5568d3;
}

/* 底部 */
footer {
    background: #333;
    color: white;
    text-align: center;
    padding: 2rem 0;
    margin-top: 3rem;
}

footer a {
    color: #667eea;
    text-decoration: none;
}

/* 无结果提示 */
.no-results {
    text-align: center;
    padding: 3rem;
    color: #999;
    font-size: 1.1rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
    header h1 {
        font-size: 2rem;
    }
    
    .filters {
        justify-content: center;
    }
    
    .paper-meta {
        flex-direction: column;
        gap: 0.3rem;
    }
}
"""
        
        css_dir = self.output_dir / "css"
        css_dir.mkdir(parents=True, exist_ok=True)
        
        with open(css_dir / "style.css", 'w', encoding='utf-8') as f:
            f.write(css)
        
        logger.info("生成 CSS 样式文件")
    
    def generate_js(self):
        """生成 JavaScript 文件"""
        js = """// 筛选和搜索功能
document.addEventListener('DOMContentLoaded', function() {
    const statusBtns = document.querySelectorAll('.status-btn');
    const categoryBtns = document.querySelectorAll('.category-btn');
    const searchInput = document.getElementById('searchInput');
    const papers = document.querySelectorAll('.paper-card');
    
    let currentStatus = 'all';
    let currentCategory = 'all';
    let searchTerm = '';
    
    // 发表状态筛选按钮点击事件
    statusBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // 更新按钮状态
            statusBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            currentStatus = this.dataset.status;
            filterPapers();
        });
    });
    
    // 研究领域筛选按钮点击事件
    categoryBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            // 更新按钮状态
            categoryBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            currentCategory = this.dataset.category;
            filterPapers();
        });
    });
    
    // 搜索输入事件
    searchInput.addEventListener('input', function() {
        searchTerm = this.value.toLowerCase();
        filterPapers();
    });
    
    // 筛选论文
    function filterPapers() {
        let visibleCount = 0;
        
        papers.forEach(paper => {
            const tags = paper.dataset.tags.split(',');
            const status = paper.dataset.status;
            const text = paper.textContent.toLowerCase();
            
            // 检查发表状态筛选
            const matchStatus = currentStatus === 'all' || status === currentStatus;
            
            // 检查研究领域筛选
            const matchCategory = currentCategory === 'all' || tags.includes(currentCategory);
            
            // 检查搜索关键词
            const matchSearch = searchTerm === '' || text.includes(searchTerm);
            
            if (matchStatus && matchCategory && matchSearch) {
                paper.style.display = 'block';
                visibleCount++;
            } else {
                paper.style.display = 'none';
            }
        });
        
        // 显示无结果提示
        const container = document.getElementById('papers-container');
        let noResults = container.querySelector('.no-results');
        
        if (visibleCount === 0) {
            if (!noResults) {
                noResults = document.createElement('p');
                noResults.className = 'no-results';
                noResults.textContent = '未找到匹配的论文';
                container.appendChild(noResults);
            }
        } else {
            if (noResults) {
                noResults.remove();
            }
        }
    }
});
"""
        
        js_dir = self.output_dir / "js"
        js_dir.mkdir(parents=True, exist_ok=True)
        
        with open(js_dir / "main.js", 'w', encoding='utf-8') as f:
            f.write(js)
        
        logger.info("生成 JavaScript 文件")
    
    def run(self):
        """运行生成流程"""
        logger.info("开始生成静态网页...")
        
        self.load_papers()
        self.generate_css()
        self.generate_js()
        self.generate_index_html()
        
        logger.info(f"网页生成完成! 输出目录: {self.output_dir}")


def main():
    generator = HTMLGenerator()
    generator.run()


if __name__ == "__main__":
    main()

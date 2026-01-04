// 筛选和搜索功能 - 优化版本
document.addEventListener('DOMContentLoaded', function() {
    const statusBtns = document.querySelectorAll('.status-btn');
    const categoryBtns = document.querySelectorAll('.category-btn');
    const searchInput = document.getElementById('searchInput');
    const papers = document.querySelectorAll('.paper-card');
    
    let currentStatus = 'all';
    let currentCategory = 'all';
    let searchTerm = '';
    
    // Cache paper data for better performance
    const paperCache = [];
    papers.forEach(paper => {
        paperCache.push({
            element: paper,
            tags: paper.dataset.tags.split(','),
            status: paper.dataset.status,
            // Cache lowercase text content once instead of recalculating
            textContent: paper.textContent.toLowerCase()
        });
    });
    
    // Debounce function for search input
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
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
    
    // 搜索输入事件 - 使用防抖优化
    searchInput.addEventListener('input', debounce(function() {
        searchTerm = this.value.toLowerCase();
        filterPapers();
    }, 300));
    
    // 筛选论文 - 优化版本，使用CSS类而非内联样式
    function filterPapers() {
        let visibleCount = 0;
        
        paperCache.forEach(paper => {
            // 检查发表状态筛选
            const matchStatus = currentStatus === 'all' || paper.status === currentStatus;
            
            // 检查研究领域筛选
            const matchCategory = currentCategory === 'all' || paper.tags.includes(currentCategory);
            
            // 检查搜索关键词 - 使用缓存的文本内容
            const matchSearch = searchTerm === '' || paper.textContent.includes(searchTerm);
            
            if (matchStatus && matchCategory && matchSearch) {
                paper.element.classList.remove('hidden');
                visibleCount++;
            } else {
                paper.element.classList.add('hidden');
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

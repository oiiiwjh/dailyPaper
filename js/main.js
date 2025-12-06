// 筛选和搜索功能
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

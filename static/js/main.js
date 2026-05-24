// ==========================================
// 全局工具函数
// ==========================================

/** HTML 转义（防 XSS） */
function escapeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str || '';
    return div.innerHTML;
}

/** 弹出 Toast 提示 */
function showToast(msg, type = 'success') {
    const el = document.createElement('div');
    el.className = `toast align-items-center text-bg-${type} border-0 position-fixed bottom-0 end-0 m-3`;
    el.setAttribute('role', 'alert');
    el.innerHTML = `<div class="d-flex">
        <div class="toast-body">${escapeHtml(msg)}</div>
        <button class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button></div>`;
    document.body.appendChild(el);
    const bs = bootstrap.Toast.getOrCreateInstance(el);
    bs.show();
    el.addEventListener('hidden.bs.toast', () => el.remove());
}

/** 获取 API 数据，401 时自动跳转登录 */
async function apiFetch(url, options = {}) {
    const res = await fetch(url, options);
    if (res.status === 401) {
        window.location.href = '/login';
        throw new Error('Unauthorized');
    }
    return res;
}

/** 格式化价格为显示字符串 */
function fmtPrice(val) {
    return Number(val).toFixed(2);
}

// ==========================================
// 全局退出登录
// ==========================================
async function logout() {
    await fetch('/api/auth/logout');
    window.location.href = '/login';
}

// ==========================================
// 订单状态映射
// ==========================================
const ORDER_STATUS = {
    pending:   { label: '待处理',  cls: 'bg-warning text-dark' },
    confirmed: { label: '已确认',  cls: 'bg-info text-dark' },
    completed: { label: '已完成',  cls: 'bg-success' },
    cancelled: { label: '已取消',  cls: 'bg-secondary' }
};

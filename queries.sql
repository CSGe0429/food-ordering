-- ============================================================================
--  在线点单系统 — 常用查询示例
--  数据库课程作业 — 展示多表连接、聚合、子查询等核心 SQL 操作
-- ============================================================================
USE online_ordering;

-- ==========================================
-- 1. 查询所有菜品及其分类（INNER JOIN）
-- ==========================================
SELECT m.id, m.name AS item_name, c.name AS category, m.price
FROM menu_items m
JOIN categories c ON m.category_id = c.id
WHERE m.is_available = 1
ORDER BY c.sort_order, m.id;

-- ==========================================
-- 2. 查询各分类下的菜品数量（GROUP BY + 聚合）
-- ==========================================
SELECT c.name AS category, COUNT(m.id) AS item_count,
       COALESCE(MIN(m.price), 0) AS min_price,
       COALESCE(MAX(m.price), 0) AS max_price
FROM categories c
LEFT JOIN menu_items m ON c.id = m.category_id AND m.is_available = 1
GROUP BY c.id, c.name
ORDER BY c.sort_order;

-- ==========================================
-- 3. 查询某个用户的订单列表（多表关联）
-- ==========================================
SELECT o.id AS order_id, o.total_amount, o.status,
       o.delivery_address, o.created_at,
       COUNT(oi.id) AS item_count
FROM orders o
LEFT JOIN order_items oi ON o.id = oi.order_id
WHERE o.user_id = 1
GROUP BY o.id
ORDER BY o.created_at DESC;

-- ==========================================
-- 4. 查询某个订单的完整详情
-- ==========================================
SELECT oi.id, mi.name AS item_name, oi.quantity,
       oi.unit_price, (oi.quantity * oi.unit_price) AS subtotal
FROM order_items oi
JOIN menu_items mi ON oi.menu_item_id = mi.id
WHERE oi.order_id = 1;

-- ==========================================
-- 5. 计算总销售额（聚合查询）
-- ==========================================
SELECT COUNT(*)                               AS total_orders,
       COALESCE(SUM(total_amount), 0)         AS total_revenue,
       COALESCE(AVG(total_amount), 0)         AS avg_order_value
FROM orders
WHERE status != 'cancelled';

-- ==========================================
-- 6. 各菜品销量排行（TOP N 查询）
-- ==========================================
SELECT mi.name,
       SUM(oi.quantity)       AS total_sold,
       SUM(oi.quantity * oi.unit_price) AS total_revenue
FROM order_items oi
JOIN menu_items mi ON oi.menu_item_id = mi.id
JOIN orders o ON oi.order_id = o.id
WHERE o.status != 'cancelled'
GROUP BY mi.id, mi.name
ORDER BY total_sold DESC
LIMIT 10;

-- ==========================================
-- 7. 查询今日订单（日期筛选）
-- ==========================================
SELECT id, total_amount, status, created_at
FROM orders
WHERE DATE(created_at) = CURDATE()
ORDER BY created_at DESC;

-- ==========================================
-- 8. 查询某用户的购物车（多表关联）
-- ==========================================
SELECT ci.id, mi.name, mi.price, ci.quantity,
       (mi.price * ci.quantity) AS subtotal
FROM cart_items ci
JOIN menu_items mi ON ci.menu_item_id = mi.id
WHERE ci.user_id = 1;

-- ==========================================
-- 9. 统计各状态订单数量（分组统计）
-- ==========================================
SELECT status, COUNT(*) AS count
FROM orders
GROUP BY status;

-- ==========================================
-- 10. 找出下单最多的用户（子查询 + TOP N）
-- ==========================================
SELECT u.username, COUNT(o.id) AS order_count,
       COALESCE(SUM(o.total_amount), 0) AS total_spent
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.status != 'cancelled'
GROUP BY u.id, u.username
ORDER BY order_count DESC
LIMIT 5;

-- ==========================================
-- 11. 事务示例：下单操作
-- ==========================================
-- START TRANSACTION;
-- INSERT INTO orders (user_id, total_amount, delivery_address)
--      VALUES (1, 56.00, '北京市朝阳区');
-- SET @order_id = LAST_INSERT_ID();
-- INSERT INTO order_items (order_id, menu_item_id, quantity, unit_price)
--      VALUES (@order_id, 1, 2, 28.00);
-- DELETE FROM cart_items WHERE user_id = 1;
-- COMMIT;
-- -- 如果任一步骤失败：ROLLBACK;

-- ==========================================
-- 12. 创建视图：订单汇总
-- ==========================================
-- CREATE VIEW v_order_summary AS
-- SELECT o.id, u.username, o.total_amount, o.status,
--        o.delivery_address, o.created_at,
--        COUNT(oi.id) AS item_count
-- FROM orders o
-- JOIN users u ON o.user_id = u.id
-- LEFT JOIN order_items oi ON o.id = oi.order_id
-- GROUP BY o.id;

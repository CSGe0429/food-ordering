-- ============================================================================
--  在线点单系统 — 数据库建表脚本
--  数据库课程作业
--  使用方法: mysql -u root -p < init_db.sql
-- ============================================================================
--                          ER 关系说明
--  ┌──────────┐       ┌──────────────┐       ┌────────────┐
--  │  users   │1────N│    orders    │1────N│ order_items│N────1│ menu_items │
--  └──────────┘       └──────────────┘       └────────────┘       └────────────┘
--       │                                                              │
--       1                                                              N
--       │                                                              │
--       N                                                              1
--  ┌──────────┐                                                  ┌────────────┐
--  │cart_items│N────────────────────────────────────────────1│ categories │
--  └──────────┘                                                  └────────────┘
-- ============================================================================

CREATE DATABASE IF NOT EXISTS online_ordering
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE online_ordering;

-- ========================================
-- 1. 用户表
-- ========================================
CREATE TABLE users (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    username    VARCHAR(50)  NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    phone       VARCHAR(20),
    address     VARCHAR(200),
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- ========================================
-- 2. 菜品分类表
-- ========================================
CREATE TABLE categories (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(50) NOT NULL,
    sort_order INT DEFAULT 0
) ENGINE=InnoDB;

-- ========================================
-- 3. 菜品表
-- ========================================
CREATE TABLE menu_items (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    name         VARCHAR(100)   NOT NULL,
    description  VARCHAR(500),
    price        DECIMAL(10, 2) NOT NULL,
    image_url    VARCHAR(300),
    category_id  INT            NOT NULL,
    is_available TINYINT(1)     DEFAULT 1,
    FOREIGN KEY (category_id) REFERENCES categories(id)
) ENGINE=InnoDB;

-- ========================================
-- 4. 购物车表
-- ========================================
CREATE TABLE cart_items (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    user_id      INT  NOT NULL,
    menu_item_id INT  NOT NULL,
    quantity     INT  NOT NULL DEFAULT 1,
    FOREIGN KEY (user_id)      REFERENCES users(id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
) ENGINE=InnoDB;

-- ========================================
-- 5. 订单表
-- ========================================
CREATE TABLE orders (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    user_id          INT            NOT NULL,
    total_amount     DECIMAL(10, 2) NOT NULL,
    status           ENUM('pending','confirmed','completed','cancelled')
                     DEFAULT 'pending',
    delivery_address VARCHAR(200)   NOT NULL,
    notes            VARCHAR(300),
    created_at       DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB;

-- ========================================
-- 6. 订单明细表（快照下单时单价）
-- ========================================
CREATE TABLE order_items (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    order_id     INT            NOT NULL,
    menu_item_id INT            NOT NULL,
    quantity     INT            NOT NULL,
    unit_price   DECIMAL(10, 2) NOT NULL COMMENT '下单时单价，防止菜品涨价影响历史订单',
    FOREIGN KEY (order_id)     REFERENCES orders(id),
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id)
) ENGINE=InnoDB;

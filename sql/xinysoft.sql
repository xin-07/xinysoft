/*
 Navicat Premium Dump SQL

 Source Server         : 127.0.0.1
 Source Server Type    : MySQL
 Source Server Version : 80409 (8.4.9)
 Source Host           : localhost:3306
 Source Schema         : xinysoft

 Target Server Type    : MySQL
 Target Server Version : 80409 (8.4.9)
 File Encoding         : 65001

 Date: 10/06/2026 18:51:17
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for profile
-- ----------------------------
DROP TABLE IF EXISTS `profile`;
CREATE TABLE `profile`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'xiny' COMMENT '姓名',
  `avatar_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '头像URL',
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '头衔',
  `bio` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '个人简介',
  `tech_tags` json NULL COMMENT '技术标签数组',
  `github` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT 'GitHub 链接',
  `gitee` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT 'Gitee 链接',
  `wechat` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '微信号',
  `qq` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT 'QQ号',
  `email` json NULL COMMENT '邮箱列表（JSON数组）',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '个人信息表（前台展示）' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of profile
-- ----------------------------
INSERT INTO `profile` VALUES (1, 'xiny', 'D:\\File\\photos\\落日.jpg', '全栈开发工程师 · AI Agent 探索者', '持续追踪 AI Agent 前沿技术，通过实践快速掌握。具备跨专业协作能力，坚持每周技术复盘。', '[\"Vue3\", \"FastAPI\", \"MySQL\", \"OpenClaw\", \"HarmonyOS\", \"ECharts\"]', 'https://github.com/xin-07', 'https://gitee.com/xin-keep-going', 'Yyk-293342', '2074835619', '[\"2074835619@qq.com\", \"xin_y0607@outlook.com\", \"xiny0607.23@gmail.com\", \"13886527881@163.com\"]', '2026-06-09 18:50:32', '2026-06-10 13:58:04');

-- ----------------------------
-- Table structure for projects
-- ----------------------------
DROP TABLE IF EXISTS `projects`;
CREATE TABLE `projects`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '项目名称',
  `subtitle` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '项目副标题',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '项目描述',
  `tech_stack` json NULL COMMENT '技术栈数组，如 [\"Vue3\", \"FastAPI\"]',
  `cover_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '封面图URL（本地路径或网络URL）',
  `screenshots` json NULL COMMENT '截图列表',
  `live_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '线上地址（可选，非上线项目为NULL）',
  `repo_url` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '源码地址（可选，闭源项目为NULL）',
  `is_featured` tinyint(1) NULL DEFAULT 0 COMMENT '是否精选（首页展示）',
  `sort_order` int NULL DEFAULT 0 COMMENT '排序权重（越大越靠前）',
  `status` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT 'published' COMMENT '状态: draft/published',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '项目作品集表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of projects
-- ----------------------------
INSERT INTO `projects` VALUES (1, '智能路径规划与物流配送系统', '鲜途智送 · 物流配送智能管理平台', '基于 Vue 3 的智能路径优化与物流配送管理系统，集成天地图 API，提供路径规划、团队协作、仓库管理、大屏数据可视化等功能。后端采用 Flask 框架，使用混合蚁群-粒子群优化算法解决车辆路径问题(VRP)，实现高效的配送路线规划。', '[\"Vue 3\", \"Vite\", \"Three.js\", \"天地图 API\", \"ECharts\", \"Flask\", \"MySQL\", \"Redis\", \"蚂蚁群+粒子群混合算法\"]', NULL, NULL, 'https://smile050417.site/', NULL, 1, 3, 'published', '2026-06-10 18:50:40', '2026-06-10 18:50:40');
INSERT INTO `projects` VALUES (2, '昕悦读 分布式小说阅读系统', 'HarmonyOS 原生小说阅读应用', '基于 HarmonyOS（鸿蒙）平台开发的小说阅读应用，采用 Spring Boot 微服务架构与 MySQL 数据库，前端使用 ArkTS + ArkUI 构建原生鸿蒙界面。支持多本书籍在线阅读、用户登录注册、阅读进度同步等功能。', '[\"Spring Boot\", \"MySQL\", \"MyBatis\", \"ArkTS\", \"ArkUI\", \"HarmonyOS\"]', NULL, NULL, NULL, NULL, 1, 2, 'published', '2026-06-10 18:50:40', '2026-06-10 18:50:40');
INSERT INTO `projects` VALUES (3, 'xinysoft 个人作品集', 'Vue 3 + FastAPI 全栈个人网站', '基于 Vue 3 + Vite 构建的个人作品集网站，后端使用 FastAPI + MySQL 提供 API 服务。包含个人资料展示、项目作品集、主题切换、响应式设计等功能，用于展示个人品牌与技术能力。', '[\"Vue 3\", \"Vite\", \"Vue Router\", \"FastAPI\", \"MySQL\", \"PyMySQL\"]', NULL, NULL, NULL, NULL, 1, 1, 'published', '2026-06-10 18:50:40', '2026-06-10 18:50:40');

SET FOREIGN_KEY_CHECKS = 1;

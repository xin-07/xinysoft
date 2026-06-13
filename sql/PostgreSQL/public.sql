/*
 Navicat Premium Dump SQL

 Source Server         : PostgreSQL127.0.0.1
 Source Server Type    : PostgreSQL
 Source Server Version : 180004 (180004)
 Source Host           : localhost:5432
 Source Catalog        : xinysoftdb
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 180004 (180004)
 File Encoding         : 65001

 Date: 13/06/2026 15:52:56
*/


-- ----------------------------
-- Sequence structure for admin_users_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."admin_users_id_seq";
CREATE SEQUENCE "public"."admin_users_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for contact_messages_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."contact_messages_id_seq";
CREATE SEQUENCE "public"."contact_messages_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for profile_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."profile_id_seq";
CREATE SEQUENCE "public"."profile_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for projects_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."projects_id_seq";
CREATE SEQUENCE "public"."projects_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Table structure for admin_users
-- ----------------------------
DROP TABLE IF EXISTS "public"."admin_users";
CREATE TABLE "public"."admin_users" (
  "id" int4 NOT NULL DEFAULT nextval('admin_users_id_seq'::regclass),
  "username" varchar(50) COLLATE "pg_catalog"."default" NOT NULL,
  "password_hash" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;
COMMENT ON COLUMN "public"."admin_users"."id" IS '主键ID';
COMMENT ON COLUMN "public"."admin_users"."username" IS '管理员用户名';
COMMENT ON COLUMN "public"."admin_users"."password_hash" IS 'bcrypt密码哈希';
COMMENT ON COLUMN "public"."admin_users"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."admin_users"."updated_at" IS '更新时间（需在应用层手动更新）';
COMMENT ON TABLE "public"."admin_users" IS '管理员用户表';

-- ----------------------------
-- Records of admin_users
-- ----------------------------
INSERT INTO "public"."admin_users" VALUES (1, 'admin', '$2b$12$SH1xPO/EQ5cDB5wgeqtQzeJvMU4czyiXk17Wqw4TcpMp/FyrGYrJq', '2026-06-12 14:18:14', '2026-06-12 14:18:14');

-- ----------------------------
-- Table structure for contact_messages
-- ----------------------------
DROP TABLE IF EXISTS "public"."contact_messages";
CREATE TABLE "public"."contact_messages" (
  "id" int4 NOT NULL DEFAULT nextval('contact_messages_id_seq'::regclass),
  "name" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "email" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "message" text COLLATE "pg_catalog"."default" NOT NULL,
  "is_read" bool NOT NULL DEFAULT false,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;
COMMENT ON COLUMN "public"."contact_messages"."id" IS '主键ID';
COMMENT ON COLUMN "public"."contact_messages"."name" IS '发送者姓名';
COMMENT ON COLUMN "public"."contact_messages"."email" IS '发送者邮箱';
COMMENT ON COLUMN "public"."contact_messages"."message" IS '留言内容（最大1000字）';
COMMENT ON COLUMN "public"."contact_messages"."is_read" IS '是否已读: false=未读, true=已读';
COMMENT ON COLUMN "public"."contact_messages"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."contact_messages"."updated_at" IS '更新时间（需在应用层手动更新）';
COMMENT ON TABLE "public"."contact_messages" IS '访客留言表（P1功能预留）';

-- ----------------------------
-- Records of contact_messages
-- ----------------------------

-- ----------------------------
-- Table structure for profile
-- ----------------------------
DROP TABLE IF EXISTS "public"."profile";
CREATE TABLE "public"."profile" (
  "id" int4 NOT NULL DEFAULT nextval('profile_id_seq'::regclass),
  "name" varchar(50) COLLATE "pg_catalog"."default" NOT NULL DEFAULT 'xiny'::character varying,
  "avatar_url" varchar(255) COLLATE "pg_catalog"."default",
  "title" varchar(100) COLLATE "pg_catalog"."default",
  "bio" text COLLATE "pg_catalog"."default",
  "tech_tags" jsonb,
  "github" varchar(255) COLLATE "pg_catalog"."default",
  "gitee" varchar(255) COLLATE "pg_catalog"."default",
  "wechat" varchar(50) COLLATE "pg_catalog"."default",
  "qq" varchar(20) COLLATE "pg_catalog"."default",
  "email" jsonb,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;
COMMENT ON COLUMN "public"."profile"."id" IS '主键ID';
COMMENT ON COLUMN "public"."profile"."name" IS '姓名';
COMMENT ON COLUMN "public"."profile"."avatar_url" IS '头像URL';
COMMENT ON COLUMN "public"."profile"."title" IS '头衔';
COMMENT ON COLUMN "public"."profile"."bio" IS '个人简介';
COMMENT ON COLUMN "public"."profile"."tech_tags" IS '技术标签数组';
COMMENT ON COLUMN "public"."profile"."github" IS 'GitHub 链接';
COMMENT ON COLUMN "public"."profile"."gitee" IS 'Gitee 链接';
COMMENT ON COLUMN "public"."profile"."wechat" IS '微信号';
COMMENT ON COLUMN "public"."profile"."qq" IS 'QQ号';
COMMENT ON COLUMN "public"."profile"."email" IS '邮箱列表（JSON数组）';
COMMENT ON COLUMN "public"."profile"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."profile"."updated_at" IS '更新时间（需在应用层手动更新）';
COMMENT ON TABLE "public"."profile" IS '个人信息表（前台展示）';

-- ----------------------------
-- Records of profile
-- ----------------------------
INSERT INTO "public"."profile" VALUES (1, 'xiny', 'D:\File\photos\落日.jpg', '全栈开发工程师 · AI Agent 探索者', '持续追踪 AI Agent 前沿技术，通过实践快速掌握。具备跨专业协作能力，坚持每周技术复盘。', '["Vue3", "FastAPI", "MySQL", "OpenClaw", "HarmonyOS", "ECharts"]', 'https://github.com/xin-07', 'https://gitee.com/xin-keep-going', 'Yyk-293342', '2074835619', '["2074835619@qq.com", "xin_y0607@outlook.com", "xiny0607.23@gmail.com", "13886527881@163.com"]', '2026-06-09 18:50:32', '2026-06-10 13:58:04');

-- ----------------------------
-- Table structure for projects
-- ----------------------------
DROP TABLE IF EXISTS "public"."projects";
CREATE TABLE "public"."projects" (
  "id" int4 NOT NULL DEFAULT nextval('projects_id_seq'::regclass),
  "title" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "subtitle" varchar(200) COLLATE "pg_catalog"."default",
  "description" text COLLATE "pg_catalog"."default",
  "tech_stack" jsonb,
  "cover_url" varchar(255) COLLATE "pg_catalog"."default",
  "screenshots" jsonb,
  "live_url" varchar(255) COLLATE "pg_catalog"."default",
  "repo_url" varchar(255) COLLATE "pg_catalog"."default",
  "is_featured" bool DEFAULT false,
  "sort_order" int4 DEFAULT 0,
  "status" varchar(20) COLLATE "pg_catalog"."default" DEFAULT 'published'::character varying,
  "created_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP
)
;
COMMENT ON COLUMN "public"."projects"."id" IS '主键ID';
COMMENT ON COLUMN "public"."projects"."title" IS '项目名称';
COMMENT ON COLUMN "public"."projects"."subtitle" IS '项目副标题';
COMMENT ON COLUMN "public"."projects"."description" IS '项目描述';
COMMENT ON COLUMN "public"."projects"."tech_stack" IS '技术栈数组';
COMMENT ON COLUMN "public"."projects"."cover_url" IS '封面图URL';
COMMENT ON COLUMN "public"."projects"."screenshots" IS '截图列表';
COMMENT ON COLUMN "public"."projects"."live_url" IS '线上地址';
COMMENT ON COLUMN "public"."projects"."repo_url" IS '源码地址';
COMMENT ON COLUMN "public"."projects"."is_featured" IS '是否精选（首页展示）';
COMMENT ON COLUMN "public"."projects"."sort_order" IS '排序权重（越大越靠前）';
COMMENT ON COLUMN "public"."projects"."status" IS '状态: draft/published';
COMMENT ON COLUMN "public"."projects"."created_at" IS '创建时间';
COMMENT ON COLUMN "public"."projects"."updated_at" IS '更新时间（需在应用层手动更新）';
COMMENT ON TABLE "public"."projects" IS '项目作品集表';

-- ----------------------------
-- Records of projects
-- ----------------------------
INSERT INTO "public"."projects" VALUES (1, '智能路径规划与物流配送系统', '鲜途智送 · 物流配送智能管理平台', '基于 Vue 3 的智能路径优化与物流配送管理系统，集成天地图 API，提供路径规划、团队协作、仓库管理、大屏数据可视化等功能。后端采用 Flask 框架，使用混合蚁群-粒子群优化算法解决车辆路径问题(VRP)，实现高效的配送路线规划。', '["Vue 3", "Vite", "Three.js", "天地图 API", "ECharts", "Flask", "MySQL", "Redis", "蚂蚁群+粒子群混合算法"]', NULL, '["D:/Project/web/xinysoft_Vite/public/鲜途智送-首页.png", "D:/Project/web/xinysoft_Vite/public/鲜途智送-主页.png", "D:/Project/web/xinysoft_Vite/public/鲜途智送-底部订单管理.png"]', 'https://smile050417.site/', NULL, 't', 3, 'published', '2026-06-10 18:50:40', '2026-06-11 18:36:24');
INSERT INTO "public"."projects" VALUES (2, '昕悦读 分布式小说阅读系统', 'HarmonyOS 原生小说阅读应用', '基于 HarmonyOS（鸿蒙）平台开发的小说阅读应用，采用 Spring Boot 微服务架构与 MySQL 数据库，前端使用 ArkTS + ArkUI 构建原生鸿蒙界面。支持多本书籍在线阅读、用户登录注册、阅读进度同步等功能。', '["Spring Boot", "MySQL", "MyBatis", "ArkTS", "ArkUI", "HarmonyOS"]', NULL, NULL, NULL, NULL, 'f', 2, 'published', '2026-06-10 18:50:40', '2026-06-11 11:10:11');
INSERT INTO "public"."projects" VALUES (3, 'xinysoft 个人作品集', 'Vue 3 + FastAPI 全栈个人网站', '基于 Vue 3 + Vite 构建的个人作品集网站，后端使用 FastAPI + MySQL 提供 API 服务。包含个人资料展示、项目作品集、主题切换、响应式设计等功能，用于展示个人品牌与技术能力。', '["Vue 3", "Vite", "Vue Router", "FastAPI", "MySQL", "PyMySQL"]', NULL, NULL, NULL, NULL, 't', 1, 'published', '2026-06-10 18:50:40', '2026-06-10 18:50:40');

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."admin_users_id_seq"
OWNED BY "public"."admin_users"."id";
SELECT setval('"public"."admin_users_id_seq"', 1, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."contact_messages_id_seq"
OWNED BY "public"."contact_messages"."id";
SELECT setval('"public"."contact_messages_id_seq"', 1, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."profile_id_seq"
OWNED BY "public"."profile"."id";
SELECT setval('"public"."profile_id_seq"', 1, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."projects_id_seq"
OWNED BY "public"."projects"."id";
SELECT setval('"public"."projects_id_seq"', 3, true);

-- ----------------------------
-- Uniques structure for table admin_users
-- ----------------------------
ALTER TABLE "public"."admin_users" ADD CONSTRAINT "admin_users_username_key" UNIQUE ("username");

-- ----------------------------
-- Primary Key structure for table admin_users
-- ----------------------------
ALTER TABLE "public"."admin_users" ADD CONSTRAINT "admin_users_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table contact_messages
-- ----------------------------
ALTER TABLE "public"."contact_messages" ADD CONSTRAINT "contact_messages_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table profile
-- ----------------------------
ALTER TABLE "public"."profile" ADD CONSTRAINT "profile_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table projects
-- ----------------------------
ALTER TABLE "public"."projects" ADD CONSTRAINT "projects_pkey" PRIMARY KEY ("id");

/*
 Navicat Premium Data Transfer

 Source Server         : deepin
 Source Server Type    : MySQL
 Source Server Version : 50721
 Source Host           : localhost:3306
 Source Schema         : pydata

 Target Server Type    : MySQL
 Target Server Version : 50721
 File Encoding         : 65001

 Date: 10/11/2019 17:11:22
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for admin
-- ----------------------------
DROP TABLE IF EXISTS `admin`;
CREATE TABLE `admin`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `password` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `is_super` smallint(6) NULL DEFAULT NULL,
  `role_id` int(11) NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE,
  INDEX `role_id`(`role_id`) USING BTREE,
  INDEX `ix_admin_addtime`(`addtime`) USING BTREE,
  CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of admin
-- ----------------------------
INSERT INTO `admin` VALUES (1, 'crazy696', 'pbkdf2:sha256:150000$5j5og4Ph$a57ef3bac86f01b96d1b9bf589377bfcaa705951e4ca83eb658b00c657af0904', 0, 2, '2019-06-29 12:36:36');
INSERT INTO `admin` VALUES (2, 'crazy262', 'pbkdf2:sha256:150000$IDxupRUx$b16ce2155063e08d6dc39274212baff229fb4d17b752f40df725533c2e4c5309', 1, 5, '2019-06-29 20:54:48');
INSERT INTO `admin` VALUES (3, '233', 'pbkdf2:sha256:150000$rpaQexaz$3976ce0c9326558f3ab2a9028bed59c048b5b25c4166b62c8bb10b5b305896bc', 1, 6, '2019-08-09 22:36:38');
INSERT INTO `admin` VALUES (4, '666', 'pbkdf2:sha256:150000$305CBrlR$573ed94decb12ff9be3b8d91fc96db0099a67ec692f5daeba5bf633be7ed1302', 1, 7, '2019-08-10 21:10:31');
INSERT INTO `admin` VALUES (5, '55', 'pbkdf2:sha256:150000$ZpZKsuEZ$51556a7aec936ddfdbc4c7695023c32021ffa780bea37f662dd69b48b933274e', 1, 8, '2019-08-11 09:55:21');

-- ----------------------------
-- Table structure for adminlog
-- ----------------------------
DROP TABLE IF EXISTS `adminlog`;
CREATE TABLE `adminlog`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NULL DEFAULT NULL,
  `ip` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `sign_in_time` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `ix_adminlog_sign_in_time`(`sign_in_time`) USING BTREE,
  CONSTRAINT `adminlog_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `admin` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 35 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of adminlog
-- ----------------------------
INSERT INTO `adminlog` VALUES (1, 1, '127.0.0.1', '2019-07-21 17:16:38');
INSERT INTO `adminlog` VALUES (2, 1, '127.0.0.1', '2019-07-21 21:55:30');
INSERT INTO `adminlog` VALUES (3, 1, '127.0.0.1', '2019-07-22 20:09:43');
INSERT INTO `adminlog` VALUES (4, 1, '127.0.0.1', '2019-07-22 20:10:21');
INSERT INTO `adminlog` VALUES (5, 1, '127.0.0.1', '2019-07-22 20:10:46');
INSERT INTO `adminlog` VALUES (6, 1, '127.0.0.1', '2019-07-22 21:08:58');
INSERT INTO `adminlog` VALUES (7, 1, '127.0.0.1', '2019-07-22 21:09:58');
INSERT INTO `adminlog` VALUES (8, 1, '127.0.0.1', '2019-07-22 21:14:22');
INSERT INTO `adminlog` VALUES (9, 1, '127.0.0.1', '2019-07-22 21:14:58');
INSERT INTO `adminlog` VALUES (10, 1, '127.0.0.1', '2019-07-23 22:36:20');
INSERT INTO `adminlog` VALUES (11, 1, '127.0.0.1', '2019-07-25 19:37:31');
INSERT INTO `adminlog` VALUES (12, 1, '127.0.0.1', '2019-08-08 21:39:37');
INSERT INTO `adminlog` VALUES (13, 1, '127.0.0.1', '2019-08-09 21:51:41');
INSERT INTO `adminlog` VALUES (14, 1, '127.0.0.1', '2019-08-10 21:00:32');
INSERT INTO `adminlog` VALUES (15, 1, '127.0.0.1', '2019-08-11 09:23:22');
INSERT INTO `adminlog` VALUES (16, 5, '127.0.0.1', '2019-08-11 09:55:35');
INSERT INTO `adminlog` VALUES (17, 1, '127.0.0.1', '2019-08-12 22:01:50');
INSERT INTO `adminlog` VALUES (18, 1, '127.0.0.1', '2019-08-18 18:21:19');
INSERT INTO `adminlog` VALUES (19, 1, '127.0.0.1', '2019-08-19 19:52:52');
INSERT INTO `adminlog` VALUES (20, 1, '127.0.0.1', '2019-08-25 11:03:11');
INSERT INTO `adminlog` VALUES (21, 1, '127.0.0.1', '2019-08-29 21:47:38');
INSERT INTO `adminlog` VALUES (22, 1, '127.0.0.1', '2019-09-01 20:47:22');
INSERT INTO `adminlog` VALUES (23, 1, '127.0.0.1', '2019-09-09 21:03:56');
INSERT INTO `adminlog` VALUES (24, 1, '127.0.0.1', '2019-09-11 23:11:24');
INSERT INTO `adminlog` VALUES (25, 1, '127.0.0.1', '2019-09-11 23:13:14');
INSERT INTO `adminlog` VALUES (26, 1, '127.0.0.1', '2019-09-11 23:17:23');
INSERT INTO `adminlog` VALUES (27, 1, '127.0.0.1', '2019-09-12 22:51:06');
INSERT INTO `adminlog` VALUES (28, 1, '127.0.0.1', '2019-09-13 11:03:53');
INSERT INTO `adminlog` VALUES (29, 1, '127.0.0.1', '2019-09-15 20:27:59');
INSERT INTO `adminlog` VALUES (30, 1, '127.0.0.1', '2019-09-18 19:42:29');
INSERT INTO `adminlog` VALUES (31, 1, '127.0.0.1', '2019-09-19 21:07:22');
INSERT INTO `adminlog` VALUES (32, 1, '127.0.0.1', '2019-09-19 22:32:56');
INSERT INTO `adminlog` VALUES (33, 1, '127.0.0.1', '2019-09-20 20:09:46');
INSERT INTO `adminlog` VALUES (34, 1, '127.0.0.1', '2019-09-30 22:23:50');

-- ----------------------------
-- Table structure for auth
-- ----------------------------
DROP TABLE IF EXISTS `auth`;
CREATE TABLE `auth`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_auth_addtime`(`addtime`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 36 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of auth
-- ----------------------------
INSERT INTO `auth` VALUES (1, '添加标签', '/tag/add/', '2019-07-22 21:45:50');
INSERT INTO `auth` VALUES (2, '标签列表', '/tag/list/<int:page>/', '2019-08-08 21:57:44');
INSERT INTO `auth` VALUES (3, '删除标签', '/tag/del/<int:id>/', '2019-08-08 21:58:20');
INSERT INTO `auth` VALUES (4, '编辑标签', '/tag/edit/<int:id>/', '2019-08-08 21:58:59');
INSERT INTO `auth` VALUES (5, '添加电影', '/movie/add/', '2019-08-08 21:59:19');
INSERT INTO `auth` VALUES (6, '电影列表', '/movie/list/<int:page>/', '2019-08-10 15:17:52');
INSERT INTO `auth` VALUES (7, '删除电影', '/movie/del/<int:id>/', '2019-08-10 15:17:54');
INSERT INTO `auth` VALUES (8, '编辑电影', '/movie/edit/<int:id>/', '2019-08-10 15:17:56');
INSERT INTO `auth` VALUES (9, '添加预告', '/preview/add/', '2019-08-10 15:17:57');
INSERT INTO `auth` VALUES (10, '预告列表', '/preview/list/<int:page>/', '2019-08-10 15:17:58');
INSERT INTO `auth` VALUES (11, '删除预告', '/preview/del/<int:id>/', '2019-08-10 15:17:58');
INSERT INTO `auth` VALUES (12, '编辑预告', '/preview/edit/<int:id>/', '2019-08-10 15:17:59');
INSERT INTO `auth` VALUES (13, '会员列表', '/user/list/<int:page>/', '2019-08-10 15:18:00');
INSERT INTO `auth` VALUES (14, '会员详情页', '/user/view/<int:id>/', '2019-08-10 15:18:01');
INSERT INTO `auth` VALUES (15, '删除会员', '/user/del/<int:id>/', '2019-08-10 15:21:25');
INSERT INTO `auth` VALUES (16, '评论列表', '/comment/list/<int:page>/', '2019-08-10 15:21:26');
INSERT INTO `auth` VALUES (17, '删除评论', '/comment/del/<int:id>/', '2019-08-10 15:21:26');
INSERT INTO `auth` VALUES (18, '电影收藏', '/moviecol/list/<int:page>/', '2019-08-10 15:21:32');
INSERT INTO `auth` VALUES (19, '编辑电影收藏', '/moviecol/edit/<int:id>/', '2019-08-10 15:21:33');
INSERT INTO `auth` VALUES (20, '删除电影收藏', '/moviecol/del/<int:id>/', '2019-08-10 15:21:34');
INSERT INTO `auth` VALUES (21, '操作电影日志', '/oplog/list/<int:page>/', '2019-08-10 15:21:35');
INSERT INTO `auth` VALUES (22, '管理员登入日志', '/adminloginlog/list/<int:page>/', '2019-08-10 15:21:36');
INSERT INTO `auth` VALUES (23, '会员登入日志', '/userloginlog/list/<int:page>/', '2019-08-10 15:21:37');
INSERT INTO `auth` VALUES (24, '添加权限', '/auth/add/', '2019-08-10 15:21:38');
INSERT INTO `auth` VALUES (25, '权限列表', '/auth/list/<int:page>/', '2019-08-10 15:29:00');
INSERT INTO `auth` VALUES (26, '删除权限', '/auth/del/<int:id>/', '2019-08-10 15:29:02');
INSERT INTO `auth` VALUES (27, '编辑权限', '/auth/edit/<int:id>/', '2019-08-10 15:29:02');
INSERT INTO `auth` VALUES (28, '添加角色', '/role/add/', '2019-08-10 15:29:03');
INSERT INTO `auth` VALUES (29, '角色列表', '/role/list/<int:page>/', '2019-08-10 15:29:04');
INSERT INTO `auth` VALUES (30, '删除角色', '/role/del/<int:id>/', '2019-08-10 15:29:04');
INSERT INTO `auth` VALUES (31, '编辑角色', '/role/edit/<int:id>/', '2019-08-10 15:29:05');
INSERT INTO `auth` VALUES (32, '添加管理员', '/admin/add/', '2019-08-10 15:29:06');
INSERT INTO `auth` VALUES (33, '管理员列表', '/admin/list/<int:page>/', '2019-08-10 15:29:07');
INSERT INTO `auth` VALUES (34, '搜索标签', '/tag/list/search/<int:page>/', '2019-09-19 22:07:32');
INSERT INTO `auth` VALUES (35, '搜索电影', '/tag/list/search/<int:page>/', '2019-09-19 22:55:12');

-- ----------------------------
-- Table structure for comment
-- ----------------------------
DROP TABLE IF EXISTS `comment`;
CREATE TABLE `comment`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `content` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `movie_id` int(11) NULL DEFAULT NULL,
  `user_id` int(11) NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `content`(`content`) USING BTREE,
  INDEX `movie_id`(`movie_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `ix_comment_addtime`(`addtime`) USING BTREE,
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 27 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of comment
-- ----------------------------
INSERT INTO `comment` VALUES (22, '<p><img src=\"http://img.baidu.com/hi/tsj/t_0028.gif\"/></p>', 13, 2, '2019-09-13 13:53:02');
INSERT INTO `comment` VALUES (23, '<p>超好看的<img src=\"http://img.baidu.com/hi/jx2/j_0057.gif\"/></p>', 13, 2, '2019-09-13 14:01:00');
INSERT INTO `comment` VALUES (24, '<p>大雄傻逼吧</p>', 13, 2, '2019-09-13 14:03:28');
INSERT INTO `comment` VALUES (25, '<p><img src=\"http://img.baidu.com/hi/babycat/C_0006.gif\"/></p>', NULL, 2, '2019-09-13 14:52:39');
INSERT INTO `comment` VALUES (26, '<p><img src=\"http://img.baidu.com/hi/face/i_f03.gif\"/><img src=\"http://img.baidu.com/hi/bobo/B_0001.gif\"/></p>', 12, 4, '2019-09-13 22:16:54');

-- ----------------------------
-- Table structure for login
-- ----------------------------
DROP TABLE IF EXISTS `login`;
CREATE TABLE `login`  (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `password` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `cellphone_number` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `email` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `age` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `area` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`user_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of login
-- ----------------------------
INSERT INTO `login` VALUES (1, '不成熟不成熟', '123456', '134562', 'c15151', '13', '广东');
INSERT INTO `login` VALUES (2, '啊', '123', '159', '561', '66', '上海');
INSERT INTO `login` VALUES (3, 'crazy696', '689986', '13763958221', '447459298@qq.com', '16', '江西');
INSERT INTO `login` VALUES (4, 'crazy696', '689986', '13763958221', '44749298@qq.com', '2000-08-08T11:27', '广西');
INSERT INTO `login` VALUES (5, '1', '1', '1', '1@1', '2019-06-19T13:59', '1');

-- ----------------------------
-- Table structure for movie
-- ----------------------------
DROP TABLE IF EXISTS `movie`;
CREATE TABLE `movie`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `url` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `info` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `logo` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `star` smallint(6) NULL DEFAULT NULL,
  `playnum` bigint(20) NULL DEFAULT NULL,
  `commentnum` bigint(20) NULL DEFAULT NULL,
  `tag_id` int(11) NULL DEFAULT NULL,
  `area` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `release_time` date NULL DEFAULT NULL,
  `length` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  `movie_head` int(11) NULL DEFAULT NULL,
  `movie_tail` int(11) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `title`(`title`) USING BTREE,
  UNIQUE INDEX `url`(`url`) USING BTREE,
  UNIQUE INDEX `logo`(`logo`) USING BTREE,
  INDEX `tag_id`(`tag_id`) USING BTREE,
  INDEX `ix_movie_addtime`(`addtime`) USING BTREE,
  CONSTRAINT `movie_ibfk_1` FOREIGN KEY (`tag_id`) REFERENCES `tag` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 18 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of movie
-- ----------------------------
INSERT INTO `movie` VALUES (12, '流浪地球', '20190912234321623f735c9a1c482cbf0fb87307b9d3fe.mkv', '近未来，科学家们发现太阳急速衰老膨胀，短时间内包括地球在内的整个太阳系都将被太阳所吞没。为了自救，人类提出一个名为“流浪地球”的大胆计划，即倾全球之力在地球表面建造上万座发动机和转向发动机，推动地球离开太阳系，用2500年的时间奔往另外一个栖息之地。中国航天员刘培强（吴京 饰）在儿子刘启四岁那年前往国际空间站，和国际同侪肩负起领航者的重任。转眼刘启（屈楚萧 饰）长大，他带着妹妹朵朵（赵今麦 饰）偷偷跑到地表，偷开外公韩子昂（吴孟达 饰）的运输车，结果不仅遭到逮捕，还遭遇了全球发动机停摆的事件。为了修好发动机，阻止地球坠入木星，全球开始展开饱和式营救，连刘启他们的车也被强征加入。在与时间赛跑的过程中，无数的人前仆后继，奋不顾身，只为延续百代子孙生存的希望…… ', '201909122343215ce277a2f84e42ffb93fb6dd278ebb20.jpg', 4, 28, 1, 25, '中国', '2019-02-05', '125', '2019-09-12 23:43:29', 420, 7200);
INSERT INTO `movie` VALUES (13, '哆啦A梦：大雄的月球探险记', '201909122347565e3a3ee68b774548bb2c0cae8bb3a1ef.mp4', '月球探测器在月亮上捕捉到了白影，大雄认为这道白影是月亮上的兔子，惹来了大家的耻笑，于是哆啦A 梦为了帮助大雄，利用道具“异说俱乐部徽章”，在月球背面制造了一个兔子王国。一天，神秘少年露卡转学而来，与大雄和伙伴们一同前往月亮上的月兔王国展开了一场别开生面的浪漫想象力之旅。', '201909122347567cbd7c6947e14e6d8a24a58408ce4bd1.jpeg', 4, 38, 3, 6, '日本', '2019-06-01', '111', '2019-09-12 23:47:59', 309, 6392);
INSERT INTO `movie` VALUES (14, '蜘蛛侠：英雄远征', '201909122355336fb1d6906f4e44f2ae302d24fbe3bc17.mp4', '在复仇者联盟众英雄的努力下，于灭霸无限手套事件中化作为灰烬的人们，重新回到了人世间，曾经消失的蜘蛛侠 彼得帕克 也回归到了普通的生活之中，数月后，蜘蛛侠彼得帕克所在的学校举行了欧洲旅游，帕克也在其中， 在欧州威尼斯旅行时，一个巨大无比的水怪袭击了威尼斯，不敌敌人的蜘蛛侠幸得一位自称神秘客的男子搭救才击退敌人，之后 神盾局局长找上正在旅游的彼得帕克并要求其加入神盾局，并安排神秘客协助帕克，神秘客自称来自其他宇宙，并告知一群名为元素众的邪恶势力已经入侵这个宇宙了，为了守护来之不易的和平，蜘蛛侠决定与神秘客联手，然而在神秘客那头罩之中，似乎隐藏着什么不为人知的真相……', '20190912235533b3bf211c0b1947028df2f05c5396d98e.jpg', 4, 2, 0, 25, '美国', '2019-06-28', '127', '2019-09-12 23:55:36', 120, 7000);
INSERT INTO `movie` VALUES (15, '哥斯拉2：怪兽之王', '201909122357569893f6a0db00456ba3eb1170a434947b.mp4', '随着《哥斯拉》和《金刚：骷髅岛》在全球范围内取得成功，传奇影业和华纳兄弟影业联手开启了怪兽宇宙系列电影的新篇章—一部史诗级动作冒险巨制。在这部电影中，哥斯拉将和众多大家在流行文化中所熟知的怪兽展开较量。全新故事中，研究神秘动物学的机构“帝王组织”将勇敢直面巨型怪兽，其中强大的哥斯拉也将和魔斯拉、拉顿和它的死对头——三头王者基多拉展开激烈对抗。当这些只存在于传说里的超级生物再度崛起时，它们将展开王者争霸，人类的命运岌岌可危……', '201909122357560b7a14c4bdec453395f05444c5cb708a.jpg', 3, 2, 0, 25, '美国', '2019-05-31', '132', '2019-09-12 23:58:01', 0, 7300);
INSERT INTO `movie` VALUES (16, '名侦探柯南：绀青之拳', '20190918224152a59b834296fb43fda501895c22126292.mp4', '\n“名侦探柯南系列”第23部动画剧场版，票房和口碑也屡破纪录。作为平成年代最后一部柯南电影，首次将案件发生地设立在海外，基德时隔四年后再度回归，与柯南合体展开行动。\n\n故事围绕着19世纪末与海盗船一同沉入海底、世界上最大的蓝宝石“绀青之拳”展开。\n', '20190918224206dfe4e4d25e2f416aa2950704fbbfbfbd.jpg', 62, 9, 0, 6, ' 日本', '2019-09-13', '110', '2019-09-13 12:16:00', 660, 6000);
INSERT INTO `movie` VALUES (17, '哪吒之魔童降世', '201909182131018dd020b264af4b5e95c2d016f8fee422.mp4', '\n天地灵气孕育出一颗能量巨大的混元珠，元始天尊将混元珠提炼成灵珠和魔丸，灵珠投胎为人，助周伐纣时可堪大用；而魔丸则会诞出魔王，为祸人间。元始天尊启动了天劫咒语，3年后天雷将会降临，摧毁魔丸。太乙受命将灵珠托生于陈塘关李靖家的儿子哪吒身上。然而阴差阳错，灵珠和魔丸竟然被掉包。本应是灵珠英雄的哪吒却成了混世大魔王。调皮捣蛋顽劣不堪的哪吒却徒有一颗做英雄的心。然而面对众人对魔丸的误解和即将来临的天雷的降临，哪吒是否命中注定会立地成魔？他将何去何从？\n', '20190918213101d7f8354a868b46ef917190b2e05eb80b.jpg', 86, 14, 0, 6, ' 中国大陆', '2019-07-26', '110', '2019-09-18 21:31:16', 60, 6180);

-- ----------------------------
-- Table structure for moviecol
-- ----------------------------
DROP TABLE IF EXISTS `moviecol`;
CREATE TABLE `moviecol`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `movie_id` int(11) NULL DEFAULT NULL,
  `user_id` int(11) NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `movie_id`(`movie_id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `ix_moviecol_addtime`(`addtime`) USING BTREE,
  CONSTRAINT `moviecol_ibfk_1` FOREIGN KEY (`movie_id`) REFERENCES `movie` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `moviecol_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of moviecol
-- ----------------------------
INSERT INTO `moviecol` VALUES (3, 13, 2, '2019-09-13 14:09:53');
INSERT INTO `moviecol` VALUES (4, 12, 4, '2019-09-13 22:16:10');

-- ----------------------------
-- Table structure for oplog
-- ----------------------------
DROP TABLE IF EXISTS `oplog`;
CREATE TABLE `oplog`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NULL DEFAULT NULL,
  `ip` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `reason` varchar(600) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `sign_in_time` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `ix_oplog_sign_in_time`(`sign_in_time`) USING BTREE,
  CONSTRAINT `oplog_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `admin` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of oplog
-- ----------------------------
INSERT INTO `oplog` VALUES (1, 1, '127.0.0.1', '添加标签9999', '2019-07-21 15:06:28');

-- ----------------------------
-- Table structure for person
-- ----------------------------
DROP TABLE IF EXISTS `person`;
CREATE TABLE `person`  (
  `p_id` int(11) NOT NULL AUTO_INCREMENT,
  `p_name` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`p_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of person
-- ----------------------------
INSERT INTO `person` VALUES (1, '身做了试试88');

-- ----------------------------
-- Table structure for preview
-- ----------------------------
DROP TABLE IF EXISTS `preview`;
CREATE TABLE `preview`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `logo` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `title`(`title`) USING BTREE,
  UNIQUE INDEX `logo`(`logo`) USING BTREE,
  INDEX `ix_preview_addtime`(`addtime`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of preview
-- ----------------------------
INSERT INTO `preview` VALUES (1, '哆啦A梦：大雄的太空探险记', '201909131105422836d9517458401fbf8a184a2be3f3d0.jpg', '2019-09-13 11:05:42');
INSERT INTO `preview` VALUES (2, '哪吒：魔童降世', '2019091311094229b41a0feaa849228a52940c31ce4111.jpg', '2019-08-25 11:03:46');
INSERT INTO `preview` VALUES (3, '蜘蛛侠2：英雄远征', '20190913111112265409f00be64f45a4e34de5d806b071.jpg', '2019-09-13 11:11:13');
INSERT INTO `preview` VALUES (4, '流浪地球', '2019091311085611bddd2ed9284748a22fb08fd0266f8b.jpg', '2019-08-25 11:04:25');
INSERT INTO `preview` VALUES (5, '名侦探柯南：绀青之拳', '201909131156062769ede1082a4b2dbb9ca4fcbc208c25.jpg', '2019-09-13 11:56:06');

-- ----------------------------
-- Table structure for role
-- ----------------------------
DROP TABLE IF EXISTS `role`;
CREATE TABLE `role`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `auths` varchar(600) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `ix_role_addtime`(`addtime`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of role
-- ----------------------------
INSERT INTO `role` VALUES (2, '超级管理员', '1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35', '2019-08-08 22:44:07');
INSERT INTO `role` VALUES (5, '标签管理员', '1,2,3,4', '2019-08-09 22:20:57');
INSERT INTO `role` VALUES (6, '电影及预告管理员', '5,6,7,8,9,10,11,12', '2019-08-11 09:46:29');
INSERT INTO `role` VALUES (7, '会员及日志管理员', '13,14,15,16,17,18,19,20,21,22,23', '2019-08-11 09:48:12');
INSERT INTO `role` VALUES (8, '权限管理员', '24,25,26,27,28,29,30,31,32,33', '2019-08-11 09:48:41');

-- ----------------------------
-- Table structure for student
-- ----------------------------
DROP TABLE IF EXISTS `student`;
CREATE TABLE `student`  (
  `p_id` int(11) NOT NULL AUTO_INCREMENT,
  `p_name` varchar(16) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`p_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of student
-- ----------------------------
INSERT INTO `student` VALUES (1, '小花');
INSERT INTO `student` VALUES (2, '小花');

-- ----------------------------
-- Table structure for tag
-- ----------------------------
DROP TABLE IF EXISTS `tag`;
CREATE TABLE `tag`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `addtime` datetime(0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `title`(`title`) USING BTREE,
  INDEX `ix_tag_addtime`(`addtime`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 26 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of tag
-- ----------------------------
INSERT INTO `tag` VALUES (2, '爱情', '2019-06-30 11:07:25');
INSERT INTO `tag` VALUES (3, '动作', '2019-06-30 11:07:34');
INSERT INTO `tag` VALUES (4, '家庭', '2019-06-30 11:07:44');
INSERT INTO `tag` VALUES (5, '喜剧', '2019-06-30 11:07:50');
INSERT INTO `tag` VALUES (6, '动画', '2019-06-30 11:08:23');
INSERT INTO `tag` VALUES (7, '恐怖', '2019-06-30 11:08:37');
INSERT INTO `tag` VALUES (10, '剧情', '2019-06-30 14:37:34');
INSERT INTO `tag` VALUES (11, '悬疑', '2019-06-30 14:37:46');
INSERT INTO `tag` VALUES (12, '灾难', '2019-06-30 15:32:27');
INSERT INTO `tag` VALUES (13, '奇幻', '2019-06-30 15:32:44');
INSERT INTO `tag` VALUES (14, '战争', '2019-06-30 15:32:53');
INSERT INTO `tag` VALUES (15, '历史', '2019-06-30 15:33:06');
INSERT INTO `tag` VALUES (16, '都市', '2019-06-30 15:33:11');
INSERT INTO `tag` VALUES (17, '青春', '2019-06-30 15:34:33');
INSERT INTO `tag` VALUES (18, '文艺', '2019-06-30 15:34:39');
INSERT INTO `tag` VALUES (19, '励志', '2019-06-30 15:34:45');
INSERT INTO `tag` VALUES (22, '武侠', '2019-06-30 16:28:12');
INSERT INTO `tag` VALUES (23, '纪录片', '2019-06-30 16:29:05');
INSERT INTO `tag` VALUES (24, '情色', '2019-06-30 16:29:27');
INSERT INTO `tag` VALUES (25, '科幻', '2019-07-02 15:51:36');

-- ----------------------------
-- Table structure for test
-- ----------------------------
DROP TABLE IF EXISTS `test`;
CREATE TABLE `test`  (
  `datatime` datetime(0) NULL DEFAULT NULL,
  `data` int(255) NULL DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `password` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `email` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `phone` varchar(11) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `face` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `info` text CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `registered_time` datetime(0) NULL DEFAULT NULL,
  `uuid` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE,
  UNIQUE INDEX `email`(`email`) USING BTREE,
  UNIQUE INDEX `phone`(`phone`) USING BTREE,
  UNIQUE INDEX `face`(`face`) USING BTREE,
  UNIQUE INDEX `uuid`(`uuid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO `user` VALUES (2, '666', 'pbkdf2:sha256:150000$IyUGImsi$1d37739f1f6141cbaf6a65d51ad9b541c27312a82b118b2f7f4aec50c26fc14c', '666@qq.com', '13666666666', '20190901204316aede3c149d1a4648be29312f629140a9.jpg', '看电影', '2019-08-11 22:09:42', 'a989c0a0369c43abb7ea42105e862e9e');
INSERT INTO `user` VALUES (4, '111', 'pbkdf2:sha256:150000$cGCiko5a$07fede5f00188f50be7fd87e0e542bb0cd19e1420662c4d05d577a8df17741dc', '111@qq.com', '13111111111', '201908181825511242ae18e8dc484d857c3b825b1d9d3b.jpg', '1', '2019-08-11 22:13:15', '6ea69756a4034f35bbd57c6ec27953c5');

-- ----------------------------
-- Table structure for userlog
-- ----------------------------
DROP TABLE IF EXISTS `userlog`;
CREATE TABLE `userlog`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NULL DEFAULT NULL,
  `ip` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `sign_in_time` datetime(0) NULL DEFAULT NULL,
  `ip_area` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `user_id`(`user_id`) USING BTREE,
  INDEX `ix_userlog_sign_in_time`(`sign_in_time`) USING BTREE,
  CONSTRAINT `userlog_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 34 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of userlog
-- ----------------------------
INSERT INTO `userlog` VALUES (1, NULL, '0.0.0.0', '2019-07-21 13:54:49', NULL);
INSERT INTO `userlog` VALUES (2, 4, '127.0.0.1', '2019-08-12 20:43:28', NULL);
INSERT INTO `userlog` VALUES (3, 4, '127.0.0.1', '2019-08-12 20:43:51', NULL);
INSERT INTO `userlog` VALUES (4, 4, '127.0.0.1', '2019-08-12 21:50:30', NULL);
INSERT INTO `userlog` VALUES (5, 4, '127.0.0.1', '2019-08-12 21:56:33', NULL);
INSERT INTO `userlog` VALUES (6, 4, '127.0.0.1', '2019-08-16 22:32:27', NULL);
INSERT INTO `userlog` VALUES (7, 4, '127.0.0.1', '2019-08-18 12:56:18', NULL);
INSERT INTO `userlog` VALUES (8, 4, '127.0.0.1', '2019-08-18 16:44:09', NULL);
INSERT INTO `userlog` VALUES (9, 4, '127.0.0.1', '2019-08-18 17:38:34', NULL);
INSERT INTO `userlog` VALUES (10, 4, '127.0.0.1', '2019-08-18 21:53:25', NULL);
INSERT INTO `userlog` VALUES (11, 4, '127.0.0.1', '2019-08-18 21:58:26', NULL);
INSERT INTO `userlog` VALUES (12, 4, '127.0.0.1', '2019-08-19 19:28:50', NULL);
INSERT INTO `userlog` VALUES (13, 4, '127.0.0.1', '2019-08-20 19:56:03', NULL);
INSERT INTO `userlog` VALUES (14, 4, '127.0.0.1', '2019-08-25 10:49:42', NULL);
INSERT INTO `userlog` VALUES (15, 4, '127.0.0.1', '2019-09-01 10:14:58', NULL);
INSERT INTO `userlog` VALUES (16, 4, '127.0.0.1', '2019-09-01 11:12:40', NULL);
INSERT INTO `userlog` VALUES (17, 4, '127.0.0.1', '2019-09-01 16:54:28', NULL);
INSERT INTO `userlog` VALUES (18, 2, '127.0.0.1', '2019-09-01 20:42:36', NULL);
INSERT INTO `userlog` VALUES (19, 4, '127.0.0.1', '2019-09-01 21:46:25', NULL);
INSERT INTO `userlog` VALUES (20, 4, '127.0.0.1', '2019-09-08 18:59:15', NULL);
INSERT INTO `userlog` VALUES (21, 4, '127.0.0.1', '2019-09-09 20:34:32', NULL);
INSERT INTO `userlog` VALUES (22, 4, '127.0.0.1', '2019-09-09 20:54:10', NULL);
INSERT INTO `userlog` VALUES (23, 4, '127.0.0.1', '2019-09-10 16:57:47', NULL);
INSERT INTO `userlog` VALUES (24, 4, '127.0.0.1', '2019-09-10 17:03:08', NULL);
INSERT INTO `userlog` VALUES (25, 4, '127.0.0.1', '2019-09-10 17:17:00', NULL);
INSERT INTO `userlog` VALUES (26, 4, '127.0.0.1', '2019-09-10 17:21:46', NULL);
INSERT INTO `userlog` VALUES (27, 4, '127.0.0.1', '2019-09-11 23:18:12', NULL);
INSERT INTO `userlog` VALUES (28, 4, '127.0.0.1', '2019-09-11 23:31:31', '本地主机');
INSERT INTO `userlog` VALUES (29, 2, '192.168.31.170', '2019-09-11 23:36:15', '本地局域网');
INSERT INTO `userlog` VALUES (30, 2, '127.0.0.1', '2019-09-12 23:48:12', '本地主机');
INSERT INTO `userlog` VALUES (31, 2, '127.0.0.1', '2019-09-13 12:26:00', '本地主机');
INSERT INTO `userlog` VALUES (32, 4, '127.0.0.1', '2019-09-13 22:15:57', '本地主机');
INSERT INTO `userlog` VALUES (33, 4, '127.0.0.1', '2019-09-14 20:11:42', '本地主机');

-- ----------------------------
-- Procedure structure for autodel_test0
-- ----------------------------
DROP PROCEDURE IF EXISTS `autodel_test0`;
delimiter ;;
CREATE PROCEDURE `autodel_test0`()
BEGIN
    delete From test where DATE(datatime) <= DATE(DATE_SUB(NOW(),INTERVAL 1 minute));
    END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;

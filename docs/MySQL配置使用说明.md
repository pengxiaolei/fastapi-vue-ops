# MySQL 数据库配置使用说明

## 配置说明

本项目已从 SQLite 切换为 MySQL 数据库，以下是完整的配置和使用说明。

---

## 1. 环境依赖安装

### 1.1 安装 Python 依赖

```bash
cd backend
pip install -r requirements.txt
```

**新增依赖：**
- `pymysql>=1.1.0` - MySQL Python 驱动
- `cryptography>=42.0.0` - 加密库（用于 MySQL8.0+ 密码认证）

### 1.2 MySQL 服务要求

- MySQL 版本：5.7+ 或 8.0+（推荐 8.0）
- 字符集：utf8mb4（支持 emoji 和特殊字符）
- 认证方式：支持 mysql_native_password

---

## 2. 数据库配置

### 2.1 环境变量配置

编辑 `backend/.env` 文件：

```env
# MySQL 数据库连接配置
# 格式: mysql+pymysql://用户名:密码@主机:端口/数据库名?charset=utf8mb4
DATABASE_URL=mysql+pymysql://root:123456@localhost:3306/devops_db?charset=utf8mb4
```

### 2.2 配置说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| 用户名 | MySQL 登录用户名 | root |
| 密码 | MySQL 登录密码 | 123456 |
| 主机 | MySQL 服务器地址 | localhost |
| 端口 | MySQL 服务端口 | 3306 |
| 数据库名 | 要连接的数据库名称 | devops_db |
| charset | 字符集 | utf8mb4 |

### 2.3 密码含特殊字符处理

如果密码中包含特殊字符（如 `@`, `#`, `:`, `/` 等），系统会自动进行 URL 编码，无需手动处理。

---

## 3. 数据库初始化

### 3.1 自动初始化（推荐）

项目提供了一键初始化脚本：

```bash
cd backend
python init_mysql.py
```

脚本会自动：
1. 连接到 MySQL 服务器
2. 创建数据库（如果不存在）
3. 创建所有数据表
4. 显示已创建的表信息

### 3.2 手动初始化步骤

如果自动脚本有问题，可以手动执行以下步骤：

#### 步骤 1：创建数据库

```sql
-- 登录 MySQL
mysql -u root -p

-- 创建数据库
CREATE DATABASE IF NOT EXISTS `devops_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 查看数据库
SHOW DATABASES;
```

#### 步骤 2：创建数据表

```bash
cd backend
python -c "
from app.database import Base, engine
# 导入所有模型
from app.models.machine import Machine, MachineTag, MachineGroup

# 创建所有表
Base.metadata.create_all(bind=engine)
print('所有表创建成功!')
"
```

---

## 4. 连接池配置

项目已配置优化的 MySQL 连接池参数：

```python
# database.py 中的配置
pool_size = 10           # 连接池大小
max_overflow = 20        # 最大溢出连接数
pool_pre_ping = True     # 自动检测失效连接
pool_recycle = 3600      # 连接回收时间（秒）
connect_timeout = 10     # 连接超时时间
```

### 4.1 配置说明

- **pool_size**: 保持在连接池中的连接数，建议根据并发量调整
- **max_overflow**: 连接池满时可以额外创建的连接数
- **pool_pre_ping**: 每次从连接池获取连接时自动检测连接是否有效，防止 8 小时断连问题
- **pool_recycle**: 连接超过指定时间自动回收，防止 MySQL 自动关闭空闲连接

---

## 5. 数据库表结构

### 5.1 机器表 (machines)

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INTEGER | 主键 |
| name | VARCHAR(100) | 机器名称 |
| hostname | VARCHAR(255) | 主机地址 |
| port | INTEGER | SSH 端口 |
| username | VARCHAR(50) | SSH 用户名 |
| auth_type | ENUM | 认证类型 (password/key) |
| password | VARCHAR(255) | 加密密码 |
| private_key | TEXT | 加密私钥 |
| os_type | VARCHAR(50) | 操作系统 |
| status | ENUM | 状态 (online/offline/maintenance) |
| cpu_cores | INTEGER | CPU 核心数 |
| memory_total | BIGINT | 总内存 (MB) |
| disk_total | BIGINT | 总磁盘 (GB) |
| cpu_usage | FLOAT | CPU 使用率 |
| memory_usage | FLOAT | 内存使用率 |
| disk_usage | FLOAT | 磁盘使用率 |
| environment | VARCHAR(50) | 环境 (dev/test/prod) |
| last_heartbeat | DATETIME | 最后心跳时间 |
| description | TEXT | 描述 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |
| is_deleted | BOOLEAN | 是否删除 |

### 5.2 标签表 (machine_tags)

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INTEGER | 主键 |
| name | VARCHAR(50) | 标签名称 |
| color | VARCHAR(7) | 标签颜色 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |
| is_deleted | BOOLEAN | 是否删除 |

### 5.3 分组表 (machine_groups)

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INTEGER | 主键 |
| name | VARCHAR(100) | 分组名称 |
| description | TEXT | 描述 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |
| is_deleted | BOOLEAN | 是否删除 |

### 5.4 关联表

- **machine_tag_relation**: 机器-标签多对多关联
- **machine_group_relation**: 机器-分组多对多关联

---

## 6. 常见问题

### 6.1 连接失败 - Authentication plugin 'caching_sha2_password'

**问题**: MySQL 8.0 默认使用 caching_sha2_password 认证，导致连接失败

**解决方法**:

方法 1：修改用户认证方式
```sql
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '你的密码';
FLUSH PRIVILEGES;
```

方法 2：在连接URL中指定认证插件（已自动处理）

### 6.2 连接失败 - Access denied

**问题**: 用户名或密码错误

**解决方法**:
1. 检查 `.env` 中的数据库配置
2. 确认 MySQL 用户权限：
```sql
SELECT user, host FROM mysql.user;
GRANT ALL PRIVILEGES ON devops_db.* TO 'root'@'localhost';
FLUSH PRIVILEGES;
```

### 6.3 字符集问题 - Incorrect string value

**问题**: 插入 emoji 或特殊字符失败

**解决方法**:
确保数据库和表使用 utf8mb4 字符集：
```sql
-- 修改数据库字符集
ALTER DATABASE devops_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 修改表字符集
ALTER TABLE machines CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6.4 连接池问题 - MySQL server has gone away

**问题**: 长时间空闲后连接失效

**解决方法**: 已通过 `pool_pre_ping=True` 和 `pool_recycle=3600` 自动处理

### 6.5 如何切换回 SQLite

如果需要切换回 SQLite 开发，修改 `.env` 文件：

```env
# DATABASE_URL=mysql+pymysql://root:123456@localhost:3306/devops_db?charset=utf8mb4
DATABASE_URL=sqlite:///./devops.db
```

---

## 7. 数据库备份与恢复

### 7.1 备份数据库

```bash
# 备份整个数据库
mysqldump -u root -p devops_db > backup_devops_$(date +%Y%m%d).sql

# 仅备份结构
mysqldump -u root -p -d devops_db > schema_devops.sql

# 仅备份数据
mysqldump -u root -p -t devops_db > data_devops.sql
```

### 7.2 恢复数据库

```bash
# 恢复数据库
mysql -u root -p devops_db < backup_devops_20240101.sql

# 恢复到新数据库
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS devops_db CHARACTER SET utf8mb4;"
mysql -u root -p devops_db < backup_devops_20240101.sql
```

---

## 8. 性能优化建议

### 8.1 添加索引

```sql
-- 机器表索引
CREATE INDEX idx_machines_status ON machines(status);
CREATE INDEX idx_machines_environment ON machines(environment);
CREATE INDEX idx_machines_hostname ON machines(hostname);

-- 标签索引
CREATE UNIQUE INDEX idx_tags_name ON machine_tags(name);

-- 分组索引
CREATE UNIQUE INDEX idx_groups_name ON machine_groups(name);
```

### 8.2 MySQL 配置优化

修改 MySQL 配置文件 `my.cnf` 或 `my.ini`:

```ini
[mysqld]
# 字符集
character-set-server = utf8mb4
collation-server = utf8mb4_unicode_ci

# 最大连接数
max_connections = 200

# 超时设置
wait_timeout = 28800
interactive_timeout = 28800

# 缓冲区设置
innodb_buffer_pool_size = 1G
innodb_log_file_size = 256M
```

---

## 9. 验证配置

启动应用前，先验证数据库连接是否正常：

```bash
cd backend
python -c "
from app.database import engine
from sqlalchemy import text

# 测试连接
with engine.connect() as conn:
    result = conn.execute(text('SELECT VERSION()'))
    print(f'✅ MySQL 连接成功! 版本: {result.fetchone()[0]}')

    # 查看当前数据库
    result = conn.execute(text('SELECT DATABASE()'))
    print(f'✅ 当前数据库: {result.fetchone()[0]}')
"
```

如果显示连接成功，说明数据库配置正确！

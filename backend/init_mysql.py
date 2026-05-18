"""
MySQL 数据库初始化脚本
用于创建数据库和初始表结构
"""
import pymysql
from sqlalchemy import text

from app.config import settings
from app.database import Base, engine

def create_database_if_not_exists():
    """创建数据库（如果不存在）"""
    # 从配置中提取数据库连接信息
    url = settings.database_url
    if not url.startswith('mysql'):
        print("当前不是 MySQL 配置，跳过数据库创建")
        return False

    # 解析数据库连接信息
    from urllib.parse import urlparse
    parsed = urlparse(url)
    db_name = parsed.path.lstrip('/').split('?')[0]

    # 创建无数据库的连接
    print(f"连接到 MySQL 服务器: {parsed.hostname}:{parsed.port}")

    try:
        # 先直接用 pymysql 连接创建数据库
        conn = pymysql.connect(
            host=parsed.hostname,
            port=parsed.port or 3306,
            user=parsed.username,
            password=parsed.password,
            charset='utf8mb4'
        )
        cursor = conn.cursor()

        # 创建数据库
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        print(f"✅ 数据库 `{db_name}` 创建成功或已存在")

        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ 创建数据库失败: {str(e)}")
        return False


def create_tables():
    """创建所有表结构"""
    print("正在创建数据表...")
    try:
        # 导入所有模型确保 Base 能找到它们
        from app.models.machine import Machine, MachineTag, MachineGroup
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        print("✅ 所有数据表创建成功")
        return True
    except Exception as e:
        print(f"❌ 创建数据表失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def show_tables():
    """显示已创建的表"""
    from app.database import engine
    from sqlalchemy import inspect

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    print("\n📋 已创建的表:")
    for table in tables:
        columns = inspector.get_columns(table)
        col_names = [col['name'] for col in columns]
        print(f"  - {table} ({len(col_names)} 列): {', '.join(col_names[:5])}{'...' if len(col_names) > 5 else ''}")


def test_connection():
    """测试数据库连接"""
    print("\n🔍 测试数据库连接...")
    try:
        from app.database import engine
        with engine.connect() as conn:
            result = conn.execute(text('SELECT VERSION()'))
            version = result.fetchone()[0]
            print(f"✅ MySQL 连接成功! 版本: {version}")

            result = conn.execute(text('SELECT DATABASE()'))
            current_db = result.fetchone()[0]
            print(f"✅ 当前数据库: {current_db}")
            return True
    except Exception as e:
        print(f"❌ 数据库连接失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("MySQL 数据库初始化")
    print("=" * 60)

    # 0. 测试连接
    if test_connection():
        # 1. 创建数据库
        if create_database_if_not_exists():
            # 2. 创建数据表
            if create_tables():
                show_tables()
                print("\n🎉 数据库初始化完成!")
            else:
                print("\n❌ 数据表创建失败!")
        else:
            print("\n❌ 数据库创建失败!")
    else:
        print("\n❌ 无法连接到 MySQL 服务器，请检查配置!")

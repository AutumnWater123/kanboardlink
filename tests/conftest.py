import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.core.database import Base
from backend.main import app
from fastapi.testclient import TestClient

# 设置测试数据库连接字符串
TEST_DB_URL = "postgresql://testuser:testpwd@localhost:5432/progress_test?client_encoding=UTF8"

# 创建测试数据库引擎和会话
engine = create_engine(TEST_DB_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False)

@pytest.fixture(scope="session", autouse=True)
def init_test_db():
    # 初始化测试数据库
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    # 清理测试数据库
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db():
    # 创建数据库连接和事务
    conn = engine.connect()
    trans = conn.begin()
    sess = TestingSessionLocal(bind=conn)
    yield sess
    # 回滚事务，清理数据
    trans.rollback()
    conn.close()

@pytest.fixture
def client():
    # 创建 FastAPI 测试客户端
    with TestClient(app) as c:
        yield c
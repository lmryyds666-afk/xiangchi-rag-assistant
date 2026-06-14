"""
config_data.py - 统一配置文件
直接读取 .env 文件，不依赖 python-dotenv，避免装包问题
"""
import os


def _load_env_file():
    """手动解析 .env 文件，兼容 KEY=VALUE 格式，忽略注释和空行"""
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if not os.path.exists(env_path):
        return
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            # ⚠️ 用 os.environ[key] = value 强制覆盖，避免系统环境变量里的旧值污染 .env
            os.environ[key.strip()] = value.strip()


# 启动时自动加载
_load_env_file()

# ===== 模型密钥（从 .env 读取，文件不要提交到 Git）=====
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY")
if not DASHSCOPE_API_KEY:
    raise ValueError(
        "未设置 DASHSCOPE_API_KEY，请检查项目根目录下的 .env 文件是否存在并正确填写"
    )

# （提示：生产环境可删除此打印行）
# print(f"[config] DASHSCOPE_API_KEY 已加载: {DASHSCOPE_API_KEY[:8]}...{DASHSCOPE_API_KEY[-4:]}")

md5_path = './md5.text'

# chroma
collection_name = "rag"
persist_directory = './chroma_db'

# spliter
chunk_size = 80
chunk_overlap = 10
separators = ["\n\n", "\n", ".", "!", "?", "。", "？", " ", ""]
max_split_char_number = 60  # 文本分割的阈值

similarity_threshold = 1

embedding_model_name = "text-embedding-v4"
chat_model_name = "qwen3-max"

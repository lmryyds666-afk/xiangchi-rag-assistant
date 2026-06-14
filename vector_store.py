import config_data as config
from langchain_chroma import Chroma
import os

# 配置通义密钥（从 config_data 统一读取）
os.environ["DASHSCOPE_API_KEY"] = config.DASHSCOPE_API_KEY

# 创建向量存储服务
class VectorStoreService(object):
    def __init__(self, embedding):
        self.embedding = embedding
        # 创建向量库 vector_store
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory
        )

    def get_retriever(self):
        return self.vector_store.as_retriever(
            # 必须添加检索类型，才能启用分数过滤
            # search_type="similarity_score_threshold",
            search_kwargs={
                "k": 1,  # k固定整数：只想要1条就写1，不再读取阈值参数
                # "score_threshold": 0.7 # 阈值单独配置
            }
        )

if __name__ == '__main__':
    from langchain_community.embeddings import DashScopeEmbeddings
    # 1. 创建向量服务
    service = VectorStoreService(DashScopeEmbeddings(model="text-embedding-v4"))
    # 2. 获取检索器
    retriever = service.get_retriever()
    # 3. 用户提问检索
    res = retriever.invoke("香驰控股的大豆蛋白产品主要有哪些？")
    print(res)
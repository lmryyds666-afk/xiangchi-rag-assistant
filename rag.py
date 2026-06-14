from operator import itemgetter
from vector_store import VectorStoreService
from langchain_community.embeddings import DashScopeEmbeddings
import config_data as config
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.chat_models import ChatTongyi
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from file_history_store import get_file_history
import os

os.environ["DASHSCOPE_API_KEY"] = config.DASHSCOPE_API_KEY


class RagService():
    def __init__(self):
        # 向量检索服务
        self.vector_service = VectorStoreService(
            embedding=DashScopeEmbeddings(model=config.embedding_model_name)
        )

        # 提示词（含历史消息占位符）
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "以我提供的已知参考资料为主，简洁和专业的回答用户的问题。参考资料：{context}"),
            MessagesPlaceholder(variable_name="history"),   # 历史对话注入点
            ("user", "请回答用户的提问：{input}")
        ])

        # 大模型
        self.chat_model = ChatTongyi(model=config.chat_model_name)

        # 构建带历史记录的链
        self.chain = self.__get_chain()

    def __get_chain(self):
        retriever = self.vector_service.get_retriever()

        # 文档格式化
        def format_document(docs: list[Document]):
            if not docs:
                return "无相关参考资料"
            return "".join(f"文档片段：{doc.page_content}\n" for doc in docs)

        # 基础 RAG 链
        # RunnableWithMessageHistory 传入的是字典 {"input": "...", "history": [...]}
        # 必须用 itemgetter 从字典中取出对应字段，再分别交给 retriever 和 prompt
        base_chain = (
            {
                "input":   itemgetter("input"),                          # 原始问题 → prompt {input}
                "context": itemgetter("input") | retriever | format_document,  # 原始问题 → 检索 → 格式化
                "history": itemgetter("history"),                        # 历史消息 → prompt {history}
            }
            | self.prompt_template
            | self.chat_model
            | StrOutputParser()
        )

        # 包装成带历史记录的链
        chain_with_history = RunnableWithMessageHistory(
            base_chain,
            get_session_history=get_file_history,
            input_messages_key="input",
            history_messages_key="history",
        )
        return chain_with_history

    def chat(self, question: str, session_id: str = "default") -> str:
        """
        对话入口，session_id 区分不同用户/会话。
        同一 session_id 的对话历史会持久化到本地文件。
        """
        return self.chain.invoke(
            {"input": question},
            config={"configurable": {"session_id": session_id}}
        )


# 测试
if __name__ == '__main__':
    service = RagService()

    # 模拟多轮对话
    session = "user_001"

    q1 = "香驰控股的主营业务有哪些，大豆蛋白产品有什么优势？"
    print(f"用户: {q1}")
    print(f"AI: {service.chat(q1, session_id=session)}\n")

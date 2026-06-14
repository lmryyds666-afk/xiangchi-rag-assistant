import streamlit as st
from rag import RagService

# ── 页面配置 ──
st.set_page_config(page_title="香驰 RAG 智能检索助手", page_icon="🤖")
st.title("🤖 香驰智答")
st.caption("基于香驰公司的 RAG 知识库智能问答系统，支持多轮对话记忆")

# ── 初始化服务（只执行一次） ──
if "rag_service" not in st.session_state:
    st.session_state["rag_service"] = RagService()

# ── 初始化聊天记录（页面刷新时保留） ──
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# ── 侧边栏：会话管理 ──
with st.sidebar:
    st.header("⚙️ 会话管理")

    # 输入 session_id
    session_id = st.text_input("会话 ID", value="default", key="session_input")
    st.caption("不同 ID 对应不同对话历史")

    # 清空当前会话
    if st.button("🗑️ 清空当前对话"):
        st.session_state["chat_history"] = []
        # 同时清空文件历史
        from file_history_store import FileHistoryStore
        FileHistoryStore(session_id=session_id).clear()
        st.rerun()

    # 清空屏幕但保留历史（仅清 UI）
    if st.button("🔄 重新开始（保留历史）"):
        st.session_state["chat_history"] = []
        st.rerun()

    st.divider()
    st.caption("💡 提示：输入问题后按回车或点击发送按钮")

# ── 聊天消息区域 ──
# 渲染历史消息
for msg in st.session_state["chat_history"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── 用户输入 ──
if prompt := st.chat_input("请输入您的问题..."):
    # 1. 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state["chat_history"].append({"role": "user", "content": prompt})

    # 2. 调用 RAG 服务获取回答
    with st.chat_message("assistant"):
        with st.spinner("🤔 思考中..."):
            answer = st.session_state["rag_service"].chat(
                question=prompt,
                session_id=session_id
            )
        st.markdown(answer)
    st.session_state["chat_history"].append({"role": "assistant", "content": answer})

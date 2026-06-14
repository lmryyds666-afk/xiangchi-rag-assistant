import streamlit as st
import time
from knowledge_base import KnowledgeBaseService

# 添加网页标题
st.title("知识库更新服务")

# file_uploader上传文件服务
uploader_files=st.file_uploader(
    "请上传TXT文件",
    type=["txt"],
    accept_multiple_files=False # false表示仅接收一个文件的上传
)

if "server" not in st.session_state:
    st.session_state["server"]=KnowledgeBaseService()

if uploader_files is not None:
    # 提取文件的信息
    file_name=uploader_files.name
    file_type=uploader_files.type
    file_size=uploader_files.size/1024  # KB

    st.subheader(f"文件名：{file_name}")
    st.write(f"格式：{file_type}|大小：{file_size:.3f}KB")

    # 获取文件的内容 .getvalue只能得到文件的二进制编码，通过.decode("utf-8")转为utf-8编码
    # 把上传的整个文件内容，一次性读取出来，变成字符串！uploader_files.getvalue().decode("utf-8")
    text=uploader_files.getvalue().decode("utf-8")
    st.write(text)

    with st.spinner("载入知识库中...."):
        time.sleep(1)
        result=st.session_state["server"].upload_by_str(text,file_name)
        st.write(result)

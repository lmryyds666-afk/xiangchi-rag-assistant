# 香驰智能问答助手 (xiangchi-rag-assistant)

基于 RAG（检索增强生成）的企业知识库智能问答系统，
支持多轮对话记忆、文件上传自动入库、阿里云百炼大模型调用。

## 核心功能
- 📚 知识库检索：基于 Chroma 向量数据库的语义检索
- 💬 多轮对话：支持上下文记忆
- 📤 文件上传：自动解析、入库、向量化
- 🔐 配置隔离：API Key 通过 .env 管理，不入 git

## 技术栈
- Python 3.11
- LangChain + ChromaDB
- 阿里云百炼 (DashScope) - text-embedding-v4 / qwen3-max
- Streamlit Web UI

## 快速开始

### 1. 克隆仓库
```bash
git clone https://github.com/lmryyds666-afk/xiangchi-rag-assistant.git
cd xiangchi-rag-assistant
```
### 2.安装依赖
```bash
pip install -r requirementes.txt
```
### 3.配置API Key
在项目根目录手动创建.env,填入
```bash
DASHSCOPE_API_KEY=你的百炼API_Key
```
### 4.放入知识库
把你的.txt/.md企业资料放进data/目录
### 5.启动
```bash
streamlit run app_qa.py
```
注意事项
.env 文件包含敏感信息，已加入 .gitignore，请勿提交
data/ 目录用于存放企业内部资料，已加入 .gitignore
首次运行会自动创建 chroma_db/ 和 chat_history/ 目录

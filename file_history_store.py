import json
import os
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, messages_from_dict, messages_to_dict


class FileHistoryStore(BaseChatMessageHistory):
    """
    基于本地 JSON 文件的对话历史记录实现。
    每个 session_id 对应一个独立的 JSON 文件，持久化存储在 history_dir 目录下。
    """

    def __init__(self, session_id: str, history_dir: str = "./chat_history"):
        self.session_id = session_id
        self.history_dir = history_dir
        os.makedirs(history_dir, exist_ok=True)
        self.file_path = os.path.join(history_dir, f"{session_id}.json")

    @property
    def messages(self) -> list[BaseMessage]:
        """从文件中读取历史消息"""
        if not os.path.exists(self.file_path):
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return messages_from_dict(data)
        except (json.JSONDecodeError, Exception):
            return []

    def add_message(self, message: BaseMessage) -> None:
        """追加一条消息并持久化到文件"""
        current = self.messages
        current.append(message)
        self._save(current)

    def add_messages(self, messages: list[BaseMessage]) -> None:
        """批量追加消息并持久化到文件"""
        current = self.messages
        current.extend(messages)
        self._save(current)

    def clear(self) -> None:
        """清空当前 session 的历史记录"""
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def _save(self, messages: list[BaseMessage]) -> None:
        """将消息列表序列化并写入 JSON 文件"""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(messages_to_dict(messages), f, ensure_ascii=False, indent=2)

    def __repr__(self):
        return f"FileHistoryStore(session_id={self.session_id!r}, file={self.file_path!r}, messages={len(self.messages)})"


def get_file_history(session_id: str, history_dir: str = "./chat_history") -> FileHistoryStore:
    """
    工厂函数，供 RunnableWithMessageHistory 使用。
    用法：
        RunnableWithMessageHistory(..., get_session_history=get_file_history)
    """
    return FileHistoryStore(session_id=session_id, history_dir=history_dir)


# ── 测试 ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    store = FileHistoryStore(session_id="test_session")
    store.clear()  # 先清空，保证测试干净

    from langchain_core.messages import HumanMessage, AIMessage

    store.add_message(HumanMessage(content="你好，我身高168，体重150斤"))
    store.add_message(AIMessage(content="根据您的身材，推荐 XL 码。"))
    store.add_message(HumanMessage(content="再推荐一件外套"))
    store.add_message(AIMessage(content="建议选择宽松版型的 L/XL 码外套。"))

    print(f"共 {len(store.messages)} 条记录：")
    for msg in store.messages:
        role = "用户" if msg.type == "human" else "AI"
        print(f"  [{role}] {msg.content}")

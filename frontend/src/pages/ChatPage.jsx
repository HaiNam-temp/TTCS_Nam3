import { useEffect, useState } from "react";

import { useAuth } from "../features/auth/AuthContext";
import {
  createConversationApi,
  deleteConversationApi,
  listConversationsApi,
  listMessagesApi,
  sendMessageApi,
} from "../shared/api/chatApi";
import { AppShell } from "../shared/components/AppShell";

export function ChatPage() {
  const { token } = useAuth();
  const [conversations, setConversations] = useState([]);
  const [selectedConversationId, setSelectedConversationId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    refreshConversations();
  }, []);

  async function refreshConversations() {
    const data = await listConversationsApi(token);
    setConversations(data || []);
    if (data?.length && !selectedConversationId) {
      setSelectedConversationId(data[0].id);
      const loadedMessages = await listMessagesApi(token, data[0].id);
      setMessages(loadedMessages || []);
    }
  }

  async function onNewConversation() {
    const created = await createConversationApi(token, "Cuộc hội thoại mới");
    setConversations((prev) => [created, ...prev]);
    setSelectedConversationId(created.id);
    setMessages([]);
  }

  async function onSelectConversation(conversationId) {
    setSelectedConversationId(conversationId);
    const loadedMessages = await listMessagesApi(token, conversationId);
    setMessages(loadedMessages || []);
  }

  async function onDeleteConversation(conversationId) {
    await deleteConversationApi(token, conversationId);
    const next = conversations.filter((item) => item.id !== conversationId);
    setConversations(next);
    if (selectedConversationId === conversationId) {
      setSelectedConversationId(next[0]?.id || null);
      if (next[0]?.id) {
        const loadedMessages = await listMessagesApi(token, next[0].id);
        setMessages(loadedMessages || []);
      } else {
        setMessages([]);
      }
    }
  }

  async function onSend(event) {
    event.preventDefault();
    if (!input.trim() || !selectedConversationId || loading) {
      return;
    }

    setLoading(true);
    try {
      const response = await sendMessageApi(token, selectedConversationId, input.trim());
      const newMessages = await listMessagesApi(token, selectedConversationId);
      setMessages(newMessages || []);
      setInput("");
      if (!response?.response) {
        throw new Error("Phản hồi rỗng");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <AppShell>
      <div className="chat-page">
        <div className="section-header">
          <div>
            <h2>AI Assistant</h2>
            <p>Nhắn tin với trợ lý và quản lý toàn bộ hội thoại của bạn theo thời gian thực.</p>
          </div>
        </div>

        <div className="chat-layout">
        <aside className="chat-sidebar">
          <button className="btn" onClick={onNewConversation}>+ Cuộc hội thoại mới</button>
          <div className="chat-conversation-list">
            {conversations.map((conversation) => (
              <div
                key={conversation.id}
                className={conversation.id === selectedConversationId ? "conversation-item active" : "conversation-item"}
              >
                <button onClick={() => onSelectConversation(conversation.id)}>{conversation.title}</button>
                <button className="btn-mini" onClick={() => onDeleteConversation(conversation.id)} title="Xóa hội thoại">
                  Xóa
                </button>
              </div>
            ))}

            {!conversations.length ? <p className="empty-state">Chưa có hội thoại nào.</p> : null}
          </div>
        </aside>

        <section className="chat-panel">
          <div className="chat-messages">
            {messages.map((message) => (
              <div key={message.id} className={message.role === "assistant" ? "bubble assistant" : "bubble user"}>
                <strong>{message.role === "assistant" ? "Trợ lý AI" : "Bạn"}</strong>
                <p>{message.content}</p>
              </div>
            ))}

            {!messages.length && selectedConversationId ? (
              <p className="empty-state">Hãy gửi tin nhắn đầu tiên để bắt đầu.</p>
            ) : null}

            {!selectedConversationId ? (
              <p className="empty-state">Tạo hội thoại mới để trò chuyện với AI Assistant.</p>
            ) : null}
          </div>

          <form className="inline-form" onSubmit={onSend}>
            <input
              value={input}
              onChange={(event) => setInput(event.target.value)}
              placeholder="Nhập nội dung bạn muốn hỏi..."
            />
            <button className="btn" type="submit" disabled={loading || !selectedConversationId}>
              {loading ? "Đang gửi..." : "Gửi"}
            </button>
          </form>
        </section>
        </div>
      </div>
    </AppShell>
  );
}

import { useEffect, useRef, useState } from "react";
import { askQuestion } from "../router";
import ChatMessage from "./ChatMessage";
import { TEXT } from "../constants/text";
import "../css/ChatAssistant.css";

export default function ChatAssistant({ onShowAllData }) {
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function handleSend(e) {
    e.preventDefault();
    const q = question.trim();
    if (!q) return;

    setMessages((prev) => [...prev, { role: "user", content: q }]);
    setQuestion("");
    setLoading(true);

    try {
      const result = await askQuestion(q);

      if (result.action === "SHOW_ALL_DATA") {
        await onShowAllData();
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: TEXT.chatAssistant.showAllDataAnswer },
        ]);
      } else {
        setMessages((prev) => [...prev, { role: "assistant", content: result.answer }]);
      }
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: TEXT.chatAssistant.askError },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="chat-assistant">
      <h2 className="chat-assistant__heading">
        <span className="chat-assistant__heading-emoji">{TEXT.chatAssistant.agentEmoji}</span>
        {TEXT.chatAssistant.heading}
      </h2>

      <div className="chat-assistant__messages">
        {messages.length === 0 && (
          <div className="chat-assistant__empty">
            {TEXT.chatAssistant.emptyState}
          </div>
        )}
        {messages.map((m, i) => (
          <ChatMessage key={i} role={m.role} content={m.content} />
        ))}
        {loading && (
          <div className="chat-assistant__loading">
            <span className="chat-assistant__heading-emoji">{TEXT.chatAssistant.agentEmoji}</span>
            <span className="chat-assistant__loading-dots">
              <span></span>
              <span></span>
              <span></span>
            </span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSend} className="chat-assistant__form">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder={TEXT.chatAssistant.inputPlaceholder}
          className="chat-assistant__input"
          disabled={loading}
        />
        <button type="submit" className="chat-assistant__send-btn" disabled={loading}>
          {TEXT.chatAssistant.sendIcon}
        </button>
      </form>
    </section>
  );
}

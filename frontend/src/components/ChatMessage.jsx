import "../css/ChatMessage.css";
import { TEXT } from "../constants/text";

export default function ChatMessage({ role, content }) {
  const isAssistant = role === "assistant";

  return (
    <div className={`chat-message chat-message--${role}`}>
      {isAssistant && <span className="chat-message__avatar">{TEXT.chatAssistant.agentEmoji}</span>}
      <span className="chat-message__bubble">{content}</span>
    </div>
  );
}

import { ThreadListPrimitive } from '@assistant-ui/react'

export default function ConversationSidebar() {
  return (
    <aside className="sidebar">
      <ThreadListPrimitive.New className="new-chat-button">
        + Start new conversation
      </ThreadListPrimitive.New>

      <div className="sidebar-section">
        <p className="sidebar-label">THIS SESSION</p>
        <p className="conversation-history-note">
          Your current chat is available during this browser session. Saved
          conversation history is not available yet.
        </p>
      </div>
    </aside>
  )
}

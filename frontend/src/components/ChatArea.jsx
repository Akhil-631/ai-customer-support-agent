import { Thread } from './thread.aui'

export default function ChatArea() {
  return (
    <main className="chat-area">
      <div className="chat-header">
        <div>
          <h2>Customer Support</h2>

          <p>
            <span className="status-dot" />
            Resolve AI is ready to help
          </p>
        </div>
      </div>

      <div className="assistant-thread">
        <Thread />
      </div>
    </main>
  )
}

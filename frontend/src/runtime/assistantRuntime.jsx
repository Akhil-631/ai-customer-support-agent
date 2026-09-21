import {
  AssistantRuntimeProvider,
  useAuiState,
  useLocalRuntime,
} from '@assistant-ui/react'
import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useRef,
  useState,
} from 'react'
import { getConversationState, sendChatMessage } from '@/api/chatApi'

const HumanReviewContext = createContext(null)

export function useHumanReview() {
  return useContext(HumanReviewContext)
}

function ConversationIdSynchronizer({
  conversationIdRef,
  conversationIdsByThreadRef,
  onThreadChange,
}) {
  const threadId = useAuiState((state) => state.threads.mainThreadId)

  useEffect(() => {
    if (!conversationIdsByThreadRef.current.has(threadId)) {
      conversationIdsByThreadRef.current.set(threadId, crypto.randomUUID())
    }

    conversationIdRef.current = conversationIdsByThreadRef.current.get(threadId)
    onThreadChange()
  }, [conversationIdRef, conversationIdsByThreadRef, onThreadChange, threadId])

  return null
}

export function AssistantRuntime({ children }) {
  const conversationIdRef = useRef(crypto.randomUUID())
  const conversationIdsByThreadRef = useRef(new Map())
  const [humanReview, setHumanReview] = useState(null)
  const [humanReviewResult, setHumanReviewResult] = useState(null)
  const clearHumanReview = useCallback(() => setHumanReview(null), [])

  useEffect(() => {
  if (!humanReview) return

  const interval = setInterval(async () => {
    try {
      const state = await getConversationState(
        conversationIdRef.current,
      )

      if (!state.human_review_required && state.human_decision && state.final_response) {
        setHumanReviewResult(state.final_response)
        setHumanReview(null)
        clearInterval(interval)
      }
    } catch (error) {
      console.error('Failed to check human review state:', error)
    }
  }, 2000)

  return () => clearInterval(interval)
}, [humanReview])

  const chatModel = {
    async run({ messages }) {
      const lastUserMessage = [...messages]
        .reverse()
        .find((message) => message.role === 'user')

      const textPart = lastUserMessage?.content?.find(
        (part) => part.type === 'text',
      )

      const message = textPart?.text ?? ''

      const result = await sendChatMessage(
        message,
        conversationIdRef.current,
      )

      if (result.human_review_required) {
        setHumanReview(result.human_review_data)
      } else {
        setHumanReview(null)
      }

      return {
        content: [
          {
            type: 'text',
            text: result.response,
          },
        ],
      }
    },
  }

  const runtime = useLocalRuntime(chatModel)

  return (
    <HumanReviewContext.Provider value={{data:humanReview, result:humanReviewResult}}>
      <AssistantRuntimeProvider runtime={runtime}>
        <ConversationIdSynchronizer
          conversationIdRef={conversationIdRef}
          conversationIdsByThreadRef={conversationIdsByThreadRef}
          onThreadChange={clearHumanReview}
        />
        {children}
      </AssistantRuntimeProvider>
    </HumanReviewContext.Provider>
  )
}

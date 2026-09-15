const API_BASE_URL = 'http://127.0.0.1:8000'

export async function sendChatMessage(message, conversationId) {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message,
      conversation_id: conversationId,
    }),
  })

  if (!response.ok) {
    throw new Error(`Chat request failed: ${response.status}`)
  }

  return response.json()
}

export async function sendHumanReviewDecision(
  conversationId,
  decision,
) {
  const response = await fetch(`${API_BASE_URL}/human-review`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      conversation_id: conversationId,
      decision,
    }),
  })

  if (!response.ok) {
    throw new Error(`Human review request failed: ${response.status}`)
  }

  return response.json()
}
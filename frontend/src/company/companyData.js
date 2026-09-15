// DEMO / UI-ONLY data. The current backend has no endpoint that lists
// pending human-review requests, so these records are never live queue data.
export const demoReviewRequests = [
  {
    id: 'demo-review-10482',
    conversationId: 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    customerName: 'Alex Morgan',
    customerRequest: 'Please cancel order CA-2017-152156 before it ships.',
    intent: 'cancel_order',
    confidence: 0.94,
    orderId: 'CA-2017-152156',
    status: 'Pending review',
    submittedAt: 'Demo request · moments ago',
    note: 'Cancellation requests require a staff decision before execution.',
  },
  {
    id: 'demo-review-10483',
    conversationId: null,
    customerName: 'Jordan Lee',
    customerRequest: 'I was charged twice and need help with my payment.',
    intent: 'human_support',
    confidence: 0.78,
    orderId: null,
    status: 'Awaiting conversation reference',
    submittedAt: 'Demo request · 12 minutes ago',
    note: 'A future queue API must provide a resumable conversation ID.',
  },
]

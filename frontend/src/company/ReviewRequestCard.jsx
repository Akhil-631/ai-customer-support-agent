import { useState } from 'react'
import { AlertCircle, Check, ChevronRight, Clock3, LoaderCircle, X } from 'lucide-react'
import { sendHumanReviewDecision } from '@/api/chatApi'

const intentLabels = {
  cancel_order: 'Cancel order',
  human_support: 'Human support',
}

export default function ReviewRequestCard({ request }) {
  const [decision, setDecision] = useState(null)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const submitDecision = async (nextDecision) => {
    if (!request.conversationId || decision) return

    setDecision(nextDecision)
    setError(null)
    setResult(null)

    try {
      const response = await sendHumanReviewDecision(
        request.conversationId,
        nextDecision,
      )
      setResult(response)
    } catch (requestError) {
      setError(requestError.message || 'The decision could not be submitted.')
    } finally {
      setDecision(null)
    }
  }

  const actionUnavailable = !request.conversationId

  return (
    <article className="review-card">
      <div className="review-card-topline">
        <div>
          <p className="review-customer-name">{request.customerName}</p>
          <p className="review-timestamp"><Clock3 size={13} /> {request.submittedAt}</p>
        </div>
        <span className={`review-status ${actionUnavailable ? 'is-muted' : ''}`}>
          Demo {request.status}
        </span>
      </div>

      <div className="review-request">
        <p className="review-label">CUSTOMER REQUEST</p>
        <p>{request.customerRequest}</p>
      </div>

      <dl className="review-metadata">
        <div>
          <dt>Intent</dt>
          <dd>{intentLabels[request.intent] || request.intent}</dd>
        </div>
        <div>
          <dt>Confidence</dt>
          <dd>{typeof request.confidence === 'number' ? `${Math.round(request.confidence * 100)}%` : 'Not available'}</dd>
        </div>
        <div>
          <dt>Order ID</dt>
          <dd>{request.orderId || 'Not provided'}</dd>
        </div>
      </dl>

      <p className="review-note"><ChevronRight size={15} /> {request.note}</p>

      {actionUnavailable && (
        <p className="review-api-note"><AlertCircle size={15} /> A decision cannot be sent until a backend queue supplies a conversation ID.</p>
      )}

      {result && (
        <div className="review-result is-success">
          <Check size={16} />
          <span>Backend response received: {result.response || 'Decision processed.'}</span>
        </div>
      )}

      {error && (
        <div className="review-result is-error">
          <AlertCircle size={16} />
          <span>Backend request failed: {error}</span>
        </div>
      )}

      <div className="review-actions">
        <button
          className="review-action approve"
          disabled={actionUnavailable || Boolean(decision)}
          onClick={() => submitDecision('approve')}
          type="button"
        >
          {decision === 'approve' ? <LoaderCircle className="spin" size={16} /> : <Check size={16} />}
          Approve
        </button>
        <button
          className="review-action reject"
          disabled={actionUnavailable || Boolean(decision)}
          onClick={() => submitDecision('reject')}
          type="button"
        >
          {decision === 'reject' ? <LoaderCircle className="spin" size={16} /> : <X size={16} />}
          Reject
        </button>
        <button
          className="review-action escalate"
          disabled={actionUnavailable || Boolean(decision)}
          onClick={() => submitDecision('escalate')}
          type="button"
        >
          {decision === 'escalate' ? <LoaderCircle className="spin" size={16} /> : <AlertCircle size={16} />}
          Escalate
        </button>
      </div>
    </article>
  )
}

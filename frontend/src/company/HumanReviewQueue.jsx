import { DatabaseZap, Info } from 'lucide-react'
import ReviewRequestCard from './ReviewRequestCard'

export default function HumanReviewQueue({ requests, onReviewProcessed }) {
  return (
    <section className="company-page-content">
      <div className="company-notice" role="status">
        <Info size={18} />
        <div>
          <strong>Live human review queue</strong>
          <p>
            These requests are retrieved from the backend and represent
            customer requests currently awaiting a human decision.
          </p>
        </div>
      </div>

      <div className="company-queue-summary">
        <div>
          <p className="company-section-kicker">REVIEW OPERATIONS</p>
          <h2>Requests awaiting a human decision</h2>
          <p>Approve, reject, or escalate only when a matching, pending backend conversation is available.</p>
        </div>
        <div className="company-summary-badge"><DatabaseZap size={17} /> Live data</div>
      </div>

      <div className="review-list">
        {requests.length > 0 ? (
          requests.map((request) => (
            <ReviewRequestCard
              key={request.review_id}
              request={request}
              onReviewProcessed={onReviewProcessed}
            />
          ))
        ) : (
          <div className="company-placeholder">
            <p className="company-section-kicker">QUEUE CLEAR</p>
            <h2>No pending human reviews</h2>
            <p>
              New requests requiring human review will appear here.
            </p>
          </div>
        )}
      </div>
    </section>
  )
}

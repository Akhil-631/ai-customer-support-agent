import { DatabaseZap, Info } from 'lucide-react'
import ReviewRequestCard from './ReviewRequestCard'

export default function HumanReviewQueue({ requests, onReviewProcessed }) {
  return (
    <section className="company-page-content">
      <div className="company-notice" role="status">
        <Info size={18} />
        <div>
          <strong>Live queue retrieval is not available yet.</strong>
          <p>The existing backend has no pending-review list endpoint. The requests below are DEMO / UI-ONLY records; they are not live or persistent.</p>
        </div>
      </div>

      <div className="company-queue-summary">
        <div>
          <p className="company-section-kicker">REVIEW OPERATIONS</p>
          <h2>Requests awaiting a human decision</h2>
          <p>Approve, reject, or escalate only when a matching, pending backend conversation is available.</p>
        </div>
        <div className="company-summary-badge"><DatabaseZap size={17} /> Demo data</div>
      </div>

      <div className="review-list">
        {requests.map((request) => <ReviewRequestCard key={request.id} request={request} onReviewProcessed={onReviewProcessed} />)}
      </div>
    </section>
  )
}

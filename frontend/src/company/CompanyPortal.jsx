import { useEffect, useState } from 'react'
import './company.css'
import CompanyHeader from './CompanyHeader'
import CompanyPlaceholderPage from './CompanyPlaceholderPage'
import CompanySidebar from './CompanySidebar'
import HumanReviewQueue from './HumanReviewQueue'

export default function CompanyPortal() {
  const [activePage, setActivePage] = useState('review-queue')
  const [reviewRequests, setReviewRequests] = useState([])

  const isReviewQueue = activePage === 'review-queue'

  const pageTitles = {
    conversations: 'Conversations',
    customers: 'Customers',
    orders: 'Orders',
    tickets: 'Tickets',
    'knowledge-base': 'Knowledge Base',
    analytics: 'Analytics',
    settings: 'Settings',
  }

  const handleReviewProcessed = (conversationId) => {
  setReviewRequests((currentRequests) =>
    currentRequests.filter(
      (request) => request.conversation_id !== conversationId
    )
  )
  }

  useEffect(() => {
    if (!isReviewQueue) {
      return
    }

    const fetchHumanReviews = async () => {
      try {
        const response = await fetch(
          'http://127.0.0.1:8000/human-reviews'
        )

        if (!response.ok) {
          throw new Error('Failed to fetch human review requests')
        }

        const data = await response.json()

        setReviewRequests(data.reviews || [])
      } catch (error) {
        console.error('Failed to load human review requests:', error)
        setReviewRequests([])
      }
    }

    fetchHumanReviews()
  }, [isReviewQueue])

  const title = isReviewQueue
    ? 'Human Review Queue'
    : pageTitles[activePage] || activePage

  const subtitle = isReviewQueue
    ? 'Review high-impact customer requests before the workflow continues.'
    : 'This area is ready for a future backend integration.'

  return (
    <div className="company-portal">
      <CompanySidebar
        activePage={activePage}
        onNavigate={setActivePage}
      />

      <main className="company-main">
        <CompanyHeader
          title={title}
          subtitle={subtitle}
        />

        {isReviewQueue
          ? <HumanReviewQueue
             requests={reviewRequests}
             onReviewProcessed={handleReviewProcessed}
           />
          : <CompanyPlaceholderPage pageName={title} />}
      </main>
    </div>
  )
}
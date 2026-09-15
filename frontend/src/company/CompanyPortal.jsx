import { useState } from 'react'
import './company.css'
import CompanyHeader from './CompanyHeader'
import CompanyPlaceholderPage from './CompanyPlaceholderPage'
import CompanySidebar from './CompanySidebar'
import HumanReviewQueue from './HumanReviewQueue'
import { demoReviewRequests } from './companyData'

export default function CompanyPortal() {
  const [activePage, setActivePage] = useState('review-queue')
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

  const title = isReviewQueue
  ? 'Human Review Queue'
  : pageTitles[activePage] || activePage
  const subtitle = isReviewQueue
    ? 'Review high-impact customer requests before the workflow continues.'
    : 'This area is ready for a future backend integration.'

  return (
    <div className="company-portal">
      <CompanySidebar activePage={activePage} onNavigate={setActivePage} />
      <main className="company-main">
        <CompanyHeader title={title} subtitle={subtitle} />
        {isReviewQueue
          ? <HumanReviewQueue requests={demoReviewRequests} />
          : <CompanyPlaceholderPage pageName={title} />}
      </main>
    </div>
  )
}

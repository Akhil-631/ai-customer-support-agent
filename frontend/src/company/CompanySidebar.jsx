import {
  BarChart3,
  BookOpen,
  FileText,
  LayoutDashboard,
  Package,
  Settings,
  Ticket,
  Users,
} from 'lucide-react'

const navigation = [
  { label: 'Conversations', icon: FileText },
  { label: 'Customers', icon: Users },
  { label: 'Orders', icon: Package },
  { label: 'Tickets', icon: Ticket },
  { label: 'Knowledge Base', icon: BookOpen },
  { label: 'Analytics', icon: BarChart3 },
  { label: 'Settings', icon: Settings },
]

export default function CompanySidebar({ activePage, onNavigate }) {
  return (
    <aside className="company-sidebar">
      <a className="company-brand" href="/company" aria-label="AI Customer Support home">
        <span className="company-brand-mark"><LayoutDashboard size={18} /></span>
        <span>
          <strong>AI Customer Support</strong>
          <small>Agent workspace</small>
        </span>
      </a>

      <nav className="company-navigation" aria-label="Company portal navigation">
        <p>WORKSPACE</p>
        <button
          className={`company-nav-item ${activePage === 'review-queue' ? 'is-active' : ''}`}
          type="button"
          onClick={() => onNavigate('review-queue')}
        >
          <span className="company-nav-icon"><Ticket size={17} /></span>
          Human Review Queue
        </button>

        <p className="company-nav-divider">MANAGE</p>
        {navigation.map(({ label, icon: Icon }) => (
          <button
            className={`company-nav-item ${activePage === label ? 'is-active' : ''}`}
            key={label}
            type="button"
            onClick={() => onNavigate(label)}
          >
            <span className="company-nav-icon"><Icon size={17} /></span>
            {label}
          </button>
        ))}
      </nav>

      <a className="company-customer-link" href="/">Open customer portal</a>
    </aside>
  )
}

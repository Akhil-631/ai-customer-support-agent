export default function CompanyHeader({ title, subtitle }) {
  return (
    <header className="company-header">
      <div>
        <p className="company-eyebrow">Operations</p>
        <h1>{title}</h1>
        <p className="company-header-subtitle">{subtitle}</p>
      </div>

      <div className="company-agent-profile" aria-label="Signed-in agent placeholder">
        <span>AM</span>
        <div>
          <strong>Support agent</strong>
          <small>Staff workspace</small>
        </div>
      </div>
    </header>
  )
}

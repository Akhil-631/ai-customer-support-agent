export default function CompanyPlaceholderPage({ pageName }) {
  return (
    <section className="company-page-content">
      <div className="company-placeholder">
        <p className="company-section-kicker">BACKEND INTEGRATION PENDING</p>
        <h2>{pageName}</h2>
        <p>
          This workspace area is intentionally a UI-only placeholder. The current API does not provide the data or operations required to make it live.
        </p>
      </div>
    </section>
  )
}

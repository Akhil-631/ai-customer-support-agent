export default function OrderPanel() {
  return (
    <aside className="order-panel">
      <p className="panel-label">ORDER CONTEXT</p>

      <div className="order-context-empty">
        <div className="order-context-icon">⌁</div>
        <h3>Order context unavailable</h3>
        <p>
          Live order details are not yet available in the customer portal.
          Ask a question in chat for the latest order support information.
        </p>
      </div>
    </aside>
  )
}

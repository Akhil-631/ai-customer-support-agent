import './App.css'
import Header from './components/Header'
import ConversationSidebar from './components/ConversationSidebar'
import ChatArea from './components/ChatArea'
import OrderPanel from './components/OrderPanel'
import { AssistantRuntime } from './runtime/assistantRuntime'
import CompanyPortal from './company/CompanyPortal'

function CustomerPortal() {
  return (
    <AssistantRuntime>
      <div className="app">
        <Header />

        <div className="app-body">
          <ConversationSidebar />

          <ChatArea />

          <OrderPanel />
        </div>
      </div>
    </AssistantRuntime>
  )
}

function App() {
  return window.location.pathname.startsWith('/company')
    ? <CompanyPortal />
    : <CustomerPortal />
}

export default App

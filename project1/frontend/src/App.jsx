import { useState } from 'react'
import Login from './Login'

function App() {
  const [loggedInUser, setLoggedInUser] = useState(null)

  if (loggedInUser) {
    return (
      <div className="login-page">
        <p>
          Welcome, {loggedInUser.first_name}! ({loggedInUser.is_admin ? 'Admin' : 'Customer'})
        </p>
      </div>
    )
  }

  return <Login onLoginSuccess={setLoggedInUser} />
}

export default App


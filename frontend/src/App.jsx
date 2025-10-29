import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import AdminDashboard from './pages/AdminDashboard'
import TouristApp from './pages/TouristApp'
import TouristSignup from './pages/TouristSignup'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<TouristSignup />} />
        <Route path="/tourist" element={<TouristApp />} />
        <Route path="/admin" element={<AdminDashboard />} />
      </Routes>
    </Router>
  )
}

export default App
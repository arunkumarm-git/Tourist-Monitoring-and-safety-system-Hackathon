import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { sendSOS } from '../services/api'
import PanicButton from '../components/PanicButton'

function TouristApp() {
  const navigate = useNavigate()
  const [touristId, setTouristId] = useState(null)
  const [location, setLocation] = useState(null)
  const [status, setStatus] = useState('safe')

  useEffect(() => {
    const id = localStorage.getItem('tourist_id')
    if (!id) {
      navigate('/')
      return
    }
    setTouristId(id)

    if ('geolocation' in navigator) {
      const watchId = navigator.geolocation.watchPosition(
        (position) => {
          setLocation({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude
          })
        },
        (error) => {
          console.error('Geolocation error:', error)
        },
        { enableHighAccuracy: true, maximumAge: 5000 }
      )

      return () => navigator.geolocation.clearWatch(watchId)
    }
  }, [navigate])

  const handlePanic = async () => {
    if (!location) return

    try {
      await sendSOS({
        tourist_id: touristId,
        latitude: location.latitude,
        longitude: location.longitude
      })
      alert('Emergency alert sent!')
    } catch (error) {
      alert('Failed to send alert')
    }
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1>T-MASS Tourist Tracker</h1>
        <div style={{...styles.status, background: status === 'safe' ? '#4CAF50' : '#f44336'}}>
          {status === 'safe' ? 'You are in a safe zone' : 'Warning: Unsafe area'}
        </div>
      </div>
      
      <div style={styles.content}>
        {location && (
          <div style={styles.locationInfo}>
            <p>Latitude: {location.latitude.toFixed(6)}</p>
            <p>Longitude: {location.longitude.toFixed(6)}</p>
          </div>
        )}
      </div>

      <PanicButton onClick={handlePanic} />
    </div>
  )
}

const styles = {
  container: {
    height: '100vh',
    display: 'flex',
    flexDirection: 'column',
    background: '#f5f5f5'
  },
  header: {
    background: 'white',
    padding: '20px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
    textAlign: 'center'
  },
  status: {
    marginTop: '10px',
    padding: '10px',
    borderRadius: '5px',
    color: 'white',
    fontWeight: 'bold'
  },
  content: {
    flex: 1,
    padding: '20px'
  },
  locationInfo: {
    background: 'white',
    padding: '20px',
    borderRadius: '10px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
  }
}

export default TouristApp
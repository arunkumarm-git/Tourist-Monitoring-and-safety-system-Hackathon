import React, { useState, useEffect } from 'react'
import MapView from '../components/Map/MapView'
import AlertsPanel from '../components/AlertsPanel'
import { useTourists, useAlerts } from '../hooks/useFirebase'

function AdminDashboard() {
  const { value: tourists } = useTourists()
  const { value: alerts } = useAlerts()
  const [selectedTourist, setSelectedTourist] = useState(null)

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1>T-MASS Admin Dashboard</h1>
        <div style={styles.stats}>
          <div style={styles.statBox}>
            <div style={styles.statNumber}>{tourists ? Object.keys(tourists).length : 0}</div>
            <div style={styles.statLabel}>Active Tourists</div>
          </div>
          <div style={styles.statBox}>
            <div style={styles.statNumber}>{alerts ? Object.keys(alerts).length : 0}</div>
            <div style={styles.statLabel}>Active Alerts</div>
          </div>
        </div>
      </div>

      <div style={styles.main}>
        <div style={styles.mapContainer}>
          <MapView tourists={tourists} alerts={alerts} onTouristClick={setSelectedTourist} />
        </div>
        <div style={styles.sidebar}>
          <AlertsPanel alerts={alerts} tourists={tourists} />
        </div>
      </div>
    </div>
  )
}

const styles = {
  container: {
    height: '100vh',
    display: 'flex',
    flexDirection: 'column'
  },
  header: {
    background: 'white',
    padding: '20px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
  },
  stats: {
    display: 'flex',
    gap: '20px',
    marginTop: '15px'
  },
  statBox: {
    background: '#f5f5f5',
    padding: '15px',
    borderRadius: '8px',
    textAlign: 'center'
  },
  statNumber: {
    fontSize: '32px',
    fontWeight: 'bold',
    color: '#667eea'
  },
  statLabel: {
    fontSize: '14px',
    color: '#666',
    marginTop: '5px'
  },
  main: {
    flex: 1,
    display: 'flex',
    overflow: 'hidden'
  },
  mapContainer: {
    flex: 1
  },
  sidebar: {
    width: '400px',
    background: 'white',
    borderLeft: '1px solid #ddd',
    overflow: 'auto'
  }
}

export default AdminDashboard
import React from 'react'
import { getAlertColor, getAlertText, formatTimestamp } from '../utils/helpers'
import { resolveAlert } from '../services/api'

function AlertsPanel({ alerts, tourists }) {
  if (!alerts) return <div style={styles.container}>No active alerts</div>

  const handleResolve = async (alertId) => {
    try {
      await resolveAlert(alertId)
    } catch (error) {
      console.error('Failed to resolve alert:', error)
    }
  }

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Active Alerts</h2>
      <div style={styles.alertsList}>
        {Object.entries(alerts)
          .filter(([_, alert]) => !alert.resolved)
          .map(([id, alert]) => (
            <div key={id} style={{...styles.alertCard, borderLeft: `4px solid ${getAlertColor(alert.alert_level)}`}}>
              <div style={styles.alertHeader}>
                <span style={styles.alertLevel}>{getAlertText(alert.alert_level)}</span>
                <span style={styles.alertTime}>{formatTimestamp(alert.timestamp)}</span>
              </div>
              <div style={styles.alertBody}>
                <p><strong>Tourist:</strong> {alert.tourist_id}</p>
                <p><strong>Type:</strong> {alert.alert_type}</p>
                <p><strong>Zone:</strong> {alert.zone_type}</p>
              </div>
              <button onClick={() => handleResolve(id)} style={styles.resolveButton}>
                Resolve
              </button>
            </div>
          ))}
      </div>
    </div>
  )
}

const styles = {
  container: {
    padding: '20px'
  },
  title: {
    marginBottom: '20px',
    color: '#333'
  },
  alertsList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '15px'
  },
  alertCard: {
    background: 'white',
    padding: '15px',
    borderRadius: '8px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
  },
  alertHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '10px'
  },
  alertLevel: {
    fontWeight: 'bold',
    fontSize: '14px'
  },
  alertTime: {
    fontSize: '12px',
    color: '#666'
  },
  alertBody: {
    fontSize: '14px',
    marginBottom: '10px'
  },
  resolveButton: {
    background: '#4CAF50',
    color: 'white',
    border: 'none',
    padding: '8px 16px',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '14px'
  }
}

export default AlertsPanel
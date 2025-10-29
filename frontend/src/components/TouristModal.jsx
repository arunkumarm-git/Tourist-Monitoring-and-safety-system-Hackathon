import React from 'react'

function TouristModal({ tourist, onClose }) {
  if (!tourist) return null

  return (
    <div style={styles.overlay} onClick={onClose}>
      <div style={styles.modal} onClick={e => e.stopPropagation()}>
        <h2>Tourist Details</h2>
        <div style={styles.content}>
          <p><strong>ID:</strong> {tourist.id}</p>
          <p><strong>Status:</strong> {tourist.status}</p>
          <p><strong>Current Zone:</strong> {tourist.current_zone}</p>
          {tourist.last_location && (
            <>
              <p><strong>Latitude:</strong> {tourist.last_location.lat}</p>
              <p><strong>Longitude:</strong> {tourist.last_location.lng}</p>
            </>
          )}
        </div>
        <button onClick={onClose} style={styles.closeButton}>Close</button>
      </div>
    </div>
  )
}

const styles = {
  overlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: 'rgba(0,0,0,0.5)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1000
  },
  modal: {
    background: 'white',
    padding: '30px',
    borderRadius: '10px',
    maxWidth: '500px',
    width: '90%'
  },
  content: {
    margin: '20px 0'
  },
  closeButton: {
    background: '#667eea',
    color: 'white',
    border: 'none',
    padding: '10px 20px',
    borderRadius: '5px',
    cursor: 'pointer'
  }
}

export default TouristModal
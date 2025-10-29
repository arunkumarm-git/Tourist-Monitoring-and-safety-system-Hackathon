import React, { useState } from 'react'

function PanicButton({ onClick }) {
  const [pressed, setPressed] = useState(false)

  const handleClick = () => {
    setPressed(true)
    onClick()
    setTimeout(() => setPressed(false), 2000)
  }

  return (
    <div style={styles.container}>
      <button
        onClick={handleClick}
        disabled={pressed}
        style={{...styles.button, opacity: pressed ? 0.5 : 1}}
      >
        {pressed ? 'ALERT SENT!' : 'EMERGENCY'}
      </button>
    </div>
  )
}

const styles = {
  container: {
    position: 'fixed',
    bottom: '40px',
    left: '50%',
    transform: 'translateX(-50%)',
    zIndex: 1000
  },
  button: {
    width: '150px',
    height: '150px',
    borderRadius: '50%',
    background: 'linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%)',
    color: 'white',
    fontSize: '20px',
    fontWeight: 'bold',
    border: '5px solid white',
    boxShadow: '0 10px 30px rgba(255, 65, 108, 0.5)',
    cursor: 'pointer',
    transition: 'all 0.3s'
  }
}

export default PanicButton
export const formatTimestamp = (timestamp) => {
  return new Date(timestamp).toLocaleString()
}

export const getAlertColor = (level) => {
  switch(level) {
    case 0: return 'green'
    case 1: return 'blue'
    case 2: return 'orange'
    case 3: return 'red'
    default: return 'gray'
  }
}

export const getAlertText = (level) => {
  switch(level) {
    case 0: return 'Normal'
    case 1: return 'Info'
    case 2: return 'Warning'
    case 3: return 'Critical'
    default: return 'Unknown'
  }
}

export const calculateDistance = (lat1, lng1, lat2, lng2) => {
  const R = 6371000
  const dLat = (lat2 - lat1) * Math.PI / 180
  const dLng = (lng2 - lng1) * Math.PI / 180
  const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
            Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
            Math.sin(dLng/2) * Math.sin(dLng/2)
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))
  return R * c
}
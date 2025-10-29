import React from 'react'
import { Marker, Popup } from 'react-leaflet'
import L from 'leaflet'
import { getAlertColor } from '../../utils/helpers'

function TouristMarker({ tourist, alert, onClick }) {
  const color = alert ? getAlertColor(alert.alert_level) : 'green'
  
  const icon = L.divIcon({
    className: 'custom-marker',
    html: `<div style="background: ${color}; width: 20px; height: 20px; border-radius: 50%; border: 2px solid white;"></div>`,
    iconSize: [20, 20]
  })

  if (!tourist.last_location) return null

  return (
    <Marker
      position={[tourist.last_location.lat, tourist.last_location.lng]}
      icon={icon}
      eventHandlers={{ click: onClick }}
    >
      <Popup>
        <div>
          <strong>Tourist ID:</strong> {tourist.id}<br />
          <strong>Status:</strong> {tourist.status}<br />
          <strong>Zone:</strong> {tourist.current_zone}
        </div>
      </Popup>
    </Marker>
  )
}

export default TouristMarker
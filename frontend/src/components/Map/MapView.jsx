import React from 'react'
import { MapContainer, TileLayer } from 'react-leaflet'
import TouristMarker from './TouristMarker'
import ZoneOverlay from './ZoneOverlay'
import ClusterOverlay from './ClusterOverlay'

function MapView({ tourists, alerts, onTouristClick }) {
  const center = [13.05, 80.28]

  return (
    <MapContainer center={center} zoom={14} style={{ width: '100%', height: '100%' }}>
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; OpenStreetMap contributors'
      />
      
      <ZoneOverlay />
      
      {tourists && Object.entries(tourists).map(([id, tourist]) => (
        <TouristMarker
          key={id}
          tourist={{ id, ...tourist }}
          alert={alerts?.[id]}
          onClick={() => onTouristClick({ id, ...tourist })}
        />
      ))}
    </MapContainer>
  )
}

export default MapView
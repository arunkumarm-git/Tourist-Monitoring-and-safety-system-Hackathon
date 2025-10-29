import React from 'react'
import { Polygon } from 'react-leaflet'

const zones = {
  marina: [
    [13.06761, 80.28465],
    [13.06550, 80.29025],
    [13.03937, 80.27903],
    [13.03874, 80.28135]
  ],
  fishing: [
    [13.04498, 80.28259],
    [13.04493, 80.28369],
    [13.04029, 80.28276],
    [13.04037, 80.28143]
  ],
  deep_water: [
    [13.064994, 80.290795],
    [13.064979, 80.291600],
    [13.036658, 80.281407],
    [13.036670, 80.281890]
  ]
}

function ZoneOverlay() {
  return (
    <>
      <Polygon positions={zones.marina} pathOptions={{ color: 'green', fillOpacity: 0.1 }} />
      <Polygon positions={zones.fishing} pathOptions={{ color: 'orange', fillOpacity: 0.1 }} />
      <Polygon positions={zones.deep_water} pathOptions={{ color: 'red', fillOpacity: 0.1 }} />
    </>
  )
}

export default ZoneOverlay
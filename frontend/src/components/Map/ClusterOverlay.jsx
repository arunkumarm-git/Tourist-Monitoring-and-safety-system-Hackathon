import React from 'react'
import { Circle, Popup } from 'react-leaflet'

function ClusterOverlay({ clusters }) {
  if (!clusters) return null

  return (
    <>
      {clusters.map((cluster, idx) => (
        <Circle
          key={idx}
          center={[cluster.center_lat, cluster.center_lng]}
          radius={50}
          pathOptions={{ color: 'blue', fillOpacity: 0.2 }}
        >
          <Popup>
            <div>
              <strong>Cluster {cluster.cluster_id}</strong><br />
              Tourists: {cluster.count}
            </div>
          </Popup>
        </Circle>
      ))}
    </>
  )
}

export default ClusterOverlay
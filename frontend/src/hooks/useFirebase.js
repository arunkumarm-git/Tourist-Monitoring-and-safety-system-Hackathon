import { useState, useEffect } from 'react'
import { ref, onValue, off } from 'firebase/database'
import { database } from '../config/firebase'

export const useFirebaseValue = (path) => {
  const [value, setValue] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const dbRef = ref(database, path)
    
    const unsubscribe = onValue(dbRef, (snapshot) => {
      setValue(snapshot.val())
      setLoading(false)
    }, (error) => {
      setError(error)
      setLoading(false)
    })

    return () => off(dbRef, 'value', unsubscribe)
  }, [path])

  return { value, loading, error }
}

export const useTourists = () => {
  return useFirebaseValue('tourists')
}

export const useAlerts = () => {
  return useFirebaseValue('alerts')
}

export const useLocations = () => {
  return useFirebaseValue('locations')
}
import { useState, useEffect } from 'react'
import { supabase } from '../config/supabase'

export const useSupabaseQuery = (table, query = {}) => {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        let queryBuilder = supabase.from(table).select('*')
        
        if (query.eq) {
          Object.entries(query.eq).forEach(([key, value]) => {
            queryBuilder = queryBuilder.eq(key, value)
          })
        }
        
        const { data: result, error: err } = await queryBuilder
        
        if (err) throw err
        setData(result)
      } catch (err) {
        setError(err)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [table, JSON.stringify(query)])

  return { data, loading, error }
}
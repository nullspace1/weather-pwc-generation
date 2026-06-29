import { useEffect, useReducer } from 'react'

type Subscribable = {
  subscribe(listener: () => void): () => void
}

export function useStateObject<T extends Subscribable>(state: T): T {
  const [, rerender] = useReducer((count: number) => count + 1, 0)

  useEffect(() => state.subscribe(() => rerender()), [state])

  return state
}

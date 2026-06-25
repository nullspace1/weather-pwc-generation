import type { LocationDTO } from '../lib/dto/location'
import { searchLocations } from '../lib/api/locations'

type Listener = () => void

class LocationState {
  query = ''
  results: LocationDTO[] = []
  selected: LocationDTO | null = null
  loading = false
  error: string | null = null

  private listeners = new Set<Listener>()

  subscribe(listener: Listener): () => void {
    this.listeners.add(listener)
    return () => this.listeners.delete(listener)
  }

  private notify(): void {
    this.listeners.forEach((listener) => listener())
  }

  setQuery(query: string): void {
    this.query = query
    this.notify()
  }

  select(location: LocationDTO): void {
    this.selected = location
    this.notify()
  }

  clearSelection(): void {
    this.selected = null
    this.notify()
  }

  async search(): Promise<void> {
    const trimmed = this.query.trim()
    if (!trimmed) {
      this.results = []
      this.error = null
      this.notify()
      return
    }

    this.loading = true
    this.error = null
    this.notify()

    try {
      const response = await searchLocations(trimmed)
      this.results = response.locations
    } catch {
      this.error = 'Failed to search locations'
      this.results = []
    } finally {
      this.loading = false
      this.notify()
    }
  }
}

export const locationState = new LocationState()

import type { LocationDTO } from '../lib/dto/location'
import {
  deleteSavedLocation,
  getStoredLocations,
  saveLocation as saveLocationApi,
} from '../lib/api/locations'
import { locationState } from './locationState'

type Listener = () => void

class SavedLocationsState {
  saved: LocationDTO[] = []
  loading = false
  saving = false
  deleting: number | null = null
  error: string | null = null
  customName = ''
  customLatitude = ''
  customLongitude = ''

  private listeners = new Set<Listener>()

  subscribe(listener: Listener): () => void {
    this.listeners.add(listener)
    return () => this.listeners.delete(listener)
  }

  private notify(): void {
    this.listeners.forEach((listener) => listener())
  }

  async loadSaved(): Promise<void> {
    this.loading = true
    this.error = null
    this.notify()

    try {
      const response = await getStoredLocations()
      this.saved = response.locations
    } catch {
      this.error = 'Failed to load saved locations'
      this.saved = []
    } finally {
      this.loading = false
      this.notify()
    }
  }

  async saveLocation(location: LocationDTO): Promise<void> {
    this.saving = true
    this.error = null
    this.notify()

    try {
      await saveLocationApi({
        name: location.name,
        latitude: location.latitude,
        longitude: location.longitude,
      })
      await this.loadSaved()
    } catch {
      this.error = 'Failed to save location'
    } finally {
      this.saving = false
      this.notify()
    }
  }

  setCustomName(name: string): void {
    this.customName = name
    this.notify()
  }

  setCustomLatitude(latitude: string): void {
    this.customLatitude = latitude
    this.notify()
  }

  setCustomLongitude(longitude: string): void {
    this.customLongitude = longitude
    this.notify()
  }

  canSaveCustomLocation(): boolean {
    const name = this.customName.trim()
    const latitude = Number(this.customLatitude)
    const longitude = Number(this.customLongitude)
    return (
      name !== '' &&
      !Number.isNaN(latitude) &&
      latitude >= -90 &&
      latitude <= 90 &&
      !Number.isNaN(longitude) &&
      longitude >= -180 &&
      longitude <= 180
    )
  }

  async saveCustomLocation(): Promise<void> {
    if (!this.canSaveCustomLocation()) {
      this.error = 'Enter a valid name and coordinates'
      this.notify()
      return
    }

    const location: LocationDTO = {
      name: this.customName.trim(),
      latitude: Number(this.customLatitude),
      longitude: Number(this.customLongitude),
    }

    await this.saveLocation(location)

    if (!this.error) {
      this.customName = ''
      this.customLatitude = ''
      this.customLongitude = ''
      this.notify()
    }
  }

  selectSaved(location: LocationDTO): void {
    locationState.select(location)
  }

  async deleteLocation(locationId: number): Promise<void> {
    this.deleting = locationId
    this.error = null
    this.notify()

    try {
      await deleteSavedLocation(locationId)
      await this.loadSaved()
    } catch {
      this.error = 'Failed to delete location'
    } finally {
      this.deleting = null
      this.notify()
    }
  }
}

export const savedLocationsState = new SavedLocationsState()

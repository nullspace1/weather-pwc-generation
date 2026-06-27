import type { LocationResponseDTO, LocationSaveRequestDTO } from '../dto/location'
import { apiDelete, apiGet, apiPostJson } from './client'

export function searchLocations(name: string): Promise<LocationResponseDTO> {
  return apiGet<LocationResponseDTO>('/locations', { name })
}

export function getStoredLocations(): Promise<LocationResponseDTO> {
  return apiGet<LocationResponseDTO>('/weather/locations')
}

export function saveLocation(location: LocationSaveRequestDTO): Promise<void> {
  return apiPostJson('/weather/locations', location)
}

export function deleteSavedLocation(locationId: number): Promise<void> {
  return apiDelete(`/weather/locations/${locationId}`)
}

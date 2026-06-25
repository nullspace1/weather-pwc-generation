import type { LocationResponseDTO } from '../dto/location'
import { apiGet } from './client'

export function searchLocations(location: string): Promise<LocationResponseDTO> {
  return apiGet<LocationResponseDTO>('/locations', { location })
}

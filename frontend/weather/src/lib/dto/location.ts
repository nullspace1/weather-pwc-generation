export interface LocationDTO {
  id?: number
  name: string
  latitude: number
  longitude: number
}

export interface LocationResponseDTO {
  locations: LocationDTO[]
}

export interface LocationSaveRequestDTO {
  name: string
  latitude: number
  longitude: number
}

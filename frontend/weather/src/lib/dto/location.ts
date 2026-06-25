export interface LocationDTO {
  name: string
  country: string
  latitude: number
  longitude: number
}

export interface LocationResponseDTO {
  locations: LocationDTO[]
}

export interface LocationRequestDTO {
  location: string
}

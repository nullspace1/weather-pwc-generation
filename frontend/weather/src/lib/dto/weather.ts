export interface WeatherDataRequestDTO {
  lat: number
  lon: number
  from_date: string
  to_date: string
  file_name: string
}

export interface WeatherDataResponseDTO {
  file_path: string
}

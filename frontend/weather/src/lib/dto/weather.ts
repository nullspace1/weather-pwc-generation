export interface WeatherDataRequestDTO {
  lat: number
  lon: number
  from_date: string
  to_date: string
  report_name: string
  save_to_cache?: boolean
  location_name?: string
}

export interface WeatherDataResponseDTO {
  file_path: string
}

import type { WeatherDataRequestDTO, WeatherDataResponseDTO } from '../dto/weather'
import { apiGet } from './client'

export function generateWeatherData(request: WeatherDataRequestDTO): Promise<WeatherDataResponseDTO> {
  return apiGet<WeatherDataResponseDTO>('/weather', {
    lat: String(request.lat),
    lon: String(request.lon),
    from_date: request.from_date,
    to_date: request.to_date,
    file_name: request.file_name,
  })
}

import type { WeatherDataRequestDTO, WeatherDataResponseDTO } from '../dto/weather'
import { apiGet } from './client'

export function generateWeatherData(request: WeatherDataRequestDTO): Promise<WeatherDataResponseDTO> {
  const params: Record<string, string> = {
    lat: String(request.lat),
    lon: String(request.lon),
    from_date: request.from_date,
    to_date: request.to_date,
    report_name: request.report_name,
  }
  if (request.save_to_cache) {
    params.save_to_cache = 'true'
  }
  if (request.location_name) {
    params.location_name = request.location_name
  }
  return apiGet<WeatherDataResponseDTO>('/weather', params)
}

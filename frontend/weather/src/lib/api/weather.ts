import type { WeatherDataRequestDTO } from '../dto/weather'

const API_BASE_URL = 'http://localhost:8000'

export async function generateWeatherData(request: WeatherDataRequestDTO): Promise<void> {
  const url = new URL('/weather', API_BASE_URL)
  url.searchParams.set('lat', String(request.lat))
  url.searchParams.set('lon', String(request.lon))
  url.searchParams.set('from_date', request.from_date)
  url.searchParams.set('to_date', request.to_date)
  url.searchParams.set('output_path', request.output_path)

  const response = await fetch(url)
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`)
  }
}

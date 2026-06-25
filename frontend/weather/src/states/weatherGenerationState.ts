import { generateWeatherData } from '../lib/api/weather'

type Listener = () => void

class WeatherGenerationState {
  fromDate = ''
  toDate = ''
  outputPath = ''
  loading = false
  error: string | null = null
  success = false

  private listeners = new Set<Listener>()

  subscribe(listener: Listener): () => void {
    this.listeners.add(listener)
    return () => this.listeners.delete(listener)
  }

  private notify(): void {
    this.listeners.forEach((listener) => listener())
  }

  setFromDate(fromDate: string): void {
    this.fromDate = fromDate
    this.success = false
    this.notify()
  }

  setToDate(toDate: string): void {
    this.toDate = toDate
    this.success = false
    this.notify()
  }

  setOutputPath(outputPath: string): void {
    this.outputPath = outputPath
    this.success = false
    this.notify()
  }

  async generate(lat: number, lon: number): Promise<void> {
    this.loading = true
    this.error = null
    this.success = false
    this.notify()

    try {
      await generateWeatherData({
        lat,
        lon,
        from_date: this.fromDate,
        to_date: this.toDate,
        output_path: this.outputPath,
      })
      this.success = true
    } catch {
      this.error = 'Failed to generate weather data'
    } finally {
      this.loading = false
      this.notify()
    }
  }
}

export const weatherGenerationState = new WeatherGenerationState()

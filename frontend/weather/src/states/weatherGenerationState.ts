import { generateWeatherData } from '../lib/api/weather'
import { savedReportsState } from './savedReportsState'

type Listener = () => void

class WeatherGenerationState {
  fromDate = ''
  toDate = ''
  reportName = ''
  saveToCache = false
  savedFilePath: string | null = null
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

  setReportName(reportName: string): void {
    this.reportName = reportName
    this.success = false
    this.notify()
  }

  setSaveToCache(saveToCache: boolean): void {
    this.saveToCache = saveToCache
    this.notify()
  }

  async generate(lat: number, lon: number, locationName?: string): Promise<void> {
    this.loading = true
    this.error = null
    this.success = false
    this.savedFilePath = null
    this.notify()

    try {
      const response = await generateWeatherData({
        lat,
        lon,
        from_date: this.fromDate,
        to_date: this.toDate,
        report_name: this.reportName,
        save_to_cache: this.saveToCache,
        location_name: locationName,
      })
      this.savedFilePath = response.file_path
      this.success = true
      if (this.saveToCache) {
        await savedReportsState.loadReports()
      }
    } catch {
      this.error = 'Failed to generate weather data'
    } finally {
      this.loading = false
      this.notify()
    }
  }
}

export const weatherGenerationState = new WeatherGenerationState()

import type { ReportDTO } from '../lib/dto/report'
import { deleteCachedReport, exportCachedReport, getCachedReports } from '../lib/api/reports'

type Listener = () => void

class SavedReportsState {
  reports: ReportDTO[] = []
  loading = false
  deleting: string | null = null
  resaving: string | null = null
  resavedFilePath: string | null = null
  error: string | null = null

  private listeners = new Set<Listener>()

  subscribe(listener: Listener): () => void {
    this.listeners.add(listener)
    return () => this.listeners.delete(listener)
  }

  private notify(): void {
    this.listeners.forEach((listener) => listener())
  }

  async loadReports(): Promise<void> {
    this.loading = true
    this.error = null
    this.notify()

    try {
      const response = await getCachedReports()
      this.reports = response.reports
    } catch {
      this.error = 'Failed to load saved reports'
      this.reports = []
    } finally {
      this.loading = false
      this.notify()
    }
  }

  async deleteReport(name: string): Promise<void> {
    this.deleting = name
    this.error = null
    this.resavedFilePath = null
    this.notify()

    try {
      await deleteCachedReport(name)
      await this.loadReports()
    } catch {
      this.error = 'Failed to delete report'
    } finally {
      this.deleting = null
      this.notify()
    }
  }

  async resaveReport(name: string): Promise<void> {
    this.resaving = name
    this.error = null
    this.resavedFilePath = null
    this.notify()

    try {
      const response = await exportCachedReport(name)
      this.resavedFilePath = response.file_path
    } catch {
      this.error = 'Failed to re-save report'
    } finally {
      this.resaving = null
      this.notify()
    }
  }
}

export const savedReportsState = new SavedReportsState()

import { useEffect } from 'react'
import { Card } from './Card'
import type { ReportDTO } from '../lib/dto/report'
import { savedReportsState } from '../states/savedReportsState'
import { useStateObject } from '../states/useStateObject'

function formatDate(isoDate: string): string {
  return new Date(isoDate).toLocaleString()
}

function formatLocation(report: ReportDTO): string {
  if (report.location_name) {
    return report.location_name
  }
  if (report.latitude != null && report.longitude != null) {
    return `${report.latitude.toFixed(4)}, ${report.longitude.toFixed(4)}`
  }
  return 'Unknown location'
}

function formatDateRange(report: ReportDTO): string | null {
  if (report.from_date && report.to_date) {
    return `${report.from_date} – ${report.to_date}`
  }
  return null
}

export function SavedReportsCard() {
  const state = useStateObject(savedReportsState)

  useEffect(() => {
    void savedReportsState.loadReports()
  }, [])

  return (
    <div className="saved-reports-card">
      <Card title="Saved Reports">
        {state.error && <p className="message error">{state.error}</p>}
        {state.loading && <p className="message">Loading saved reports…</p>}
        {!state.loading && state.reports.length === 0 && (
          <p className="message">No saved reports yet.</p>
        )}
        {!state.loading && state.reports.length > 0 && (
          <ul className="result-list">
            {state.reports.map((report) => {
              const dateRange = formatDateRange(report)
              return (
              <li key={report.name}>
                <div className="result-row">
                  <div className="report-item">
                    <span className="result-name">{report.name}</span>
                    <span className="result-meta">{formatLocation(report)}</span>
                    {dateRange && <span className="result-meta">{dateRange}</span>}
                    <span className="result-meta">Saved {formatDate(report.created_at)}</span>
                  </div>
                  <div className="result-actions">
                    <button
                      type="button"
                      className="button"
                      onClick={() => void state.resaveReport(report.name)}
                      disabled={state.resaving === report.name || state.deleting === report.name}
                    >
                      {state.resaving === report.name ? 'Saving…' : 'Re-save'}
                    </button>
                    <button
                      type="button"
                      className="button button-secondary"
                      onClick={() => void state.deleteReport(report.name)}
                      disabled={state.deleting === report.name || state.resaving === report.name}
                    >
                      {state.deleting === report.name ? 'Deleting…' : 'Delete'}
                    </button>
                  </div>
                </div>
              </li>
              )
            })}
          </ul>
        )}
        {state.resavedFilePath && (
          <p className="message success">Report saved to {state.resavedFilePath}</p>
        )}
      </Card>
    </div>
  )
}

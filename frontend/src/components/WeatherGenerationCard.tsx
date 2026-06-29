import { useEffect } from 'react'
import { Card } from './Card'
import { folderState } from '../states/folderState'
import { locationState } from '../states/locationState'
import { weatherGenerationState } from '../states/weatherGenerationState'
import { useStateObject } from '../states/useStateObject'

export function WeatherGenerationCard() {
  const location = useStateObject(locationState)
  const folder = useStateObject(folderState)
  const generation = useStateObject(weatherGenerationState)

  useEffect(() => {
    void folderState.loadSelectedFolder()
  }, [])

  const handleGenerate = () => {
    if (!location.selected) {
      return
    }
    void generation.generate(
      location.selected.latitude,
      location.selected.longitude,
      location.selected.name
    )
  }

  const canGenerate =
    location.selected !== null &&
    folder.selectedPath !== null &&
    generation.fromDate !== '' &&
    generation.toDate !== '' &&
    generation.reportName.trim() !== ''

  return (
    <div className="weather-generation-card">
    <Card title="Generate weather data">
      <div className="form">
        <label className="field">
          <span className="field-label">From date</span>
          <input
            type="date"
            className="input"
            value={generation.fromDate}
            onChange={(event) => generation.setFromDate(event.target.value)}
          />
        </label>

        <label className="field">
          <span className="field-label">To date</span>
          <input
            type="date"
            className="input"
            value={generation.toDate}
            onChange={(event) => generation.setToDate(event.target.value)}
          />
        </label>

        <div className="field">
          <span className="field-label">Output folder</span>
          <div className="field-row">
            <input
              type="text"
              className="input"
              readOnly
              placeholder="No folder selected"
              value={folder.selectedPath ?? ''}
            />
            <button
              type="button"
              className="button"
              onClick={() => void folder.selectFolder()}
              disabled={folder.loading}
            >
              {folder.loading ? 'Selecting…' : 'Select folder'}
            </button>
          </div>
        </div>

        <label className="field">
          <span className="field-label">Report name</span>
          <input
            type="text"
            className="input"
            placeholder="my-report"
            value={generation.reportName}
            onChange={(event) => generation.setReportName(event.target.value)}
          />
        </label>

        <label className="field checkbox-field">
          <input
            type="checkbox"
            checked={generation.saveToCache}
            onChange={(event) => generation.setSaveToCache(event.target.checked)}
          />
          <span className="field-label">Save report locally</span>
        </label>

        {!location.selected && (
          <p className="message">Select a location before generating weather data.</p>
        )}

        {folder.error && <p className="message error">{folder.error}</p>}
        {generation.error && <p className="message error">{generation.error}</p>}
        {generation.success && generation.savedFilePath && (
          <p className="message success">
            Weather data saved to {generation.savedFilePath}
            {generation.saveToCache && ' and cached locally.'}
          </p>
        )}

        <button
          type="button"
          className="button"
          onClick={handleGenerate}
          disabled={!canGenerate || generation.loading}
        >
          {generation.loading ? 'Generating…' : 'Generate .wea'}
        </button>
      </div>
    </Card>
    </div>
  )
}

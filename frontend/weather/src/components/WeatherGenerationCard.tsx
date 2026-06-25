import { Card } from './Card'
import { locationState } from '../states/locationState'
import { weatherGenerationState } from '../states/weatherGenerationState'
import { useStateObject } from '../states/useStateObject'

export function WeatherGenerationCard() {
  const location = useStateObject(locationState)
  const generation = useStateObject(weatherGenerationState)

  const handleGenerate = () => {
    if (!location.selected) {
      return
    }
    void generation.generate(location.selected.latitude, location.selected.longitude)
  }

  const canGenerate =
    location.selected !== null &&
    generation.fromDate !== '' &&
    generation.toDate !== '' &&
    generation.outputPath.trim() !== ''

  return (
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

        <label className="field">
          <span className="field-label">Output file path</span>
          <input
            type="text"
            className="input"
            placeholder="C:\data\weather.csv"
            value={generation.outputPath}
            onChange={(event) => generation.setOutputPath(event.target.value)}
          />
        </label>

        {!location.selected && (
          <p className="message">Select a location before generating weather data.</p>
        )}

        {generation.error && <p className="message error">{generation.error}</p>}
        {generation.success && (
          <p className="message success">Weather data saved to {generation.outputPath}</p>
        )}

        <button
          type="button"
          className="button"
          onClick={handleGenerate}
          disabled={!canGenerate || generation.loading}
        >
          {generation.loading ? 'Generating…' : 'Generate CSV'}
        </button>
      </div>
    </Card>
  )
}

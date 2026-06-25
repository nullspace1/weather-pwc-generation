import { type FormEvent } from 'react'
import { Card } from './Card'
import { locationState } from '../states/locationState'
import { useStateObject } from '../states/useStateObject'

export function LocationCard() {
  const state = useStateObject(locationState)

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    void state.search()
  }

  return (
    <Card title="Location">
      <form className="form" onSubmit={handleSubmit}>
        <label className="field">
          <span className="field-label">Search</span>
          <div className="field-row">
            <input
              type="text"
              className="input"
              placeholder="City or place name"
              value={state.query}
              onChange={(event) => state.setQuery(event.target.value)}
            />
            <button type="submit" className="button" disabled={state.loading}>
              {state.loading ? 'Searching…' : 'Search'}
            </button>
          </div>
        </label>
      </form>

      {state.error && <p className="message error">{state.error}</p>}

      {state.selected && (
        <div className="selection">
          <p className="selection-label">Selected location</p>
          <p className="selection-value">
            {state.selected.name}, {state.selected.country}
          </p>
          <p className="selection-meta">
            {state.selected.latitude.toFixed(4)}, {state.selected.longitude.toFixed(4)}
          </p>
          <button type="button" className="button button-secondary" onClick={() => state.clearSelection()}>
            Clear
          </button>
        </div>
      )}

      {!state.selected && state.results.length > 0 && (
        <ul className="result-list">
          {state.results.map((location) => (
            <li key={`${location.name}-${location.latitude}-${location.longitude}`}>
              <button type="button" className="result-item" onClick={() => state.select(location)}>
                <span className="result-name">
                  {location.name}, {location.country}
                </span>
                <span className="result-meta">
                  {location.latitude.toFixed(4)}, {location.longitude.toFixed(4)}
                </span>
              </button>
            </li>
          ))}
        </ul>
      )}
    </Card>
  )
}

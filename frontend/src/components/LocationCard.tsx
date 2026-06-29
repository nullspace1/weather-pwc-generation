import { useEffect, type FormEvent } from 'react'
import { Card } from './Card'
import { locationState } from '../states/locationState'
import { savedLocationsState } from '../states/savedLocationsState'
import { useStateObject } from '../states/useStateObject'
import type { LocationDTO } from '../lib/dto/location'

function formatLocation(location: LocationDTO): string {
  return location.name
}

export function LocationCard() {
  const state = useStateObject(locationState)
  const saved = useStateObject(savedLocationsState)

  useEffect(() => {
    void savedLocationsState.loadSaved()
  }, [])

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    void state.search()
  }

  const handleSave = (location: LocationDTO) => {
    void saved.saveLocation(location)
  }

  return (
    <div className="location-card">
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
            <p className="selection-value">{formatLocation(state.selected)}</p>
            <p className="selection-meta">
              {state.selected.latitude.toFixed(4)}, {state.selected.longitude.toFixed(4)}
            </p>
            <div className="field-row">
              <button
                type="button"
                className="button button-secondary"
                onClick={() => state.clearSelection()}
              >
                Clear
              </button>
              <button
                type="button"
                className="button"
                onClick={() => handleSave(state.selected!)}
                disabled={saved.saving}
              >
                {saved.saving ? 'Saving…' : 'Save'}
              </button>
            </div>
          </div>
        )}

        {!state.selected && state.results.length > 0 && (
          <ul className="result-list">
            {state.results.map((location) => (
              <li key={`${location.name}-${location.latitude}-${location.longitude}`}>
                <div className="result-row">
                  <button
                    type="button"
                    className="result-item"
                    onClick={() => state.select(location)}
                  >
                    <span className="result-name">{formatLocation(location)}</span>
                    <span className="result-meta">
                      {location.latitude.toFixed(4)}, {location.longitude.toFixed(4)}
                    </span>
                  </button>
                  <button
                    type="button"
                    className="button button-secondary"
                    onClick={() => handleSave(location)}
                    disabled={saved.saving}
                  >
                    Save
                  </button>
                </div>
              </li>
            ))}
          </ul>
        )}
      </Card>

      <Card title="Saved Locations">
        <form
          className="form"
          onSubmit={(event) => {
            event.preventDefault()
            void saved.saveCustomLocation()
          }}
        >
          <label className="field">
            <span className="field-label">Custom location name</span>
            <input
              type="text"
              className="input"
              placeholder="My field site"
              value={saved.customName}
              onChange={(event) => saved.setCustomName(event.target.value)}
            />
          </label>
          <div className="form-grid">
            <label className="field">
              <span className="field-label">Latitude</span>
              <input
                type="text"
                className="input"
                placeholder="52.5200"
                value={saved.customLatitude}
                onChange={(event) => saved.setCustomLatitude(event.target.value)}
              />
            </label>
            <label className="field">
              <span className="field-label">Longitude</span>
              <input
                type="text"
                className="input"
                placeholder="13.4050"
                value={saved.customLongitude}
                onChange={(event) => saved.setCustomLongitude(event.target.value)}
              />
            </label>
          </div>
          <button
            type="submit"
            className="button"
            disabled={!saved.canSaveCustomLocation() || saved.saving}
          >
            {saved.saving ? 'Saving…' : 'Save custom location'}
          </button>
        </form>

        {saved.error && <p className="message error">{saved.error}</p>}
        {saved.loading && <p className="message">Loading saved locations…</p>}
        {!saved.loading && saved.saved.length === 0 && (
          <p className="message">No saved locations yet.</p>
        )}
        {!saved.loading && saved.saved.length > 0 && (
          <ul className="result-list">
            {saved.saved.map((location) => (
              <li key={location.id ?? `${location.name}-${location.latitude}-${location.longitude}`}>
                <div className="result-row">
                  <button
                    type="button"
                    className="result-item"
                    onClick={() => saved.selectSaved(location)}
                  >
                    <span className="result-name">{formatLocation(location)}</span>
                    <span className="result-meta">
                      {location.latitude.toFixed(4)}, {location.longitude.toFixed(4)}
                    </span>
                  </button>
                  {location.id !== undefined && (
                    <button
                      type="button"
                      className="button button-secondary"
                      onClick={() => void saved.deleteLocation(location.id!)}
                      disabled={saved.deleting === location.id}
                    >
                      {saved.deleting === location.id ? 'Deleting…' : 'Delete'}
                    </button>
                  )}
                </div>
              </li>
            ))}
          </ul>
        )}
      </Card>
    </div>
  )
}

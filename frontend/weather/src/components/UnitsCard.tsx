import { useEffect } from 'react'
import type {
  ConfigUnitsDTO,
  ETZeroUnits,
  PrecipitationUnits,
  RadiationUnits,
  TemperatureUnits,
  WindSpeedUnits,
} from '../lib/dto/config'
import { Card } from './Card'
import { unitsState } from '../states/unitsState'
import { useStateObject } from '../states/useStateObject'

const precipitationOptions: PrecipitationUnits[] = ['mm/day', 'cm/day', 'in/day']
const temperatureOptions: TemperatureUnits[] = ['C', 'F', 'K']
const windSpeedOptions: WindSpeedUnits[] = ['m/s', 'km/h', 'mph']
const radiationOptions: RadiationUnits[] = ['W/m²', 'kW/m²', 'MJ/m^2/day', 'La/day']
const et0Options: ETZeroUnits[] = ['mm/day', 'cm/day', 'in/day']

export function UnitsCard() {
  const state = useStateObject(unitsState)

  useEffect(() => {
    void state.load()
  }, [state])

  const updateField = <K extends keyof ConfigUnitsDTO>(key: K, value: ConfigUnitsDTO[K]) => {
    if (!state.units) {
      return
    }
    void state.update({ ...state.units, [key]: value })
  }

  return (
    <Card title="Units">


      {state.loading && <p className="message">Loading units…</p>}
      {state.saving && <p className="message">Saving…</p>}
      {state.error && <p className="message error">{state.error}</p>}

      {state.units && (
        <div className="form form-grid">
          <label className="field">
            <span className="field-label">Precipitation</span>
            <select
              className="select"
              value={state.units.precipitation_sum}
              disabled={state.saving}
              onChange={(event) => updateField('precipitation_sum', event.target.value as PrecipitationUnits)}
            >
              {precipitationOptions.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>

          <label className="field">
            <span className="field-label">Temperature</span>
            <select
              className="select"
              value={state.units.temperature_2m_mean}
              disabled={state.saving}
              onChange={(event) => updateField('temperature_2m_mean', event.target.value as TemperatureUnits)}
            >
              {temperatureOptions.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>

          <label className="field">
            <span className="field-label">Wind speed</span>
            <select
              className="select"
              value={state.units.wind_speed_10m_mean}
              disabled={state.saving}
              onChange={(event) => updateField('wind_speed_10m_mean', event.target.value as WindSpeedUnits)}
            >
              {windSpeedOptions.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>

          <label className="field">
            <span className="field-label">Radiation</span>
            <select
              className="select"
              value={state.units.shortwave_radiation_sum}
              disabled={state.saving}
              onChange={(event) => updateField('shortwave_radiation_sum', event.target.value as RadiationUnits)}
            >
              {radiationOptions.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>

          <label className="field">
            <span className="field-label">ET₀</span>
            <select
              className="select"
              value={state.units.et0_fao_evapotranspiration}
              disabled={state.saving}
              onChange={(event) =>
                updateField('et0_fao_evapotranspiration', event.target.value as ETZeroUnits)
              }
            >
              {et0Options.map((option) => (
                <option key={option} value={option}>
                  {option}
                </option>
              ))}
            </select>
          </label>
        </div>
      )}
    </Card>
  )
}

import type { ConfigUnitsDTO, ConfigUnitsRequestDTO } from '../dto/config'
import { apiGet, apiPost } from './client'

export function getUnits(): Promise<ConfigUnitsDTO> {
  return apiGet<ConfigUnitsDTO>('/config/units')
}

export function setUnits(units: ConfigUnitsRequestDTO): Promise<void> {
  return apiPost('/config/units', {
    precipitation_sum: units.precipitation_sum,
    et0_fao_evapotranspiration: units.et0_fao_evapotranspiration,
    temperature_2m_mean: units.temperature_2m_mean,
    wind_speed_10m_mean: units.wind_speed_10m_mean,
    shortwave_radiation_sum: units.shortwave_radiation_sum,
  })
}

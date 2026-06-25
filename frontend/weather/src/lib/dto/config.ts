export type PrecipitationUnits = 'cm/day' | 'mm/day' | 'in/day'
export type TemperatureUnits = 'C' | 'F' | 'K'
export type WindSpeedUnits = 'm/s' | 'km/h' | 'mph'
export type RadiationUnits = 'W/m²' | 'kW/m²' | 'MJ/m^2/day' | 'La/day'
export type ETZeroUnits = 'cm/day' | 'mm/day' | 'in/day'

export interface ConfigUnitsDTO {
  precipitation_sum: PrecipitationUnits
  et0_fao_evapotranspiration: ETZeroUnits
  temperature_2m_mean: TemperatureUnits
  wind_speed_10m_mean: WindSpeedUnits
  shortwave_radiation_sum: RadiationUnits
}

export type ConfigUnitsRequestDTO = ConfigUnitsDTO

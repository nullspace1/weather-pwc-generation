import { LocationCard } from '../components/LocationCard'
import { UnitsCard } from '../components/UnitsCard'
import { WeatherGenerationCard } from '../components/WeatherGenerationCard'

export function WeatherPage() {
  return (
    <div className="page">
      <LocationCard />
      <UnitsCard />
      <WeatherGenerationCard />
    </div>
  )
}

import { LocationCard } from '../components/LocationCard'
import { SavedReportsCard } from '../components/SavedReportsCard'
import { WeatherGenerationCard } from '../components/WeatherGenerationCard'

export function WeatherPage() {
  return (
    <div className="page">
      <LocationCard />
      <WeatherGenerationCard />
      <SavedReportsCard />
    </div>
  )
}

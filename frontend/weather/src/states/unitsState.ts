import type { ConfigUnitsDTO } from '../lib/dto/config'
import { getUnits, setUnits } from '../lib/api/config'

type Listener = () => void

class UnitsState {
  units: ConfigUnitsDTO | null = null
  loading = false
  saving = false
  error: string | null = null

  private listeners = new Set<Listener>()

  subscribe(listener: Listener): () => void {
    this.listeners.add(listener)
    return () => this.listeners.delete(listener)
  }

  private notify(): void {
    this.listeners.forEach((listener) => listener())
  }

  async load(): Promise<void> {
    this.loading = true
    this.error = null
    this.notify()

    try {
      this.units = await getUnits()
    } catch {
      this.error = 'Failed to load units'
    } finally {
      this.loading = false
      this.notify()
    }
  }

  async update(units: ConfigUnitsDTO): Promise<void> {
    this.saving = true
    this.error = null
    this.notify()

    try {
      await setUnits(units)
      this.units = units
    } catch {
      this.error = 'Failed to update units'
    } finally {
      this.saving = false
      this.notify()
    }
  }
}

export const unitsState = new UnitsState()

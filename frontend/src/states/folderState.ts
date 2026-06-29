import { getSelectedFolder, selectFolder } from '../lib/api/folders'

type Listener = () => void

class FolderState {
  selectedPath: string | null = null
  loading = false
  error: string | null = null

  private listeners = new Set<Listener>()

  subscribe(listener: Listener): () => void {
    this.listeners.add(listener)
    return () => this.listeners.delete(listener)
  }

  private notify(): void {
    this.listeners.forEach((listener) => listener())
  }

  async loadSelectedFolder(): Promise<void> {
    try {
      const response = await getSelectedFolder()
      this.selectedPath = response.path
      this.error = null
    } catch {
      this.selectedPath = null
      this.error = 'Failed to load selected folder'
    } finally {
      this.notify()
    }
  }

  async selectFolder(): Promise<void> {
    this.loading = true
    this.error = null
    this.notify()

    try {
      const response = await selectFolder()
      this.selectedPath = response.path
    } catch {
      this.error = 'Folder selection cancelled'
    } finally {
      this.loading = false
      this.notify()
    }
  }
}

export const folderState = new FolderState()

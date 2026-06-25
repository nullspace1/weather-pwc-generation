type TabNavProps = {
  activeTab?: string
}

export function TabNav({ activeTab = 'weather' }: TabNavProps) {
  return (
    <nav className="tab-nav" aria-label="Main navigation">
      <button type="button" className="tab active" aria-current={activeTab === 'weather' ? 'page' : undefined}>
        Weather
      </button>
    </nav>
  )
}

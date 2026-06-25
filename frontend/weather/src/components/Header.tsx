import logo from '../assets/logo.svg'
import { TabNav } from './TabNav'

export function Header() {
  return (
    <header className="app-header">
      <div className="brand">
        <img src={logo} alt="" className="brand-logo" />
        <span className="brand-name">Weather</span>
      </div>
      <TabNav />
    </header>
  )
}

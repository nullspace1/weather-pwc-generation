import { Footer } from './components/Footer'
import { Header } from './components/Header'
import { WeatherPage } from './pages/WeatherPage'
import './App.css'

function App() {
  return (
    <div className="app">
      <Header />
      <main className="app-main">
        <WeatherPage />
      </main>
      <Footer />
    </div>
  )
}

export default App

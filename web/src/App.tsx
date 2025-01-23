import LiveComponents from "./components/live"
import EventGraph from "./components/events"
import SearchEvents from "./components/search"

function App() {
  return (
    <main className="flex flex-col gap-5 h-screen p-5">
      <div className="flex flex-row gap-5">
        <LiveComponents />
        <SearchEvents />
      </div>
      <EventGraph />
    </main>
  )
}

export default App

import { Loader2 } from "lucide-react"
import CountComponent from "./components/count"
import EventGraph from "./components/events"
import LiveComponents from "./components/live"
import RecentComponents from "./components/recent"
import SearchEvents from "./components/search"
import { Card } from "./components/ui/card"
import { options, useQuery } from "./hooks/fetcher"

function App() {
  const { data, error, isLoading, isValidating, mutate } = useQuery(
    "/api/events/", undefined, options
  );

  console.log(data);

  return (
    <main className="flex flex-col gap-3 justify-between min-h-screen p-5">
      <div className="flex  md:flex-row gap-3 flex-col h-full">
        <Card className="p-2 min-h-96 aspect-video">
          <LiveComponents />
        </Card>
        <Card className="p-2 flex-row flex gap-2">
          {isLoading ? <Loader2 className="m-auto animate-spin" /> :
            <RecentComponents data={data?.data} />}
        </Card>
        <div className="flex flex-row md:flex-col gap-2 w-full">
          <SearchEvents mutate={mutate} />
        </div>
      </div>
      <div className="flex flex-col w-full md:flex-row gap-3">
        <Card className="w-full min-h-32 flex flex-col">
          {isLoading ? <Loader2 className="m-auto animate-spin" /> :
            <EventGraph events={data?.events} />}
        </Card>
        <Card className="flex flex-col min-h-32 min-w-32">
          {isLoading ? <Loader2 className="m-auto animate-spin" /> :
            <CountComponent data={data?.data} />}
        </Card>
      </div>
    </main>
  )
}

export default App

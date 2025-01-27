import LiveComponents from "./components/live"
import RecentComponents from "./components/recent"
import EventGraph from "./components/events"
import SearchEvents from "./components/search"
import { Button } from "./components/ui/button"
import { PersonStandingIcon } from "lucide-react"
import { Card } from "./components/ui/card"
import CountComponent from "./components/count"
import { useQuery } from "@/hooks/fetcher"

function App() {
    const { data, error, isLoading, isValidating, mutate } = useQuery(
      "/api/events/images"
    );
  
    console.log(data);
  
  return (
    <main className="flex flex-col gap-3 justify-between min-h-screen p-5">
      <div className="flex  md:flex-row gap-3 flex-col h-full">
        <Card className="p-2 min-h-96 aspect-video">
          <LiveComponents />
        </Card>
        <Card className="p-2 flex-row flex gap-2">
          <RecentComponents data={data} />
        </Card>
        <div className="flex flex-row md:flex-col gap-2 w-full">
          <div className="flex flex-row md:w-full gap-2">
            <Button size={"icon"} variant={"default"}>
              <PersonStandingIcon />
            </Button>
            <Button size={"icon"} variant={"default"}>
              <PersonStandingIcon />
            </Button>
            <Button size={"icon"} variant={"default"}>
              <PersonStandingIcon />
            </Button>
          </div>
          <SearchEvents />
        </div>
      </div>
      <div className="flex flex-col w-full md:flex-row gap-3">
        <EventGraph />
        <CountComponent />
      </div>
    </main>
  )
}

export default App

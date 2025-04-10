import { CarIcon, PersonStandingIcon, RefreshCcw } from "lucide-react"
import { useState } from "react"
import { Button } from "../components/ui/button"
import { AsyncSelect } from "../components/ui/search"
import { backend } from "../hooks/fetcher"
import triedAsync from "../lib/utils"

type Event = {
    id: string
    text: string
    icon?: string
}

const SearchEvents = ({mutate}:{mutate: () => void}) => {
    const [selectedEvent, setSelectedEvent] = useState<string>("")

    const searchAllEvents = async (query?: string) => {
        if (!query || query.length < 5) return []

        const {isSuccess, data} = await triedAsync(
            (async () => {
                const res = await fetch(backend + `/api/search?q=${encodeURIComponent(query)}`)
                const data = (await res.json()) as Event[]

                return data
            })()
        )

        if (!isSuccess) {
            return []
        }

        return data
    }
    return (
        <>
            <div className="flex flex-row md:w-full gap-2">
                <Button onClick={mutate} size={"icon"} variant={"default"}>
                    <RefreshCcw />
                </Button>
                <Button size={"icon"} variant={"default"}>
                    <PersonStandingIcon />
                </Button>
                <Button size={"icon"} variant={"default"}>
                    <CarIcon />
                </Button>
            </div>
            <AsyncSelect<Event>
                fetcher={searchAllEvents}
                filterFn={(event, query) => event.id.toLowerCase().includes(query.toLowerCase())}
                renderOption={(event) => (
                    <div className="flex items-center gap-2">
                        {/* <img
                        src={event.query}
                        alt={event.title}
                        width={24}
                        height={24}
                        className="rounded-full"
                    /> */}
                        <div className="flex flex-col">
                            <div className="text-xs text-muted-foreground">{event.text}</div>
                        </div>
                    </div>
                )}
                getOptionValue={(event) => event.id}
                getDisplayValue={(event) => (
                    <div className="flex items-center gap-2 text-left">
                        {/* <img
                        src={event.query}
                        alt={event.title}
                        width={24}
                        height={24}
                        className="rounded-full"
                    /> */}
                        <div className="flex flex-col leading-tight">
                            <div className="text-xxs text-muted-foreground">{event.text}</div>
                        </div>
                    </div>
                )}
                notFound={<div className="py-6 text-center text-sm">No events found <br /> Type more spefically</div>}
                label="Event"
                placeholder="Search events..."
                value={selectedEvent}
                onChange={setSelectedEvent}
                className="w-full"
            />
        </>
    );
}

export default SearchEvents;
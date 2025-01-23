import { AsyncSelect } from "../components/ui/search"
import { useState } from "react"

const searchAllEvents = async () => ([
    {
        query: "hi",
        title: "hi",
        icon: "hi",
    },
    {
        query: "hi",
        title: "hi",
        icon: "hi",
    },
    {
        query: "hi",
        title: "hi",
        icon: "hi",
    },
    {
        query: "hi",
        title: "hi",
        icon: "hi",
    },
    {
        query: "hi",
        title: "hi",
        icon: "hi",
    },
])

type Event = {
    query: string
    title: string
    icon?: string
}

const SearchEvents = () => {
    const [selectedEvent, setSelectedEvent] = useState<string>("")
    return (
        <AsyncSelect<Event>
            fetcher={searchAllEvents}
            preload
            filterFn={(event, query) => event.query.toLowerCase().includes(query.toLowerCase())}
            renderOption={(event) => (
                <div className="flex items-center gap-2">
                    <img
                        src={event.query}
                        alt={event.title}
                        width={24}
                        height={24}
                        className="rounded-full"
                    />
                    <div className="flex flex-col">
                        <div className="font-medium">{event.title}</div>
                        <div className="text-xs text-muted-foreground">{event.query}</div>
                    </div>
                </div>
            )}
            getOptionValue={(event) => event.query}
            getDisplayValue={(event) => (
                <div className="flex items-center gap-2 text-left">
                    <img
                        src={event.query}
                        alt={event.title}
                        width={24}
                        height={24}
                        className="rounded-full"
                    />
                    <div className="flex flex-col leading-tight">
                        <div className="font-medium">{event.title}</div>
                        <div className="text-xxs text-muted-foreground">{event.query}</div>
                    </div>
                </div>
            )}
            notFound={<div className="py-6 text-center text-sm">No events found</div>}
            label="Event"
            placeholder="Search events..."
            value={selectedEvent}
            onChange={setSelectedEvent}
            width="100%"
            className=""
        />
    );
}

export default SearchEvents;
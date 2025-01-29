import { Dot } from "lucide-react";
import { backend } from "../hooks/fetcher";

const LiveComponents = () => {
    const src = `${backend}/live/stream`
    return (
        <div className="rounded-xl overflow-hidden w-full h-full relative">
            <span className="absolute bg-red-600 m-2 rounded-md pe-2 flex items-center">
                <Dot className="animate-ping font-bolder"/> LIVE
            </span>
            <img id="video-feed" src={src} className="w-full h-auto border-0" />
        </div>
    );
}

export default LiveComponents;
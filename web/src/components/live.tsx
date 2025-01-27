import { backend } from "../hooks/fetcher";

const LiveComponents = () => {
    const src = `${backend}/live/stream`
    return (
        <div className="rounded-xl overflow-hidden w-full h-full">
            <img id="video-feed" src={src} className="w-full h-auto border-0" />
        </div>
    );
}

export default LiveComponents;
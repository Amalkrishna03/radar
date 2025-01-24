const LiveComponents = () => {
    const src = "https://github.com/user-attachments/assets/42645a0c-adf7-4c21-8502-2b6979ca01a1"
    return (
        <div className="rounded-xl overflow-hidden w-full h-full">
            <img id="video-feed" src={src} className="w-full h-auto border-0" />
        </div>
    );
}

export default LiveComponents;
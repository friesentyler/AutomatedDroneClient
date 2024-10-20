import './App.css';
import {APIProvider, Map, useMap} from '@vis.gl/react-google-maps';
import {useEffect, useState, useRef} from "react";
import droneImgSrc from './images/drone.png';

const MarkerComponent = ({position}) => {
    // IT APPEARS THAT GOOGLE MAPS WILL ONLY UPDATE THE MARKER POSITION IF IT NOTICES A DIFFERENCE OF AT LEAST 0.00001
    const map = useMap();
    const markerRef = useRef(null); // Use ref to store the marker instance

    useEffect(() => {
        const updateMarkerPosition = async () => {
            if (!map || !window.google || !window.google.maps) return;

            // Load the marker library
            const {AdvancedMarkerElement} = await window.google.maps.importLibrary('marker');

            if (!markerRef.current) {
                // If marker does not exist, create it
                const droneImg = document.createElement('img');
                droneImg.src = droneImgSrc;
                droneImg.style.position = 'absolute';
                droneImg.style.top = '-12.5px';
                droneImg.style.left = '-12.5px';

                markerRef.current = new AdvancedMarkerElement({
                    map: map,
                    position: position,
                    content: droneImg,
                    title: 'A marker using a custom PNG Image',
                });
            } else {
                // If marker already exists, just update its position
                markerRef.current.position = position;
            }
        };

        updateMarkerPosition();
    }, [map, position]); // Re-run when the map or position changes

    return null;
};


function MapClickEvent({coordinates}) {
    const map = useMap();
    const flightPath = useRef(null);

    useEffect(() => {
        let listener;
        let flightPlanCoordinates;


        if (map && window.google && window.google.maps) {
            listener = map.addListener("click", async (e) => {

                // delete the line that already exists (if there is one)
                if (flightPath.current) {
                    flightPath.current.setMap(null);
                }

                // draw the line to the clicked coordinates on the map
                console.log(coordinates);
                console.log(e.latLng.toJSON().lat, e.latLng.toJSON().lng);
                flightPlanCoordinates = [
                    {lat: coordinates.lat, lng: coordinates.lng},
                    {lat: e.latLng.toJSON().lat, lng: e.latLng.toJSON().lng}
                ];
                flightPath.current = new window.google.maps.Polyline({
                    path: flightPlanCoordinates,
                    strokeColor: "#FF0000",
                    strokeOpacity: 1.0,
                    strokeWeight: 2,
                });
                flightPath.current.setMap(map);

                // sends a request to the backend telling the drone to go to the specified coordinates from the click
                const baseUrl = "http://127.0.0.1:8000"
                const urlWithPath = baseUrl + `/goto/${e.latLng.toJSON().lat}/${e.latLng.toJSON().lng}`;
                console.log(urlWithPath);
                let response = await fetch(baseUrl + "/cancel")
                response = await fetch(urlWithPath);

                return () => {
                    console.log("unmounted")
                    window.google.maps.event.removeListener(listener);
                };


            });
        }

    }, [map, coordinates]);
    return null;
}

function CircleCreatorButton({coordinates}) {
    const map = useMap();
    const circle = useRef(null);

    function createCircle() {
        if (map && window.google && window.google.maps) {
            clearCircle();
            circle.current = new window.google.maps.Circle({
                strokeColor: "#FF0000",
                strokeOpacity: 0.8,
                strokeWeight: 2,
                fillColor: "#FF0000",
                fillOpacity: 0.35,
                map,
                center: coordinates,
                radius: 3000,
            });
            circle.current.setMap(map);
        }
    }

    function clearCircle() {
        if (map && window.google && window.google.maps) {
            if (circle.current) {
                circle.current.setMap(null);
            }
        }
    }

    return (
        <>
            <button onClick={createCircle}>
                Create Circle
            </button>
            <button onClick={clearCircle}>
                Clear Circle
            </button>
        </>
    );
}

function TakeOffButton () {

    async function takeOff() {
        const baseUrl = "http://127.0.0.1:8000"
        const urlWithPath = baseUrl + `/takeoff/`;
        const response = await fetch(urlWithPath);
    }

    return (
        <>
            <button onClick={takeOff}>
                Takeoff
            </button>
        </>
    );
}

function LandButton () {
    async function landing() {
        const baseUrl = "http://127.0.0.1:8000"
        const urlWithPath = baseUrl + `/land/`;
        const response = await fetch(urlWithPath);
    }

    return (
        <>
            <button onClick={landing}>
                Land
            </button>
        </>
    )
}

function App() {
    const [droneCoordinates, setDroneCoordinates] = useState({lat: 47.3977413, lng: 8.545592899999999});

    function clicked() {
        let newLat = droneCoordinates.lat
        let newLng = droneCoordinates.lng
        setDroneCoordinates({lat: newLat + 0.001, lng: newLng + 0.001})
    }

    useEffect(() => {

        const socket = new WebSocket('ws://127.0.0.1:8000/ws/gps/');

        socket.onopen = function (event) {
            console.log("WebSocket is open now.")
        }

        socket.onmessage = function (event) {
            const gpsData = JSON.parse(event.data);
            console.log(gpsData.lat + " " + gpsData.long)
            setDroneCoordinates({lat: Number(gpsData.lat), lng: Number(gpsData.long)})
        }

        socket.onclose = function (event) {
            console.log('WebSocket is closed now.');
        };

        socket.onerror = function (error) {
            console.log('WebSocket error:', error);
        };

        /*return () => {
            //console.log('WebSocket closed.');
            socket.close();
        };*/
    }, []);

    return (
        <div className="App">
            <header className="App-header">
                <APIProvider apiKey={'AIzaSyCaHPO79ej6YBd5YOnyn5m0oCZneJm_yc0'}
                             onLoad={() => console.log('Maps API has loaded.')}>
                    <div className="map-container">
                        <Map
                            defaultZoom={13}
                            defaultCenter={{lat: droneCoordinates.lat, lng: droneCoordinates.lng}}
                            mapTypeId={'satellite'}
                            mapId={'740a767ea9270ac5'}
                            onCameraChanged={(ev) =>
                                console.log('camera changed:', ev.detail.center, 'zoom:', ev.detail.zoom)
                            }>
                            <MarkerComponent position={droneCoordinates}/>
                            <MapClickEvent coordinates={droneCoordinates}/>
                        </Map>
                    </div>
                    <CircleCreatorButton coordinates={droneCoordinates}/>
                    <TakeOffButton/>
                    <LandButton/>
                </APIProvider>
                <a
                    className="App-link"
                    href="https://reactjs.org"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    Learn React
                </a>
                <button onClick={clicked}>yeet change coords</button>
            </header>
        </div>
    );
}

export default App;

import {
  LocalUser,
  RemoteUser,
  useIsConnected,
  useJoin,
  useLocalMicrophoneTrack,
  useLocalCameraTrack,
  usePublish,
  useRemoteUsers,
} from "agora-rtc-react";
import React, { useState } from "react";
export const Basics = () => {
  const [calling, setCalling] = useState(false);
  const isConnected = useIsConnected(); // Store the user's connection status
  const [appId, setAppId] = useState("");
  const [channel, setChannel] = useState("");
  const [token, setToken] = useState("");

  useJoin({appid: appId, channel: channel, token: token ? token : null}, calling);

  const [micOn, setMic] = useState(true);
  const [cameraOn, setCamera] = useState(true);
  const { localMicrophoneTrack } = useLocalMicrophoneTrack(micOn);
  const { localCameraTrack } = useLocalCameraTrack(cameraOn);
  usePublish([localMicrophoneTrack, localCameraTrack]);

  const remoteUsers = useRemoteUsers();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-4xl">
        {isConnected ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 bg-white rounded-lg shadow-md">
            <div className="relative w-full h-64 md:h-96">
              <LocalUser
                audioTrack={localMicrophoneTrack}
                cameraOn={cameraOn}
                micOn={micOn}
                videoTrack={localCameraTrack}
                cover="https://www.agora.io/en/wp-content/uploads/2022/10/3d-spatial-audio-icon.svg"
                className="w-full h-full bg-gray-300 rounded-lg overflow-hidden flex items-center justify-center"
              >
                <span className="absolute bottom-2 left-2 bg-black bg-opacity-50 text-white px-2 py-1 rounded">You</span>
              </LocalUser>
            </div>
            {remoteUsers.map((user) => (
              <div key={user.uid} className="relative w-full h-64">
                <RemoteUser
                  user={user}
                  cover="https://www.agora.io/en/wp-content/uploads/2022/10/3d-spatial-audio-icon.svg"
                  className="w-full h-full bg-gray-300 rounded-lg overflow-hidden"
                >
                  <span className="absolute bottom-2 left-2 bg-black bg-opacity-50 text-white px-2 py-1 rounded">{user.uid}</span>
                </RemoteUser>
              </div>
            ))}
          </div>
        ) : (
          <div className="flex flex-col items-center p-6 bg-white border border-gray-300 rounded-lg">
            <input
              className="my-2 p-2 w-72 border border-gray-300 rounded"
              onChange={e => setAppId(e.target.value)}
              placeholder="<Your app ID>"
              value={appId}
            />
            <input
              className="my-2 p-2 w-72 border border-gray-300 rounded"
              onChange={e => setChannel(e.target.value)}
              placeholder="<Your channel Name>"
              value={channel}
            />
            <input
              className="my-2 p-2 w-72 border border-gray-300 rounded"
              onChange={e => setToken(e.target.value)}
              placeholder="<Your token>"
              value={token}
            />
            <button
              className={`mt-4 px-4 py-2 rounded ${
                !appId || !channel
                  ? 'bg-gray-300 cursor-not-allowed'
                  : 'bg-blue-500 hover:bg-blue-600 text-white'
              }`}
              disabled={!appId || !channel}
              onClick={() => setCalling(true)}
            >
              <span>Join Channel</span>
            </button>
          </div>
        )}
      </div>
      {isConnected && (
        <div className="mt-4 flex space-x-4">
          <button
            className={`p-2 rounded-full ${micOn ? 'bg-blue-500' : 'bg-red-500'} text-white`}
            onClick={() => setMic(a => !a)}
          >
            {micOn ? '🎤' : '🔇'}
          </button>
          <button
            className={`p-2 rounded-full ${cameraOn ? 'bg-blue-500' : 'bg-red-500'} text-white`}
            onClick={() => setCamera(a => !a)}
          >
            {cameraOn ? '📷' : '🚫'}
          </button>
          <button
            className={`p-2 rounded-full ${calling ? 'bg-red-500' : 'bg-green-500'} text-white`}
            onClick={() => setCalling(a => !a)}
          >
            {calling ? '📞' : '📞'}
          </button>
        </div>
      )}
    </div>
  );
};

export default Basics;

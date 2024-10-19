"use client";

import React, { useState, useEffect } from "react";
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
import Image from 'next/image';

export const Basics = () => {
  const [calling, setCalling] = useState(false);
  const [appId, setAppId] = useState("");
  const [channel, setChannel] = useState("");
  const [token, setToken] = useState("");

  const isConnected = useIsConnected();

  useJoin({appid: appId, channel: channel, token: token ? token : null}, calling);

  // Local user
  const [micOn, setMic] = useState(true);
  const [cameraOn, setCamera] = useState(true);
  const { localMicrophoneTrack } = useLocalMicrophoneTrack(micOn);
  const { localCameraTrack } = useLocalCameraTrack(cameraOn);
  usePublish([localMicrophoneTrack, localCameraTrack]);

  // Remote users
  const remoteUsers = useRemoteUsers();

  useEffect(() => {
    console.log('Local camera track:', localCameraTrack);
  }, [localCameraTrack]);

  useEffect(() => {
    return () => {
      localCameraTrack?.close();
    };
  }, [localCameraTrack]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      {isConnected ? (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 bg-white rounded-lg shadow-md w-full max-w-4xl">
            <div className="relative w-full h-64 md:h-96">
              <LocalUser
                audioTrack={localMicrophoneTrack}
                cameraOn={cameraOn}
                micOn={micOn}
                videoTrack={localCameraTrack}
                className="w-full h-full bg-gray-300 rounded-lg overflow-hidden flex items-center justify-center"
              >
                {!localCameraTrack && (
                  <div className="text-gray-500">Camera not available</div>
                )}
                <span className="absolute bottom-2 left-2 bg-black bg-opacity-50 text-white px-2 py-1 rounded">You</span>
              </LocalUser>
            </div>
            {remoteUsers.map((user) => (
              <div key={user.uid} className="relative">
                <RemoteUser user={user} className="w-full h-48 bg-gray-300 rounded-lg overflow-hidden">
                  <span className="absolute bottom-2 left-2 bg-black bg-opacity-50 text-white px-2 py-1 rounded">{user.uid}</span>
                </RemoteUser>
              </div>
            ))}
          </div>
          <div className="mt-4 flex space-x-4">
            <button
              className={`p-2 rounded-full ${micOn ? 'bg-blue-500' : 'bg-red-500'}`}
              onClick={() => setMic(a => !a)}
            >
              {micOn ? '🎤' : '🔇'}
            </button>
            <button
              className={`p-2 rounded-full ${cameraOn ? 'bg-blue-500' : 'bg-red-500'}`}
              onClick={() => setCamera(a => !a)}
            >
              {cameraOn ? '📷' : '🚫'}
            </button>
            <button
              className="p-2 rounded-full bg-red-500 text-white"
              onClick={() => setCalling(false)}
            >
              Leave
            </button>
          </div>
        </>
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
  );
};

export default Basics;

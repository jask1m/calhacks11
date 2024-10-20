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
import React, { useState, useEffect } from "react";
import axios from "axios";
import { useRTCClient, useClientEvent } from "agora-rtc-react";

export const Basics = () => {
  const appId = import.meta.env.VITE_AGORA_APP_ID;
  const token = import.meta.env.VITE_AGORA_APP_TOKEN;
  const customerKey = import.meta.env.AGORA_CUSTOMER_KEY;
  const customerSecret = import.meta.env.AGORA_CUSTOMER_SECRET;
  const [calling, setCalling] = useState(false);
  const isConnected = useIsConnected(); // Store the user's connection status
  const [channel, setChannel] = useState("");
  const [builderToken, setBuilderToken] = useState("");
  const [taskId, setTaskId] = useState("");
  const [transcription, setTranscription] = useState("");

  const { client } = useRTCClient(); // Get the client object

  useClientEvent(client, "stream-message", (uid, payload) => { 
    console.log(`received data stream message from ${uid}: `, payload);

    setTranscription(payload.text);
  });

  useJoin({appid: appId, channel: channel, token: token ? token : null}, calling);

  const [micOn, setMic] = useState(true);
  const [cameraOn, setCamera] = useState(true);
  const { localMicrophoneTrack } = useLocalMicrophoneTrack(micOn);
  const { localCameraTrack } = useLocalCameraTrack(cameraOn);
  usePublish([localMicrophoneTrack, localCameraTrack]);

  const remoteUsers = useRemoteUsers();

  useEffect(() => {
    // Fetch the builder token once the connection is established
    const fetchBuilderToken = async () => {
      if (isConnected) {
        try {
          const response = await axios.post(
            `https://api.agora.io/v1/projects/${appId}/rtsc/speech-to-text/builderTokens`,
            { instanceId: channel },
            {
              auth: {
                username: "11e18849071c4fcf8ee438073381a8a1",
                password: "6b3600168a114a289300ba72ec4e404d",
              },
              headers: {
                'Content-Type': 'application/json',
              }
            },
          );

          setBuilderToken(response.data.tokenName);
          console.log("Builder Token: ", response.data.tokenName);
        } catch (error) {
          console.error("Error fetching builder token: ", error);
        }
      }
    };

    fetchBuilderToken();
  }, [isConnected]);

  // useEffect(() => {
  //   const startTranscription = async () => {
  //     if (!isConnected || !builderToken) return;
  //     try {
  //       const startResponse = await axios.post(
  //         `https://api.agora.io/v1/projects/${appId}/rtsc/speech-to-text/tasks?builderToken=${builderToken}`,
  //         {
  //           languages: ["en-US"],
  //           maxIdleTime: 60,
  //           rtcConfig: {
  //             channelName: channel,
  //             subBotUid: "777",
  //             subBotToken: "007lnoquitehr98ter89hdfnvfdvdfvdf",
  //             pubBotUid: "666",
  //             pubBotToken: "007lnoquitehr98ter89hdfnvfdvdfvdf",
  //           }
  //         },
  //         {
  //           auth: {
  //             username: "11e18849071c4fcf8ee438073381a8a1",
  //             password: "6b3600168a114a289300ba72ec4e404d",
  //           },
  //           headers: {
  //             'Content-Type': 'application/json',
  //           }
  //         },
  //       )
        
  //       console.log(channel, builderToken);
  //       setTaskId(startResponse.data.taskId);
  //       console.log("Start Response: ", startResponse.data.taskId);
  //     } catch (error) {
  //       console.error("Error starting transcription: ", error);
  //     }
  //   }

  //   startTranscription();
  // }, [isConnected, builderToken]);

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
              onChange={e => setChannel(e.target.value)}
              placeholder="<Your channel Name>"
              value={channel}
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
          <h1>{transcription}</h1>
        </div>
      )}
    </div>
  );
};

export default Basics;
// U1hyQUPyr1hDB59gaWhYIDxsAs8Bx2cySMPcRakb3Uh5CogqyLSIUKkNwEeIXL6HuTZUHdJG97eSl3UP4KDX49OD7LwcsWTyZUqS03bjVfl5QOOYzzecOk5qW7Fd9R523nLfQG3Yq561yzqapNeJHXGL-F5Z9MLv4-ejrN2_OFjozg_MIhk4XqyA0eyN-WYkdZBgXxGCRUVU7d6oYB1N9S4W_Pe10vPUnwaR5g2_6Vg
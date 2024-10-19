"use client";

import React, { useState, useEffect } from 'react';
import dynamic from 'next/dynamic';

const AgoraRTCProvider = dynamic(() => import('agora-rtc-react').then(mod => mod.AgoraRTCProvider), { ssr: false });

export default function AgoraProvider({ children }) {
  const [client, setClient] = useState(null);

  useEffect(() => {
    const initClient = async () => {
      try {
        const AgoraRTC = (await import('agora-rtc-sdk-ng')).default;
        const agoraClient = AgoraRTC.createClient({ mode: "rtc", codec: "vp8" });
        setClient(agoraClient);
      } catch (error) {
        console.error("Failed to initialize Agora client:", error);
      }
    };
    initClient();
  }, []);

  if (!client) return null;

  return (
    <AgoraRTCProvider client={client}>
      {children}
    </AgoraRTCProvider>
  );
}

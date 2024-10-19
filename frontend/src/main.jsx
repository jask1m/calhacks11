import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import App from './App.jsx'
import ErrorPage from './pages/Error.jsx'
import Home from './pages/Home.jsx'
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";
import AgoraRTC, { AgoraRTCProvider } from "agora-rtc-react";
import './index.css'

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "/",
        element: <Home />,
      },
    ],
  },
]);

const client = AgoraRTC.createClient({ mode: "rtc", codec: "vp8" });

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AgoraRTCProvider client={client}>
      <RouterProvider router={router} />
    </AgoraRTCProvider>
  </StrictMode>,
)

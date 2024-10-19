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
import RootLayout from './layouts/root-layout'
import DashboardLayout from './layouts/dashboard-layout'
import IndexPage from './routes'
import ContactPage from './routes/contact'
import SignInPage from './routes/sign-in'
import SignUpPage from './routes/sign-up'
import DashboardPage from './routes/dashboard'
import './index.css'

const router = createBrowserRouter([
  {
    element: <RootLayout />,
    children: [
      { path: '/', element: <IndexPage /> },
      { path: '/contact', element: <ContactPage /> },
      { path: '/sign-in/*', element: <SignInPage /> },
      { path: '/sign-up/*', element: <SignUpPage /> },
      {
        element: <DashboardLayout />,
        path: 'dashboard',
        children: [
          { path: '/dashboard', element: <DashboardPage /> },
        ],
      },
    ],
  },
])

const client = AgoraRTC.createClient({ mode: "rtc", codec: "vp8" });

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AgoraRTCProvider client={client}>
      <RouterProvider router={router} />
    </AgoraRTCProvider>
  </StrictMode>,
)

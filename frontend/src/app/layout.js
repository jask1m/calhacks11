import "./globals.css";
import AgoraProvider from "./components/AgoraProvider";

export const metadata = {
  title: "Team-DDD",
  description: "Cal Hacks 11.0 Project",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <AgoraProvider>
          {children}
        </AgoraProvider>
      </body>
    </html>
  );
}

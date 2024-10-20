import { Link, Outlet, useNavigate } from 'react-router-dom'
import { ClerkProvider, SignedIn, SignedOut, UserButton } from '@clerk/clerk-react'

const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY

if (!PUBLISHABLE_KEY) {
  throw new Error('Missing Publishable Key')
}

export default function RootLayout() {
  const navigate = useNavigate()

  return (
    <ClerkProvider
      routerPush={(to) => navigate(to)}
      routerReplace={(to) => navigate(to, { replace: true })}
      publishableKey={PUBLISHABLE_KEY}
    >
      <div className="flex flex-col min-h-screen bg-white text-gray-900">
        <header className="bg-white border-b border-gray-200 shadow-sm">
          <nav className="container mx-auto px-4 py-3 flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <Link to="/" className="text-xl font-bold hover:text-gray-600 transition-colors">
                MeetAI
              </Link>
            </div>
            <div className="flex items-center space-x-4">
              <SignedIn>
                <UserButton 
                  appearance={{
                    elements: {
                      avatarBox: "w-10 h-10"
                    }
                  }}
                />
              </SignedIn>
              <SignedOut>
                <Link 
                  to="/sign-in" 
                  className="bg-white text-gray-900 border border-gray-300 hover:bg-gray-100 font-semibold py-2 px-4 rounded transition-colors"
                >
                  Sign In
                </Link>
              </SignedOut>
            </div>
          </nav>
        </header>
        <main className="flex-grow container mx-auto px-4 py-8">
          <Outlet />
        </main>
      </div>
    </ClerkProvider>
  )
}
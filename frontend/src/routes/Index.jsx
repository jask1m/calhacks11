import { Link } from 'react-router-dom'

export default function IndexPage() {
  return (
    <div className="h-full pt-20 bg-white flex flex-col items-center justify-center px-4 sm:px-6 lg:px-8">
      <div className="max-w-3xl w-full space-y-8 text-center">
        <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold text-gray-900 tracking-tight">
          Video Calls <br /><i>Supercharged</i>
        </h1>
        <p className="mt-3 text-xl text-gray-500 sm:mt-4">
          Real-time context, notes, and reference for your meetings and conversations
        </p>
        <div className="mt-8">
          <Link
            to="/dashboard"
            className="inline-flex items-center justify-center px-8 py-3 border border-transparent text-base font-medium rounded-md text-white bg-black hover:bg-gray-800 transition duration-150 ease-in-out"
          >
            Get Started
          </Link>
        </div>
      </div>
    </div>
  )
}
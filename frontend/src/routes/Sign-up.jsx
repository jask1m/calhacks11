import { SignUp } from '@clerk/clerk-react'

export default function SignUpPage() {
  return (
    <div className="h-full bg-white flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-md">
        <h1 className="text-2xl font-bold text-center text-gray-900 mb-6">
          Sign up to MeetAI
        </h1>
        <SignUp path="/sign-up" />
      </div>
      <p className="mt-8 text-center text-sm text-gray-600 max-w-md">
        Real-time context, notes, and reference for your meetings and conversations
      </p>
    </div>
  )
}
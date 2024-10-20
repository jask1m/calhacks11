import { Link } from 'react-router-dom'
import Basics from '../components/Basics'
export default function DashboardPage() {
  return (
    <>
      <h1>Dashboard page</h1>
      <p>This is a protected page.</p>
      <Link to="/">Return to index</Link>
      <Basics />
    </>
  )
}
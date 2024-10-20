import { Link } from 'react-router-dom'

export default function IndexPage() {
  return (
    <div>
      <h1>Click Below.</h1>
      <div>
        <ul>
          <li>
            <Link to="/dashboard">Get Started.</Link>
          </li>
        </ul>
      </div>
    </div>
  )
}
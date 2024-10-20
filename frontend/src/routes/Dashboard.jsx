import { Link } from 'react-router-dom'
import { useState } from 'react'
import Basics from '../components/Basics'
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu"

export default function DashboardPage() {
  const [option, setOption] = useState("videocall");
  
  return (
    <>
      <NavigationMenu>
        <NavigationMenuList>
          <NavigationMenuItem>
            <Link to="/" legacyBehavior passHref>
              <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                Return
              </NavigationMenuLink>
            </Link>
          </NavigationMenuItem>
          <NavigationMenuItem>
            <button
              onClick={() => setOption("videocall")}
              className={`${navigationMenuTriggerStyle()} border-2 border-grey-500 rounded-md`}
            >
              Video Call
            </button>
          </NavigationMenuItem>
          <NavigationMenuItem>
            <button
              onClick={() => setOption("viewreports")}
              className={`${navigationMenuTriggerStyle()} border-2 border-grey-500 rounded-md`}
            >
              View Reports
            </button>
          </NavigationMenuItem>
        </NavigationMenuList>
      </NavigationMenu>
      <div>
        {option === "videocall" ? (
          <Basics />
        ) : (
          <h1 className="text-2xl font-bold mt-4">Here are the reports.</h1>
        )}
      </div>
    </>
  )
}
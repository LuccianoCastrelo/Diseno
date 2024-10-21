import { Routes, Route } from "react-router-dom";
import { SignedIn, SignedOut, SignInButton, UserButton } from "@clerk/clerk-react";
import Home from "./Componentes/Home.jsx";
import Workers from "./Componentes/Workers.jsx"; 
import Sidebar from "./Componentes/Sidebar.jsx"; 
import "./Componentes/style.css";
import '@material/web/all.js';

export default function App() {

  return (
    <>
      <md-top-app-bar>
        <div slot="actionItems">
          <SignedOut>
            <SignInButton />
          </SignedOut>
          <SignedIn>
            <UserButton className="custom-user-button" />
          </SignedIn>
        </div>
      </md-top-app-bar>
      <md-drawer>
        <div slot="appContent">
          <Sidebar />
          <main className="flex-grow-1 p-3">
            <SignedIn>
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/workers" element={<Workers />} />
              </Routes>
            </SignedIn>
          </main>
        </div>
      </md-drawer>
    </>
  );
}
import { Routes, Route } from "react-router-dom";
import { SignedIn, SignedOut, SignInButton, UserButton } from "@clerk/clerk-react";
import Home from "./Componentes/Home.jsx";
import "./Componentes/style.css";

export default function App() {
  
  return (
    <>
      <header>
        <nav className="navbar navbar-expand-sm navbar-dark bg-transparent">
          <button className="navbar-toggler" type="button">
            <i className="bi bi-justify fs-4" />
          </button>
          <div className="collapse navbar-collapse" id="navbarContent">
            <ul className="navbar-nav ms-auto">
              <li className="nav-item">
                <SignedOut>
                  <SignInButton />
                  <h1>Welcome</h1>
                </SignedOut>
                <SignedIn>
                  <UserButton className="custom-user-button" />
                </SignedIn>
              </li>
            </ul>
          </div>
        </nav>
      </header>
      <main>
        <SignedIn>
          <Routes>
            <Route path="/" element={<Home />} />
            {/* Otras rutas */}
          </Routes>
        </SignedIn>
      </main>
    </>
  );
}

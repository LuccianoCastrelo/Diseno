import { Routes, Route } from "react-router-dom";
import { SignedIn, SignedOut, SignInButton, UserButton } from "@clerk/clerk-react";
import Home from "./Componentes/Home.jsx";

export default function App() {
  return (
    <>
      <header>
        <SignedOut>
          <SignInButton />
          <h1>Por favor inicia sesión</h1>
        </SignedOut>
        <SignedIn>
          <UserButton />
          <Routes>
            <Route path="/" element={<Home />} />
            {/* Puedes agregar más rutas aquí */}
          </Routes>
        </SignedIn>
      </header>
    </>
  );
}

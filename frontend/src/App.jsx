import { Routes, Route } from "react-router-dom";
import { SignedIn, SignedOut, SignInButton, UserButton } from "@clerk/clerk-react";
import Home from "./Componentes/Home.jsx";
import Workers from "./Componentes/Workers.jsx"; 
import Sidebar from "./Componentes/Sidebar.jsx"; 
import "./Componentes/style.css";
import logo from "./Componentes/logo.jpeg";
import '@material/web/all.js';

export default function App() {
  return (
    <>
      <md-top-app-bar className="md-top-app-bar">
        <div slot="actionItems">
          {/* Botón de usuario si el usuario SÍ está autenticado */}
          <SignedIn>
            <UserButton className="custom-user-button" />
          </SignedIn>
        </div>
      </md-top-app-bar>

      {/* Mostrar el botón de Sign In en pantalla completa si el usuario NO está autenticado */}
      
      <SignedOut>
        <div className="sign-in-container">
          <img
            src={logo}
            alt="Logo de la empresa"
            className="company-logo"
          />
          <SignInButton mode="modal" className="sign-in-button" />
        </div>
      </SignedOut>

      {/* Mostrar Sidebar y rutas solo si el usuario está autenticado */}
      <SignedIn>
        <md-drawer>
          <div slot="appContent">
            <Sidebar />
            <main className="flex-grow-1 p-3">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/workers" element={<Workers />} />
              </Routes>
            </main>
          </div>
        </md-drawer>
      </SignedIn>
    </>
  );
}

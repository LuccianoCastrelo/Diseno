import { Routes, Route } from "react-router-dom";
import { SignedIn, SignedOut, SignInButton, UserButton } from "@clerk/clerk-react";
import Home from "./Componentes/Home.jsx";
import Workers from "./Componentes/Workers.jsx";
import Sidebar from "./Componentes/Sidebar.jsx";
import "./Componentes/style.css";
import logo from "./Componentes/logo.jpeg";
import '@material/web/all.js';
import { useTranslation } from 'react-i18next';
import './i18n.js';

export default function App() {
  const { t, i18n } = useTranslation();

  // Función para cambiar el idioma
  const changeLanguage = (lng) => {
    i18n.changeLanguage(lng);
  };

  return (
    <>
      {/* Barra superior con opciones de usuario */}
      <md-top-app-bar className="md-top-app-bar">
        <div slot="actionItems">
          {/* El botón del usuario se moverá a una posición flotante */}
        </div>
      </md-top-app-bar>

      {/* Botones de selección de idioma - posición flotante */}
      <div className="language-switcher">
        <button onClick={() => changeLanguage('es')} className="language-button">
          {t('language.spanish')}
        </button>
        <button onClick={() => changeLanguage('en')} className="language-button">
          {t('language.english')}
        </button>
      </div>

      {/* Botón de usuario flotante solo si el usuario está autenticado */}
      <SignedIn>
        <div className="floating-user-button">
          <UserButton className="user-button" />
        </div>
      </SignedIn>

      {/* Mostrar el botón de Sign In en pantalla completa si el usuario NO está autenticado */}
      <SignedOut>
        <div className="sign-in-container">
          <img
            src={logo}
            alt={t('company.logoAlt')}
            className="company-logo"
          />
          <SignInButton mode="modal" className="sign-in-button">
            {t('buttons.signIn')}
          </SignInButton>
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

import React, { useState, useEffect } from "react";
import Sidebar from "./Sidebar";
import Nav from "./Nav";
import MainContent from "./MainContent";
import "./style.css";

function Home() {
  const [toggle, setToggle] = useState(true); // Sidebar initially expanded

  const Toggle = () => setToggle(!toggle);

  useEffect(() => {
    const handleResize = () => {
      // Abrir barra lateral automáticamente en pantallas grandes, cerrar en pantallas pequeñas
      setToggle(window.innerWidth > 768);
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return (
    <div className="home-container d-flex vh-100">
      {/* Sidebar */}
      <div className={`sidebar ${toggle ? "" : "closed"}`}>
        <Sidebar toggle={toggle} Toggle={Toggle} />
      </div>

      {/* Main Content */}
      <div className={`main-content-wrapper flex-grow-1 ${toggle ? "" : "closed"}`}>
        <Nav Toggle={Toggle} />
        <MainContent />
      </div>
    </div>
  );
}

export default Home;

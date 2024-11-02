import React, { useState, useEffect } from "react";
import Sidebar from "./Sidebar";
import Nav from "./Nav";
import MainContent from "./MainContent";
import "./style.css";

function Home() {
  const [toggle, setToggle] = useState(true); // Sidebar initially expanded

  const Toggle = () => setToggle(!toggle);

  return (
    <div className="home-container d-flex">
      {/* Sidebar */}
      <div className={`sidebar ${toggle ? "" : "closed"}`}>
        <Sidebar toggle={toggle} Toggle={Toggle} />
      </div>

      {/* Main Content */}
      <div className={`main-content-wrapper flex-grow-1 ${toggle ? "" : "sidebar-closed"}`}>
        <Nav Toggle={Toggle} />
        <MainContent />
      </div>
    </div>
  );
}

export default Home;

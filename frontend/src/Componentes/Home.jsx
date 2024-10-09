import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import Sidebar from "./Sidebar";
import Nav from "./Nav";
import MainContent from "./MainContent";
import "./style.css"; // Custom CSS for transitions

function Home() {
  const [toggle, setToggle] = useState(true); // Sidebar initially expanded

  const Toggle = () => setToggle(!toggle);

  return (
    <div className="container-fluid vw-100 vh-100 bg-secondary d-flex flex-column flex-md-row"> {/* Full height and width, responsive */}
      {/* Sidebar */}
      <div
        className={`sidebar-wrapper ${
          toggle ? "col-12 col-md-2" : "col-md-1"
        } bg-white vh-100 sidebar-transition d-flex flex-column`}
      >
        <Sidebar toggle={toggle} Toggle={Toggle} />
      </div>

      {/* Main Content */}
      <div className={`main-content-wrapper flex-grow-1 ${toggle ? "col-12 col-md-10" : "col-md-11"} ms-auto`}>
        <div className="px-3">
          <Nav Toggle={Toggle} />
          <MainContent />
        </div>
      </div>

      {/* Button to show sidebar when collapsed */}
      {/*!toggle && (
        <button
          className="btn btn-primary position-fixed top-0 start-0 mt-3 ms-3"
          onClick={Toggle}
        >
          <i className="bi bi-list"></i>
        </button>
      )*/}
    </div>
  );
}

export default Home;

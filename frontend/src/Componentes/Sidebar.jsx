import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./style.css";
import logo from "./logo.jpeg";

const menuItems = [
  { icon: "bi-speedometer2", label: "Dashboard", path: "/dashboard" },
  { icon: "bi-house", label: "Home", path: "/" },
  { icon: "bi-table", label: "Workers", path: "/workers" },
  { icon: "bi-people", label: "Clients", path: "/clients" },
  { icon: "bi-gear", label: "Machines", path: "/machines" },
];

function Sidebar({ toggle, Toggle }) {
  const [isMobile, setIsMobile] = useState(window.innerWidth <= 768);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth <= 768);
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  useEffect(() => {
    if (isMobile && toggle) {
      Toggle(); // Close the sidebar if switching to mobile view
    }
  }, [isMobile]);

  return (
    <div className={`sidebar ${toggle ? "sidebar-open" : "sidebar-closed"}`}>
      <div className="sidebar-header d-flex justify-content-between align-items-center">
        <img src={logo} alt="Brand Logo" className="brand-icon" />
        {toggle && (
          <button className="btn-close d-md-none" onClick={Toggle}>
            <i className="bi bi-x-lg" />
          </button>
        )}
      </div>
      <div className="list-group">
        {menuItems.map((item, index) => (
          <Link key={index} to={item.path} className="list-group-item">
            <i className={`bi ${item.icon} me-3`} />
            <span className={`${toggle ? "" : "d-none d-md-inline"}`}>{item.label}</span>
          </Link>
        ))}
      </div>
      {!toggle && (
        <button className="btn-toggle d-md-none" onClick={Toggle}>
          <i className="bi bi-list" /> Show Menu
        </button>
      )}
    </div>
  );
}

export default Sidebar;

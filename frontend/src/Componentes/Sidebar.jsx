import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./style.css";

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
    <div className={`sidebar bg-white vh-100 d-flex flex-column ${toggle ? "sidebar-open" : "sidebar-closed"}`}>
      <div className="m-2 d-flex justify-content-between align-items-center">
        <i className="bi bi-bootstrap-fill" />
        <span className={`brand-name fs-4 ${toggle ? "" : "d-none d-md-inline"}`}>Maquinsa</span>
        {toggle && (
          <button className="btn btn-link d-md-none" onClick={Toggle}>
            <i className="bi bi-x-lg" />
          </button>
        )}
      </div>
      <hr className="text-dark" />
      <div className="list-group list-group-flush me-3 fs-4">
        {menuItems.map((item, index) => (
          <Link key={index} to={item.path} className="list-group-item py-2 my-1 d-flex align-items-center">
            <i className={`bi ${item.icon} fs-5 me-3`} />
            <span className={`${toggle ? "" : "d-none d-md-inline"}`}>{item.label}</span>
          </Link>
        ))}
      </div>
      {!toggle && (
        <button className="btn btn-secondary d-md-none mt-2 small-button" onClick={Toggle}>
          <i className="bi bi-list" /> Show Menu
        </button>
      )}
    </div>
  );
}

export default Sidebar;

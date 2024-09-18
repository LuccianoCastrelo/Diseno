import React from "react";
import { Link } from "react-router-dom";
import "./style.css";

const menuItems = [
  { icon: "bi-speedometer2", label: "Dashboard", path: "/dashboard" },
  { icon: "bi-house", label: "Home", path: "/" },
  { icon: "bi-table", label: "Workers", path: "/workers" },
  { icon: "bi-people", label: "Clients", path: "/clients" },
  { icon: "bi-gear", label: "Machines", path: "/machines" },
];

function Sidebar({ toggle }) {
  return (
    <div className={`sidebar bg-white vh-100 position-fixed ${toggle ? "d-block" : "d-none d-md-block"}`}>
      <div className="m-2">
        <i className="bi bi-bootstrap-fill" />
        <span className="brand-name fs-4">Maquinsa</span>
      </div>
      <hr className="text-dark" />
      <div className="list-group list-group-flush me-3 fs-4">
        {menuItems.map((item, index) => (
          <Link
            key={index}
            to={item.path}
            className="list-group-item py-2 my-1"
          >
            <i className={`bi ${item.icon} fs-5 me-3`} />
            <span>{item.label}</span>
          </Link>
        ))}
      </div>
    </div>
  );
}

export default Sidebar;

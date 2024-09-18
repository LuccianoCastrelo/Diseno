import React, { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import Sidebar from "./Sidebar";
import Nav from "./Nav";
import Card from "./Card";
import Table from "./Table"; // Importa el componente Table

function Home() {
  const [toggle, setToggle] = useState(false);

  const Toggle = () => setToggle(!toggle);

  const stats = [
    { value: "230", label: "Workers", icon: "bi-cart-plus" },
    { value: "150", label: "Hours", icon: "bi-clock" },
    { value: "$1.5M", label: "Factures", icon: "bi-currency-collar" },
    { value: "5", label: "Clients", icon: "bi-people" },
  ];

  return (
    <div className="container-fluid bg-secondary win-vh-100">
      <div className="row">
        <nav className="navbar navbar-expand-sm navbar-dark bg-transparent d-md-none">
          <button className="navbar-toggler" type="button" onClick={Toggle}>
            <i className="bi bi-justify fs-4" />
          </button>
        </nav>
        {toggle && (
          <div className="col-12 col-md-2 bg-white vh-100 position-fixed d-md-block">
            <Sidebar toggle={toggle} />
          </div>
        )}
        <div className={`col ${toggle ? "offset-md-2" : ""}`}>
          <div className="px-3">
            <Nav Toggle={Toggle} />
            <div className="container-fluid">
              <div className="row g-3 my-2">
                {stats.map((stat, index) => (
                  <Card key={index} {...stat} />
                ))}
              </div>
              <Table /> {/* Usa el componente Table */}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;

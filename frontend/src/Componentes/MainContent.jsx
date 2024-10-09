// MainContent.jsx
import React from "react";
import Card from "./Card";
import Table from "./Table";

const MainContent = () => {
  const stats = [
    { value: "230", label: "Workers", icon: "bi-cart-plus" },
    { value: "150", label: "Hours", icon: "bi-clock" },
    { value: "$1.5M", label: "Factures", icon: "bi-currency-collar" },
    { value: "5", label: "Clients", icon: "bi-people" },
  ];

  return (
    <div className="container-fluid main-content-wrapper">
      <div className="row g-3 my-2">
        {stats.map((stat, index) => (
          <Card key={index} {...stat} />
        ))}
      </div>
      <div className="row g-3 my-2">
        <Table />
      </div>
    </div>
  );
};

export default MainContent;

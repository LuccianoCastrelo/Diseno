// Card.jsx
import React from "react";

const Card = ({ value, label, icon }) => (
  <div className="col-md-3 p-1">
    <div className="p-3 bg-white shadow-sm d-flex justify-content-around align-items-center rounded">
      <div>
        <h3 className="fs-2">{value}</h3>
        <p className="fs-5">{label}</p>
      </div>
      <i className={`bi ${icon} p-3 fs-1`} />
    </div>
  </div>
);

export default Card;

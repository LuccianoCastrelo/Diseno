import React, { useEffect, useState } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";

import "./style.css"; // Custom CSS for transitions


const Workers = () => {
  const [workers, setWorkers] = useState([]);

  useEffect(() => {
    const fetchWorkers = async () => {
      try {
        const response = await axios.get("http://localhost:8000/trabajadores/");
        setWorkers(response.data);
      } catch (error) {
        console.error("Error fetching workers:", error);
      }
    };

    fetchWorkers();
  }, []);

  return (
    <div className="container-fluid mt-4 vh-100 vw-100">
      <h1>Workers</h1>
      <div className="workers-table" >
        <table className="table caption-top bg-white rounded mt-2">
          <caption className="text-dark fs-4">Workers</caption>
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Name</th>
              <th scope="col">Rut</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            {workers.length > 0 ? (
              workers.map((worker, index) => (
                <tr key={worker.id_trabajador}>
                  <th scope="row">{index + 1}</th>
                  <td>{worker.nombre}</td>
                  <td>{worker.rut}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="4" className="text-center">No workers found</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Workers;
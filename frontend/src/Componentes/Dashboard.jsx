import React, { useEffect, useState } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";

import "./style.css"; // Custom CSS for transitions

const Dashboard = () => {
    const [sueldos, setWorkers] = useState([]);
    const [selectedWorker, setSelectedWorker] = useState(null);
      
    // Fetch workers on component mount
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

    useEffect(() => {
      const fetchHoras = async () => {
        try {
          const response = await axios.get("http://localhost:8000/registro_horas_trabajadas/");
          setHoras(response.data);
        } catch (error) {
          console.error("Error fetching Horas Trabajadas:", error);
        }
      };
  
      fetchHoras();
    }, []);

    useEffect(() => {
        const fetchSueldos = async () => {
          try {
            const response = await axios.get("http://localhost:8000/sueldos/");
            setSueldos(response.data);
          } catch (error) {
            console.error("Error fetching Horas Trabajadas:", error);
          }
        };
    
        fetchSueldos();
      }, []);
  


    return (
        <div className="container-fluid mt-4 vh-100 vw-100">
          <h1>Sueldos</h1>
          <div className="sueldos-table">
            <table className="table caption-top bg-white rounded mt-2">
              <caption className="text-dark fs-4">Visualización del sueldo de los trabajadores</caption>
              <thead>
                <tr>
                  <th scope="col">#</th>
                  <th scope="col">ID del trabajador</th>
                  <th scope="col">Rut</th>
                  <th scope="col">Sueldos</th>
                </tr>
              </thead>
              <tbody>
                {sueldos.length > 0 ? (
                  sueldos.map((sueldos, index) => (
                    <tr key={sueldos.id_sueldo}>
                      <th scope="row">{index + 1}</th>
                      <td>{sueldos.id_trabajador}</td>
                      <td>{sueldos.fecha}</td>
                      <td>{sueldos.horas_trabajadas}</td>
                      
                      <td>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="4" className="text-center">
                      No workers found
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      );
}
export default Dashboard;
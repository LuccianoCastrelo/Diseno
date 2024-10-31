import React, { useEffect, useState } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";

import "./style.css"; // Custom CSS for transitions

const Workers = () => {
  const [workers, setWorkers] = useState([]);
  const [selectedWorker, setSelectedWorker] = useState(null);
  const [registro, setRegistro] = useState({ fecha: "", horaInicio: "", horaFin: "" });
  const [isModalOpen, setIsModalOpen] = useState(false);

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

  // Open modal for adding a time log
  const openModal = (worker) => {
    setSelectedWorker(worker);
    setIsModalOpen(true);
  };

  // Close modal
  const closeModal = () => {
    setSelectedWorker(null);
    setRegistro({ fecha: "", horaInicio: "", horaFin: "" });
    setIsModalOpen(false);
  };

  // Handle input changes in the form
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setRegistro({ ...registro, [name]: value });
  };

  // Handle form submission to create a time log
  const handleFormSubmit = async () => {
    try {
        const payload = {
            id_trabajador: selectedWorker.id_trabajador,
            fecha: registro.fecha,
            hora_inicio: registro.horaInicio,  // Enviar hora de inicio
            hora_fin: registro.horaFin         // Enviar hora de fin
        };

        // Enviar la petición al backend
        await axios.post("http://localhost:8000/registrohoras/", payload);
        closeModal();
        alert("Registro agregado correctamente.");
    } catch (error) {
        console.error("Error al agregar el registro:", error);
    }
  };

  return (
    <div className="container-fluid mt-4 vh-100 vw-100">
      <h1>Workers</h1>
      <div className="workers-table">
        <table className="table caption-top bg-white rounded mt-2">
          <caption className="text-dark fs-4"></caption>
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
                  <td>
                    <button
                      className="btn btn-primary btn-sm me-2"
                      onClick={() => openModal(worker)}
                    >
                      Agregar Registro
                    </button>
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

      {/* Modal for adding time logs */}
      {isModalOpen && (
        <div className="modal show d-block">
          <div className="modal-dialog">
            <div className="modal-content">
              <div className="custom-modal-header">
                <h5 className="modal-title">Agregar Registro de Horas</h5>
                <button type="button" className="btn-close" onClick={closeModal}></button>
              </div>
              <div className="modal-body">
                <div className="mb-3">
                  <label className="form-label">Fecha</label>
                  <input
                    type="date"
                    className="form-control"
                    name="fecha"
                    value={registro.fecha}
                    onChange={handleInputChange}
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Hora de Inicio</label>
                  <input
                    type="time"
                    className="form-control"
                    name="horaInicio"
                    value={registro.horaInicio}
                    onChange={handleInputChange}
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">Hora de Fin</label>
                  <input
                    type="time"
                    className="form-control"
                    name="horaFin"
                    value={registro.horaFin}
                    onChange={handleInputChange}
                  />
                </div>
              </div>
              <div className="modal-footer">
                <button className="btn btn-secondary" onClick={closeModal}>
                  Cancelar
                </button>
                <button className="btn btn-primary" onClick={handleFormSubmit}>
                  Guardar
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Workers;

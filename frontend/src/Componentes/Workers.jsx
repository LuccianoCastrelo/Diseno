import React, { useEffect, useState } from "react";
import axios from "axios";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap-icons/font/bootstrap-icons.css";
import { useTranslation } from "react-i18next";

import "./style.css"; // Custom CSS for transitions

const Workers = () => {
  const { t } = useTranslation();

  const [workers, setWorkers] = useState([]);
  const [machines, setMachines] = useState([]);
  const [companies, setCompanies] = useState([]); // Estado para las empresas
  const [selectedWorker, setSelectedWorker] = useState(null);
  const [registro, setRegistro] = useState({ fecha: "", horaInicio: "", horaFin: "", idMaquina: "", idEmpresa: "" });
  const [isModalOpen, setIsModalOpen] = useState(false);

  // Fetch workers, machines, and companies on component mount
  useEffect(() => {
    const fetchWorkers = async () => {
      try {
        const response = await axios.get("http://localhost:8000/trabajadores/");
        setWorkers(response.data);
      } catch (error) {
        console.error("Error fetching workers:", error);
      }
    };

    const fetchMachines = async () => {
      try {
        const response = await axios.get("http://localhost:8000/machines/");
        setMachines(response.data);
      } catch (error) {
        console.error("Error fetching machines:", error);
      }
    };

    const fetchCompanies = async () => {
      try {
        const response = await axios.get("http://localhost:8000/empresas/");
        setCompanies(response.data);
      } catch (error) {
        console.error("Error fetching companies:", error);
      }
    };

    fetchWorkers();
    fetchMachines();
    fetchCompanies();
  }, []);

  // Open modal for adding a time log
  const openModal = (worker) => {
    setSelectedWorker(worker);
    setIsModalOpen(true);
  };

  // Close modal
  const closeModal = () => {
    setSelectedWorker(null);
    setRegistro({ fecha: "", horaInicio: "", horaFin: "", idMaquina: "", idEmpresa: "" });
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
        hora_inicio: registro.horaInicio,
        hora_fin: registro.horaFin,
        id_maquina: parseInt(registro.idMaquina, 10),
        id_empresa: parseInt(registro.idEmpresa, 10), // Asociar la empresa seleccionada
      };

      await axios.post("http://localhost:8000/registrohoras/", payload);
      closeModal();
      alert(t("messages.logAdded"));
    } catch (error) {
      console.error(t("messages.errorAddingLog"), error);
    }
  };

  return (
    <div className="container-fluid mt-4 vh-100 vw-100">
      <h1>{t("workers.title")}</h1>
      <div className="workers-table">
        <table className="table caption-top bg-white rounded mt-2">
          <caption className="text-dark fs-4">{t("workers.list")}</caption>
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">{t("workers.name")}</th>
              <th scope="col">{t("workers.rut")}</th>
              <th scope="col">{t("workers.actions")}</th>
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
                      {t("buttons.addLog")}
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="4" className="text-center">
                  {t("workers.noWorkersFound")}
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
                <h5 className="modal-title">{t("modals.addLogTitle")}</h5>
                <button type="button" className="btn-close" onClick={closeModal}></button>
              </div>
              <div className="modal-body">
                <div className="mb-3">
                  <label className="form-label">{t("form.date")}</label>
                  <input
                    type="date"
                    className="form-control"
                    name="fecha"
                    value={registro.fecha}
                    onChange={handleInputChange}
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">{t("form.startTime")}</label>
                  <input
                    type="time"
                    className="form-control"
                    name="horaInicio"
                    value={registro.horaInicio}
                    onChange={handleInputChange}
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">{t("form.endTime")}</label>
                  <input
                    type="time"
                    className="form-control"
                    name="horaFin"
                    value={registro.horaFin}
                    onChange={handleInputChange}
                  />
                </div>
                <div className="mb-3">
                  <label className="form-label">{t("form.machine")}</label>
                  <select
                    className="form-control"
                    name="idMaquina"
                    value={registro.idMaquina}
                    onChange={handleInputChange}
                  >
                    <option value="">{t("form.selectMachine")}</option>
                    {machines.map((machine) => (
                      <option key={machine.id_maquina} value={machine.id_maquina}>
                        {machine.descripcion_maquina}
                      </option>
                    ))}
                  </select>
                </div>
                <div className="mb-3">
                  <label className="form-label">{t("form.company")}</label>
                  <select
                    className="form-control"
                    name="idEmpresa"
                    value={registro.idEmpresa}
                    onChange={handleInputChange}
                  >
                    <option value="">{t("form.selectCompany")}</option>
                    {companies.map((company) => (
                      <option key={company.id_empresa} value={company.id_empresa}>
                        {company.nombre_empresa}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
              <div className="modal-footer">
                <button className="btn btn-secondary" onClick={closeModal}>
                  {t("buttons.cancel")}
                </button>
                <button className="btn btn-primary" onClick={handleFormSubmit}>
                  {t("buttons.save")}
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

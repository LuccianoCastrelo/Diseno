import React, { useState, useEffect } from "react";
import axios from "axios";
import { Modal, Button, Spinner } from "react-bootstrap";
import { useTranslation } from "react-i18next";
import * as yup from "yup";

const MachinesTable = ({ onMetricsUpdate }) => {
  const { t } = useTranslation();
  const [machines, setMachines] = useState([]);
  const [fuelConsumption, setFuelConsumption] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [currentMachine, setCurrentMachine] = useState({
    descripcion_maquina: "",
    consumo_promedio: "",
    costo_mantenimiento: "",
    fecha_instalacion: "",
    ultima_fecha_mantenimiento: "",
    tipo_maquina: "",
    tiempo_entre_mantencion: "",
  });
  const [isEditing, setIsEditing] = useState(false);
  const [showModal, setShowModal] = useState(false);

  const fetchMachines = async () => {
    setIsLoading(true);
    try {
      // 1. Obtener todas las máquinas
      const response = await axios.get("http://localhost:8000/machines/");
      const machinesData = response.data || [];

      // 2. Obtener fechas de mantención para cada máquina
      const maintenancePromises = machinesData.map((machine) =>
        axios
          .get(`http://localhost:8000/machines/${machine.id_maquina}/next_maintenance_date`)
          .then((res) => ({
            id_maquina: machine.id_maquina,
            next_maintenance_date: res.data.proxima_fecha_mantenimiento,
          }))
          .catch(() => ({
            id_maquina: machine.id_maquina,
            next_maintenance_date: t("messages.noData"),
          }))
      );

      const maintenanceData = await Promise.all(maintenancePromises);

      // 3. Asignar las fechas de mantención a las máquinas
      const machinesWithMaintenance = machinesData.map((machine) => {
        const maintenance = maintenanceData.find((item) => item.id_maquina === machine.id_maquina);
        return {
          ...machine,
          next_maintenance_date: maintenance?.next_maintenance_date,
        };
      });

      setMachines(machinesWithMaintenance);

      // 4. Obtener consumo promedio por máquina
      const fuelResponse = await axios.get("http://localhost:8000/metrics/fuel_consumed_per_machine");
      const fuelData = fuelResponse.data.machines_fuel_consumption.reduce((acc, item) => {
        acc[item.id_maquina] = item.total_combustible.toFixed(2);
        return acc;
      }, {});

      setFuelConsumption(fuelData);
    } catch (error) {
      console.error("Error fetching machines:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchMachines();
  }, []);

  const machineSchema = yup.object().shape({
    descripcion_maquina: yup.string().required(t("messages.required")),
    consumo_promedio: yup.number().positive(t("messages.invalidNumber")).required(t("messages.required")),
    costo_mantenimiento: yup.number().positive(t("messages.invalidNumber")),
    tiempo_entre_mantencion: yup.number().positive(t("messages.invalidNumber")),
    fecha_instalacion: yup.date().nullable(),
    ultima_fecha_mantenimiento: yup.date().nullable(),
  });

  const handleSave = async () => {
    try {
      await machineSchema.validate(currentMachine);

      setIsLoading(true);
      if (isEditing) {
        await axios.put(`http://localhost:8000/machines/${currentMachine.id_maquina}`, currentMachine);
      } else {
        await axios.post("http://localhost:8000/machines/", currentMachine);
      }

      fetchMachines();
      onMetricsUpdate();
      setShowModal(false);
    } catch (error) {
      console.error("Error saving machine:", error);
      alert(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (id) => {
    try {
      setIsLoading(true);
      await axios.delete(`http://localhost:8000/machines/${id}`);
      fetchMachines();
      onMetricsUpdate();
    } catch (error) {
      console.error("Error deleting machine:", error);
      alert(t("messages.deleteError"));
    } finally {
      setIsLoading(false);
    }
  };

  const openModal = (machine = null) => {
    setCurrentMachine(
      machine || {
        descripcion_maquina: "",
        consumo_promedio: "",
        costo_mantenimiento: "",
        fecha_instalacion: "",
        ultima_fecha_mantenimiento: "",
        tipo_maquina: "",
        tiempo_entre_mantencion: "",
      }
    );
    setIsEditing(!!machine);
    setShowModal(true);
  };

  const closeModal = () => {
    setShowModal(false);
    setCurrentMachine({});
  };

  return (
    <div>
      <Button variant="success" onClick={() => openModal()}>
        {t("buttons.addMachine")}
      </Button>

      {isLoading ? (
        <Spinner animation="border" />
      ) : (
        <table className="table caption-top bg-white rounded mt-2">
          <caption className="text-dark fs-4">{t("table.machines")}</caption>
          <thead>
            <tr>
              <th>#</th>
              <th>{t("table.description")}</th>
              <th>{t("table.type")}</th>
              <th>{t("table.installationDate")}</th>
              <th>{t("table.nextMaintenanceDate")}</th>
              <th>{t("table.fuelConsumption")}</th>
              <th>{t("table.actions")}</th>
            </tr>
          </thead>
          <tbody>
            {machines.map((machine, index) => (
              <tr key={machine.id_maquina}>
                <th>{index + 1}</th>
                <td>{machine.descripcion_maquina}</td>
                <td>{machine.tipo_maquina || t("messages.noData")}</td>
                <td>{machine.fecha_instalacion || t("messages.noData")}</td>
                <td>{machine.next_maintenance_date || t("messages.noData")}</td>
                <td>{fuelConsumption[machine.id_maquina] || t("messages.noData")} Lts</td>
                <td>
                  <button className="btn btn-primary me-2" onClick={() => openModal(machine)}>
                    {t("buttons.edit")}
                  </button>
                  <button className="btn btn-danger" onClick={() => handleDelete(machine.id_maquina)}>
                    {t("buttons.delete")}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {/* Modal para agregar/editar */}
      <Modal show={showModal} onHide={closeModal}>
        <Modal.Header closeButton>
          <Modal.Title>{isEditing ? t("modals.editMachine") : t("modals.addMachine")}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="mb-3">
            <label htmlFor="descripcion_maquina" className="form-label">
              {t("form.description")}
            </label>
            <input
              id="descripcion_maquina"
              type="text"
              placeholder="E.g., Conveyor Belt Model X"
              className="form-control"
              value={currentMachine.descripcion_maquina}
              onChange={(e) => setCurrentMachine({ ...currentMachine, descripcion_maquina: e.target.value })}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="consumo_promedio" className="form-label">
              {t("form.averageConsumption")}
            </label>
            <input
              id="consumo_promedio"
              type="number"
              placeholder="E.g., 10.5 (kWh)"
              className="form-control"
              value={currentMachine.consumo_promedio}
              onChange={(e) => setCurrentMachine({ ...currentMachine, consumo_promedio: e.target.value })}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="costo_mantenimiento" className="form-label">
              {t("form.maintenanceCost")}
            </label>
            <input
              id="costo_mantenimiento"
              type="number"
              placeholder="E.g., 500 (USD)"
              className="form-control"
              value={currentMachine.costo_mantenimiento}
              onChange={(e) => setCurrentMachine({ ...currentMachine, costo_mantenimiento: e.target.value })}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="fecha_instalacion" className="form-label">
              {t("form.installationDate")}
            </label>
            <input
              id="fecha_instalacion"
              type="date"
              className="form-control"
              value={currentMachine.fecha_instalacion}
              onChange={(e) => setCurrentMachine({ ...currentMachine, fecha_instalacion: e.target.value })}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="ultima_fecha_mantenimiento" className="form-label">
              {t("form.lastMaintenance")}
            </label>
            <input
              id="ultima_fecha_mantenimiento"
              type="date"
              className="form-control"
              value={currentMachine.ultima_fecha_mantenimiento}
              onChange={(e) => setCurrentMachine({ ...currentMachine, ultima_fecha_mantenimiento: e.target.value })}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="tipo_maquina" className="form-label">
              {t("form.type")}
            </label>
            <input
              id="tipo_maquina"
              type="text"
              placeholder="E.g., Industrial"
              className="form-control"
              value={currentMachine.tipo_maquina}
              onChange={(e) => setCurrentMachine({ ...currentMachine, tipo_maquina: e.target.value })}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="tiempo_entre_mantencion" className="form-label">
              {t("form.maintenanceInterval")}
            </label>
            <input
              id="tiempo_entre_mantencion"
              type="number"
              placeholder="E.g., 90 (days)"
              className="form-control"
              value={currentMachine.tiempo_entre_mantencion}
              onChange={(e) => setCurrentMachine({ ...currentMachine, tiempo_entre_mantencion: e.target.value })}
            />
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={closeModal}>{t("buttons.cancel")}</Button>
          <Button variant="primary" onClick={handleSave} disabled={isLoading}>
            {isLoading ? <Spinner as="span" animation="border" size="sm" /> : t("buttons.saveChanges")}
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default MachinesTable;

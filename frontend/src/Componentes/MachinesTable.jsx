import React, { useState, useEffect } from "react";
import axios from "axios";
import { Modal, Button, Spinner } from "react-bootstrap";
import { useTranslation } from 'react-i18next';

const MachinesTable = ({ onMetricsUpdate }) => {
  const { t } = useTranslation();
  const [machines, setMachines] = useState([]);
  const [editingMachine, setEditingMachine] = useState({ descripcion_maquina: "", uso_para_mantenimiento: "" });
  const [newMachine, setNewMachine] = useState({ descripcion_maquina: "", uso_para_mantenimiento: "" });
  const [showEditModal, setShowEditModal] = useState(false);
  const [showAddModal, setShowAddModal] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const fetchMachines = async () => {
    setIsLoading(true);
    try {
      const response = await axios.get("http://localhost:8000/machines/");
      setMachines(response.data);
    } catch (error) {
      console.error("Error fetching machines:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchMachines();
  }, []);

  const handleEdit = (machine) => {
    setEditingMachine(machine);
    setShowEditModal(true);
  };

  const handleUpdate = async () => {
    try {
      setIsLoading(true);
      await axios.put(`http://localhost:8000/machines/${editingMachine.id_maquina}`, editingMachine);
      fetchMachines();
      onMetricsUpdate();
      setShowEditModal(false);
    } catch (error) {
      console.error("Error updating machine:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddMachine = async () => {
    if (!newMachine.descripcion_maquina.trim() || !newMachine.uso_para_mantenimiento.trim()) {
      alert(t("messages.invalidData"));
      return;
    }

    try {
      setIsLoading(true);
      const response = await axios.post("http://localhost:8000/machines/", newMachine);
      setMachines([...machines, response.data]);
      onMetricsUpdate();
      setShowAddModal(false);
      setNewMachine({ descripcion_maquina: "", uso_para_mantenimiento: "" });
    } catch (error) {
      console.error("Error adding machine:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteMachine = async (id) => {
    try {
      setIsLoading(true);
      await axios.delete(`http://localhost:8000/machines/${id}`);
      setMachines(machines.filter((machine) => machine.id_maquina !== id));
      onMetricsUpdate();
    } catch (error) {
      console.error("Error deleting machine:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div>
      <Button variant="success" onClick={() => setShowAddModal(true)}>{t("buttons.addMachine")}</Button>

      {isLoading ? (
        <Spinner animation="border" />
      ) : (
        <table className="table caption-top bg-white rounded mt-2">
          <caption className="text-dark fs-4">{t("table.machines")}</caption>
          <thead>
            <tr>
              <th>#</th>
              <th>{t("table.description")}</th>
              <th>{t("table.usage")}</th>
              <th>{t("table.actions")}</th>
            </tr>
          </thead>
          <tbody>
            {machines.map((machine, index) => (
              <tr key={machine.id_maquina}>
                <th>{index + 1}</th>
                <td>{machine.descripcion_maquina}</td>
                <td>{machine.uso_para_mantenimiento}</td>
                <td>
                  <button className="btn btn-primary me-2" onClick={() => handleEdit(machine)}>{t("buttons.edit")}</button>
                  <button className="btn btn-danger" onClick={() => handleDeleteMachine(machine.id_maquina)}>{t("buttons.delete")}</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}

      {/* Modal para Editar */}
      <Modal show={showEditModal} onHide={() => setShowEditModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>{t("modals.editMachine")}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <input
            type="text"
            placeholder={t("form.description")}
            className="form-control"
            value={editingMachine.descripcion_maquina}
            onChange={(e) => setEditingMachine({ ...editingMachine, descripcion_maquina: e.target.value })}
          />
          <input
            type="text"
            placeholder={t("form.usage")}
            className="form-control mt-2"
            value={editingMachine.uso_para_mantenimiento}
            onChange={(e) => setEditingMachine({ ...editingMachine, uso_para_mantenimiento: e.target.value })}
          />
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowEditModal(false)}>{t("buttons.cancel")}</Button>
          <Button variant="primary" onClick={handleUpdate}>{t("buttons.saveChanges")}</Button>
        </Modal.Footer>
      </Modal>

      {/* Modal para Agregar */}
      <Modal show={showAddModal} onHide={() => setShowAddModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>{t("modals.addMachine")}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <input
            type="text"
            placeholder={t("form.description")}
            className="form-control"
            value={newMachine.descripcion_maquina}
            onChange={(e) => setNewMachine({ ...newMachine, descripcion_maquina: e.target.value })}
          />
          <input
            type="text"
            placeholder={t("form.usage")}
            className="form-control mt-2"
            value={newMachine.uso_para_mantenimiento}
            onChange={(e) => setNewMachine({ ...newMachine, uso_para_mantenimiento: e.target.value })}
          />
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowAddModal(false)}>{t("buttons.cancel")}</Button>
          <Button variant="primary" onClick={handleAddMachine}>{t("buttons.addMachine")}</Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default MachinesTable;

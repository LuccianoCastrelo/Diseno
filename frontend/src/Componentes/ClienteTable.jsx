import React, { useEffect, useState } from "react";
import axios from "axios";
import { Modal, Button } from "react-bootstrap";
import { useTranslation } from "react-i18next";
import "./style.css";

const ClienteTable = () => {
  const { t } = useTranslation();

  const [clients, setClients] = useState([]);
  const [clientStats, setClientStats] = useState({}); // Guardar horas y turnos trabajados por cliente
  const [editingClient, setEditingClient] = useState({ nombre_empresa: "", direccion: "", telefono: "", email: "" });
  const [newClient, setNewClient] = useState({ nombre_empresa: "", direccion: "", telefono: "", email: "" });
  const [showModal, setShowModal] = useState(false);
  const [showAddModal, setShowAddModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [clientToDelete, setClientToDelete] = useState(null);

  useEffect(() => {
    const fetchClients = async () => {
      try {
        const response = await axios.get("http://localhost:8000/clientes/");
        setClients(response.data);
      } catch (error) {
        console.error("Error fetching clients:", error);
      }
    };

    const fetchClientStats = async () => {
      try {
        const response = await axios.get("http://localhost:8000/metrics/clients_hours_turns/");
        setClientStats(response.data);
      } catch (error) {
        console.error("Error fetching client stats:", error);
      }
    };

    fetchClients();
    fetchClientStats();
  }, []);

  // Abrir modal de edición
  const handleEdit = (client) => {
    setEditingClient(client);
    setShowModal(true);
  };

  const handleUpdate = async () => {
    if (!editingClient.id_cliente) {
      console.error("El cliente no tiene un ID válido.");
      return;
    }
    try {
      const response = await axios.put(`http://localhost:8000/cliente/${editingClient.id_cliente}`, editingClient);
      setClients(
        clients.map((client) =>
          client.id_cliente === editingClient.id_cliente ? response.data : client
        )
      );
      setShowModal(false);
    } catch (error) {
      console.error("Error updating client:", error);
    }
  };

  // Confirmar eliminación
  const handleDeleteConfirmation = (client) => {
    setClientToDelete(client);
    setShowDeleteModal(true);
  };

  // Eliminar cliente
  const handleDelete = async () => {
    if (!clientToDelete || !clientToDelete.id_cliente) {
      console.error("El cliente no tiene un ID válido.");
      return;
    }
    try {
      await axios.delete(`http://localhost:8000/cliente/${clientToDelete.id_cliente}`);
      setClients(clients.filter((client) => client.id_cliente !== clientToDelete.id_cliente));
      setShowDeleteModal(false);
      setClientToDelete(null);
    } catch (error) {
      console.error("Error deleting client:", error);
    }
  };
  

  // Agregar cliente
  const handleAddClient = async () => {
    try {
      const response = await axios.post("http://localhost:8000/clientes/", newClient);
      setClients([...clients, response.data]);
      setShowAddModal(false);
      setNewClient({ nombre_empresa: "", direccion: "", telefono: "", email: "" });
    } catch (error) {
      console.error("Error adding client:", error);
    }
  };

  return (
    <div>
      <Button variant="success" onClick={() => setShowAddModal(true)}>
        {t("buttons.addClient")}
      </Button>

      <table className="table caption-top bg-white rounded mt-2">
        <caption className="text-dark fs-4">{t("table.clients")}</caption>
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">{t("table.companyName")}</th>
            <th scope="col">{t("table.address")}</th>
            <th scope="col">{t("table.phone")}</th>
            <th scope="col">{t("table.email")}</th>
            <th scope="col">{t("table.hoursWorked")}</th>
            <th scope="col">{t("table.turnsWorked")}</th>
            <th scope="col">{t("table.actions")}</th>
          </tr>
        </thead>
        <tbody>
          {clients.map((client, index) => (
            <tr key={client.id_cliente}>
              <th scope="row">{index + 1}</th>
              <td>{client.nombre_empresa}</td>
              <td>{client.direccion}</td>
              <td>{client.telefono}</td>
              <td>{client.email}</td>
              <td>{clientStats[client.id_cliente]?.total_hours || 0}</td>
              <td>{clientStats[client.id_cliente]?.total_turns || 0}</td>
              <td>
                <button className="btn btn-primary me-2" onClick={() => handleEdit(client)}>
                  {t("buttons.edit")}
                </button>
                <button className="btn btn-danger" onClick={() => handleDeleteConfirmation(client)}>
                  {t("buttons.delete")}
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Modal para Editar */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>{t("modals.editClient")}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="form-group">
            <label>{t("form.company")}</label>
            <input
              type="text"
              className="form-control"
              value={editingClient.nombre_empresa}
              onChange={(e) => setEditingClient({ ...editingClient, nombre_empresa: e.target.value })}
            />
          </div>
          <div className="form-group">
            <label>{t("form.address")}</label>
            <input
              type="text"
              className="form-control"
              value={editingClient.direccion}
              onChange={(e) => setEditingClient({ ...editingClient, direccion: e.target.value })}
            />
          </div>
          <div className="form-group">
            <label>{t("form.phone")}</label>
            <input
              type="text"
              className="form-control"
              value={editingClient.telefono}
              onChange={(e) => setEditingClient({ ...editingClient, telefono: e.target.value })}
            />
          </div>
          <div className="form-group">
            <label>{t("form.email")}</label>
            <input
              type="email"
              className="form-control"
              value={editingClient.email}
              onChange={(e) => setEditingClient({ ...editingClient, email: e.target.value })}
            />
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            {t("buttons.cancel")}
          </Button>
          <Button variant="primary" onClick={handleUpdate}>
            {t("buttons.saveChanges")}
          </Button>
        </Modal.Footer>
      </Modal>

      {/* Modal para Confirmar Eliminación */}
      <Modal show={showDeleteModal} onHide={() => setShowDeleteModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>{t("modals.deleteClient")}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {t("modals.deleteConfirmation", { clientName: clientToDelete?.nombre_empresa })}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowDeleteModal(false)}>
            {t("buttons.cancel")}
          </Button>
          <Button variant="danger" onClick={handleDelete}>
            {t("buttons.delete")}
          </Button>
        </Modal.Footer>
      </Modal>

      {/* Modal para Agregar Cliente */}
      <Modal show={showAddModal} onHide={() => setShowAddModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>{t("modals.addClient")}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="form-group">
            <label>{t("form.company")}</label>
            <input
              type="text"
              className="form-control"
              value={newClient.nombre_empresa}
              onChange={(e) => setNewClient({ ...newClient, nombre_empresa: e.target.value })}
            />
          </div>
          <div className="form-group">
            <label>{t("form.address")}</label>
            <input
              type="text"
              className="form-control"
              value={newClient.direccion}
              onChange={(e) => setNewClient({ ...newClient, direccion: e.target.value })}
            />
          </div>
          <div className="form-group">
            <label>{t("form.phone")}</label>
            <input
              type="text"
              className="form-control"
              value={newClient.telefono}
              onChange={(e) => setNewClient({ ...newClient, telefono: e.target.value })}
            />
          </div>
          <div className="form-group">
            <label>{t("form.email")}</label>
            <input
              type="email"
              className="form-control"
              value={newClient.email}
              onChange={(e) => setNewClient({ ...newClient, email: e.target.value })}
            />
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowAddModal(false)}>
            {t("buttons.cancel")}
          </Button>
          <Button variant="primary" onClick={handleAddClient}>
            {t("buttons.addClient")}
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default ClienteTable;

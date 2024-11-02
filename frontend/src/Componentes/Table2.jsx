import React, { useEffect, useState } from "react";
import axios from "axios";
import { Modal, Button } from "react-bootstrap";

const Table2 = () => {
  const [workers, setWorkers] = useState([]);
  const [newWorkerName, setNewWorkerName] = useState(""); // Nuevo estado para el nombre del nuevo trabajador
  const [newWorkerType, setNewWorkerType] = useState("eventual"); // Nuevo estado para el tipo de trabajador
  const [newWorkerPayment, setNewWorkerPayment] = useState(""); // Nuevo estado para el pago por turno
  const [newWorkerSalary, setNewWorkerSalary] = useState(""); // Nuevo estado para el salario base
  const [showAddModal, setShowAddModal] = useState(false); // Modal para agregar trabajador

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

  // Abrir modal para agregar trabajador
  const handleShowAddModal = () => {
    setShowAddModal(true);
  };

  // Cerrar modal para agregar trabajador
  const handleCloseAddModal = () => {
    setShowAddModal(false);
  };

  // Función para agregar un nuevo trabajador
  const handleAddWorker = async () => {
    try {
      const response = await axios.post("http://localhost:8000/trabajadores/", {
        nombre: newWorkerName,
        tipo: newWorkerType,
        pago_por_turno: parseInt(newWorkerPayment), // Asegúrate de que sea un número
        salario_base: newWorkerType === "permanente" ? parseInt(newWorkerSalary) : null, // Solo si es permanente
      });

      // Actualiza la lista de trabajadores con el nuevo trabajador
      setWorkers([...workers, response.data]);

      // Cerrar el modal y limpiar los campos de entrada
      setShowAddModal(false);
      setNewWorkerName("");
      setNewWorkerType("eventual");
      setNewWorkerPayment("");
      setNewWorkerSalary("");
    } catch (error) {
      console.error("Error adding worker:", error);
    }
  };

  return (
    <div>
      <table className="table caption-top bg-white rounded mt-2">
        <caption className="text-dark fs-4">Workers</caption>
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Name</th>
            <th scope="col">Handle</th>
          </tr>
        </thead>
        <tbody>
          {workers.map((worker, index) => (
            <tr key={worker.id_trabajador}>
              <th scope="row">{index + 1}</th>
              <td>{worker.nombre}</td>
              <td>@{worker.nombre.toLowerCase()}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Botón para abrir el modal de agregar trabajador */}
      <button className="btn btn-success" onClick={handleShowAddModal}>
        Add Worker
      </button>

      {/* Modal de agregar trabajador */}
      <Modal show={showAddModal} onHide={handleCloseAddModal}>
        <Modal.Header closeButton>
          <Modal.Title>Add Worker</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="form-group">
            <label>Worker Name</label>
            <input
              type="text"
              className="form-control"
              value={newWorkerName}
              onChange={(e) => setNewWorkerName(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label>Worker Type</label>
            <select
              className="form-control"
              value={newWorkerType}
              onChange={(e) => setNewWorkerType(e.target.value)}
            >
              <option value="eventual">Eventual</option>
              <option value="permanente">Permanente</option>
            </select>
          </div>
          <div className="form-group">
            <label>Payment per Shift</label>
            <input
              type="number"
              className="form-control"
              value={newWorkerPayment}
              onChange={(e) => setNewWorkerPayment(e.target.value)}
            />
          </div>
          {newWorkerType === "permanente" && (
            <div className="form-group">
              <label>Base Salary</label>
              <input
                type="number"
                className="form-control"
                value={newWorkerSalary}
                onChange={(e) => setNewWorkerSalary(e.target.value)}
              />
            </div>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseAddModal}>
            Cancel
          </Button>
          <Button variant="primary" onClick={handleAddWorker}>
            Add Worker
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default Table2;

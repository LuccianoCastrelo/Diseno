  import React, { useEffect, useState } from "react";
  import axios from "axios";
  import { Modal, Button } from "react-bootstrap";
  import "./style.css";

  const Table = () => {
    const [workers, setWorkers] = useState([]);
    const [editingWorker, setEditingWorker] = useState({ nombre: "", tipo: "", pago_por_turno: "", salario_base: "", rut: "" });
    const [newWorker, setNewWorker] = useState({ nombre: "", tipo: "", pago_por_turno: "", salario_base: "", rut: "" });
    const [showModal, setShowModal] = useState(false);
    const [showDeleteModal, setShowDeleteModal] = useState(false);
    const [showAddModal, setShowAddModal] = useState(false); // Modal para agregar trabajador
    const [workerToDelete, setWorkerToDelete] = useState(null);

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

    // Abrir modal de edición
    const handleEdit = (worker) => {
      setEditingWorker(worker);
      setShowModal(true);  // Abrir modal de edición
    };

    // Actualizar trabajador
    const handleUpdate = async () => {
      try {
        const payload = {
          id_trabajador: editingWorker.id_trabajador,
          nombre: editingWorker.nombre,
          tipo: editingWorker.tipo,
          pago_por_turno: parseInt(editingWorker.pago_por_turno, 10),
          rut: editingWorker.rut
        };
    
        // Si es permanente, incluir salario_base
        if (editingWorker.tipo === 'permanente') {
          payload.salario_base = parseInt(editingWorker.salario_base, 10);
        }
    
        await axios.put(`http://localhost:8000/trabajador/${editingWorker.id_trabajador}`, payload);
    
        setWorkers(
          workers.map((worker) =>
            worker.id_trabajador === editingWorker.id_trabajador ? editingWorker : worker
          )
        );
    
        setShowModal(false);
      } catch (error) {
        console.error("Error updating worker:", error);
      }
    };
    

    // Confirmar eliminación
    const handleDeleteConfirmation = (worker) => {
      setWorkerToDelete(worker);
      setShowDeleteModal(true);
    };

    // Eliminar trabajador
    const handleDelete = async () => {
      try {
        await axios.delete(`http://localhost:8000/trabajador/${workerToDelete.id_trabajador}`);
        setWorkers(workers.filter((worker) => worker.id_trabajador !== workerToDelete.id_trabajador));
        setShowDeleteModal(false);
        setWorkerToDelete(null);
      } catch (error) {
        console.error("Error deleting worker:", error);
      }
    };
    
    const handleAddWorker = async () => {
      try {
        const payload = {
          nombre: newWorker.nombre,
          tipo: newWorker.tipo,
          pago_por_turno: parseInt(newWorker.pago_por_turno, 10),
          rut: newWorker.rut  // Añadir el rut al post
        };
    
        // Si es permanente, incluir salario_base
        if (newWorker.tipo === 'permanente') {
          payload.salario_base = parseInt(newWorker.salario_base, 10);
        }
    
        const response = await axios.post("http://localhost:8000/trabajadores/", payload);
        setWorkers([...workers, response.data]);
        setShowAddModal(false);
        setNewWorker({ nombre: "", tipo: "", pago_por_turno: "", salario_base: "", rut: "" });
      } catch (error) {
        console.error("Error adding worker:", error);
      }
    };
    

    return (
      <div>
        <Button variant="success" onClick={() => setShowAddModal(true)}>Agregar Trabajador</Button> {/* Botón para agregar */}
        
        <table className="table caption-top bg-white rounded mt-2">
          <caption className="text-dark fs-4">Workers</caption>
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Name</th>
              <th scope="col">RUT</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            {workers.map((worker, index) => (
              <tr key={worker.id_trabajador}>
                <th scope="row">{index + 1}</th>
                <td>{worker.nombre}</td>
                <td>{worker.rut}</td>
                <td>
                  <button className="btn btn-primary me-2" onClick={() => handleEdit(worker)}>Edit</button>
                  <button className="btn btn-danger" onClick={() => handleDeleteConfirmation(worker)}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {/* Modal para Editar */}
        <Modal show={showModal} onHide={() => setShowModal(false)}>
          <Modal.Header closeButton className="custom-modal-header">
            <Modal.Title>Editar Trabajador</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <div className="form-group">
              <label>Nombre</label>
              <input
                type="text"
                className="form-control"
                value={editingWorker.nombre}
                onChange={(e) => setEditingWorker({ ...editingWorker, nombre: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>RUT</label>
              <input
                type="text"
                className="form-control"
                value={editingWorker.rut}
                onChange={(e) => setEditingWorker({ ...editingWorker, rut: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Tipo</label>
              <input
                type="text"
                className="form-control"
                value={editingWorker.tipo}
                onChange={(e) => setEditingWorker({ ...editingWorker, tipo: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Pago por turno</label>
              <input
                type="number"
                className="form-control"
                value={editingWorker.pago_por_turno}
                onChange={(e) => setEditingWorker({ ...editingWorker, pago_por_turno: e.target.value })}
              />
            </div>
            {editingWorker.tipo === 'permanente' && (
              <div className="form-group">
                <label>Salario base</label>
                <input
                  type="number"
                  className="form-control"
                  value={editingWorker.salario_base}
                  onChange={(e) => setEditingWorker({ ...editingWorker, salario_base: e.target.value })}
                />
              </div>
            )}
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => setShowModal(false)}>Cancelar</Button>
            <Button variant="primary" onClick={handleUpdate}>Guardar Cambios</Button>
          </Modal.Footer>
        </Modal>

        {/* Modal para Confirmar Eliminación */}
        <Modal show={showDeleteModal} onHide={() => setShowDeleteModal(false)}>
          <Modal.Header closeButton className="custom-modal-header">
            <Modal.Title>Eliminar Trabajador</Modal.Title>
          </Modal.Header>
          <Modal.Body>¿Estás seguro de que quieres eliminar al trabajador: <strong>{workerToDelete?.nombre}</strong>?</Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => setShowDeleteModal(false)}>Cancelar</Button>
            <Button variant="danger" onClick={handleDelete}>Eliminar</Button>
          </Modal.Footer>
        </Modal>

        {/* Modal para Agregar Trabajador */}
        <Modal show={showAddModal} onHide={() => setShowAddModal(false)}>
          <Modal.Header closeButton className="custom-modal-header">
            <Modal.Title>Agregar Trabajador</Modal.Title>
          </Modal.Header>
          <Modal.Body>
            <div className="form-group">
              <label>Nombre</label>
              <input
                type="text"
                className="form-control"
                value={newWorker.nombre}
                onChange={(e) => setNewWorker({ ...newWorker, nombre: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>RUT</label>
              <input
                type="text"
                className="form-control"
                value={newWorker.rut}
                onChange={(e) => setNewWorker({ ...newWorker, rut: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Tipo</label>
              <input
                type="text"
                className="form-control"
                value={newWorker.tipo}
                onChange={(e) => setNewWorker({ ...newWorker, tipo: e.target.value })}
              />
            </div>
            <div className="form-group">
              <label>Pago por turno</label>
              <input
                type="number"
                className="form-control"
                value={newWorker.pago_por_turno}
                onChange={(e) => setNewWorker({ ...newWorker, pago_por_turno: e.target.value })}
              />
            </div>
            {newWorker.tipo === 'permanente' && (
              <div className="form-group">
                <label>Salario base</label>
                <input
                  type="number"
                  className="form-control"
                  value={newWorker.salario_base}
                  onChange={(e) => setNewWorker({ ...newWorker, salario_base: e.target.value })}
                />
              </div>
            )}
          </Modal.Body>
          <Modal.Footer>
            <Button variant="secondary" onClick={() => setShowAddModal(false)}>Cancelar</Button>
            <Button variant="primary" onClick={handleAddWorker}>Agregar Trabajador</Button>
          </Modal.Footer>
        </Modal>
      </div>
    );
  };

  export default Table;

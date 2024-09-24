import React, { useEffect, useState } from "react";
import axios from "axios";
import { Modal, Button } from "react-bootstrap";

const Table = () => {
  const [workers, setWorkers] = useState([]);
  const [editingWorker, setEditingWorker] = useState(null);
  const [editedName, setEditedName] = useState("");
  const [showModal, setShowModal] = useState(false);

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

  // Open modal and populate form with selected worker's info
  const handleEdit = (worker) => {
    setEditingWorker(worker);
    setEditedName(worker.nombre);
    setShowModal(true);  // Open the modal
  };

  // Update the worker's information
  const handleUpdate = async () => {
    try {
      await axios.put(`http://localhost:8000/trabajador/${editingWorker.id_trabajador}`, {
        id_trabajador: editingWorker.id_trabajador,
        nombre: editedName,
      });

      // Update the workers list with the edited name
      setWorkers(
        workers.map((worker) =>
          worker.id_trabajador === editingWorker.id_trabajador
            ? { ...worker, nombre: editedName }
            : worker
        )
      );

      // Close the modal after the update
      setShowModal(false);
      setEditingWorker(null);
      setEditedName("");
    } catch (error) {
      console.error("Error updating worker:", error);
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
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody>
          {workers.map((worker, index) => (
            <tr key={worker.id_trabajador}>
              <th scope="row">{index + 1}</th>
              <td>{worker.nombre}</td>
              <td>@{worker.nombre.toLowerCase()}</td>
              <td>
                <button
                  className="btn btn-primary"
                  onClick={() => handleEdit(worker)}
                >
                  Edit
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Bootstrap Modal for Editing */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Edit Worker</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <div className="form-group">
            <label>New Name</label>
            <input
              type="text"
              className="form-control"
              value={editedName}
              onChange={(e) => setEditedName(e.target.value)}
            />
          </div>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowModal(false)}>
            Cancel
          </Button>
          <Button variant="primary" onClick={handleUpdate}>
            Save Changes
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default Table;

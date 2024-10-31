import React, { useEffect, useState } from "react";
import axios from "axios";
import { Modal, Button, Form, Alert } from "react-bootstrap";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";

const Dashboard = () => {
    const [workers, setWorkers] = useState([]);
    const [calculatedSalaries, setCalculatedSalaries] = useState({}); // Guarda el último sueldo calculado para cada trabajador
    const [showModal, setShowModal] = useState(false);
    const [selectedWorker, setSelectedWorker] = useState(null);
    const [salaryType, setSalaryType] = useState(""); // "diario", "semanal", o "mensual"
    const [selectedDate, setSelectedDate] = useState(null);
    const [errorMessage, setErrorMessage] = useState(""); // Mensaje de error para fechas sin registros
    const [hourLogs, setHourLogs] = useState([]); // Almacena los registros de horas para el periodo seleccionado

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

    // Open modal and set selected worker
    const openModal = (worker) => {
        setSelectedWorker(worker);
        setSalaryType(""); // Reset salary type when reopening modal
        setSelectedDate(null); // Reset date when reopening modal
        setErrorMessage(""); // Reset error message when reopening modal
        setHourLogs([]); // Reset hour logs when reopening modal
        setShowModal(true);
    };

    // Fetch hour logs based on the selected date and salary type
    const fetchHourLogs = async () => {
      if (!selectedWorker || !selectedDate || !salaryType) return;
  
      let endpoint = "";
      let params = {};
  
      if (salaryType === "diario") {
          endpoint = `/trabajadores/${selectedWorker.id_trabajador}/registros_diarios`;
          params = { fecha: selectedDate.toISOString().split("T")[0] };
      } else if (salaryType === "semanal") {
          endpoint = `/trabajadores/${selectedWorker.id_trabajador}/registros_semanales`;
          params = { fecha_inicio_semana: selectedDate.toISOString().split("T")[0] };
      } else if (salaryType === "mensual") {
          const selectedMonth = selectedDate.toLocaleDateString("en-CA", { month: "2-digit" });
          endpoint = `/trabajadores/${selectedWorker.id_trabajador}/registros_mensuales`;
          params = { mes: selectedMonth };
      }
  
      try {
          const response = await axios.get(`http://localhost:8000${endpoint}`, { params });
          setHourLogs(response.data.registros || []); // Actualizar para acceder a `registros`
      } catch (error) {
          console.error("Error fetching hour logs:", error);
          setHourLogs([]); // Clear hour logs if there's an error
      }
  };

    // Run fetchHourLogs when date or salary type changes
    useEffect(() => {
        if (selectedDate && salaryType) {
            fetchHourLogs();
        }
    }, [selectedDate, salaryType]);

    // Handle calculate salary request
    const handleCalculateSalary = async () => {
        if (!salaryType || !selectedDate) {
            alert("Selecciona el tipo de sueldo y la fecha.");
            return;
        }

        let endpoint = "";
        let params = {};

        if (salaryType === "diario") {
            endpoint = `/trabajadores/${selectedWorker.id_trabajador}/calcular_sueldo_diario`;
            params = { fecha: selectedDate.toISOString().split("T")[0] };
        } else if (salaryType === "semanal") {
            endpoint = `/trabajadores/${selectedWorker.id_trabajador}/calcular_sueldo_semanal`;
            params = { fecha_inicio_semana: selectedDate.toISOString().split("T")[0] };
        } else if (salaryType === "mensual") {
            const selectedMonth = selectedDate.toLocaleDateString("en-CA", { month: "2-digit" });
            endpoint = `/trabajadores/${selectedWorker.id_trabajador}/calcular_sueldo_mensual`;
            params = { mes: selectedMonth };
        }

        try {
            const response = await axios.get(`http://localhost:8000${endpoint}`, { params });
            if (response.data.message) {
                setErrorMessage(response.data.message); // Muestra el mensaje si no hay registros
            } else {
                setCalculatedSalaries(prevState => ({
                    ...prevState,
                    [selectedWorker.id_trabajador]: response.data[`${salaryType === 'diario' ? 'sueldo_diario' : salaryType === 'semanal' ? 'sueldo_semanal' : 'sueldo_mensual'}`]
                }));
                setShowModal(false); // Cierra el modal al completar el cálculo
            }
        } catch (error) {
            console.error("Error calculating salary:", error);
            setErrorMessage("No existen registros en el periodo seleccionado.");
        }
    };

    return (
        <div className="container-fluid mt-4 vh-100 vw-100">
            <h1>Trabajadores</h1>
            <div className="workers-table">
                <table className="table caption-top bg-white rounded mt-2">
                    <caption className="text-dark fs-4">RUT de los trabajadores y sueldos calculados</caption>
                    <thead>
                        <tr>
                            <th scope="col">#</th>
                            <th scope="col">RUT del Trabajador</th>
                            <th scope="col">Acciones</th>
                            <th scope="col">Último Sueldo Calculado</th>
                        </tr>
                    </thead>
                    <tbody>
                        {workers.length > 0 ? (
                            workers.map((worker, index) => (
                                <tr key={worker.id_trabajador}>
                                    <th scope="row">{index + 1}</th>
                                    <td>{worker.rut}</td>
                                    <td>
                                        <button
                                            className="btn btn-primary"
                                            onClick={() => openModal(worker)}
                                        >
                                            Calcular Sueldo
                                        </button>
                                    </td>
                                    <td>
                                        {calculatedSalaries[worker.id_trabajador] !== undefined
                                            ? `$${calculatedSalaries[worker.id_trabajador]}`
                                            : "No calculado"}
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

            {/* Modal for selecting the salary type and period */}
            <Modal show={showModal} onHide={() => setShowModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>Seleccionar Tipo de Sueldo</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {errorMessage && <Alert variant="warning">{errorMessage}</Alert>}
                    <Form>
                        <Form.Group controlId="formSalaryType">
                            <Form.Label>Selecciona el Tipo de Sueldo</Form.Label>
                            <Form.Control
                                as="select"
                                value={salaryType}
                                onChange={(e) => setSalaryType(e.target.value)}
                            >
                                <option value="">Selecciona un tipo</option>
                                <option value="diario">Diario</option>
                                <option value="semanal">Semanal</option>
                                <option value="mensual">Mensual</option>
                            </Form.Control>
                        </Form.Group>
                        {salaryType === "diario" || salaryType === "semanal" ? (
                            <Form.Group controlId="formDate" className="mt-3">
                                <Form.Label>Selecciona una Fecha</Form.Label>
                                <DatePicker
                                    selected={selectedDate}
                                    onChange={(date) => setSelectedDate(date)}
                                    dateFormat="yyyy-MM-dd"
                                    className="form-control"
                                    placeholderText="Elige una fecha"
                                />
                            </Form.Group>
                        ) : salaryType === "mensual" ? (
                            <Form.Group controlId="formMonth" className="mt-3">
                                <Form.Label>Selecciona el Mes</Form.Label>
                                <DatePicker
                                    selected={selectedDate}
                                    onChange={(date) => setSelectedDate(date)}
                                    dateFormat="MM/yyyy"
                                    showMonthYearPicker
                                    className="form-control"
                                    placeholderText="Elige un mes"
                                />
                            </Form.Group>
                        ) : null}
                    </Form>

                    {/* Display Hour Logs */}
                    {hourLogs.length > 0 ? (
                      <div className="mt-3">
                          <h5>Registros de Horas</h5>
                          <ul className="list-group">
                              {hourLogs.map((log, index) => (
                                  <li key={index} className="list-group-item">
                                      <div>{`Fecha: ${log.fecha}`}</div>
                                      <div>{`Horas trabajadas: ${log.horas_trabajadas}`}</div>
                                      <div>{`Turnos asociados: ${log.cantidad_turnos_trabajados}`}</div>
                                      {log.es_domingo && <div className="text-danger">* Día domingo</div>}
                                  </li>
                              ))}
                          </ul>
                      </div>
                  ) : (
                      <p className="mt-3">No hay registros para el período seleccionado.</p>
                  )}
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShowModal(false)}>
                        Cancelar
                    </Button>
                    <Button variant="primary" onClick={handleCalculateSalary} disabled={!salaryType || !selectedDate}>
                        Calcular
                    </Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
};

export default Dashboard;

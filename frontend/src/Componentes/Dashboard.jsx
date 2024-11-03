import React, { useEffect, useState } from "react";
import axios from "axios";
import { Modal, Button, Form, Alert } from "react-bootstrap";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import { useTranslation } from 'react-i18next'; // Importar el hook de traducción

const Dashboard = () => {
    const { t } = useTranslation(); // Usar el hook de traducción
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
                console.error(t("errors.fetchWorkers"), error);
            }
        };
        fetchWorkers();
    }, [t]);

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
            console.error(t("errors.fetchHourLogs"), error);
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
            alert(t("errors.selectSalaryTypeDate"));
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
                setErrorMessage(response.data.message);
            } else {
                setCalculatedSalaries(prevState => ({
                    ...prevState,
                    [selectedWorker.id_trabajador]: response.data[`${salaryType === 'diario' ? 'sueldo_diario' : salaryType === 'semanal' ? 'sueldo_semanal' : 'sueldo_mensual'}`]
                }));
                setShowModal(false); // Close the modal after calculating the salary
            }
        } catch (error) {
            console.error(t("errors.calculateSalary"), error);
            setErrorMessage(t("errors.noRecordsForPeriod"));
        }
    };

    return (
        <div className="container-fluid mt-4 vh-100 vw-100">
            <h1>{t("workers.title2")}</h1>
            <div className="workers-table">
                <table className="table caption-top bg-white rounded mt-2">
                    <caption className="text-dark fs-4">{t("workers.caption")}</caption>
                    <thead>
                        <tr>
                            <th scope="col">#</th>
                            <th scope="col">{t("workers.rut")}</th>
                            <th scope="col">{t("workers.actions")}</th>
                            <th scope="col">{t("workers.lastCalculatedSalary")}</th>
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
                                            {t("workers.calculateSalary")}
                                        </button>
                                    </td>
                                    <td>
                                        {calculatedSalaries[worker.id_trabajador] !== undefined
                                            ? `$${calculatedSalaries[worker.id_trabajador]}`
                                            : t("workers.notCalculated")}
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

            {/* Modal for selecting the salary type and period */}
            <Modal show={showModal} onHide={() => setShowModal(false)}>
                <Modal.Header closeButton>
                    <Modal.Title>{t("workers.selectSalaryType")}</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    {errorMessage && <Alert variant="warning">{errorMessage}</Alert>}
                    <Form>
                        <Form.Group controlId="formSalaryType">
                            <Form.Label>{t("workers.salaryType")}</Form.Label>
                            <Form.Control
                                as="select"
                                value={salaryType}
                                onChange={(e) => setSalaryType(e.target.value)}
                            >
                                <option value="">{t("workers.selectType")}</option>
                                <option value="diario">{t("workers.daily")}</option>
                                <option value="semanal">{t("workers.weekly")}</option>
                                <option value="mensual">{t("workers.monthly")}</option>
                            </Form.Control>
                        </Form.Group>
                        {salaryType === "diario" || salaryType === "semanal" ? (
                            <Form.Group controlId="formDate" className="mt-3">
                                <Form.Label>{t("workers.selectDate")}</Form.Label>
                                <DatePicker
                                    selected={selectedDate}
                                    onChange={(date) => setSelectedDate(date)}
                                    dateFormat="yyyy-MM-dd"
                                    className="form-control"
                                    placeholderText={t("workers.chooseDate")}
                                />
                            </Form.Group>
                        ) : salaryType === "mensual" ? (
                            <Form.Group controlId="formMonth" className="mt-3">
                                <Form.Label>{t("workers.selectMonth")}</Form.Label>
                                <DatePicker
                                    selected={selectedDate}
                                    onChange={(date) => setSelectedDate(date)}
                                    dateFormat="MM/yyyy"
                                    showMonthYearPicker
                                    className="form-control"
                                    placeholderText={t("workers.chooseMonth")}
                                />
                            </Form.Group>
                        ) : null}
                    </Form>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={() => setShowModal(false)}>
                        {t("buttons.cancel")}
                    </Button>
                    <Button variant="primary" onClick={handleCalculateSalary} disabled={!salaryType || !selectedDate}>
                        {t("workers.calculate")}
                    </Button>
                </Modal.Footer>
            </Modal>
        </div>
    );
};

export default Dashboard;

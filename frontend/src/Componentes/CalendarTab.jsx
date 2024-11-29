import React, { useState, useEffect } from "react";
import { Calendar, momentLocalizer } from "react-big-calendar";
import moment from "moment";
import "react-big-calendar/lib/css/react-big-calendar.css";
import axios from "axios";

const localizer = momentLocalizer(moment);

const CalendarTab = () => {
    const [events, setEvents] = useState([]);

    useEffect(() => {
        axios.get("http://localhost:8000/calendar-events/")
            .then(response => {
                const formattedEvents = response.data.map(event => ({
                    title: `Horas trabajadas: ${event.horas_trabajadas}`,
                    start: new Date(`${event.fecha}T${event.hora_inicio}`),
                    end: new Date(`${event.fecha}T${event.hora_fin}`),
                    allDay: false,
                }));
                setEvents(formattedEvents);
            })
            .catch(error => console.error("Error al cargar eventos:", error));
    }, []);

    return (
        <div className="calendar-container">
            <h2>Calendario de Horas Trabajadas</h2>
            <Calendar
                localizer={localizer}
                events={events}
                startAccessor="start"
                endAccessor="end"
                style={{ height: 420}}
                className="custom-calendar"
            />
        </div>
    );
};

export default CalendarTab;

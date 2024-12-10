import React, { useState, useEffect } from "react";
import { Calendar, momentLocalizer } from "react-big-calendar";
import moment from "moment";
import "moment/locale/es"; // Importa el idioma español para moment.js
import "moment/locale/en-gb"; // Asegúrate de tener también el inglés si es necesario
import "react-big-calendar/lib/css/react-big-calendar.css";
import axios from "axios";
import { useTranslation } from "react-i18next"; // Hook para traducción
import "./style.css";

const localizer = momentLocalizer(moment);

const CalendarTab = () => {
    const { t, i18n } = useTranslation(); // Traducción y lenguaje actual
    const [events, setEvents] = useState([]);

    // Textos del calendario según el idioma
    const messages = {
        en: {
            week: "Week",
            month: "Month",
            day: "Day",
            agenda: "Agenda",
            today: "Today",
            previous: "Back",
            next: "Next",
            noEventsInRange: "There are no events in this range.",
            showMore: (count) => `+${count} more`,
        },
        es: {
            week: "Semana",
            month: "Mes",
            day: "Día",
            agenda: "Agenda",
            today: "Hoy",
            previous: "Atrás",
            next: "Siguiente",
            noEventsInRange: "No hay eventos en este rango.",
            showMore: (count) => `+${count} más`,
        },
    };

    // Cargar eventos del servidor
    useEffect(() => {
        axios
            .get("http://localhost:8000/calendar-events/")
            .then((response) => {
                const formattedEvents = response.data.map((event) => ({
                    title: `${t("calendar.hoursWorked")}: ${event.horas_trabajadas}`,
                    start: new Date(`${event.fecha}T${event.hora_inicio}`),
                    end: new Date(`${event.fecha}T${event.hora_fin}`),
                    allDay: false,
                }));
                setEvents(formattedEvents);
            })
            .catch((error) =>
                console.error(t("errors.fetchCalendarEvents"), error)
            );
    }, [t]); // Se ejecuta cuando cambian las traducciones

    return (
        <div className="calendar-container">
            <h2>{t("calendar.title")}</h2>
            <Calendar
                localizer={localizer}
                events={events}
                startAccessor="start"
                endAccessor="end"
                messages={messages[i18n.language]} // Mensajes dinámicos según idioma actual
                style={{ height: 420 }}
                className="custom-calendar"
            />
        </div>
    );
};

export default CalendarTab;

import React, { useState, useEffect } from "react";
import Card from "./Card";
import ClienteTable from "./ClienteTable";
import axios from "axios";
import { useTranslation } from "react-i18next";
import "./style.css";

const Cliente = () => {
  const { t } = useTranslation();
  const [stats, setStats] = useState([
    { value: "Loading...", label: t("stats.totalClients"), icon: "bi-people" },
  ]);
  const [isLoading, setIsLoading] = useState(true);
  const [isSmallScreen, setIsSmallScreen] = useState(false);

  useEffect(() => {
    const fetchClientMetrics = async () => {
      try {
        const response = await axios.get("http://localhost:8000/metrics/total_clients");

        setStats([
          { value: response.data.total_clients || 0, label: t("stats.totalClients"), icon: "bi-people" },
        ]);
        setIsLoading(false);
      } catch (error) {
        console.error("Error fetching client metrics:", error);
        setStats([{ value: "Error", label: t("stats.totalClients"), icon: "bi-people" }]);
        setIsLoading(false);
      }
    };

    fetchClientMetrics();

    const checkScreenSize = () => {
      setIsSmallScreen(window.innerWidth <= 1024); // Define si es pantalla pequeña
    };

    checkScreenSize(); // Ejecuta al cargar el componente
    window.addEventListener("resize", checkScreenSize); // Escucha cambios en el tamaño de la ventana

    return () => window.removeEventListener("resize", checkScreenSize); // Limpia el evento



  }, [t]);

  return (
    <div className={`container-fluid main-content-wrapper ${
      isSmallScreen ? "ms-5" : ""}`}>
      <div className="row g-3 my-2">
        {isLoading ? (
          <p>{t("loading")}</p>
        ) : (
          stats.map((stat, index) => <Card key={index} {...stat} />)
        )}
      </div>
      <div className="row g-3 my-2">
        <ClienteTable />
      </div>
    </div>
  );
};

export default Cliente;

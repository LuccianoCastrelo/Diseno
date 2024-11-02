import React, { useState, useEffect } from "react";
import Card from "./Card";
import axios from "axios";
import Table from "./Table";
import { useTranslation } from 'react-i18next'; // Importar el hook de traducción

const MainContent = () => {
  const { t } = useTranslation(); // Usar el hook de traducción
  const [stats, setStats] = useState([
    { value: "Loading...", label: t("stats.hours"), icon: "bi-clock" },
    { value: "Loading...", label: t("stats.shifts"), icon: "bi-briefcase" },
    { value: "Loading...", label: t("stats.permanentWorkers"), icon: "bi-person-fill" },
    { value: "Loading...", label: t("stats.eventualWorkers"), icon: "bi-person-dash" },
  ]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const [workersRes, hoursRes, shiftsRes, permanentRes] = await Promise.all([
          axios.get("http://localhost:8000/metrics/total_eventual_workers"),
          axios.get("http://localhost:8000/metrics/total_horas_trabajadas"),
          axios.get("http://localhost:8000/metrics/total_turnos"),
          axios.get("http://localhost:8000/metrics/total_permanent_workers"),
        ]);

        setStats([
          { value: workersRes.data.total_eventual_workers || 0, label: t("stats.eventualWorkers"), icon: "bi-person-dash" },
          { value: hoursRes.data.total_horas_trabajadas || 0, label: t("stats.hours"), icon: "bi-clock" },
          { value: shiftsRes.data.total_turnos || 0, label: t("stats.shifts"), icon: "bi-briefcase" },
          { value: permanentRes.data.total_permanent_workers || 0, label: t("stats.permanentWorkers"), icon: "bi-person-fill" },
        ]);
        setIsLoading(false);
      } catch (error) {
        console.error("Error fetching metrics:", error);
        setStats([
          { value: "Error", label: t("stats.eventualWorkers"), icon: "bi-person-dash" },
          { value: "Error", label: t("stats.hours"), icon: "bi-clock" },
          { value: "Error", label: t("stats.shifts"), icon: "bi-briefcase" },
          { value: "Error", label: t("stats.permanentWorkers"), icon: "bi-person-fill" },
        ]);
        setIsLoading(false);
      }
    };

    fetchMetrics();
  }, [t]);

  return (
    <div className="container-fluid main-content-wrapper">
      <div className="row g-3 my-2">
        {isLoading ? (
          <p>{t('loading')}</p>
        ) : (
          stats.map((stat, index) => <Card key={index} {...stat} />)
        )}
      </div>
      <div className="row g-3 my-2">
        <Table />
      </div>
    </div>
  );
};

export default MainContent;

import React, { useState, useEffect } from "react";
import Card from "./Card";
import axios from "axios";
import MachinesTable from "./MachinesTable";
import { useTranslation } from 'react-i18next';

const Machines = () => {
  const { t } = useTranslation();
  const [stats, setStats] = useState([
    { value: "Loading...", label: t("stats.totalMachines"), icon: "bi-cpu" },
    { value: "Loading...", label: t("stats.totalFuelConsumed"), icon: "bi-fuel-pump" },
  ]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchMetrics = async () => {
    setIsLoading(true);
    try {
      const [totalRes, fuelRes] = await Promise.all([
        axios.get("http://localhost:8000/metrics/total_machines"),
        axios.get("http://localhost:8000/metrics/total_fuel_consumed"),
      ]);

      setStats([
        { value: totalRes.data.total_machines || 0, label: t("stats.totalMachines"), icon: "bi-cpu" },
        { value: parseFloat(fuelRes.data.total_fuel_consumed).toFixed(2) || 0, label: t("stats.totalFuelConsumed"), icon: "bi-fuel-pump" },
      ]);
    } catch (error) {
      console.error("Error fetching machine metrics:", error);
      setStats([
        { value: "Error fetching data", label: t("stats.totalMachines"), icon: "bi-cpu" },
        { value: "Error fetching data", label: t("stats.totalFuelConsumed"), icon: "bi-fuel-pump" },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchMetrics();
  }, [t]);

  return (
    <div className="container-fluid main-content-wrapper">
      <div className="row g-3 my-2">
        {isLoading ? (
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">{t("loading")}</span>
          </div>
        ) : (
          stats.map((stat, index) => (
            <Card key={index} {...stat} />
          ))
        )}
      </div>
      <div className="row g-3 my-2">
        <MachinesTable onMetricsUpdate={fetchMetrics} />
      </div>
    </div>
  );
};

export default Machines;

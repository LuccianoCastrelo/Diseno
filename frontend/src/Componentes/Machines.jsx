import React, { useState, useEffect } from "react";
import Card from "./Card";
import axios from "axios";
import MachinesTable from "./MachinesTable";
import { useTranslation } from 'react-i18next';

const Machines = () => {
  const { t } = useTranslation();
  const [stats, setStats] = useState([
    { value: "Loading...", label: t("stats.totalMachines"), icon: "bi-cpu" },
    { value: "Loading...", label: t("stats.operationalMachines"), icon: "bi-tools" },
    { value: "Loading...", label: t("stats.nonOperationalMachines"), icon: "bi-exclamation-circle" },
  ]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchMetrics = async () => {
    setIsLoading(true);
    try {
      const [totalRes, operationalRes, nonOperationalRes] = await Promise.all([
        axios.get("http://localhost:8000/metrics/total_machines"),
        axios.get("http://localhost:8000/metrics/operational_machines"),
        axios.get("http://localhost:8000/metrics/non_operational_machines"),
      ]);

      setStats([
        { value: totalRes.data.total_machines || 0, label: t("stats.totalMachines"), icon: "bi-cpu" },
        { value: operationalRes.data.operational_machines || 0, label: t("stats.operationalMachines"), icon: "bi-tools" },
        { value: nonOperationalRes.data.non_operational_machines || 0, label: t("stats.nonOperationalMachines"), icon: "bi-exclamation-circle" },
      ]);
    } catch (error) {
      console.error("Error fetching machine metrics:", error);
      setStats([
        { value: "Error", label: t("stats.totalMachines"), icon: "bi-cpu" },
        { value: "Error", label: t("stats.operationalMachines"), icon: "bi-tools" },
        { value: "Error", label: t("stats.nonOperationalMachines"), icon: "bi-exclamation-circle" },
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
          <p>{t("loading")}</p>
        ) : (
          stats.map((stat, index) => <Card key={index} {...stat} />)
        )}
      </div>
      <div className="row g-3 my-2">
        <MachinesTable onMetricsUpdate={fetchMetrics} />
      </div>
    </div>
  );
};

export default Machines;

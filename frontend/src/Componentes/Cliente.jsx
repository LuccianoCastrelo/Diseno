import React, { useState, useEffect } from "react";
import Card from "./Card";
import ClienteTable from "./ClienteTable";
import axios from "axios";
import { useTranslation } from "react-i18next";

const Cliente = () => {
  const { t } = useTranslation();
  const [stats, setStats] = useState([
    { value: "Loading...", label: t("stats.totalClients"), icon: "bi-people" },
  ]);
  const [isLoading, setIsLoading] = useState(true);

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
        <ClienteTable />
      </div>
    </div>
  );
};

export default Cliente;

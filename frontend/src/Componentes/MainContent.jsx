import React from "react";
import Card from "./Card";
import Table from "./Table";
import { useTranslation } from 'react-i18next'; // Importar el hook de traducción

const MainContent = () => {
  const { t } = useTranslation(); // Usar el hook de traducción
  
  const stats = [
    { value: "230", label: t("stats.workers"), icon: "bi-cart-plus" },
    { value: "150", label: t("stats.hours"), icon: "bi-clock" },
    { value: "$1.5M", label: t("stats.factures"), icon: "bi-currency-collar" },
    { value: "5", label: t("stats.clients"), icon: "bi-people" },
  ];

  return (
    <div className="container-fluid main-content-wrapper">
      <div className="row g-3 my-2">
        {stats.map((stat, index) => (
          <Card key={index} {...stat} />
        ))}
      </div>
      <div className="row g-3 my-2">
        <Table />
      </div>
    </div>
  );
};

export default MainContent;

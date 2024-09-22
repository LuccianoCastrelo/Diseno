import React, { useEffect, useState } from "react";
import axios from "axios";

const Table = () => {
  const [workers, setWorkers] = useState([]);

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

  return (
    <table className="table caption-top bg-white rounded mt-2">
      <caption className="text-dark fs-4">Workers</caption>
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">First</th>
          <th scope="col">Handle</th>
        </tr>
      </thead>
      <tbody>
        {workers.map((worker, index) => (
          <tr key={worker.id_trabajador}>
            <th scope="row">{index + 1}</th>
            <td>{worker.nombre}</td>
            <td>@{worker.nombre.toLowerCase()}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default Table;

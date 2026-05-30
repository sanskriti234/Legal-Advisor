import { useEffect, useState } from "react";
import api from "../api/api";

export default function History() {

  const [records, setRecords] = useState<any[]>([]);

  useEffect(() => {
    api.get("/history")
      .then(res => setRecords(res.data))
      .catch(console.error);
  }, []);

  return (
    <div style={{ padding: "40px" }}>
      <h1>Analysis History</h1>

      {records.map(record => (
        <div key={record.id}>
          <h3>{record.filename}</h3>
          <p>Risk Score: {record.risk_score}</p>
        </div>
      ))}
    </div>
  );
}
import { useState } from "react";
import api from "../api/api";

export default function Dashboard() {

  const [file, setFile] = useState<File | null>(null);
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const uploadFile = async () => {

    if (!file) return;

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await api.post(
        "/upload",
        formData
      );

      setResult(response.data.analysis);

    } catch (error) {
      console.error(error);
    }

    setLoading(false);
  };

  return (
    <div style={{ padding: "40px" }}>

      <h1>AI Legal Risk Analyzer</h1>

      <input
        type="file"
        accept=".pdf"
        onChange={(e) =>
          setFile(e.target.files?.[0] || null)
        }
      />

      <br />
      <br />

      <button onClick={uploadFile}>
        Analyze PDF
      </button>

      {loading && <p>Analyzing...</p>}

      {result && (
        <div>

          <h2>Summary</h2>
          <p>{result.summary}</p>

          <h2>Risk Score</h2>
          <p>{result.risk_score}</p>

        </div>
      )}

    </div>
  );
}
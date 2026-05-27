import { useEffect } from "react";
import api from "../api/api";

export default function Home() {

  useEffect(() => {
    api.get("/")
      .then(res => console.log(res.data))
      .catch(err => console.log(err));
  }, []);

  return (
    <div className="p-10">
      <h1 className="text-5xl font-bold">
        AI Legal Risk Analyzer
      </h1>
    </div>
  );
}

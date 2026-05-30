import { Link } from "react-router-dom";

export default function Home() {
  return (
    <div style={{ padding: "40px" }}>

      <h1>Legal Advisor AI</h1>

      <Link to="/dashboard">
        Go To Dashboard
      </Link>

    </div>
  );
}
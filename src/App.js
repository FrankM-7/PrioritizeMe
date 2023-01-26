import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Register from "./Register";
import MainContent from "./MainContent";
import Login from "./Login";

export default function App() {
  return (
    <Router>
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/" element={<MainContent />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </Router>
  );
}

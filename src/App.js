import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Register from "./Register";
import MainContent from "./MainContent";
import Login from "./Login";
import axios from "axios";

export default function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<MainContent />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </Router>
  );
}

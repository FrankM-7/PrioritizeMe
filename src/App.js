import { BrowserRouter , Routes, Route } from "react-router-dom";
import Register from "./Register";
import MainContent from "./MainContent";
import Login from "./Login";

export default function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainContent />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
      </Routes>
    </BrowserRouter>
  );
}

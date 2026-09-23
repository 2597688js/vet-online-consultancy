import { Routes, Route } from "react-router-dom";
import { Home } from "./pages/Home";
import { Login } from "./pages/Login";
import { Register } from "./pages/Register";
import { Book } from "./pages/Book";
import { AdminDashboard } from "./pages/AdminDashboard";
import { MyAppointments } from "./pages/MyAppointments";
import { AuthProvider } from "./context/AuthContext";
import { ScrollToHash } from "./components/ScrollToHash";

function App() {
  return (
    <AuthProvider>
      <ScrollToHash />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/book" element={<Book />} />
        <Route path="/admin" element={<AdminDashboard />} />
        <Route path="/appointments" element={<MyAppointments />} />
      </Routes>
    </AuthProvider>
  );
}

export default App;

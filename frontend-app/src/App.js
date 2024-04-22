import { Routes, Route } from 'react-router-dom';
import LoginPage from './LoginPage/Login';
import RegistrationForm from './RegistrationPage/Registration';
import CapsulePage from './CapsuleCreation/Capsule';

function App() {
  return (
    <div>
    <Routes>
        <Route path="/" element={<RegistrationForm />} />
        <Route path="/register" element={<RegistrationForm />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/create_capsule" element={<CapsulePage />} />
    </Routes>
    </div>
  );
}

export default App;

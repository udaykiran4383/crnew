import React from "react";
import { GoogleLogin } from "@react-oauth/google";
import { GoogleOAuthProvider } from "@react-oauth/google";
import axios from "axios";
import { useNavigate } from "react-router-dom";

axios.defaults.baseURL = "http://127.0.0.1:8000";


const clientId =
  "949228241511-mbfe9v2nh8u098587qflqstthjfo5oso.apps.googleusercontent.com";

function GoogleLoginComponent() {
  const navigate = useNavigate();

  const sendTokenToDjango = async (token) => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/google-login/", { token });

      if (response && response.data) {
        const { newCreated, isAuthenticated, redirectUrl } = response.data;
      
      if (newCreated) {
        localStorage.setItem("isAuthenticated", "true");
        window.dispatchEvent(new Event('storage'));
        navigate(redirectUrl); // Use redirectUrl instead of hardcoding path
      } else if (isAuthenticated) {
        localStorage.setItem("isAuthenticated", "true");
        window.dispatchEvent(new Event('storage'));
        navigate(redirectUrl); // Use redirectUrl instead of hardcoding path
      }
    }
    } catch (error) {
      console.error("Error logging in with Google:", error);
    }
  };

  const handleLoginSuccess = (credentialResponse) => {
    sendTokenToDjango(credentialResponse.credential);
  };

  const handleLoginError = () => {
    console.log("Login Failed");
  };

  return (
    <GoogleOAuthProvider clientId={clientId}>
      <GoogleLogin onSuccess={handleLoginSuccess} onError={handleLoginError} />
    </GoogleOAuthProvider>
  );
}

export default GoogleLoginComponent;

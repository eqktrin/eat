import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

// Базовые стили (можно заменить на CSS/SCSS)
import "./index.css";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

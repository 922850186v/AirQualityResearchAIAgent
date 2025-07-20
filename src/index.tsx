import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
// import "./index.css"; // Optional: your global CSS (e.g. Tailwind)

const rootElement = document.getElementById("root");
if (!rootElement) throw new Error("Failed to find root element");

const root = ReactDOM.createRoot(rootElement);
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

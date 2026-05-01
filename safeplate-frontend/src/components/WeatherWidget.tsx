import React, { useState, useEffect } from "react";
import api from "../api/api";

const WeatherWidget = () => {
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchWeather = async () => {
    try {
      const response = await api.get("/weather/?city=Moscow");
      setWeather(response.data);
      setError(null);
    } catch (err) {
      console.error("Ошибка загрузки погоды:", err);
      setError("Не удалось загрузить погоду");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWeather();
  }, []);

  if (loading) return <div style={styles.widget}>Загрузка погоды...</div>;
  if (error) return null;
  if (!weather) return null;

  return (
    <div style={styles.widget}>
      <img 
        src={`https://openweathermap.org/img/w/${weather.icon}.png`} 
        alt={weather.description}
        style={styles.icon}
      />
      <div style={styles.info}>
        <div style={styles.city}>{weather.city}</div>
        <div style={styles.temp}>{weather.temperature}°C</div>
        <div style={styles.desc}>{weather.description}</div>
      </div>
    </div>
  );
};

const styles = {
  widget: {
    display: "flex",
    alignItems: "center",
    gap: "8px",
    background: "#f0f8ff",
    padding: "5px 12px",
    borderRadius: "20px",
    fontSize: "14px",
  },
  icon: {
    width: "30px",
    height: "30px",
  },
  info: {
    textAlign: "left",
  },
  city: {
    fontWeight: "bold",
    fontSize: "12px",
  },
  temp: {
    fontSize: "16px",
    fontWeight: "600",
  },
  desc: {
    fontSize: "10px",
    color: "#666",
  },
};

export default WeatherWidget;
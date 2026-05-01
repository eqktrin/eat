import React, { useState, useEffect } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import WeatherWidget from "./WeatherWidget";
import { useAuth } from "../hooks/useAuth";

interface LinkItem {
    path: string;
    label: string;
}

const Navbar: React.FC = () => {
    const navigate = useNavigate();
    const { user, logout } = useAuth();
    const [scrolled, setScrolled] = useState<boolean>(false);

    useEffect(() => {
        const handleScroll = (): void => {
            setScrolled(window.scrollY > 20);
        };
        window.addEventListener("scroll", handleScroll);
        return () => window.removeEventListener("scroll", handleScroll);
    }, []);

    const handleLogout = (): void => {
        logout();
        navigate("/login");
    };

    const publicLinks: LinkItem[] = [
        { path: "/menu", label: "Меню" },
    ];

    const privateLinks: LinkItem[] = [
        { path: "/menu", label: "Меню" },
        { path: "/favorites", label: "Избранное" },
        { path: "/ai", label: "AI поиск" },
        { path: "/profile", label: "Профиль" },
    ];

    const links = user ? privateLinks : publicLinks;

    return (
        <nav
            style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
                padding: "15px 50px",
                backgroundColor: scrolled ? "#ffffffee" : "#ffffffcc",
                backdropFilter: "blur(8px)",
                boxShadow: scrolled
                    ? "0 12px 35px rgba(0,0,0,0.25)"
                    : "0 8px 25px rgba(0,0,0,0.2)",
                fontFamily: "'Inter', sans-serif",
                position: "sticky",
                top: 0,
                zIndex: 1000,
                transition: "all 0.3s ease",
            }}
        >
            <div
                style={{
                    fontWeight: 700,
                    fontSize: 28,
                    color: "#007bff",
                    cursor: "pointer",
                    transition: "transform 0.4s, color 0.4s",
                }}
                onClick={() => navigate("/menu")}
                onMouseEnter={(e: React.MouseEvent<HTMLDivElement>) =>
                    (e.currentTarget.style.transform = "rotate(-5deg) scale(1.1)")
                }
                onMouseLeave={(e: React.MouseEvent<HTMLDivElement>) =>
                    (e.currentTarget.style.transform = "rotate(0deg) scale(1)")
                }
            >
                SafePlate
            </div>

            <div style={{ display: "flex", gap: "30px", alignItems: "center" }}>
                {links.map((link) => (
                    <NavLink
                        key={link.path}
                        to={link.path}
                        style={({ isActive }: { isActive: boolean }) => ({
                            textDecoration: "none",
                            color: isActive ? "#007bff" : "#555",
                            fontWeight: 500,
                            fontSize: 16,
                            padding: "5px 0",
                        })}
                    >
                        {({ isActive }: { isActive: boolean }) => (
                            <span
                                style={{
                                    position: "relative",
                                    paddingBottom: 2,
                                    display: "inline-block",
                                    cursor: "pointer",
                                    transition: "transform 0.2s, text-shadow 0.2s",
                                }}
                                onMouseEnter={(e: React.MouseEvent<HTMLSpanElement>) => {
                                    e.currentTarget.style.transform = "scale(1.08)";
                                    e.currentTarget.style.textShadow = "0 2px 8px rgba(0,123,255,0.3)";
                                }}
                                onMouseLeave={(e: React.MouseEvent<HTMLSpanElement>) => {
                                    e.currentTarget.style.transform = "scale(1)";
                                    e.currentTarget.style.textShadow = "none";
                                }}
                            >
                                {link.label}
                                <span
                                    style={{
                                        position: "absolute",
                                        bottom: 0,
                                        left: 0,
                                        height: 3,
                                        width: "100%",
                                        borderRadius: 2,
                                        background: isActive
                                            ? "linear-gradient(90deg, #007bff, #00c6ff)"
                                            : "linear-gradient(90deg, transparent, transparent)",
                                        transition: "all 0.3s",
                                    }}
                                />
                            </span>
                        )}
                    </NavLink>
                ))}
                
                {user && (
                    <div style={{ display: "flex", alignItems: "center", gap: "15px" }}>
                        <span style={{ color: "#007bff", fontWeight: 500, fontSize: 14 }}>
                            {user.email}
                        </span>
                        <button
                            onClick={handleLogout}
                            style={{
                                background: "transparent",
                                border: "1px solid #dc3545",
                                color: "#dc3545",
                                padding: "6px 14px",
                                borderRadius: 8,
                                cursor: "pointer",
                                fontSize: 14,
                                fontWeight: 500,
                                transition: "all 0.3s",
                            }}
                            onMouseEnter={(e) => {
                                e.currentTarget.style.backgroundColor = "#dc3545";
                                e.currentTarget.style.color = "#fff";
                            }}
                            onMouseLeave={(e) => {
                                e.currentTarget.style.backgroundColor = "transparent";
                                e.currentTarget.style.color = "#dc3545";
                            }}
                        >
                            Выйти
                        </button>
                    </div>
                )}
                
                <WeatherWidget />
            </div>
        </nav>
    );
};

export default Navbar;
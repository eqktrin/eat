import React, { useEffect, useState, useCallback } from "react";
import { useSearchParams } from "react-router-dom";
import { HelmetProvider } from "react-helmet-async";
import api from "../api/api";
import ImageUpload from "../components/ImageUpload";
import SEO from "../components/SEO";

interface DishImage {
    id: number;
    image_url: string;
}

interface Dish {
    id: number;
    name: string;
    description: string;
    allergens: string[];
    images?: DishImage[];
}

interface UserProfile {
    id: number;
    email: string;
    role: string;
    allergens: string[];
}

const MenuPage: React.FC = () => {
    const [searchParams, setSearchParams] = useSearchParams();
    const [dishes, setDishes] = useState<Dish[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [userAllergens, setUserAllergens] = useState<string[]>([]);
    const [categories] = useState<string[]>([
        "soup", "main", "salad", "dessert", "vegan", "meat", "fish", "side_dish", "drink"
    ]);
    const [total, setTotal] = useState<number>(0);
    const [currentUser, setCurrentUser] = useState<UserProfile | null>(null);
    const [selectedImage, setSelectedImage] = useState<string | null>(null);

    const search = searchParams.get("search") || "";
    const category = searchParams.get("category") || "";
    const sortBy = searchParams.get("sortBy") || "name";
    const sortOrder = searchParams.get("sortOrder") || "asc";
    const skip = parseInt(searchParams.get("skip") || "0");
    const limit = parseInt(searchParams.get("limit") || "6");
    const showAll = searchParams.get("showAll") === "true";

    const fetchCurrentUser = useCallback(async () => {
        try {
            const res = await api.get<UserProfile>("/auth/me");
            setCurrentUser(res.data);
        } catch (err) {
            console.error("Не авторизован");
        }
    }, []);

    const fetchUserAllergens = useCallback(async () => {
        try {
            const userRes = await api.get<UserProfile>("/profile/me");
            setUserAllergens(userRes.data.allergens || []);
        } catch (err) {
            console.error("Ошибка при получении аллергенов:", err);
        }
    }, []);

    const fetchDishes = useCallback(async () => {
        setLoading(true);
        try {
            const params: Record<string, string | number | undefined> = {
                search: search || undefined,
                category: category || undefined,
                sort_by: sortBy,
                sort_order: sortOrder,
                skip,
                limit,
                safe_only: !showAll,
            };
            
            const res = await api.get<Dish[]>("/menu/", { params });
            setDishes(res.data || []);
            
            const totalCount = res.headers["x-total-count"];
            setTotal(totalCount ? parseInt(totalCount) : 0);
        } catch (err) {
            console.error("Ошибка при получении блюд:", err);
        }
        setLoading(false);
    }, [search, category, sortBy, sortOrder, skip, limit, showAll]);

    const updateParams = (updates: Record<string, string | undefined>) => {
        const newParams: Record<string, string> = {
            ...(search && { search }),
            ...(category && { category }),
            sortBy,
            sortOrder,
            skip: "0",
            limit: limit.toString(),
            ...(showAll && { showAll: "true" }),
            ...updates,
        };
        setSearchParams(newParams);
    };

    const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        updateParams({ search: e.target.value });
    };

    const handleCategoryChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        updateParams({ category: e.target.value });
    };

    const handleSortByChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        updateParams({ sortBy: e.target.value });
    };

    const handleSortOrderChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
        updateParams({ sortOrder: e.target.value });
    };

    const handleShowAllChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        updateParams({ 
            showAll: e.target.checked ? "true" : "",
            skip: "0" 
        });
    };

    const handleNextPage = () => {
        updateParams({ skip: (skip + limit).toString() });
    };

    const handlePrevPage = () => {
        updateParams({ skip: Math.max(0, skip - limit).toString() });
    };

    const handleFavorite = async (dish: Dish) => {
        try {
            await api.post("/favorites/add", { dish_id: dish.id });
            alert(`${dish.name} добавлено в избранное`);
        } catch (err) {
            console.error("Ошибка при добавлении в избранное:", err);
        }
    };

    const handleOrder = async (dish: Dish) => {
        const isDangerous = dish.allergens.some(a => userAllergens.includes(a));
        
        if (isDangerous) {
            alert("Это блюдо содержит ваши аллергены! Заказ невозможен.");
            return;
        }
        
        try {
            const userRes = await api.get<UserProfile>("/profile/me");
            const userId = userRes.data.id;
            
            await api.post("/orders/", {
                dish_id: dish.id,
                user_id: userId
            });
            alert(`Заказ "${dish.name}" оформлен!`);
        } catch (err) {
            console.error("Ошибка при заказе:", err);
            alert("Ошибка при оформлении заказа");
        }
    };

    const dangerousDishes = dishes.filter(d => 
        d.allergens.some(a => userAllergens.includes(a))
    );

    useEffect(() => {
        fetchCurrentUser();
        fetchUserAllergens();
    }, [fetchCurrentUser, fetchUserAllergens]);

    useEffect(() => {
        fetchDishes();
    }, [fetchDishes]);

    const pageTitle = "Меню";
    const pageDescription = "Ознакомьтесь с нашим меню. У нас есть блюда на любой вкус: супы, салаты, горячие блюда, десерты и напитки. Все блюда с указанием аллергенов для вашей безопасности.";
    const pageUrl = "/menu";

    return (
        <HelmetProvider>
            <SEO 
                title={pageTitle}
                description={pageDescription}
                url={pageUrl}
                type="website"
            />
            
            <div
                style={{
                    padding: "40px 20px",
                    maxWidth: 1000,
                    margin: "0 auto",
                    fontFamily: "'Inter', sans-serif",
                }}
            >
                <h1 style={{ fontSize: 32, fontWeight: 700, marginBottom: 30, color: "#333" }}>
                    Меню
                </h1>

                <div style={{
                    background: "#f8f9fa",
                    padding: 20,
                    borderRadius: 8,
                    marginBottom: 25,
                    border: "1px solid #dee2e6"
                }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 20 }}>
                        <div>
                            <strong>Статистика:</strong>
                            <span style={{ marginLeft: 15, color: "#2e7d32" }}>Безопасно: {dishes.length - dangerousDishes.length}</span>
                            <span style={{ marginLeft: 15, color: "#d32f2f" }}>Опасно: {dangerousDishes.length}</span>
                            <span style={{ marginLeft: 15, color: "#555" }}>Всего: {dishes.length}</span>
                        </div>
                        
                        <label style={{ display: "flex", alignItems: "center", gap: 8, cursor: "pointer" }}>
                            <input
                                type="checkbox"
                                checked={showAll}
                                onChange={handleShowAllChange}
                                style={{ width: 18, height: 18 }}
                            />
                            <span>Показывать все блюда</span>
                        </label>
                    </div>

                    <div style={{ display: "flex", gap: 15, flexWrap: "wrap", marginBottom: 15 }}>
                        <input
                            type="text"
                            placeholder="Поиск по названию..."
                            value={search}
                            onChange={handleSearchChange}
                            style={{
                                flex: 2,
                                minWidth: 200,
                                padding: 10,
                                borderRadius: 6,
                                border: "1px solid #ccc",
                                fontSize: 14,
                            }}
                        />

                        <select
                            value={category}
                            onChange={handleCategoryChange}
                            style={{
                                flex: 1,
                                minWidth: 150,
                                padding: 10,
                                borderRadius: 6,
                                border: "1px solid #ccc",
                                fontSize: 14,
                            }}
                        >
                            <option value="">Все категории</option>
                            {categories.map(cat => (
                                <option key={cat} value={cat}>
                                    {cat.charAt(0).toUpperCase() + cat.slice(1)}
                                </option>
                            ))}
                        </select>

                        <select
                            value={sortBy}
                            onChange={handleSortByChange}
                            style={{
                                flex: 1,
                                minWidth: 150,
                                padding: 10,
                                borderRadius: 6,
                                border: "1px solid #ccc",
                                fontSize: 14,
                            }}
                        >
                            <option value="name">По названию</option>
                            <option value="category">По категории</option>
                        </select>

                        <select
                            value={sortOrder}
                            onChange={handleSortOrderChange}
                            style={{
                                flex: 1,
                                minWidth: 120,
                                padding: 10,
                                borderRadius: 6,
                                border: "1px solid #ccc",
                                fontSize: 14,
                            }}
                        >
                            <option value="asc">По возрастанию</option>
                            <option value="desc">По убыванию</option>
                        </select>
                    </div>

                    {userAllergens.length > 0 && (
                        <div>
                            <strong style={{ fontSize: 14 }}>Ваши аллергены:</strong>
                            <div style={{ marginTop: 8, display: "flex", flexWrap: "wrap", gap: 8 }}>
                                {userAllergens.map((allergen, idx) => (
                                    <span key={idx} style={{
                                        background: "#ffebee",
                                        color: "#d32f2f",
                                        padding: "4px 12px",
                                        borderRadius: 20,
                                        fontSize: 13,
                                        fontWeight: 500,
                                    }}>
                                        {allergen}
                                    </span>
                                ))}
                            </div>
                        </div>
                    )}
                </div>

                {dangerousDishes.length > 0 && !showAll && (
                    <div style={{
                        background: "#fff5f5",
                        border: "1px solid #ffcdd2",
                        color: "#d32f2f",
                        padding: 15,
                        borderRadius: 8,
                        marginBottom: 25,
                        display: "flex",
                        justifyContent: "space-between",
                        alignItems: "center"
                    }}>
                        <span>
                            <strong>Внимание!</strong> В меню есть {dangerousDishes.length} блюд, содержащих ваши аллергены.
                        </span>
                        <button
                            onClick={() => updateParams({ showAll: "true", skip: "0" })}
                            style={{
                                padding: "8px 16px",
                                background: "#d32f2f",
                                color: "white",
                                border: "none",
                                borderRadius: 6,
                                cursor: "pointer",
                                fontWeight: 600,
                                fontSize: 14
                            }}
                        >
                            Показать все
                        </button>
                    </div>
                )}

                {loading ? (
                    <p style={{ textAlign: "center", padding: 40, color: "#555" }}>Загрузка...</p>
                ) : dishes.length === 0 ? (
                    <p style={{ textAlign: "center", padding: 40, color: "#777" }}>Нет доступных блюд</p>
                ) : (
                    <>
                        <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
                            {dishes.map((dish) => {
                                const isDangerous = dish.allergens.some(a => userAllergens.includes(a));
                                const hasAllergens = dish.allergens.length > 0;
                                
                                return (
                                    <article
                                        key={dish.id}
                                        style={{
                                            border: isDangerous ? "2px solid #d32f2f" : 
                                                   hasAllergens ? "1px solid #ffb74d" : "1px solid #e0e0e0",
                                            padding: 20,
                                            borderRadius: 12,
                                            boxShadow: "0 4px 12px rgba(0,0,0,0.05)",
                                            transition: "0.3s transform, 0.3s box-shadow",
                                            background: isDangerous ? "#fff5f5" : 
                                                       hasAllergens ? "#fffaf0" : "white"
                                        }}
                                        onMouseEnter={(e) => {
                                            e.currentTarget.style.transform = "translateY(-3px)";
                                            e.currentTarget.style.boxShadow = "0 6px 20px rgba(0,0,0,0.1)";
                                        }}
                                        onMouseLeave={(e) => {
                                            e.currentTarget.style.transform = "translateY(0)";
                                            e.currentTarget.style.boxShadow = "0 4px 12px rgba(0,0,0,0.05)";
                                        }}
                                    >
                                        <div style={{ display: "flex", gap: 20, flexWrap: "wrap", marginBottom: 15 }}>
                                            {dish.images && dish.images.length > 0 ? (
                                                <div style={{ flex: "0 0 200px" }}>
                                                    <div
                                                        onClick={() => setSelectedImage(`http://localhost:8000${dish.images![0].image_url}`)}
                                                        style={{
                                                            cursor: "pointer",
                                                            borderRadius: 12,
                                                            overflow: "hidden",
                                                            boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
                                                            transition: "transform 0.2s ease, box-shadow 0.2s ease",
                                                            width: "100%",
                                                            height: 140,
                                                            backgroundColor: "#f5f5f5",
                                                            display: "flex",
                                                            alignItems: "center",
                                                            justifyContent: "center"
                                                        }}
                                                        onMouseEnter={(e) => {
                                                            e.currentTarget.style.transform = "scale(1.02)";
                                                            e.currentTarget.style.boxShadow = "0 8px 24px rgba(0,0,0,0.15)";
                                                        }}
                                                        onMouseLeave={(e) => {
                                                            e.currentTarget.style.transform = "scale(1)";
                                                            e.currentTarget.style.boxShadow = "0 4px 12px rgba(0,0,0,0.1)";
                                                        }}
                                                    >
                                                        <img
                                                            src={`http://localhost:8000${dish.images[0].image_url}`}
                                                            alt={dish.name}
                                                            loading="lazy"
                                                            style={{
                                                                maxWidth: "100%",
                                                                maxHeight: "100%",
                                                                objectFit: "contain",
                                                                display: "block"
                                                            }}
                                                            onError={(e) => {
                                                                console.error("Ошибка загрузки картинки:", e.currentTarget.src);
                                                            }}
                                                        />
                                                    </div>
                                                    {dish.images.length > 1 && (
                                                        <div style={{ fontSize: 12, color: "#777", marginTop: 6, textAlign: "center" }}>
                                                            + ещё {dish.images.length - 1} фото
                                                        </div>
                                                    )}
                                                </div>
                                            ) : (
                                                <div style={{ 
                                                    flex: "0 0 200px", 
                                                    height: 140, 
                                                    background: "#f0f0f0", 
                                                    borderRadius: 12, 
                                                    display: "flex", 
                                                    alignItems: "center", 
                                                    justifyContent: "center", 
                                                    color: "#999",
                                                    fontSize: 14
                                                }}>
                                                    📷 Нет фото
                                                </div>
                                            )}

                                            <div style={{ flex: 1 }}>
                                                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", flexWrap: "wrap", gap: 10 }}>
                                                    <h2 style={{ fontSize: 20, fontWeight: 600, marginBottom: 8, color: "#333", margin: 0 }}>
                                                        {dish.name}
                                                    </h2>
                                                    {isDangerous ? (
                                                        <span style={{
                                                            padding: "4px 10px",
                                                            borderRadius: 4,
                                                            fontSize: 12,
                                                            fontWeight: 600,
                                                            background: "#ffebee",
                                                            color: "#d32f2f"
                                                        }}>
                                                            Опасно
                                                        </span>
                                                    ) : hasAllergens ? (
                                                        <span style={{
                                                            padding: "4px 10px",
                                                            borderRadius: 4,
                                                            fontSize: 12,
                                                            fontWeight: 600,
                                                            background: "#fff3e0",
                                                            color: "#ef6c00"
                                                        }}>
                                                            Аллергены
                                                        </span>
                                                    ) : null}
                                                </div>
                                                
                                                <p style={{ color: "#555", marginBottom: 12 }}>{dish.description}</p>

                                                <div style={{ marginBottom: 12 }}>
                                                    <strong>Аллергены:</strong>
                                                    {dish.allergens.length > 0 ? (
                                                        <div style={{ marginTop: 6, display: "flex", flexWrap: "wrap", gap: 6 }}>
                                                            {dish.allergens.map((a) => {
                                                                const isDanger = userAllergens.includes(a);
                                                                return (
                                                                    <span 
                                                                        key={a} 
                                                                        style={{
                                                                            background: isDanger ? "#ffebee" : "#fff3e0",
                                                                            color: isDanger ? "#d32f2f" : "#ef6c00",
                                                                            padding: "3px 8px",
                                                                            borderRadius: 4,
                                                                            fontSize: 12,
                                                                            fontWeight: 500,
                                                                        }}
                                                                    >
                                                                        {a}
                                                                    </span>
                                                                );
                                                            })}
                                                        </div>
                                                    ) : (
                                                        <span style={{ color: "#777", fontStyle: "italic", marginLeft: 8 }}>Нет аллергенов</span>
                                                    )}
                                                </div>

                                                {isDangerous && (
                                                    <div style={{
                                                        background: "#ffebee",
                                                        color: "#d32f2f",
                                                        padding: "6px 10px",
                                                        borderRadius: 6,
                                                        margin: "8px 0 12px 0",
                                                        fontSize: 13,
                                                        fontWeight: 500,
                                                        borderLeft: "3px solid #d32f2f"
                                                    }}>
                                                        Содержит ваши аллергены
                                                    </div>
                                                )}

                                                <div style={{ display: "flex", gap: 12 }}>
                                                    <button
                                                        onClick={() => handleOrder(dish)}
                                                        style={{
                                                            padding: "8px 16px",
                                                            backgroundColor: isDangerous ? "#f5f5f5" : "#1976d2",
                                                            color: isDangerous ? "#9e9e9e" : "#fff",
                                                            border: "none",
                                                            borderRadius: 8,
                                                            cursor: isDangerous ? "not-allowed" : "pointer",
                                                            fontWeight: 600,
                                                            transition: "0.2s",
                                                            flex: 1
                                                        }}
                                                        onMouseEnter={(e) => {
                                                            if (!isDangerous) {
                                                                e.currentTarget.style.transform = "scale(1.02)";
                                                            }
                                                        }}
                                                        onMouseLeave={(e) => {
                                                            if (!isDangerous) {
                                                                e.currentTarget.style.transform = "scale(1)";
                                                            }
                                                        }}
                                                    >
                                                        {isDangerous ? "Недоступно" : "Заказать"}
                                                    </button>
                                                    
                                                    <button
                                                        onClick={() => handleFavorite(dish)}
                                                        style={{
                                                            padding: "8px 16px",
                                                            backgroundColor: "#fff",
                                                            color: "#1976d2",
                                                            border: "1px solid #1976d2",
                                                            borderRadius: 8,
                                                            cursor: "pointer",
                                                            fontWeight: 600,
                                                            transition: "0.2s",
                                                        }}
                                                        onMouseEnter={(e) => {
                                                            e.currentTarget.style.transform = "scale(1.02)";
                                                            e.currentTarget.style.backgroundColor = "#e3f2fd";
                                                        }}
                                                        onMouseLeave={(e) => {
                                                            e.currentTarget.style.transform = "scale(1)";
                                                            e.currentTarget.style.backgroundColor = "#fff";
                                                        }}
                                                    >
                                                        В избранное
                                                    </button>
                                                </div>

                                                {currentUser?.role === "ADMIN" && (
                                                    <div style={{ marginTop: 12 }}>
                                                        <ImageUpload 
                                                            dishId={dish.id} 
                                                            onUploadComplete={() => fetchDishes()} 
                                                        />
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    </article>
                                );
                            })}
                        </div>

                        <div style={{ display: "flex", justifyContent: "center", gap: 20, marginTop: 30 }}>
                            <button
                                onClick={handlePrevPage}
                                disabled={skip === 0}
                                style={{
                                    padding: "10px 20px",
                                    backgroundColor: skip === 0 ? "#f0f0f0" : "#1976d2",
                                    color: skip === 0 ? "#999" : "white",
                                    border: "none",
                                    borderRadius: 6,
                                    cursor: skip === 0 ? "not-allowed" : "pointer",
                                    fontWeight: 600,
                                }}
                            >
                                ← Назад
                            </button>
                            <span style={{ padding: "10px 0", color: "#555" }}>
                                Страница {Math.floor(skip / limit) + 1} 
                                {total > 0 && ` из ${Math.ceil(total / limit)}`}
                            </span>
                            <button
                                onClick={handleNextPage}
                                disabled={dishes.length < limit}
                                style={{
                                    padding: "10px 20px",
                                    backgroundColor: dishes.length < limit ? "#f0f0f0" : "#1976d2",
                                    color: dishes.length < limit ? "#999" : "white",
                                    border: "none",
                                    borderRadius: 6,
                                    cursor: dishes.length < limit ? "not-allowed" : "pointer",
                                    fontWeight: 600,
                                }}
                            >
                                Вперед →
                            </button>
                        </div>
                    </>
                )}

                {selectedImage && (
                    <div
                        style={{
                            position: "fixed",
                            top: 0,
                            left: 0,
                            right: 0,
                            bottom: 0,
                            background: "rgba(0,0,0,0.9)",
                            display: "flex",
                            justifyContent: "center",
                            alignItems: "center",
                            zIndex: 1000,
                            cursor: "pointer"
                        }}
                        onClick={() => setSelectedImage(null)}
                    >
                        <img
                            src={selectedImage}
                            alt="Увеличенное фото"
                            style={{
                                maxWidth: "90%",
                                maxHeight: "90%",
                                borderRadius: 8,
                                boxShadow: "0 0 30px rgba(0,0,0,0.5)"
                            }}
                        />
                    </div>
                )}
            </div>
        </HelmetProvider>
    );
};

export default MenuPage;
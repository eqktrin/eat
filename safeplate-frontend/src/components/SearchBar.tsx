import React, { useEffect, useState, useCallback } from "react";
import { useSearchParams } from "react-router-dom";
import api from "../api/api";

interface Dish {
    id: number;
    name: string;
    description: string;
    allergens: string[];
    images?: { id: number; image_url: string }[];
}

interface UserProfile {
    id: number;
    email: string;
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

    const search = searchParams.get("search") || "";
    const category = searchParams.get("category") || "";
    const sortBy = searchParams.get("sortBy") || "name";
    const sortOrder = searchParams.get("sortOrder") || "asc";
    const skip = parseInt(searchParams.get("skip") || "0");
    const limit = parseInt(searchParams.get("limit") || "6");
    const showAll = searchParams.get("showAll") === "true";

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
            };
            
            const res = await api.get<Dish[]>("/menu/", { params });
            setDishes(res.data || []);
            
            const totalCount = parseInt(res.headers["x-total-count"] || "0");
            setTotal(totalCount || res.data.length + skip);
        } catch (err) {
            console.error("Ошибка при получении блюд:", err);
        }
        setLoading(false);
    }, [search, category, sortBy, sortOrder, skip, limit]);

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

    const displayedDishes = showAll 
        ? dishes 
        : dishes.filter(d => !d.allergens.some(a => userAllergens.includes(a)));

    const dangerousDishes = dishes.filter(d => 
        d.allergens.some(a => userAllergens.includes(a))
    );

    useEffect(() => {
        fetchUserAllergens();
    }, [fetchUserAllergens]);

    useEffect(() => {
        fetchDishes();
    }, [fetchDishes]);

    return (
        <div
            style={{
                padding: "40px 20px",
                maxWidth: 900,
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
                        <span style={{ marginLeft: 15, color: "#2e7d32" }}>✅ Безопасно: {dishes.length - dangerousDishes.length}</span>
                        <span style={{ marginLeft: 15, color: "#d32f2f" }}>⚠️ Опасно: {dangerousDishes.length}</span>
                        <span style={{ marginLeft: 15, color: "#555" }}>📊 Всего: {dishes.length}</span>
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
                        placeholder="🔍 Поиск по названию..."
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
            ) : displayedDishes.length === 0 ? (
                <p style={{ textAlign: "center", padding: 40, color: "#777" }}>Нет доступных блюд</p>
            ) : (
                <>
                    {displayedDishes.map((dish) => {
                        const isDangerous = dish.allergens.some(a => userAllergens.includes(a));
                        const hasAllergens = dish.allergens.length > 0;
                        
                        return (
                            <div
                                key={dish.id}
                                style={{
                                    border: isDangerous ? "2px solid #d32f2f" : 
                                           hasAllergens ? "1px solid #ffb74d" : "1px solid #e0e0e0",
                                    padding: 20,
                                    marginBottom: 20,
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
                                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                                    <h3 style={{ fontSize: 20, fontWeight: 600, marginBottom: 8, color: "#333" }}>
                                        {dish.name}
                                    </h3>
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

                                <div style={{ marginBottom: 15 }}>
                                    <strong>Аллергены:</strong>
                                    {dish.allergens.length > 0 ? (
                                        <div style={{ marginTop: 8, display: "flex", flexWrap: "wrap", gap: 8 }}>
                                            {dish.allergens.map((a) => {
                                                const isDanger = userAllergens.includes(a);
                                                return (
                                                    <span 
                                                        key={a} 
                                                        style={{
                                                            background: isDanger ? "#ffebee" : "#fff3e0",
                                                            color: isDanger ? "#d32f2f" : "#ef6c00",
                                                            padding: "4px 10px",
                                                            borderRadius: 4,
                                                            fontSize: 13,
                                                            fontWeight: 500,
                                                        }}
                                                    >
                                                        {a}
                                                    </span>
                                                );
                                            })}
                                        </div>
                                    ) : (
                                        <span style={{ color: "#777", fontStyle: "italic", marginLeft: 10 }}>Нет аллергенов</span>
                                    )}
                                </div>

                                {isDangerous && (
                                    <div style={{
                                        background: "#ffebee",
                                        color: "#d32f2f",
                                        padding: "10px 12px",
                                        borderRadius: 6,
                                        margin: "10px 0 15px 0",
                                        fontSize: 14,
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
                                            padding: "10px 16px",
                                            backgroundColor: isDangerous ? "#f5f5f5" : "#1976d2",
                                            color: isDangerous ? "#9e9e9e" : "#fff",
                                            border: "none",
                                            borderRadius: 8,
                                            cursor: isDangerous ? "not-allowed" : "pointer",
                                            fontWeight: 600,
                                            transition: "0.3s transform, 0.3s box-shadow",
                                            flex: 1
                                        }}
                                        onMouseEnter={(e) => {
                                            if (!isDangerous) {
                                                e.currentTarget.style.transform = "scale(1.05)";
                                                e.currentTarget.style.boxShadow = "0 6px 20px rgba(25,118,210,0.5)";
                                            }
                                        }}
                                        onMouseLeave={(e) => {
                                            if (!isDangerous) {
                                                e.currentTarget.style.transform = "scale(1)";
                                                e.currentTarget.style.boxShadow = "none";
                                            }
                                        }}
                                    >
                                        {isDangerous ? "Недоступно" : "Заказать"}
                                    </button>
                                    
                                    <button
                                        onClick={() => handleFavorite(dish)}
                                        style={{
                                            padding: "10px 16px",
                                            backgroundColor: "#fff",
                                            color: "#1976d2",
                                            border: "1px solid #1976d2",
                                            borderRadius: 8,
                                            cursor: "pointer",
                                            fontWeight: 600,
                                            transition: "0.3s transform, 0.3s box-shadow",
                                        }}
                                        onMouseEnter={(e) => {
                                            e.currentTarget.style.transform = "scale(1.05)";
                                            e.currentTarget.style.boxShadow = "0 6px 20px rgba(25,118,210,0.3)";
                                        }}
                                        onMouseLeave={(e) => {
                                            e.currentTarget.style.transform = "scale(1)";
                                            e.currentTarget.style.boxShadow = "none";
                                        }}
                                    >
                                        В избранное
                                    </button>
                                </div>
                            </div>
                        );
                    })}

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
                            disabled={displayedDishes.length < limit}
                            style={{
                                padding: "10px 20px",
                                backgroundColor: displayedDishes.length < limit ? "#f0f0f0" : "#1976d2",
                                color: displayedDishes.length < limit ? "#999" : "white",
                                border: "none",
                                borderRadius: 6,
                                cursor: displayedDishes.length < limit ? "not-allowed" : "pointer",
                                fontWeight: 600,
                            }}
                        >
                            Вперед →
                        </button>
                    </div>
                </>
            )}
        </div>
    );
};

export default MenuPage;
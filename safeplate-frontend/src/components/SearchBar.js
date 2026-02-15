import React from "react";

const SearchBar = ({ value, onChange, onSearch }) => {
  return (
    <div>
      <input
        type="text"
        placeholder="Введите запрос..."
        value={value}
        onChange={onChange}
        style={{ padding: "8px", width: "300px" }}
      />
      <button onClick={onSearch} style={{ padding: "8px 12px", marginLeft: "8px" }}>
        Найти
      </button>
    </div>
  );
};

export default SearchBar;

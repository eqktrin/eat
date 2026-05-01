import React from 'react';
import './AllergenWarning.css';

interface AllergenWarningProps {
    allergens: string[];
    userAllergens?: string[];
}

const AllergenWarning: React.FC<AllergenWarningProps> = ({ allergens, userAllergens = [] }) => {
    if (!allergens || allergens.length === 0) {
        return null;
    }

    const dangerousAllergens = allergens.filter(allergen => 
        userAllergens.includes(allergen)
    );
    
    const hasDanger = dangerousAllergens.length > 0;
    const hasWarning = allergens.length > 0 && !hasDanger;

    return (
        <div className={`allergen-warning ${hasDanger ? 'danger' : hasWarning ? 'warning' : 'safe'}`}>
            {hasDanger ? (
                <div className="danger-content">
                    <span className="danger-icon">⚠️</span>
                    <div className="danger-text">
                        <strong>Опасно!</strong>
                        <p>Содержит ваши аллергены: {dangerousAllergens.join(', ')}</p>
                    </div>
                </div>
            ) : hasWarning ? (
                <div className="warning-content">
                    <span className="warning-icon">ℹ️</span>
                    <div className="warning-text">
                        <strong>Аллергены:</strong>
                        <p>{allergens.join(', ')}</p>
                    </div>
                </div>
            ) : (
                <div className="safe-content">
                    <span className="safe-icon">✅</span>
                    <span className="safe-text">Безопасно</span>
                </div>
            )}
        </div>
    );
};

export default AllergenWarning;
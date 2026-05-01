import React, { useState } from 'react';
import api from '../api/api';

interface UploadResponse {
    id: number;
    url: string;
    file_name: string;
    file_size: number;
}

interface ImageUploadProps {
    dishId: number;
    onUploadComplete?: (data: UploadResponse) => void;
}

const ImageUpload: React.FC<ImageUploadProps> = ({ dishId, onUploadComplete }) => {
    const [uploading, setUploading] = useState<boolean>(false);
    const [error, setError] = useState<string>('');

    const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (!file) return;

        if (file.size > 5 * 1024 * 1024) {
            setError('Файл слишком большой. Максимум 5MB');
            return;
        }

        const allowedTypes = ['image/jpeg', 'image/png', 'image/gif', 'image/webp'];
        if (!allowedTypes.includes(file.type)) {
            setError('Неподдерживаемый формат. Используйте JPG, PNG, GIF или WEBP');
            return;
        }

        setUploading(true);
        setError('');

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await api.post<UploadResponse>(`/images/upload/${dishId}`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' }
            });
            
            if (onUploadComplete) {
                onUploadComplete(response.data);
            }
        } catch (err: any) {
            setError(err.response?.data?.detail || 'Ошибка загрузки');
        } finally {
            setUploading(false);
        }
    };

    return (
        <div style={{ marginTop: 10 }}>
            <input
                type="file"
                accept="image/jpeg,image/png,image/gif,image/webp"
                onChange={handleFileChange}
                disabled={uploading}
                style={{ marginRight: 10 }}
            />
            {uploading && <span>Загрузка...</span>}
            {error && <span style={{ color: 'red', marginLeft: 10 }}>{error}</span>}
        </div>
    );
};

export default ImageUpload;
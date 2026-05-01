// src/components/SEO.tsx
import React from "react";
import { Helmet } from "react-helmet-async";

interface SEOProps {
    title?: string;
    description?: string;
    keywords?: string;
    image?: string;
    url?: string;
    type?: string;
}

const SEO: React.FC<SEOProps> = ({ 
    title, 
    description, 
    keywords = "ресторан, меню, доставка еды",
    image = "/logo512.png",
    url,
    type = "website"
}) => {
    const siteTitle = "SafePlate — Ресторан здоровой еды";
    const fullTitle = title ? `${title} | ${siteTitle}` : siteTitle;
    const fullUrl = url ? `https://safeplate.ru${url}` : "https://safeplate.ru";

    return (
        <Helmet>
            <title>{fullTitle}</title>
            <meta name="description" content={description} />
            <meta name="keywords" content={keywords} />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            
            <link rel="canonical" href={fullUrl} />
            
            <meta name="robots" content="index, follow" />
            
            <meta property="og:type" content={type} />
            <meta property="og:title" content={fullTitle} />
            <meta property="og:description" content={description} />
            <meta property="og:image" content={image} />
            <meta property="og:url" content={fullUrl} />
            <meta property="og:site_name" content="SafePlate" />
            
            <meta name="twitter:card" content="summary_large_image" />
            <meta name="twitter:title" content={fullTitle} />
            <meta name="twitter:description" content={description} />
            <meta name="twitter:image" content={image} />
        </Helmet>
    );
};

export default SEO;
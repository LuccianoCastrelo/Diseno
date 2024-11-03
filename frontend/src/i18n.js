import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import en from './Idiomas/en.json';
import es from './Idiomas/es.json';

// Configuración inicial de i18n
i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: {
        translation: en
      },
      es: {
        translation: es
      }
    },
    lng: 'en', // Idioma inicial
    fallbackLng: 'es', // Idioma de respaldo
    interpolation: {
      escapeValue: false
    }
  });

export default i18n;

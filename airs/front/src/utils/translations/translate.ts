/* eslint @typescript-eslint/no-floating-promises:0 */
import type { TOptions } from "i18next";
import i18next, { t, use } from "i18next";
import { initReactI18next } from "react-i18next";

import { pageTexts } from "./en";
import { pageEsTexts } from "./es";

const isSpanish =
  typeof window === "undefined"
    ? false
    : window.location.pathname.startsWith("/es/");

use(initReactI18next).init({
  fallbackLng: "en",
  interpolation: {
    escapeValue: false,
  },
  lng: isSpanish ? "es" : "en",
  resources: {
    en: { translation: pageTexts },
    es: { translation: pageEsTexts },
  },
});

interface ITranslationFn {
  (key: string[] | string, options?: TOptions): string;
}

const translate: { t: ITranslationFn } = {
  t: (key: string[] | string, options?: TOptions): string => t(key, options),
};

export { i18next, translate };

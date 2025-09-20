import { appConfig } from "@shared/config";

const prefixKey = (key: string): string => `${appConfig.APP_NAME}:${key}`;

export const setLocalStorage = (key: string, value: string): void => {
  localStorage.setItem(prefixKey(key), value);
};

export const getLocalStorage = (key: string): string | null => localStorage.getItem(prefixKey(key));

export const deleteLocalStorage = (key: string): void => {
  localStorage.removeItem(prefixKey(key));
};

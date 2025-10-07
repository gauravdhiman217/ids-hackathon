import axios from "axios";
import { appConfig } from "@shared/config";
import { localKeys } from "@/shared/constants";
import { getLocalStorage, setLocalStorage, clearStorage } from "@/shared/utils";
import { Notification } from "@/shared/components/notifications";

const base = axios.create({
  baseURL: appConfig.API_BASE_URL,
  headers: {
    "Content-Type": "application/json"
  }
});

base.interceptors.request.use((config) => {
  const token = getLocalStorage(localKeys.access);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

base.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error?.response?.status === 401 && !originalRequest.isRetry) {
      const refreshToken = getLocalStorage(localKeys.refresh);

      if (refreshToken) {
        try {
          originalRequest.isRetry = true;

          const refreshResponse = await axios.post(`${appConfig.API_BASE_URL}/auth/refresh`, {
            refreshToken
          });

          const newAccessToken = refreshResponse?.data?.accessToken;
          if (newAccessToken) {
            setLocalStorage("access", newAccessToken);
            originalRequest.headers.Authorization = `Bearer ${newAccessToken}`;
            return base(originalRequest);
          }
        } catch (refreshError) {
          clearStorage();
          Notification.error("Session expired. Please log in again.");
        }
      }
    }

    const msg = error?.response?.data?.message
      || (error?.response?.status === 500
        ? "Internal Server Error"
        : "Something went wrong. Please try again.");
    Notification.error(msg);

    return Promise.reject(error);
  }
);

export { base }

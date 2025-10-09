import { base } from "@/shared/lib/base-axios";
import type { AxiosRequestConfig, AxiosResponse } from "axios";

interface FetchAPIParams {
  method?: AxiosRequestConfig["method"];
  url: string;
  queryParams?: Record<string, any>;
  bodyData?: Record<string, any> | FormData;
  headers?: Record<string, string>;
  responseType?: AxiosRequestConfig["responseType"];
}

export async function fetchAPI<T = any>({
  method = "GET",
  url,
  queryParams,
  bodyData,
  headers = {},
  responseType = "json"
}: FetchAPIParams): Promise<T | null> {
  try {
    const config: AxiosRequestConfig = {
      method,
      url,
      responseType,
      headers
    };
    if (queryParams) {
      const params: Record<string, any> = {};
      Object.entries(queryParams).forEach(([key, value]) => {
        if (value !== null && value !== undefined && value !== "") {
          params[key] = value;
        }
      });
      config.params = params;
    }
    if (bodyData) {
      if (bodyData instanceof FormData) {
        config.headers = config.headers || {};
        config.headers["Content-Type"] = "multipart/form-data";
        config.data = bodyData;
      } else {
        const payload: Record<string, any> = {};
        Object.entries(bodyData).forEach(([key, value]) => {
          if (typeof value === "string") { value = value.trim(); }
          if (value !== null && value !== undefined && value !== "") {
            payload[key] = value;
          }
        });
        config.data = payload;
      }
    }

    const response: AxiosResponse<T> = await base(config);
    return response.data;
  } catch (error) {
    return null;
  }
}

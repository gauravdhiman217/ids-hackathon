import type { Method } from "axios";

export type APIConfig = {
  [key: string]:
    | { url: string; method: Method }
    | ((...args: any[]) => { url: string; method: Method });
};

export interface UseDebouncedFetchResult<T> {
  loading: boolean;
  error: string | null;
  data: T | null;
}
export type FetchFunction<T> = (debouncedValue: string) => Promise<T>;

export type BodyData = FormData | Record<string, any>
export type QueryParams = Record<string, any>

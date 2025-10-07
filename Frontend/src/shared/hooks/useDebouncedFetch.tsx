import { useEffect, useState } from "react";
import type { FetchFunction, UseDebouncedFetchResult } from "../types";

export function useDebouncedFetch<T = any>(
  value: string,
  fetchFn: FetchFunction<T>,
  delay = 300
): UseDebouncedFetchResult<T> {
  const [debouncedValue, setDebouncedValue] = useState(value);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<T | null>(null);

  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(timer);
  }, [value, delay]);

  useEffect(() => {
    if (!debouncedValue) {
      setData(null);
      setLoading(false);
      return;
    }

    const run = async () => {
      setLoading(true);
      setError(null);

      try {
        const result = await fetchFn(debouncedValue);
        setData(result);
      } catch (err: any) {
        setError(err.message || "Unknown error");
      } finally {
        setLoading(false);
      }
    };

    run();
  }, [debouncedValue, fetchFn]);

  return { loading, error, data };
}

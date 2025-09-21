import type { Method } from "axios";

export type APIConfig = {
  [key: string]:
    | { url: string; method: Method } // Static endpoint
    | ((...args: any[]) => { url: string; method: Method }); // Dynamic endpoint
};

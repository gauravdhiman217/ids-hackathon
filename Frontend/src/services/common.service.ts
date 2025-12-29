import type { BodyData } from "@/shared/types";
import { COMMON, fetchAPI } from "@shared/api";

const CommonService = {
  GetUserProfile: async (username: string) => {
    const payload = {
      ...COMMON.GET_USER_PROFILE(username)
    };
    const res = await fetchAPI(payload);
    return res
  },
 
  Login: async ({ bodyData }: { bodyData: BodyData }) =>  {
    try {
        const payload = {
            ...COMMON.LOGIN,
            bodyData,
        };
        const res = await fetchAPI(payload);
        return res;
    } catch (error) {
        throw error;
    }
  },


  Register: async ({ bodyData }: { bodyData: BodyData }) => {
    try {
        const payload = {
            ...COMMON.REGISTER,
            bodyData,
        };
        const res = await fetchAPI(payload);
        return res;
    } catch (error) {
        throw error;
    }
  },

  GetDashboard: async ({ queryParams }: { queryParams?: Record<string, any> }) => {
    try {
        const payload = {
            ...COMMON.DASHBOARD,
            queryParams,
        };
        const res = await fetchAPI(payload);
        return res;
    } catch (error) {
        throw error;
    }
},

GetServices: async ({ queryParams }: { queryParams?: Record<string, any> }) => {
  try {
      const payload = {
          ...COMMON.SERVICES,
          queryParams,
      };
      const res = await fetchAPI(payload);
      return res;
  } catch (error) {
      throw error;
  }
},





};

export { CommonService };

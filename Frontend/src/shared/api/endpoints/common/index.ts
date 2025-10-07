import { defineAPIConfig } from "@/shared/utils"

const COMMON = defineAPIConfig({
  /**
   * COMMON endpoints
   */
  GET_USER_PROFILE: (username: string) => ({
    url: `/users/${username}`,
    method: "GET"
  }),

  LOGIN: {
    url: "/auth/login/",
    method: "POST"
  },

  REGISTER: {
    url: "/auth/signup/",
    method: "POST"
  },

  DASHBOARD: {
    url: "/dashboard/",
    method: "GET"
  },

  SERVICES: {
    url: "/services/",
    method: "GET"
  },

})

export { COMMON }

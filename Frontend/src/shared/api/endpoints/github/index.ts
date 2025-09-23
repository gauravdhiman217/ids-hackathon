import { defineAPIConfig } from "@/shared/utils"

const GITHUB = defineAPIConfig({
  /**
   * GITHUB endpoints
   */
  GET_USER_PROFILE: (username: string) => ({
    url: `/users/${username}`,
    method: "GET"
  })
})

export { GITHUB }

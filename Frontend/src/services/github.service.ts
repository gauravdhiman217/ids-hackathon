import { GITHUB, fetchAPI } from "@shared/api";

const GitHubService = {
  GetUserProfile: async (username: string) => {
    const payload = {
      ...GITHUB.GET_USER_PROFILE(username)
    };
    const res = await fetchAPI(payload);
    return res
  }
};

export { GitHubService };

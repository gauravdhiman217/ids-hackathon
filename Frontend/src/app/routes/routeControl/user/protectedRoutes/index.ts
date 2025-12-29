import { baseRoutes } from "@shared/constants";

const protectedRoutes = {
  TEAM_MANAGEMENT: {
    path: `${baseRoutes.userBaseRoutes}team`
  },
  DASHBOARD: {
    path: `${baseRoutes.userBaseRoutes}dashboard`
  }
};

export { protectedRoutes };

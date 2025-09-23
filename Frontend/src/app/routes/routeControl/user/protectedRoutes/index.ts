import { baseRoutes } from "@shared/constants";

const protectedRoutes = {
  EMAIL: {
    path: `${baseRoutes.userBaseRoutes}email`
  },
  DASHBOARD: {
    path: `${baseRoutes.userBaseRoutes}dashboard`
  }
};

export { protectedRoutes };

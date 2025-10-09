import { baseRoutes } from "@shared/constants";

const authRoutes = {
  LOGIN: {
    path: `${baseRoutes.userBaseRoutes}login`
  },
  INVITE: {
    path: `${baseRoutes.userBaseRoutes}invite`
  }
};

export { authRoutes };
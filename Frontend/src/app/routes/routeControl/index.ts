import { landingRoutes, authRoutes, protectedRoutes } from "./user";

const routesMap = {
  ...landingRoutes,
  ...authRoutes,
  ...protectedRoutes
};
export { routesMap };

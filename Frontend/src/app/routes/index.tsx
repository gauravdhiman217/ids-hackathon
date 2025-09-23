import { Suspense, lazy } from "react";
import { Spin } from "antd";
import { LoadingOutlined } from "@ant-design/icons";
import { NotFound } from "@shared/components/ui";
import { routesMap } from "./routeControl";

// layouts
const GuestLayout = lazy(() => import("@/app/layout/GuestLayout").then((m) => ({ default: m.GuestLayout })));
// const ProtectedLayout = lazy(() =>
//   import("@/app/layout/ProtectedLayout").then((m) => ({ default: m.ProtectedLayout }))
// );
// Pages
const LandingPage = lazy(() => import("@/pages").then((m) => ({ default: m.LandingPage })));

// const Login = lazy(() => import("@/pages/Login").then((m) => ({ default: m.Login })));
// const Invite = lazy(() =>
//   import("@/pages/Invite").then((m) => ({ default: m.Invite }))
// );
// const Dashboard = lazy(() =>
//   import("@/pages/Dashboard").then((m) => ({ default: m.Dashboard }))
// );
// const Email = lazy(() =>
//   import("@/pages/Email").then((m) => ({ default: m.Email }))
// );

const Loader = (
  <div className="flex justify-center items-center h-screen w-full">
    <Spin indicator={<LoadingOutlined style={{ fontSize: 80 }} spin />} />
  </div>
);

const routes = () => [
  {
    element: (
      <Suspense fallback={Loader}>
        <GuestLayout />
      </Suspense>
    ),
    children: [
      { path: routesMap.HOME.path, element: <LandingPage /> },
      { path: routesMap.LOGIN.path, element: <div>Login Page</div> },
      { path: routesMap.INVITE.path, element: <div>Invite Page</div> }
    ]
  },

  {
    element: (
      <Suspense fallback={Loader}>
        <div>Protected Layout</div>
      </Suspense>
    ),
    children: [
      { path: routesMap.DASHBOARD.path, element: <div>Dashboard Page</div> },
      { path: routesMap.EMAIL.path, element: <div>Email Page</div> }
    ]
  },
  { path: "*", element: <NotFound /> }
];

export { routes };

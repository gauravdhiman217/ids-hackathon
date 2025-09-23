import { Suspense, lazy } from "react";
import { Spin } from "antd";
import { LoadingOutlined } from "@ant-design/icons";
import { LandingPage } from "@/pages";
import { NotFound } from "@shared/components/ui";
import { routesMap } from "./routeControl";

const GuestLayout = lazy(() => import("../layout/GuestLayout")
  .then(m => ({ default: m.GuestLayout })));

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
      {
        path: routesMap.HOME.path,
        element: <LandingPage />
      }
    ]
  },
  {
    path: "*",
    element: <NotFound />
  }
];

export { routes };

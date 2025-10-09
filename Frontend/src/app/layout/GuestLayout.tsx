import { Outlet } from "react-router-dom";
import { VerticleLine } from "@/shared/components/ui";

function GuestLayout() {
  return (
    <div className="w-full flex min-h-[100vh] bg-[#f7f9fa] dark:bg-black">
      <VerticleLine />
      <div className="w-[calc(100vw-40px)]">
        <Outlet />
      </div>
      <VerticleLine />
    </div>
  );
}

export { GuestLayout }
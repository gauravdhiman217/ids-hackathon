import { Outlet } from "react-router-dom";
import { VerticleLine } from "@/shared/components/ui";

function GuestLayout() {
  return (
    <div className="w-full flex justify-between min-h-[100vh] bg-[#f7f9fa] dark:bg-black">
      <VerticleLine />
      <div className="container mx-auto p-2 md:p-8 pt-24">
        <Outlet />
      </div>
      <VerticleLine />
    </div>
  );
}

export { GuestLayout }
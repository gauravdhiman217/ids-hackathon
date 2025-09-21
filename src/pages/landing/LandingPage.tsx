import {
  Navbar,
  NavBody,
  MobileNav,
  NavbarLogo,
  MobileNavHeader,
  MobileNavToggle
} from "@shared/components/ui";
import { useState } from "react";
import { ThemeSwitcher } from "@/shared/components/ui/ThemeSwitch";

function Content() {
  return (
    <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
      {[
        { id: 1, title: "The", width: "md:col-span-1" },
        { id: 2, title: "First", width: "md:col-span-2" },
        { id: 3, title: "Rule", width: "md:col-span-1" },
        { id: 4, title: "Of", width: "md:col-span-3" },
        { id: 5, title: "F", width: "md:col-span-1" },
        { id: 6, title: "Club", width: "md:col-span-2" },
        { id: 7, title: "Is", width: "md:col-span-2" },
        { id: 8, title: "You", width: "md:col-span-1" },
        { id: 9, title: "Do NOT TALK about", width: "md:col-span-2" },
        { id: 10, title: "F Club", width: "md:col-span-1" }
      ].map((box) => (
        <div
          key={box.id}
          className={`${box.width} h-60 bg-neutral-100 dark:bg-neutral-800 flex items-center justify-center rounded-lg p-4 shadow-sm`}
        >
          <h2 className="text-xl font-medium text-zinc-500 dark:text-white">{box.title}</h2>
        </div>
      ))}
    </div>
  );
}

function LandingPage() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  return (
    <div className="relative w-full bg-gray-50 dark:bg-black">
      <Navbar>
        <NavBody>
          <NavbarLogo />
          <ThemeSwitcher />
        </NavBody>
        <MobileNav>
          <MobileNavHeader>
            <NavbarLogo />
            <MobileNavToggle
              isOpen={isMobileMenuOpen}
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            />
          </MobileNavHeader>
        </MobileNav>
      </Navbar>
      <Content />
    </div>
  );
}

export { LandingPage }

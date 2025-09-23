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
import { HeroSection } from "@/shared/components/ui/heroSection";

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
      <HeroSection />
    </div>
  );
}

export { LandingPage }

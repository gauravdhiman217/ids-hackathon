import { useState } from "react";
import { Link } from "react-router-dom"
import { HeroSection } from "./components/hero";
import {
  Navbar,
  NavBody,
  MobileNav,
  NavbarLogo,
  MobileNavHeader,
  MobileNavToggle
} from "./components/navbar";
import { TechStackSection } from "./components/techstack";
import { Features } from "./components/feature";
import { Footer } from "./components/footer";

function LandingPage() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  return (
    <div className="w-full">
      <div className="relative w-full mx-auto p-2 md:p-8 pt-24 bg-gray-50 dark:bg-black">
        <Navbar>
          <NavBody>
            <NavbarLogo />
            <Link
              to="/login"
              type="button"
              className="
                rounded-lg px-5 py-2 text-sm font-semibold
                border border-gray-400 text-gray-800
                hover:bg-gray-100
                dark:border-zinc-600 dark:text-zinc-100 dark:hover:bg-zinc-800
                transition-all duration-300"
            >
              Login
            </Link>
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
        <TechStackSection />
        <Features />
      </div>
      <Footer />
    </div>
  );
}

export { LandingPage };

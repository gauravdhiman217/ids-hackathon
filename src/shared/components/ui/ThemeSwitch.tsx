import { useEffect, useState } from "react";
import {
  DesktopOutlined,
  SunOutlined,
  MoonOutlined
} from "@ant-design/icons";
import { cn } from "@/shared/lib/cn";

function ThemeSwitcher() {
  const [theme, setTheme] = useState<"system" | "light" | "dark">("system");

  useEffect(() => {
    const saved = localStorage.getItem("theme") as "system" | "light" | "dark" | null;

    if (saved) { setTheme(saved); }
  }, []);

  const applyTheme = (newTheme: "system" | "light" | "dark") => {
    setTheme(newTheme);
    localStorage.setItem("theme", newTheme);

    if (newTheme === "light") {
      document.documentElement.classList.remove("dark");
    } else if (newTheme === "dark") {
      document.documentElement.classList.add("dark");
    } else {
      localStorage.removeItem("theme");
      if (window.matchMedia("(prefers-color-scheme: dark)").matches) {
        document.documentElement.classList.add("dark");
      } else {
        document.documentElement.classList.remove("dark");
      }
    }
  };

  const baseClasses = "flex h-10 items-center justify-center px-3 py-2 transition-colors";

  const getButtonClass = (btn: "system" | "light" | "dark") => cn(
    baseClasses,
    theme === btn
      ? "bg-zinc-200 text-zinc-900 dark:bg-zinc-800 dark:text-white"
      : "bg-white text-zinc-500 hover:text-zinc-900 hover:bg-zinc-100 dark:bg-zinc-900 dark:text-zinc-400 dark:hover:text-white dark:hover:bg-zinc-800"
  );

  return (
    <div className="grid grid-cols-3 w-[180px] overflow-hidden border border-zinc-300 dark:border-zinc-700 rounded-sm">
      <button type="button" onClick={() => applyTheme("system")} className={getButtonClass("system")} title="System theme">
        <DesktopOutlined />
        <span className="sr-only">System</span>
      </button>
      <button type="button" onClick={() => applyTheme("light")} className={getButtonClass("light")} title="Light theme">
        <SunOutlined />
        <span className="sr-only">Light</span>
      </button>
      <button type="button" onClick={() => applyTheme("dark")} className={getButtonClass("dark")} title="Dark theme">
        <MoonOutlined />
        <span className="sr-only">Dark</span>
      </button>
    </div>
  );
}

export { ThemeSwitcher }
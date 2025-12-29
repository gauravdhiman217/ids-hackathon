import React from "react";
import { cn } from "@shared/lib/cn";
import { ThemeSwitcher } from "@/shared/components/ui";

type FooterProps = React.ComponentProps<"footer"> & {
  children?: React.ReactNode;
};

interface LinksGroupProps {
  title: string;
  links: { title: string; href: string }[];
}

function LinksGroup({ title, links }: LinksGroupProps) {
  return (
    <div className="p-2">
      <h3 className="mt-2 mb-4 text-xs font-medium tracking-wider uppercase text-gray-700 dark:text-zinc-300">
        {title}
      </h3>
      <ul>
        {links.map((link) => (
          <li key={link.title}>
            <a
              href={link.href}
              className="text-xs text-gray-500 hover:text-gray-900 dark:text-zinc-400 dark:hover:text-white"
            >
              {link.title}
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}

export function Footer({ className, ...props }: Omit<FooterProps, "children">) {
  return (
    <footer
      className={cn(
        "border-t border-gray-200 dark:border-zinc-800",
        "bg-[radial-gradient(35%_128px_at_50%_0%,rgba(255,255,255,0.08),transparent)]",
        "dark:bg-[radial-gradient(35%_128px_at_50%_0%,rgba(0,0,0,0.3),transparent)]",
        className
      )}
      {...props}
    >
      <div className="relative mx-auto max-w-6xl">
        <div className="relative grid grid-cols-1 border-x border-gray-200 dark:border-zinc-800 md:grid-cols-4 md:divide-x md:divide-gray-200 dark:md:divide-zinc-800">
          <div>
            <LinksGroup
              title="About Us"
              links={[
                { title: "Pricing", href: "#" },
                { title: "Testimonials", href: "#" },
                { title: "FAQs", href: "#" },
                { title: "Contact Us", href: "#" },
                { title: "Blog", href: "#" }
              ]}
            />
          </div>
          <div>
            <LinksGroup
              title="Support"
              links={[
                { title: "Help Center", href: "#" },
                { title: "Terms", href: "#" },
                { title: "Privacy", href: "#" },
                { title: "Security", href: "#" },
                { title: "Cookie Policy", href: "#" }
              ]}
            />
          </div>
          <div>
            <LinksGroup
              title="Community"
              links={[
                { title: "Forum", href: "#" },
                { title: "Events", href: "#" },
                { title: "Partners", href: "#" },
                { title: "Affiliates", href: "#" },
                { title: "Career", href: "#" }
              ]}
            />
          </div>
          <div>
            <div className="p-2 w-full h-full">
              <h3 className="mt-2 mb-8 text-xs font-medium tracking-wider uppercase text-gray-700 dark:text-zinc-300">
                Theme
              </h3>
              <div className="flex justify-center items-end">
                <ThemeSwitcher />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="flex justify-center border-t border-gray-200 dark:border-zinc-800 p-3">
        <p className="text-xs text-gray-500 dark:text-zinc-400">
          Crafted with ꨄ︎ & caffeine by Prince
        </p>
      </div>
    </footer>
  );
}

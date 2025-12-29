import React, { useEffect, useState, useRef, useCallback } from "react";
import { cn } from "@shared/lib/cn";

function InfiniteMovingCards({
  items,
  direction = "left",
  speed = "fast",
  pauseOnHover = true,
  className
}: {
  items: { name: string; icon: React.ReactNode }[];
  direction?: "left" | "right";
  speed?: "fast" | "normal" | "slow";
  pauseOnHover?: boolean;
  className?: string;
}) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [start, setStart] = useState(false);

  const addAnimation = useCallback(() => {
    if (!containerRef.current) {
      return
    }

    containerRef.current.style.setProperty(
      "--animation-direction",
      direction === "left" ? "forwards" : "reverse"
    );

    // eslint-disable-next-line no-nested-ternary
    const duration = speed === "fast" ? "20s" : speed === "normal" ? "60s" : "100s";
    containerRef.current.style.setProperty("--animation-duration", duration);

    setStart(true);
  }, [direction, speed]);

  useEffect(() => {
    addAnimation();
  }, [items, addAnimation]);

  return (
    <div
      ref={containerRef}
      className={cn(
        "scroller relative z-20 max-w-8xl overflow-x-hidden",
        "[mask-image:linear-gradient(to_right,transparent,white_20%,white_80%,transparent)]",
        className
      )}
    >
      <ul
        className={cn(
          "flex w-max min-w-full shrink-0 flex-nowrap gap-4 py-4",
          start && "animate-scroll",
          pauseOnHover && "hover:[animation-play-state:paused]"
        )}
      >
        {[...items, ...items].map((item) => (
          <li
            key={item.name + Math.random()}
            className="flex items-center gap-4 max-w-full shrink-0 rounded-xl px-6 py-4"
          >
            <span className="text-4xl text-neutral-700 dark:text-neutral-200">
              {item.icon}
            </span>
            <span className="text-lg font-semibold text-neutral-600 dark:text-neutral-300 font-Aldrich">
              {item.name}
            </span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export { InfiniteMovingCards };

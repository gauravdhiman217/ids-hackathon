import type { ReactNode } from "react";
import { OpenAI, Dashboard, Team } from "@/assets/icons";
import { useTheme } from "@/shared/hooks/useTheme";
import { Card, CardContent, CardHeader } from "./featureCard";

function CardDecorator({ children }: { children: ReactNode }) {
  return (
    <div aria-hidden className="relative mx-auto size-36 [mask-image:radial-gradient(ellipse_50%_50%_at_50%_50%,#000_70%,transparent_100%)]">
      <div className="absolute inset-0 [--border:black] dark:[--border:white] bg-[linear-gradient(to_right,var(--border)_1px,transparent_1px),linear-gradient(to_bottom,var(--border)_1px,transparent_1px)] bg-[size:24px_24px] opacity-10" />
      <div className="absolute inset-0 m-auto flex size-12 items-center justify-center ">{children}</div>
    </div>
  )
}

export function Features() {
  const theme = useTheme()
  console.log("hook value", theme)
  const iconColor = theme === "dark" ? "#ffffff" : "#000000"
  console.log(iconColor)
  return (
    <section id="#feature" className="py-16 md:py-32 transition-colors duration-300">
      <div className="@container max-w-6xl m-auto ">
        {/* Section Title */}
        <div className="text-center">
          <h2 className="text-balance text-4xl font-semibold lg:text-5xl text-zinc-950 dark:text-zinc-100">
            Built to cover your needs
          </h2>
          <p className="mt-4 text-zinc-600 dark:text-zinc-400">
            Libero sapiente aliquam quibusdam aspernatur, praesentium iusto repellendus.
          </p>
        </div>
        {/* Feature Grid */}
        <div className="@min-4xl:max-w-full @min-4xl:grid-cols-3 mt-8 grid max-w-lg gap-10 *:text-center md:mt-16">
          {/* Card 1 */}
          <Card
            className="group transition-colors duration-300
            border border-zinc-200 dark:border-zinc-800
            bg-white dark:bg-zinc-950 shadow-sm hover:shadow-md"
          >
            <CardHeader className="pb-3">
              <CardDecorator>
                <OpenAI iconColor={iconColor} />
              </CardDecorator>
              <h3 className="mt-6 font-medium text-zinc-950 dark:text-zinc-100">
                AI-Powered Auto Replies
              </h3>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-zinc-600 dark:text-zinc-400">
                Automatically classify and
                respond to repetitive customer emails, freeing up time for critical tasks.
              </p>
            </CardContent>
          </Card>

          {/* Card 2 */}
          <Card
            className="group transition-colors duration-300
            border border-zinc-200 dark:border-zinc-800
            bg-white dark:bg-zinc-950 shadow-sm hover:shadow-md"
          >
            <CardHeader className="pb-3">
              <CardDecorator>
                <span>
                  <Dashboard iconColor={iconColor} />
                </span>
              </CardDecorator>
              <h3 className="mt-6 font-medium text-zinc-950 dark:text-zinc-100">
                Smart Dashboard & Analytics
              </h3>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-zinc-600 dark:text-zinc-400">
                Track incoming emails, auto-responses,
                and flagged queries with clear real-time insights.
              </p>
            </CardContent>
          </Card>

          {/* Card 3 */}
          <Card
            className="group transition-colors duration-300
            border border-zinc-200 dark:border-zinc-800
            bg-white dark:bg-zinc-950 shadow-sm hover:shadow-md"
          >
            <CardHeader className="pb-3">
              <CardDecorator>
                <span>
                  <Team iconColor={iconColor} />
                </span>
              </CardDecorator>
              <h3 className="mt-6 font-medium text-zinc-950 dark:text-zinc-100">
                L1 Team Oversight
              </h3>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-zinc-600 dark:text-zinc-400">
                Every auto-reply is visible to your L1 team for review,
                ensuring accuracy and giving humans control when needed.
              </p>
            </CardContent>
          </Card>
        </div>

      </div>
    </section>
  );
}

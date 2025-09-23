import { Button } from "antd"
import { DoubleRightOutlined, RightOutlined } from "@ant-design/icons"
import { AnimatedWrapper } from "@shared/components/ui/animated-group"
import { useTheme } from "@/shared/hooks/useTheme"

const transitionVariants = {
  item: {
    hidden: {
      opacity: 0,
      filter: "blur(12px)",
      y: 12
    },
    visible: {
      opacity: 1,
      filter: "blur(0px)",
      y: 0,
      transition: {
        type: "spring" as const,
        bounce: 0.3,
        duration: 1.5
      }
    }
  }
}

export function HeroSection() {
  const theme = useTheme()
  return (
    <main key={theme} className="overflow-hidden">
      <section>
        <div className="relative pt-24 md:pt-36">
          <AnimatedWrapper
            variants={{
              container: {
                visible: { transition: { delayChildren: 1 } }
              },
              item: {
                hidden: { opacity: 0, y: 20 },
                visible: {
                  opacity: 1,
                  y: 0,
                  transition: { type: "spring", bounce: 0.3, duration: 2 }
                }
              }
            }}
            className="absolute inset-0 -z-20"
          >
            <img
              src="https://ik.imagekit.io/lrigu76hy/tailark/night-background.jpg?updatedAt=1745733451120"
              alt="background"
              className="absolute inset-x-0 top-40 -z-20 hidden dark:block lg:top-32"
              width="3276"
              height="4095"
            />
            <img
              src="https://tailark.com/_next/image?url=%2Fmail2-light.png&w=3840&q=75" // will add our later
              alt="background"
              className="absolute inset-x-0 top-40 -z-20 block dark:hidden lg:top-32"
              width="3276"
              height="4095"
            />
          </AnimatedWrapper>
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <div className="text-center lg:text-left">
              <AnimatedWrapper variants={transitionVariants}>
                <div
                  className="group mx-auto flex w-fit items-center gap-4 rounded-full border
                    border-zinc-200 dark:border-zinc-800
                    bg-zinc-100 dark:bg-zinc-900
                    p-1 pl-4 shadow-md shadow-black/5 dark:shadow-zinc-950
                    hover:bg-white dark:hover:bg-zinc-800
                    transition-colors duration-300 ease-in-out"
                >
                  <span className="text-xs md:text-sm  text-zinc-800 dark:text-zinc-100">
                    Now with Auto Email Replies
                  </span>
                  <span className="block h-4 w-0.5 border-l text-zinc-200 dark:text-zinc-700 bg-white dark:bg-zinc-700" />
                  <div className="bg-white dark:bg-zinc-900 group-hover:bg-zinc-200 dark:group-hover:bg-zinc-800 size-6 overflow-hidden rounded-full duration-500">
                    <div className="flex w-12 -translate-x-1/2 duration-500 ease-in-out group-hover:translate-x-0">
                      <span className="flex size-6 text-zinc-900 dark:text-zinc-100 ml-0.5">
                        <DoubleRightOutlined className="m-auto size-3" />
                      </span>
                      <span className="flex size-6 text-zinc-900 dark:text-zinc-100 ml-0.5">
                        <DoubleRightOutlined className="m-auto size-3" />
                      </span>
                    </div>
                  </div>
                </div>
                <h1 className="mt-8 max-w-4xl mx-auto text-center text-balance text-4xl font-bold sm:text-5xl md:text-6xl lg:mt-16 xl:text-[5.25rem] dark:text-gray-50">
                  Modern Solutions for Smarter Support
                </h1>
                <p className="mx-auto text-center mt-6 max-w-[43rem] text-balance text-base sm:text-lg text-zinc-600 dark:text-zinc-300">
                  Our AI support platform classifies, prioritizes,
                  and replies to customer emails instantly.
                  Simple queries are auto-resolved,
                  while critical ones are flagged for human review.
                </p>
              </AnimatedWrapper>
              <AnimatedWrapper
                variants={{
                  container: {
                    visible: {
                      transition: { staggerChildren: 0.05, delayChildren: 0.75 }
                    }
                  },
                  ...transitionVariants
                }}
                className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row"
              >
                <Button size="large" className="h-11 rounded-xl px-5">
                  <a href="/dashboard" className="text-sm font-medium">
                    Launch Dashboard
                    {/* here will be adding get started is user not login then */}
                  </a>
                </Button>
              </AnimatedWrapper>
            </div>
          </div>
          <AnimatedWrapper
            variants={{
              container: {
                visible: {
                  transition: { staggerChildren: 0.05, delayChildren: 0.75 }
                }
              },
              ...transitionVariants
            }}
          >
            <div className="relative mt-10 sm:mt-16 md:mt-20 px-4 sm:px-6 lg:px-8">
              <div className="relative mx-auto max-w-6xl overflow-hidden rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 p-2 shadow-lg shadow-zinc-950/15">
                <img
                  className="hidden dark:block aspect-video rounded-2xl"
                  src="https://tailark.com/_next/image?url=%2Fmail2.png&w=3840&q=75"
                  alt="app screen dark"
                  width="2700"
                  height="1440"
                />
                <img
                  className="block dark:hidden aspect-video rounded-2xl"
                  src="https://tailark.com/_next/image?url=%2Fmail2-light.png&w=3840&q=75"
                  alt="app screen light"
                  width="2700"
                  height="1440"
                />
              </div>
            </div>
          </AnimatedWrapper>
        </div>
      </section>
      <section className="bg-white dark:bg-zinc-950 pb-16 pt-16 md:pb-32">
        <div className="group relative m-auto max-w-5xl px-4 sm:px-6 lg:px-8">
          <div className="absolute inset-0 z-10 flex scale-95 items-center justify-center opacity-0 transition duration-500 group-hover:scale-100 group-hover:opacity-100">
            <a
              href="/"
              className="flex items-center gap-1 text-sm text-zinc-700 dark:text-zinc-300 hover:opacity-75"
            >
              <span>Meet Our Customers</span>
              <RightOutlined className="size-3" />
            </a>
          </div>
          <div className="mx-auto mt-12 grid max-w-2xl grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-x-8 gap-y-8 transition-all duration-500 group-hover:opacity-50 group-hover:blur-xs sm:gap-x-12 sm:gap-y-12">
            {[
              "nvidia",
              "column",
              "github",
              "nike",
              "lemonsqueezy",
              "laravel",
              "lilly",
              "openai"
            ].map((logo) => (
              <div key={logo} className="flex">
                <img
                  className="mx-auto h-6 w-fit dark:invert"
                  src={`https://html.tailus.io/blocks/customers/${logo}.svg`}
                  alt={`${logo} logo`}
                  height="24"
                  width="auto"
                />
              </div>
            ))}
          </div>
        </div>
      </section>
    </main>
  )
}

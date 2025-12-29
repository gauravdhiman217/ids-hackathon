import { Button } from "antd";
import { DoubleRightOutlined } from "@ant-design/icons";
import { AnimatedWrapper } from "@/shared/components/wrappers/animatedWrapper";
import { useTheme } from "@/shared/hooks/useTheme";
import { Link } from "react-router-dom";
import { springTransitionVariants } from "@/shared/constants/animationTransition";
import { FollowerPointerCard } from "./followingPointer";

export function HeroSection() {
  const theme = useTheme();
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
              <AnimatedWrapper variants={springTransitionVariants}>
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
                  <div className="bg-white dark:bg-zinc-900 group-hover:bg-zinc-200 dark:group-hover:bg-zinc-800 size-6 overflow-x-hidden rounded-full duration-500">
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
                  Our AI support platform classifies, prioritizes, and replies
                  to customer emails instantly. Simple queries are
                  auto-resolved, while critical ones are flagged for human
                  review.
                </p>
              </AnimatedWrapper>
              <AnimatedWrapper
                variants={{
                  container: {
                    visible: {
                      transition: {
                        staggerChildren: 0.05,
                        delayChildren: 0.75
                      }
                    }
                  },
                  ...springTransitionVariants
                }}
                className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row cta-section"
              >
                <Button size="large" className="h-11 rounded-xl px-5">
                  <Link to="/dashboard" className="text-sm font-medium">
                    Launch Dashboard
                    {/* here will be adding get started is user not login then */}
                  </Link>
                </Button>
                {/* <Button size="large" className="h-11 rounded-xl px-5">
                  <button
                    type="button"
                    onClick={(e) => {
                      e.preventDefault();
                      document
                        .getElementById("feature")
                        ?.scrollIntoView({ behavior: "smooth" });
                    }}
                    className="text-sm font-medium"
                  >
                    Learn more
                  </button>
                </Button> */}
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
              ...springTransitionVariants
            }}
          >
            <div className="relative mt-10 sm:mt-16 md:mt-20 px-4 sm:px-6 lg:px-8">
              <div className="relative mx-auto max-w-6xl overflow-x-hidden rounded-2xl border border-zinc-200 dark:border-zinc-800 bg-white dark:bg-zinc-900 p-2 shadow-lg shadow-zinc-950/15">
                <FollowerPointerCard>
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
                </FollowerPointerCard>
              </div>
            </div>
          </AnimatedWrapper>
        </div>
      </section>
    </main>
  );
}

import {
  CloudServerOutlined,
  DatabaseOutlined,
  ApiOutlined,
  CodeOutlined,
  BranchesOutlined
} from "@ant-design/icons";
import { useTheme } from "@/shared/hooks/useTheme";
import { AnimatedWrapper } from "../../../../shared/components/wrappers/animatedWrapper";
import { InfiniteMovingCards } from "./movingcards";

function TechStackSection() {
  const theme = useTheme()
  const techStack = [
    { name: "React", icon: <CodeOutlined /> },
    { name: "Redux", icon: <BranchesOutlined /> },
    { name: "TailwindCSS", icon: <ApiOutlined /> },
    { name: "Ant Design", icon: <CloudServerOutlined /> },
    { name: "PostgreSQL", icon: <DatabaseOutlined /> }
  ];

  return (
    <section key={theme} className="w-full overflow-x-hidden my-16 flex flex-col items-center justify-center">
      {/* Heading with animation */}
      <AnimatedWrapper
        preset="fade"
        className="mb-6"
        variants={{
          container: { visible: { transition: { delayChildren: 0.5 } } }
        }}
      >
        <div>
          <h2 className="text-lg md:text-xl font-bold text-gray-900 dark:text-gray-100">
            Powered by Modern Tech
          </h2>
        </div>
      </AnimatedWrapper>

      {/* Marquee with zoom animation */}
      <AnimatedWrapper
        preset="zoom"
        className="w-full md:w-[70%]"
        variants={{
          container: { visible: { transition: { delayChildren: 0.4 } } },
          item: {
            hidden: { opacity: 0, scale: 0.7 },
            visible: {
              opacity: 1,
              scale: 1,
              transition: { type: "spring", stiffness: 200, damping: 18 }
            }
          }
        }}
      >
        <div>
          <InfiniteMovingCards items={techStack} speed="normal" />
        </div>
      </AnimatedWrapper>
    </section>
  );
}

export { TechStackSection };

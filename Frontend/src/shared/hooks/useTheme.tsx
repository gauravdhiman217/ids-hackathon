import { useEffect, useState } from "react"

export function useTheme(): string | undefined {
  const [theme, setTheme] = useState<string | undefined>("light")

  useEffect(() => {
    const observer = new MutationObserver(() => {
      const isDark = document.documentElement.classList.contains("dark")
      console.log(isDark)
      setTheme(isDark ? "dark" : "light")
    })

    observer.observe(document.documentElement, {
      attributes: true,
      attributeFilter: ["class"]
    })

    return () => observer.disconnect()
  }, [])

  return theme
}

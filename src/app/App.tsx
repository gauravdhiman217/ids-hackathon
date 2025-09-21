import { useState } from "react"
import { appConfig } from "@/shared/config"
import "../global.css"
import { ToastContainer } from "react-toastify"
import { Notification } from "@/shared/components/notifications"
// import { GitHubService } from "@/services"

function App() {
  const [count, setCount] = useState(0)

  // useEffect(() => {
  //   (async function () {
  //     const res = await GitHubService.GetUserProfile("prince")
  //     console.log(res)
  //   }())
  // }, [])

  return (
    <>
      <ToastContainer />
      <div>
        <a href="https://react.dev" target="_blank" rel="noreferrer">
          {appConfig.APP_NAME}
          ,
          {" "}
          {appConfig.NODE_ENV}
          ,
          {" "}
          {appConfig.API_BASE_URL}
          {" "}
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button
          type="button"
          onClick={() => {
            setCount(
              (prev) => prev + 1
            )
            Notification.success("Hellw i am prince here check")
          }}
        >
          count is
          {count}
        </button>
        <p>
          Edit
          <code>src/App.tsx</code>
          and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export { App }

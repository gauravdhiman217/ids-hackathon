import { ToastContainer } from "react-toastify";
import { RouterProvider, createBrowserRouter } from "react-router-dom";
import { routes } from "./routes";
import "react-toastify/dist/ReactToastify.css";
import "../global.css";

const router = createBrowserRouter(routes());

function App() {
  return (
    <>
      <ToastContainer />
      <RouterProvider router={router} />
    </>
  );
}

export { App };

import { toast } from "react-toastify"

// A simple wrapper around react-toastify to show toast notifications.
// Use this instead of calling toast.success or toast.error directly.
// Makes it easier to manage and customize notifications later if needed.
//
// Example:
//   Notification.success("Profile updated successfully");
//   Notification.error("Something went wrong");

const Notification = {
  error: (message : string) => toast.error(message),
  success: (message: string) => toast.success(message),
  info: (message:string) => toast.info(message),
  warn: (message:string) => toast.warn(message)
}

export { Notification }
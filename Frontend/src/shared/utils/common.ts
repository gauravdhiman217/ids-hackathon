import { Notification } from "../components/notifications";

export function handleSocketError(err: any) {
  Notification.error(err.message);
  return err;
}

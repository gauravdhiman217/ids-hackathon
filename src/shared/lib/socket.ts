import { io, Socket } from "socket.io-client";
import { appConfig } from "@shared/config";
import { handleSocketError } from "@shared/utils";

let socket: Socket | null = null;

/**
 * Initializes the WebSocket connection using Socket.IO.
 *
 * - Reuses the existing connection if already initialized.
 * - Sets up reconnect strategies and token-based authentication.
 * - Adds error handling for failed connections.
 *
 * @param token - Auth token for socket authentication
 * @returns A connected Socket instance
 *
 * @example
 * const socket = initSocket("user-access-token");
 * socket.emit("join-room", roomId);
 */
export function initSocket(token: string): Socket {
  if (!socket) {
    socket = io(appConfig.SOCKET_BASE_URL, {
      transports: ["websocket"], // Prefer WebSocket over polling
      auth: { token }, // Token-based authentication
      reconnection: true, // Enable auto-reconnect
      reconnectionAttempts: 5, // Retry max 5 times
      reconnectionDelay: 2000, // Wait 2s between retries
    });

    socket.on("connect_error", (err: any) => {
      handleSocketError(err);
    });
  }

  return socket;
}

/**
 * Returns the initialized socket instance.
 * Throws an error if socket is not yet connected.
 *
 * @returns The Socket instance
 *
 * @example
 * const socket = getSocket();
 * socket.emit("send-message", { text: "Hello" });
 */
export function getSocket(): Socket {
  if (!socket) throw new Error("Socket not initialized");
  return socket;
}

/**
 * Gracefully disconnects and clears the socket instance.
 * Useful when logging out or switching accounts.
 *
 * @example
 * closeSocket(); // Disconnect and clean up
 */
export function closeSocket() {
  if (socket) {
    socket.removeAllListeners(); // Prevent memory leaks
    socket.disconnect();         // Close the connection
    socket = null;
  }
}

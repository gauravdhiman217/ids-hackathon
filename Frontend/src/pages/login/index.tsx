import { useState } from "react";
import { Form, Input, Button, Checkbox, message } from "antd";
import { LockOutlined, UserOutlined } from "@ant-design/icons";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { useTheme } from "@/shared/hooks/useTheme";
import { cn } from "@shared/lib/cn";
import { CommonService } from "@/services";

export default function AdminLogin() {
  const theme = useTheme();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const handleLogin = async (values: { email: string; password: string }) => {
    setLoading(true);
    try {
      const response = await CommonService.Login({
        bodyData: values,
      });

      const isSuccess = response?.status_code === 200;

      if (isSuccess) {
        message.success(response?.message || "Login successful");
        navigate("/dashboard");
      } else {
        message.error(response?.message || "Login failed");
      }

      return response;
    } catch (error: any) {
      message.error(error?.message || "Something went wrong during login");
      throw error;
    } finally {
      setLoading(false);
    }
  };

  return (
    <section
      key={theme}
      className={cn(
        "flex min-h-screen items-center justify-center bg-zinc-50 dark:bg-zinc-950 transition-colors duration-300 px-4 login-page"
      )}
    >
      <motion.div
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ type: "spring", stiffness: 120, damping: 20 }}
        className={cn(
          "relative w-full max-w-md rounded-sm p-8 border border-zinc-200 dark:border-zinc-800 bg-white/70 dark:bg-neutral-950/70 backdrop-blur-md shadow-[0_0_24px_rgba(34,42,53,0.06),_0_1px_1px_rgba(0,0,0,0.05),_0_0_0_1px_rgba(34,42,53,0.04),_0_0_4px_rgba(34,42,53,0.08),_0_16px_68px_rgba(47,48,55,0.05)]"
        )}
      >
        <div className="flex flex-col items-center text-center">
          <div className="relative mx-auto size-20">
            <div
              className="absolute inset-0 [--border:black] dark:[--border:white] 
              bg-[linear-gradient(to_right,var(--border)_1px,transparent_1px),
              linear-gradient(to_bottom,var(--border)_1px,transparent_1px)]
              bg-[size:24px_24px] opacity-10"
            />
            <div className="absolute inset-0 flex items-center justify-center w-full">
              <span className="mt-1 text-3xl text-black dark:text-white">
                AssistEdge
              </span>
            </div>
          </div>
          <p className="text-sm text-zinc-600 dark:text-zinc-400">
            Sign in to access your dashboard
          </p>
        </div>

       
        <Form
          name="admin_login"
          layout="vertical"
          className="mt-8"
          onFinish={handleLogin}
        >
          <Form.Item
            name="email"
            label={<span className="text-zinc-900 dark:text-white">Email</span>}
            className="text-white"
            rules={[
              { required: true, message: "Please enter your email" },
              { type: "email", message: "Please enter a valid email" },
            ]}
          >
            <Input
              size="large"
              prefix={<UserOutlined className="text-zinc-400" />}
              placeholder="Email Address"
              className="rounded-lg bg-zinc-50 dark:bg-zinc-900 border-zinc-300 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100"
            />
          </Form.Item>

          <Form.Item
            name="password"
            label={<span className="text-zinc-900 dark:text-white">Password</span>}
            rules={[{ required: true, message: "Please enter your password" }]}
          >
            <Input.Password
              size="large"
              prefix={<LockOutlined className="text-zinc-400" />}
              placeholder="Password"
              className="rounded-lg bg-zinc-50 dark:bg-zinc-900 border-zinc-300 dark:border-zinc-700 text-zinc-900 dark:text-zinc-100"
            />
          </Form.Item>

          <div className="flex items-center justify-between mb-4">
            <Form.Item name="remember" valuePropName="checked" noStyle>
              <Checkbox className="text-zinc-400 dark:text-zinc-400">
                <span className="text-zinc-400 hover:underline text-sm">
                  Remember me
                </span>
              </Checkbox>
            </Form.Item>
            <a href="#" className="text-zinc-400 hover:underline text-sm">
              Forgot password?
            </a>
          </div>

          <Form.Item>
            <Button
              type="primary"
              htmlType="submit"
              block
              size="large"
              loading={loading}
              className="mt-2 rounded-lg font-medium"
            >
              Sign In
            </Button>
          </Form.Item>
        </Form>

        <p className="mt-6 text-xs text-center text-zinc-500 dark:text-zinc-400">
          © {new Date().getFullYear()} AssistEdge Admin. All rights reserved.
        </p>
      </motion.div>
    </section>
  );
}

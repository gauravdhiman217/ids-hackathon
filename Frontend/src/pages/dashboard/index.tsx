import {
  ApiOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  TeamOutlined,
  TrophyOutlined,
  UserOutlined,
} from "@ant-design/icons";
import { Avatar, Badge, message, Progress, Table } from "antd";
import {
  Card,
  CardHeader,
} from "@/pages/landing/components/feature/featureCard";
import { useEffect, useState } from "react";
import { CommonService } from "@/services";

function StatDecorator({ children }: { children: React.ReactNode }) {
  return (
    <div
      aria-hidden
      className="relative mx-auto size-16 [mask-image:radial-gradient(ellipse_50%_50%_at_50%_50%,#000_70%,transparent_100%)]"
    >
      <div className="absolute inset-0 [--border:rgba(255,255,255,0.1)] bg-[linear-gradient(to_right,var(--border)_1px,transparent_1px),linear-gradient(to_bottom,var(--border)_1px,transparent_1px)] bg-[size:12px_12px] opacity-20" />
      <div className="absolute inset-0 m-auto flex size-12 items-center justify-center bg-zinc-900/50 rounded-xl backdrop-blur-sm border border-zinc-800/50">
        {children}
      </div>
    </div>
  );
}

export default function Dashboard() {
  const [dashboardData, setDashboardData] = useState<any>(null);
  const [servicesData, setServicesData] = useState<any>(null);


  const fetchDashboard = async () => {
    try {
      const response = await CommonService.GetDashboard({});

      if (response?.status_code === 200) {
        setDashboardData(response?.data);
      } else {
        message.error(response?.message || "Failed to fetch dashboard");
      }
    } catch (error: any) {
      message.error(
        error?.message || "Something went wrong while fetching dashboard"
      );
    } finally {
    }
  };

  const fetchServices = async () => {
    try {
      const response = await CommonService.GetServices({});
      if (response?.status_code === 200) {
        setServicesData(response?.data);
      } else {
        message.error(response?.message || "Failed to fetch dashboard");
      }
    } catch (error: any) {
      message.error(
        error?.message || "Something went wrong while fetching dashboard"
      );
    } finally {
    }
  };

  useEffect(() => {
    fetchDashboard();
    fetchServices();
  }, []);

  const stats = [
    {
      title: "Total Users",
      value: dashboardData?.total_users ?? 0,
      icon: <UserOutlined className="text-xl text-blue-400" />,
    },
    {
      title: "Total Tickets",
      value: dashboardData?.total_tickets ?? 0,
      icon: <ClockCircleOutlined className="text-xl text-yellow-400" />,
    },
    {
      title: "Total Open Tickets",
      value: dashboardData?.total_open_tickets ?? 0,
      icon: <UserOutlined className="text-xl text-purple-400" />,
    },
    {
      title: "Total Closed Tickets",
      value: dashboardData?.total_closed_tickets ?? 0,
      icon: <TeamOutlined className="text-xl text-green-400" />,
    },

    {
      title: "Tasks Today",
      value: dashboardData?.tasks_today ?? 0,
      icon: <ClockCircleOutlined className="text-xl text-orange-400" />,
    },
  ];

  const topServices = dashboardData?.top_5_services || [];
  const maxTickets = Math.max(
    ...topServices.map((s: any) => s.ticket_count),
    1
  );

  const topAgents = dashboardData?.top_5_agents || [];

  const activityColumns = [
    {
      title: "Service Id",
      dataIndex: "service_id",
      key: "service_id",
    },
    {
      title: "Service Name",
      dataIndex: "service_name",
      key: "service_name",
    },
    {
      title: "SLA Id",
      dataIndex: "sla_id",
      key: "sla_id",
    },
    {
      title: "SLA Name",
      dataIndex: "sla_name",
      key: "sla_name",
    },
    {
      title: "First Response Time",
      dataIndex: "first_response_time",
      key: "first_response_time",
    },
    {
      title: "Update Time",
      dataIndex: "update_time",
      key: "update_time",
    },
    {
      title: "Solution Time",
      dataIndex: "solution_time",
      key: "solution_time",
    },
    // {
    //   title: "is_valid",
    //   dataIndex: "is_valid",
    //   key: "is_valid",
    // },
   
  ];


  return (
    <div className="min-h-screen p-8 bg-zinc-950 text-zinc-400 transition-colors duration-300">
      <div className="mb-12">
        <h1 className="text-4xl font-semibold text-zinc-400 mb-2">Dashboard</h1>
        <p className="text-zinc-400">
          Welcome back! Here's what's happening today.
        </p>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6 mb-12">
        {stats.map((stat) => (
          <Card
            key={stat?.title}
            className="group transition-colors duration-300
            border border-zinc-200 dark:border-zinc-800
            bg-white dark:bg-zinc-950 shadow-sm hover:shadow-md cursor-pointer"
          >
            <CardHeader className="pb-4 text-center">
              <span className="text-black dark:text-white text-3xl">
                {stat?.icon}
              </span>

              <h3 className="mt-4 font-medium text-zinc-950 dark:text-zinc-100">
                {stat?.title}
              </h3>

              <div className="flex items-center justify-center gap-2 mt-2">
                <p className="text-2xl font-bold text-zinc-950 dark:text-zinc-100">
                  {stat?.value}
                </p>
              </div>
            </CardHeader>
          </Card>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
        <Card
          className="border border-zinc-800 bg-zinc-950 shadow-sm hover:shadow-lg hover:shadow-zinc-900/20 transition-all duration-300"
          style={{ padding: "32px" }}
        >
          <div className="mb-6">
            <h3 className="text-xl font-semibold text-zinc-400 mb-2 flex items-center gap-2">
              <ApiOutlined className="text-green-400" />
              Top Services
            </h3>
            <p className="text-sm text-zinc-400">Services with most tickets</p>
          </div>

          <div className="space-y-6">
            {topServices.map((service: any, index: number) => (
              <div key={index}>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm font-medium text-zinc-400">
                    {service.service_name}
                  </span>
                  <Badge
                    color="white"
                    text={
                      <span className="text-xs text-zinc-400">
                        {service.ticket_count} ticket
                        {service.ticket_count > 1 ? "s" : ""}
                      </span>
                    }
                  />
                </div>
                <Progress
                  percent={Math.round(
                    (service.ticket_count / maxTickets) * 100
                  )}
                  strokeColor="#fff"
                  trailColor="rgba(63, 63, 70, 0.3)"
                  size="small"
                />
              </div>
            ))}
          </div>
        </Card>

        <Card
          className="border border-zinc-800 bg-zinc-950 shadow-sm hover:shadow-lg hover:shadow-zinc-900/20 transition-all duration-300"
          style={{ padding: "32px" }}
        >
          <div className="mb-6">
            <h3 className="text-xl font-semibold text-zinc-400 mb-2 flex items-center gap-2">
              <TrophyOutlined className="text-yellow-400" />
              Top Agents
            </h3>
            <p className="text-sm text-zinc-400">Agents with most tickets</p>
          </div>

          <div className="space-y-4">
            {topAgents.map((agent: any, index: number) => (
              <div
                key={index}
                className="flex items-center justify-between p-4 bg-zinc-900/30 rounded-lg"
              >
                <div className="flex items-center gap-3">
                  <Avatar
                    style={{ backgroundColor: "#fff", color: "#000" }}
                    className="flex items-center justify-center"
                  >
                    {agent.agent_name
                      .split(" ")
                      .map((n: any) => n[0])
                      .join("")}
                  </Avatar>
                  <div>
                    <p className="text-sm font-medium text-zinc-600">
                      {agent.agent_name}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-lg font-bold text-zinc-600">
                    {agent.ticket_count}
                  </p>
                  <p className="text-xs text-zinc-400">Ticket Count</p>
                </div>
              </div>
            ))}
          </div>
        </Card>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
        {[
          {
            icon: <UserOutlined className="text-3xl text-blue-400" />,
            label: "Manage Users",
            description: "Add, edit, and manage user accounts",
          },
          {
            icon: <TeamOutlined className="text-3xl text-green-400" />,
            label: "Manage Teams",
            description: "Organize teams and assign roles",
          },
          {
            icon: <CheckCircleOutlined className="text-3xl text-emerald-400" />,
            label: "Completed Tasks",
            description: "View finished work and achievements",
          },
          {
            icon: <ClockCircleOutlined className="text-3xl text-yellow-400" />,
            label: "Pending Tasks",
            description: "Track outstanding items and deadlines",
          },
        ].map((feature) => (
          <Card
            key={feature.label}
            className="group relative overflow-hidden transition-all duration-300 
              border border-zinc-800 bg-zinc-950 shadow-sm hover:shadow-lg 
              hover:shadow-zinc-900/20 hover:border-zinc-700/50 cursor-pointer"
            style={{ padding: "32px" }}
          >
            <div className="text-center space-y-4">
              <StatDecorator>{feature.icon}</StatDecorator>

              <div>
                <h4 className="font-semibold text-zinc-400 mb-2">
                  {feature.label}
                </h4>
                <p className="text-sm text-zinc-400 leading-relaxed">
                  {feature.description}
                </p>
              </div>
            </div>
          </Card>
        ))}
      </div>

      <Card
        className="border border-zinc-800 bg-zinc-950 shadow-sm hover:shadow-lg 
          hover:shadow-zinc-900/20 transition-all duration-300"
        style={{ padding: "32px" }}
      >
        <div className="mb-6">
          <h3 className="text-xl font-semibold text-zinc-400 mb-2">
            Services
          </h3>
          <p className="text-sm text-zinc-400">
            Latest user and system services
          </p>
        </div>
        <Table
          columns={activityColumns}
          dataSource={servicesData}
          pagination={false}
          className="
            [&_.ant-table]:!bg-zinc-950 
            [&_.ant-table-thead_.ant-table-cell]:!bg-zinc-900 
            [&_.ant-table-thead_.ant-table-cell]:!border-zinc-800 
            [&_.ant-table-thead_.ant-table-cell]:!text-zinc-400
            [&_.ant-table-tbody_.ant-table-cell]:!bg-zinc-950 
            [&_.ant-table-tbody_.ant-table-cell]:!border-zinc-800
            [&_.ant-table-tbody_.ant-table-cell]:!text-zinc-400
            [&_.ant-table-tbody_.ant-table-row:hover_.ant-table-cell]:!bg-zinc-900/50
            [&_.ant-table-tbody_.ant-table-row:hover_.ant-table-cell]:!text-zinc-400
          "
        />
      </Card>
    </div>
  );
}

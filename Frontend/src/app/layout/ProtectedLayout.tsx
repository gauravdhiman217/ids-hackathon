import { Outlet, useNavigate, useLocation } from "react-router-dom";
import { Avatar, Dropdown, Badge, Button, Tooltip } from "antd";
import {
  UserOutlined,
  LogoutOutlined,
  BellOutlined,
  DashboardOutlined,
  SettingOutlined,
  TeamOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  SearchOutlined,
  HomeOutlined,
  FileTextOutlined,
  BarChartOutlined,
  SafetyCertificateOutlined,
  CustomerServiceOutlined,
  MailOutlined,
  CalendarOutlined,
} from "@ant-design/icons";
import { useState } from "react";

function ProtectedLayout() {
  const navigate = useNavigate();
  const location = useLocation();
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);

  const handleMenuClick = (key: string) => {
    if (key === "logout") navigate("/login");
    if (key === "profile") navigate("/profile");
  };

  const userMenu = (
    <div className="flex flex-col bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 rounded-lg overflow-hidden shadow-lg min-w-48">
      <div className="px-4 py-3 border-b border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-800/50">
        <p className="text-sm font-medium text-zinc-900 dark:text-zinc-100">Admin User</p>
        <p className="text-xs text-zinc-500 dark:text-zinc-400">admin@company.com</p>
      </div>
      <button
        onClick={() => handleMenuClick("profile")}
        className="flex items-center gap-3 px-4 py-3 text-zinc-700 dark:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-zinc-800 transition-colors text-left"
      >
        <UserOutlined />
        <span>View Profile</span>
      </button>
      <button
        onClick={() => handleMenuClick("logout")}
        className="flex items-center gap-3 px-4 py-3 text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors text-left"
      >
        <LogoutOutlined />
        <span>Sign Out</span>
      </button>
    </div>
  );

  const menuItems = [
    { 
      label: "Dashboard", 
      icon: <DashboardOutlined />, 
      path: "/dashboard",
      category: "main"
    },
    { 
      label: "Analytics", 
      icon: <BarChartOutlined />, 
      path: "/analytics",
      category: "main"
    },
    { 
      label: "Team Management", 
      icon: <TeamOutlined />, 
      path: "/teams",
      category: "management"
    },
    { 
      label: "User Management", 
      icon: <UserOutlined />, 
      path: "/users",
      category: "management"
    },
    { 
      label: "Projects", 
      icon: <FileTextOutlined />, 
      path: "/projects",
      category: "management"
    },
    { 
      label: "Calendar", 
      icon: <CalendarOutlined />, 
      path: "/calendar",
      category: "tools"
    },
    { 
      label: "Messages", 
      icon: <MailOutlined />, 
      path: "/messages",
      category: "tools"
    },
    { 
      label: "Support", 
      icon: <CustomerServiceOutlined />, 
      path: "/support",
      category: "tools"
    },
    { 
      label: "Security", 
      icon: <SafetyCertificateOutlined />, 
      path: "/security",
      category: "system"
    },
    { 
      label: "Settings", 
      icon: <SettingOutlined />, 
      path: "/settings",
      category: "system"
    },
  ];

  const menuCategories = {
    main: "Overview",
    management: "Management", 
    reports: "Analytics & Reports",
    tools: "Tools",
    system: "System"
  };

  const groupedMenuItems = menuItems.reduce((acc, item) => {
    if (!acc[item.category]) {
      acc[item.category] = [];
    }
    acc[item.category].push(item);
    return acc;
  }, {} as Record<string, typeof menuItems>);

  return (
    <div className="w-full h-screen flex bg-zinc-50 dark:bg-zinc-950 overflow-hidden">
      
      <aside className={`${
        sidebarCollapsed ? 'w-16' : 'w-64'
      } bg-white dark:bg-zinc-900 border-r border-zinc-200 dark:border-zinc-800 transition-all duration-300 flex flex-col shadow-sm fixed left-0 top-0 h-full z-40`}>
        
      
        <div className="h-16 flex items-center justify-between px-4 border-b border-zinc-200 dark:border-zinc-800 flex-shrink-0">
          {!sidebarCollapsed && (
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 bg-white text-black rounded-lg flex items-center justify-center">
                <HomeOutlined className="text-white text-sm" />
              </div>
              <h1 className="text-lg font-semibold text-zinc-900 dark:text-zinc-100">AssistEdge</h1>
            </div>
          )}
          
          <Button
            type="text"
            icon={sidebarCollapsed ? <MenuUnfoldOutlined style={{
              color:"#ffffff",
              fontSize:"18px"
            }} /> : <MenuFoldOutlined  style={{
              color:"#ffffff",
              fontSize:"18px"
            }} 
            />}
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            className="text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-100"
          />
        </div>

       
        <nav className="flex-1 overflow-y-auto py-4 scrollbar-thin scrollbar-thumb-zinc-300 dark:scrollbar-thumb-zinc-600 scrollbar-track-transparent">
          {Object.entries(groupedMenuItems).map(([category, items]) => (
            <div key={category} className="mb-6">
              {!sidebarCollapsed && (
                <h3 className="px-4 mb-2 text-xs font-semibold text-zinc-500 dark:text-zinc-400 uppercase tracking-wider">
                  {menuCategories[category as keyof typeof menuCategories]}
                </h3>
              )}
              
              <div className="space-y-1 px-2">
                {items.map((item) => {
                  const isActive = location.pathname === item.path;
                  return (
                    <Tooltip
                      key={item.label}
                      title={sidebarCollapsed ? item.label : ''}
                      placement="right"
                    >
                      <button
                        onClick={() => navigate(item.path)}
                        className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-left transition-all duration-200 ${
                          isActive
                            ? "bg-blue-50 dark:bg-white-900/20 text-blue-600 dark:text-black font-medium shadow-sm"
                            : "text-zinc-700 dark:text-zinc-300 hover:bg-zinc-100 dark:hover:bg-zinc-800/50"
                        }`}
                      >
                        <span className={`text-lg ${isActive ? 'text-blue-600 dark:text-black' : ''}`}>
                          {item.icon}
                        </span>
                        {!sidebarCollapsed && (
                          <span className="truncate">{item.label}</span>
                        )}
                        {!sidebarCollapsed && isActive && (
                          <div className="ml-auto w-2 h-2 bg-blue-600 dark:bg-black rounded-full"></div>
                        )}
                      </button>
                    </Tooltip>
                  );
                })}
              </div>
            </div>
          ))}
        </nav>

      
        {!sidebarCollapsed && (
          <div className="p-4 border-t border-zinc-200 dark:border-zinc-800 flex-shrink-0">
            <div className="bg-gradient-to-r from-blue-50 to-purple-50 dark:from-blue-900/20 dark:to-blue-900/20 rounded-lg p-3">
              <h4 className="text-sm font-medium text-zinc-900 dark:text-zinc-100 mb-1">
                Need Help?
              </h4>
              <p className="text-xs text-zinc-600 dark:text-zinc-400 mb-2">
                Contact our support team
              </p>
              <Button size="small" className="w-full">
                Get Support
              </Button>
            </div>
          </div>
        )}
      </aside>

     
      <div className={`flex-1 flex flex-col h-full ${
        sidebarCollapsed ? 'ml-16' : 'ml-64'
      } transition-all duration-300`}>
        
      
        <header className="h-16 bg-white dark:bg-zinc-900 border-b border-zinc-200 dark:border-zinc-800 flex items-center justify-between px-6 shadow-sm flex-shrink-0 sticky top-0 z-30">
          
        
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 text-sm text-zinc-600 dark:text-zinc-400">
              <HomeOutlined />
              <span>/</span>
              <span className="text-zinc-900 dark:text-zinc-100 font-medium">Dashboard</span>
            </div>
          </div>

       
          <div className="flex-1 max-w-md mx-8">
            <div className="relative">
              <SearchOutlined className="absolute left-3 top-1/2 transform -translate-y-1/2 text-zinc-400" />
              <input
                type="text"
                placeholder="Search anything..."
                className="w-full pl-10 pr-4 py-2 bg-zinc-100 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-lg text-sm text-zinc-900 dark:text-zinc-100 placeholder-zinc-500 dark:placeholder-zinc-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>

         
          <div className="flex items-center gap-4">
           
            <Tooltip title="Notifications">
              <div className="relative">
                <Badge count={5} size="small" offset={[-2, 2]}>
                  <Button
                    type="text"
                    icon={<BellOutlined style={{
                      color:"#ffffff",
                      fontSize:"18px"
                    }} />}
                    className="text-zinc-600 dark:text-zinc-400 hover:text-zinc-900 dark:hover:text-zinc-400"
                  />
                </Badge>
              </div>
            </Tooltip>

           
            <Dropdown overlay={userMenu} placement="bottomRight" trigger={["click"]}>
              <div className="flex items-center gap-3 cursor-pointer hover:bg-zinc-100 dark:hover:bg-zinc-800 rounded-lg px-3 py-2 transition-colors">
                <Avatar 
                  size="small" 
                  icon={<UserOutlined />} 
                  className="bg-black"
                />
                <div className="text-left">
                  <p className="text-sm font-medium text-zinc-900 dark:text-zinc-100">Admin</p>
                  <p className="text-xs text-zinc-500 dark:text-zinc-400">Administrator</p>
                </div>
              </div>
            </Dropdown>
          </div>
        </header>

     
        <main className="flex-1 overflow-y-auto bg-zinc-50 dark:bg-zinc-950 scrollbar-thin scrollbar-thumb-zinc-300 dark:scrollbar-thumb-zinc-600 scrollbar-track-transparent">
          <div className="p-6">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}

export { ProtectedLayout };

import { NavLink, Outlet } from "react-router-dom";
import {
  LayoutDashboard,
  CreditCard,
  ShieldAlert,
  Search,
  Bot,
} from "lucide-react";

const navigation = [
  { label: "Supervision", path: "/", icon: LayoutDashboard },
  { label: "Transactions", path: "/transactions", icon: CreditCard },
  { label: "Alertes", path: "/alerts", icon: ShieldAlert },
  { label: "Investigations", path: "/investigations", icon: Search },
  { label: "Assistant IA", path: "/assistant", icon: Bot },
];

function AppShell() {
  return (
    <div className="app">
      <header className="app-header">
        <div className="brand">
          <span className="brand-name">BankDispute</span>
          <span className="brand-subtitle">Investigation</span>
        </div>
      </header>

      <div className="app-layout">
        <aside className="sidebar">
          <div className="sidebar-title">EXPLORATEUR</div>

          <nav className="sidebar-navigation">
            {navigation.map(({ label, path, icon: Icon }) => (
              <NavLink
                key={path}
                to={path}
                end={path === "/"}
                className={({ isActive }) =>
                  `nav-item ${isActive ? "active" : ""}`
                }
              >
                <Icon size={17} />
                <span>{label}</span>
              </NavLink>
            ))}
          </nav>
        </aside>

        <main className="main-content">
          <Outlet />
        </main>
      </div>

      <footer className="status-bar">
        <span>BankDispute</span>
        <span>Version 0.1.0</span>
      </footer>
    </div>
  );
}

export default AppShell;
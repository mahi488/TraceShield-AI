
import { useState } from "react";
import { motion } from "framer-motion";
import {
  Shield,
  LayoutDashboard,
  ScanSearch,
  Network,
  FileText,
  Settings,
  Bell,
  Search,
  ShieldAlert,
  ShieldCheck,
  Activity,
  ArrowUpRight,
  ChevronRight,
  LockKeyhole,
  Zap,
  Menu,
  X,
} from "lucide-react";

import FileScanner from "./components/FileScanner";
import "./App.css";

const navigation = [
  { label: "Overview", icon: LayoutDashboard },
  { label: "File Scanner", icon: ScanSearch },
  { label: "Correlation Map", icon: Network },
  { label: "Reports", icon: FileText },
];

const stats = [
  {
    title: "Files Scanned",
    value: "1,284",
    change: "+12.8%",
    icon: FileText,
    color: "violet",
  },
  {
    title: "Threats Detected",
    value: "86",
    change: "+8.4%",
    icon: ShieldAlert,
    color: "red",
  },
  {
    title: "Leaks Prevented",
    value: "73",
    change: "+18.2%",
    icon: ShieldCheck,
    color: "cyan",
  },
  {
    title: "Security Score",
    value: "94.8%",
    change: "+2.4%",
    icon: Activity,
    color: "green",
  },
];

const activities = [
  {
    file: "employee_records.pdf",
    type: "PII Exposure",
    risk: "Critical",
    time: "2 min ago",
  },
  {
    file: "session_data.json",
    type: "Session Token",
    risk: "High",
    time: "8 min ago",
  },
  {
    file: "customer_list.csv",
    type: "Personal Data",
    risk: "Medium",
    time: "14 min ago",
  },
  {
    file: "server_config.log",
    type: "API Credential",
    risk: "Critical",
    time: "21 min ago",
  },
];

function App() {
  const [activePage, setActivePage] = useState("Overview");
  const [menuOpen, setMenuOpen] = useState(false);

  const openScanner = () => {
    setActivePage("File Scanner");
    setMenuOpen(false);
  };

  return (
    <div className="app-shell">
      {/* SIDEBAR */}
      <aside className={`sidebar ${menuOpen ? "sidebar-open" : ""}`}>
        <div className="brand">
          <div className="brand-symbol">
            <Shield size={25} />
            <span />
          </div>

          <div>
            <h1>
              TRACE<span>SHIELD</span>
            </h1>
            <p>AI SECURITY INTELLIGENCE</p>
          </div>

          <button
            className="mobile-close"
            onClick={() => setMenuOpen(false)}
            aria-label="Close sidebar"
          >
            <X size={20} />
          </button>
        </div>

        <div className="workspace-label">WORKSPACE</div>

        <nav className="navigation">
          {navigation.map((item) => {
            const Icon = item.icon;

            return (
              <button
                key={item.label}
                className={`nav-item ${
                  activePage === item.label ? "active" : ""
                }`}
                onClick={() => {
                  setActivePage(item.label);
                  setMenuOpen(false);
                }}
              >
                <Icon size={19} />
                <span>{item.label}</span>

                {item.label === "File Scanner" && (
                  <span className="nav-dot" />
                )}
              </button>
            );
          })}
        </nav>

        <div className="sidebar-bottom">
          <div className="system-card">
            <div className="system-heading">
              <span className="live-dot" />
              SYSTEM STATUS
              <span className="online-label">ONLINE</span>
            </div>

            <div className="system-line">
              <span>Detection engine</span>
              <span>Operational</span>
            </div>

            <div className="system-line">
              <span>Correlation engine</span>
              <span>Operational</span>
            </div>

            <div className="system-line">
              <span>Protection layer</span>
              <span>Active</span>
            </div>
          </div>

          <button
            className={`nav-item settings-item ${
              activePage === "Settings" ? "active" : ""
            }`}
            onClick={() => {
              setActivePage("Settings");
              setMenuOpen(false);
            }}
          >
            <Settings size={19} />
            <span>Settings</span>
          </button>

          <div className="profile">
            <div className="profile-avatar">TS</div>

            <div>
              <strong>Security Analyst</strong>
              <span>Administrator</span>
            </div>

            <ChevronRight size={17} />
          </div>
        </div>
      </aside>

      {/* MOBILE OVERLAY */}
      {menuOpen && (
        <button
          className="mobile-overlay"
          aria-label="Close menu"
          onClick={() => setMenuOpen(false)}
        />
      )}

      {/* MAIN CONTENT */}
      <main className="main-content">
        <header className="topbar">
          <div className="topbar-left">
            <button
              className="mobile-menu"
              onClick={() => setMenuOpen(true)}
              aria-label="Open menu"
            >
              <Menu size={21} />
            </button>

            <div className="breadcrumb">
              <span>Workspace</span>
              <ChevronRight size={14} />
              <strong>{activePage}</strong>
            </div>
          </div>

          <div className="topbar-actions">
            <div className="connection-status">
              <span className="live-dot" />
              ALL SYSTEMS NORMAL
            </div>

            <button className="icon-button" aria-label="Search">
              <Search size={19} />
            </button>

            <button
              className="icon-button notification-button"
              aria-label="Notifications"
            >
              <Bell size={19} />
              <span />
            </button>

            <div className="top-avatar">SA</div>
          </div>
        </header>

        <div className="dashboard">
          {/* OVERVIEW PAGE */}
          {activePage === "Overview" && (
            <>
              <motion.section
                className="welcome-section"
                initial={{ opacity: 0, y: 18 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6 }}
              >
                <div>
                  <div className="eyebrow">
                    <span className="live-dot" />
                    CYBER INTELLIGENCE CENTER
                  </div>

                  <h2>
                    See the threats.
                    <br />
                    <span>Stop the exposure.</span>
                  </h2>

                  <p>
                    Your digital assets, continuously monitored.
                    Your sensitive data, protected.
                  </p>
                </div>

                <button className="primary-button" onClick={openScanner}>
                  <Zap size={17} />
                  Initiate Scan
                  <ArrowUpRight size={17} />
                </button>
              </motion.section>

              {/* STATISTICS */}
              <section className="stats-grid">
                {stats.map((stat, index) => {
                  const Icon = stat.icon;

                  return (
                    <motion.article
                      className="stat-card"
                      key={stat.title}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <div className="stat-top">
                        <div className={`stat-icon ${stat.color}`}>
                          <Icon size={20} />
                        </div>

                        <span className="stat-change">
                          {stat.change}
                        </span>
                      </div>

                      <p>{stat.title}</p>
                      <h3>{stat.value}</h3>

                      <div className="stat-footer">
                        Demo dashboard data
                      </div>
                    </motion.article>
                  );
                })}
              </section>

              {/* INTELLIGENCE NETWORK */}
              <section className="content-grid">
                <article className="panel exposure-panel">
                  <div className="panel-heading">
                    <div>
                      <div className="panel-kicker">
                        INTELLIGENCE NETWORK
                      </div>
                      <h3>Cross-artifact exposure</h3>
                    </div>

                    <span className="live-tag">
                      <span className="live-dot" /> DEMO
                    </span>
                  </div>

                  <div className="network-visual">
                    <div className="network-grid" />
                    <div className="network-ring ring-one" />
                    <div className="network-ring ring-two" />
                    <div className="network-ring ring-three" />

                    <svg
                      className="network-lines"
                      viewBox="0 0 600 300"
                      preserveAspectRatio="none"
                    >
                      <line x1="300" y1="145" x2="130" y2="65" />
                      <line x1="300" y1="145" x2="470" y2="65" />
                      <line x1="300" y1="145" x2="120" y2="235" />
                      <line x1="300" y1="145" x2="480" y2="235" />
                      <line x1="130" y1="65" x2="120" y2="235" />
                      <line x1="470" y1="65" x2="480" y2="235" />
                    </svg>

                    <div className="network-center">
                      <Shield size={31} />
                      <span>TRACE AI</span>
                      <small>ANALYZING</small>
                    </div>

                    <div className="network-node node-one">
                      <FileText />
                      <span>PDF</span>
                    </div>

                    <div className="network-node node-two">
                      <LockKeyhole />
                      <span>JSON</span>
                    </div>

                    <div className="network-node node-three">
                      <FileText />
                      <span>CSV</span>
                    </div>

                    <div className="network-node node-four">
                      <Zap />
                      <span>LOG</span>
                    </div>
                  </div>

                  <div className="network-legend">
                    <span>
                      <i className="legend-violet" />
                      Artifact connection
                    </span>
                    <span>
                      <i className="legend-cyan" />
                      Analysis node
                    </span>
                    <span>
                      <i className="legend-red" />
                      Exposure point
                    </span>
                  </div>
                </article>

                {/* THREAT INTELLIGENCE */}
                <article className="panel threat-panel">
                  <div className="panel-heading">
                    <div>
                      <div className="panel-kicker">
                        RISK DISTRIBUTION
                      </div>
                      <h3>Threat intelligence</h3>
                    </div>

                    <Activity size={19} className="muted-icon" />
                  </div>

                  <div className="threat-score">
                    <div className="score-circle">
                      <div>
                        <strong>86</strong>
                        <span>DETECTED</span>
                      </div>
                    </div>

                    <div className="score-description">
                      <strong>Exposure events</strong>
                      <span>Demo dashboard figures</span>
                      <small>
                        <span className="live-dot" />
                        Monitoring interface
                      </small>
                    </div>
                  </div>

                  <div className="risk-bars">
                    <div className="risk-row">
                      <span>Critical</span>
                      <div><i className="critical-bar" /></div>
                      <strong>18</strong>
                    </div>

                    <div className="risk-row">
                      <span>High</span>
                      <div><i className="high-bar" /></div>
                      <strong>29</strong>
                    </div>

                    <div className="risk-row">
                      <span>Medium</span>
                      <div><i className="medium-bar" /></div>
                      <strong>25</strong>
                    </div>

                    <div className="risk-row">
                      <span>Low</span>
                      <div><i className="low-bar" /></div>
                      <strong>14</strong>
                    </div>
                  </div>
                </article>
              </section>

              {/* RECENT ACTIVITY */}
              <section className="panel activity-panel">
                <div className="panel-heading">
                  <div>
                    <div className="panel-kicker">
                      SECURITY OPERATIONS
                    </div>
                    <h3>Recent detection activity</h3>
                  </div>

                  <button
                    className="text-button"
                    onClick={() => setActivePage("Reports")}
                  >
                    View all <ArrowUpRight size={15} />
                  </button>
                </div>

                <div className="activity-table">
                  <div className="table-header">
                    <span>ARTIFACT</span>
                    <span>DETECTION TYPE</span>
                    <span>RISK LEVEL</span>
                    <span>DETECTED</span>
                  </div>

                  {activities.map((item) => (
                    <div className="table-row" key={item.file}>
                      <div className="file-name">
                        <FileText size={17} />
                        {item.file}
                      </div>

                      <span className="detection-type">
                        {item.type}
                      </span>

                      <span
                        className={`risk-badge ${item.risk.toLowerCase()}`}
                      >
                        {item.risk}
                      </span>

                      <span className="activity-time">
                        {item.time}
                      </span>
                    </div>
                  ))}
                </div>
              </section>

              {/* SCAN CALL TO ACTION */}
              <section className="scan-banner">
                <div className="scan-banner-icon">
                  <ShieldCheck size={25} />
                </div>

                <div>
                  <strong>
                    Your protection layer is ready.
                  </strong>

                  <p>
                    Upload multiple artifacts to discover hidden
                    cross-file privacy exposures.
                  </p>
                </div>

                <button onClick={openScanner}>
                  Scan artifacts <ChevronRight size={17} />
                </button>
              </section>

              <footer className="footer">
                <span>
                  TRACESHIELD AI <i /> CYBER INTELLIGENCE PLATFORM
                </span>
                <span>
                  SECURE BY DESIGN · BUILT FOR PROTECTION
                </span>
              </footer>
            </>
          )}

          {/* FILE SCANNER PAGE */}
          {activePage === "File Scanner" && <FileScanner />}

          {/* OTHER PAGES - PLACEHOLDERS */}
          {["Correlation Map", "Reports", "Settings"].includes(activePage) && (
            <section className="panel" style={{ padding: "35px", margin: "25px" }}>
              <div className="panel-kicker">MODULE UNDER DEVELOPMENT</div>
              <h2 style={{ marginTop: "12px" }}>{activePage}</h2>
              <p style={{ color: "#9999ad", marginTop: "10px" }}>
                This module will be connected to the TraceShield AI
                backend in a later development step.
              </p>

              {activePage === "Correlation Map" && (
                <button
                  className="primary-button"
                  style={{ marginTop: "20px" }}
                  onClick={openScanner}
                >
                  <ScanSearch size={17} />
                  Open File Scanner
                </button>
              )}
            </section>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;

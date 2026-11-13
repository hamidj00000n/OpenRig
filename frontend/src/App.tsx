import { useEffect, useState } from "react";
import { Activity, Building2, ChevronDown, CircleHelp, Drill, Globe2, HardHat, LogOut, Plus, ShieldCheck, Warehouse } from "lucide-react";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";
type Org = { id: string; name: string; slug: string; role: string; created_at: string };
type User = { id: string; email: string; full_name: string; preferred_language: string };

const copy = {
  en: {
    subtitle: "Drilling operations platform", signIn: "Sign in", register: "Create account",
    email: "Email address", password: "Password", fullName: "Full name", welcome: "Welcome to OpenRig",
    intro: "Manage your drilling operations from one secure workspace.", organizations: "Your organizations",
    createOrg: "Create organization", orgName: "Organization name", slug: "Organization ID (e.g. north-drilling)",
    noOrgs: "You are not a member of an organization yet.", create: "Create", cancel: "Cancel",
    logout: "Sign out", dashboard: "Overview", rigs: "Rigs", equipment: "Equipment",
    warehouse: "Warehouse", maintenance: "Maintenance", procurement: "Procurement",
    secure: "Organization-scoped access", loading: "Loading…", switch: "Language",
    failed: "Something went wrong. Check the API connection and try again.", role: "Your role"
  },
  fa: {
    subtitle: "سامانه مدیریت عملیات حفاری", signIn: "ورود", register: "ایجاد حساب",
    email: "آدرس ایمیل", password: "رمز عبور", fullName: "نام کامل", welcome: "به OpenRig خوش آمدید",
    intro: "مدیریت عملیات حفاری در یک محیط امن و یکپارچه.", organizations: "سازمان‌های شما",
    createOrg: "ایجاد سازمان", orgName: "نام سازمان", slug: "شناسه سازمان (مثلاً north-drilling)",
    noOrgs: "هنوز عضو هیچ سازمانی نیستید.", create: "ایجاد", cancel: "انصراف",
    logout: "خروج", dashboard: "نمای کلی", rigs: "دکل‌ها", equipment: "تجهیزات",
    warehouse: "انبار", maintenance: "تعمیرات", procurement: "تدارکات",
    secure: "دسترسی محدود به سازمان", loading: "در حال بارگذاری…", switch: "زبان",
    failed: "خطا رخ داد. اتصال API را بررسی و دوباره تلاش کنید.", role: "نقش شما"
  }
};

export default function App() {
  const [language, setLanguage] = useState<"en" | "fa">(() => {
    const saved = localStorage.getItem("openrig-language");
    return saved === "fa" ? "fa" : "en";
  });
  const t = copy[language];
  const [token, setToken] = useState(() => localStorage.getItem("openrig-token") || "");
  const [user, setUser] = useState<User | null>(null);
  const [orgs, setOrgs] = useState<Org[]>([]);
  const [selected, setSelected] = useState<Org | null>(null);
  const [mode, setMode] = useState<"login" | "register">("login");
  const [showCreate, setShowCreate] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    localStorage.setItem("openrig-language", language);
    document.documentElement.lang = language;
    document.documentElement.dir = language === "fa" ? "rtl" : "ltr";
  }, [language]);

  async function request(path: string, options: RequestInit = {}) {
    const response = await fetch(API + path, {
      ...options,
      headers: { "Content-Type": "application/json", ...(token ? { Authorization: `Bearer ${token}` } : {}), ...options.headers }
    });
    const data = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(data.detail || t.failed);
    return data;
  }

  async function loadWorkspace(currentToken = token) {
    const headers = { Authorization: `Bearer ${currentToken}` };
    const [meResponse, orgResponse] = await Promise.all([
      fetch(API + "/api/v1/auth/me", { headers }),
      fetch(API + "/api/v1/organizations", { headers })
    ]);
    if (!meResponse.ok || !orgResponse.ok) throw new Error(t.failed);
    setUser(await meResponse.json());
    setOrgs((await orgResponse.json()).items);
  }

  useEffect(() => {
    if (token) loadWorkspace().catch(() => signOut());
    // Initial session restoration only.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  function signOut() {
    localStorage.removeItem("openrig-token");
    setToken(""); setUser(null); setOrgs([]); setSelected(null);
  }

  async function submitAuth(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault(); setBusy(true); setError("");
    const form = new FormData(event.currentTarget);
    const payload: Record<string, string> = {
      email: String(form.get("email")), password: String(form.get("password"))
    };
    if (mode === "register") payload.full_name = String(form.get("full_name"));
    try {
      const data = await request(`/api/v1/auth/${mode}`, { method: "POST", body: JSON.stringify(payload) });
      if (mode === "register") {
        setMode("login");
        setError("Account created. Please sign in.");
      } else {
        localStorage.setItem("openrig-token", data.access_token);
        setToken(data.access_token);
        await loadWorkspace(data.access_token);
      }
    } catch (e) { setError(e instanceof Error ? e.message : t.failed); }
    finally { setBusy(false); }
  }

  async function createOrganization(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault(); setBusy(true); setError("");
    const form = new FormData(event.currentTarget);
    try {
      await request("/api/v1/organizations", {
        method: "POST",
        body: JSON.stringify({ name: String(form.get("name")), slug: String(form.get("slug")).toLowerCase() })
      });
      await loadWorkspace();
      setShowCreate(false);
    } catch (e) { setError(e instanceof Error ? e.message : t.failed); }
    finally { setBusy(false); }
  }

  if (!token || !user) return (
    <main className="auth-shell">
      <section className="auth-brand">
        <div className="brand-mark"><Drill size={30} /></div>
        <div><strong>OpenRig</strong><span>{t.subtitle}</span></div>
        <div className="brand-copy"><h1>{t.welcome}</h1><p>{t.intro}</p></div>
        <div className="secure-note"><ShieldCheck size={17}/>{t.secure}</div>
      </section>
      <section className="auth-panel">
        <button className="language-switch" onClick={() => setLanguage(language === "en" ? "fa" : "en")}><Globe2 size={16}/>{language === "en" ? "فارسی" : "English"}</button>
        <div className="form-wrap">
          <div className="eyebrow">OPENRIG WORKSPACE</div>
          <h2>{mode === "login" ? t.signIn : t.register}</h2>
          <form onSubmit={submitAuth}>
            {mode === "register" && <label>{t.fullName}<input name="full_name" minLength={2} required autoComplete="name"/></label>}
            <label>{t.email}<input name="email" type="email" required autoComplete="email"/></label>
            <label>{t.password}<input name="password" type="password" minLength={mode === "register" ? 12 : 1} required autoComplete={mode === "login" ? "current-password" : "new-password"}/></label>
            <button className="primary-button" disabled={busy}>{busy ? t.loading : mode === "login" ? t.signIn : t.register}</button>
          </form>
          {error && <p className="error-text">{error}</p>}
          <p className="form-foot">{mode === "login" ? "New to OpenRig?" : "Already have an account?"} <button className="text-button" onClick={() => {setMode(mode === "login" ? "register" : "login");setError("");}}>{mode === "login" ? t.register : t.signIn}</button></p>
          <p className="small-muted">English is the default language. Persian is optional.</p>
        </div>
      </section>
    </main>
  );

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="side-brand"><div className="brand-mark small"><Drill size={21}/></div><strong>OpenRig</strong></div>
        <div className="nav-label">WORKSPACE</div>
        <button className="nav-item active"><Activity size={17}/>{t.dashboard}</button>
        <button className="nav-item"><HardHat size={17}/>{t.rigs}<span className="soon">Soon</span></button>
        <button className="nav-item"><Building2 size={17}/>{t.equipment}<span className="soon">Soon</span></button>
        <button className="nav-item"><Warehouse size={17}/>{t.warehouse}<span className="soon">Soon</span></button>
        <button className="nav-item"><ShieldCheck size={17}/>{t.maintenance}<span className="soon">Soon</span></button>
        <button className="nav-item"><Activity size={17}/>{t.procurement}<span className="soon">Soon</span></button>
        <div className="sidebar-bottom"><CircleHelp size={16}/> OpenRig early access</div>
      </aside>
      <main className="main-area">
        <header className="topbar">
          <div><span className="eyebrow">ORGANIZATION WORKSPACE</span><h1>{selected?.name || t.organizations}</h1></div>
          <div className="top-actions">
            <button className="language-switch" onClick={() => setLanguage(language === "en" ? "fa" : "en")}><Globe2 size={16}/>{language === "en" ? "فارسی" : "English"}</button>
            <button className="user-chip" onClick={signOut}><span className="avatar">{user.full_name.slice(0,1).toUpperCase()}</span><span>{user.full_name}</span><LogOut size={15}/><span className="sr-only">{t.logout}</span></button>
          </div>
        </header>
        <section className="content">
          <div className="welcome-row"><div><h2>{t.welcome}, {user.full_name.split(" ")[0]}</h2><p>{t.intro}</p></div><button className="primary-button compact" onClick={() => setShowCreate(true)}><Plus size={17}/>{t.createOrg}</button></div>
          {error && <p className="error-text">{error}</p>}
          {showCreate && <form className="create-card" onSubmit={createOrganization}><h3>{t.createOrg}</h3><label>{t.orgName}<input name="name" required minLength={2}/></label><label>{t.slug}<input name="slug" required pattern="[a-z0-9]+(-[a-z0-9]+)*"/></label><div className="form-actions"><button type="button" className="secondary-button" onClick={() => setShowCreate(false)}>{t.cancel}</button><button className="primary-button" disabled={busy}>{t.create}</button></div></form>}
          <div className="section-heading"><h3>{t.organizations}</h3><span>{orgs.length} {orgs.length === 1 ? "organization" : "organizations"}</span></div>
          {orgs.length === 0 ? <div className="empty-state"><Building2 size={30}/><p>{t.noOrgs}</p><button className="secondary-button" onClick={() => setShowCreate(true)}>{t.createOrg}</button></div> :
            <div className="org-grid">{orgs.map(org => <button className={selected?.id === org.id ? "org-card selected" : "org-card"} key={org.id} onClick={() => setSelected(org)}><div className="org-icon"><Building2 size={21}/></div><strong>{org.name}</strong><span>{org.slug}</span><small>{t.role}: {org.role}</small></button>)}</div>}
          {selected && <div className="selected-banner"><ShieldCheck size={18}/><span>{selected.name} · {selected.role}</span><span className="scope-tag">Organization scope</span></div>}
        </section>
      </main>
    </div>
  );
}

import { useEffect, useState } from "react";
import { Activity, Building2, CircleHelp, Drill, Globe2, HardHat, LogOut, Plus, ShieldCheck, Warehouse, Users, RefreshCw } from "lucide-react";

const API = import.meta.env.VITE_API_URL || "http://localhost:8000";
type Org = { id: string; name: string; slug: string; role: string; created_at: string };
type User = { id: string; email: string; full_name: string; preferred_language: string };
type Member = { user_id: string; email: string; full_name: string; role: string; is_active: boolean; joined_at: string };

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
    failed: "Something went wrong. Check the API connection and try again.", role: "Your role",
    members: "Organization members", membersHint: "View members and manage their organization roles.",
    noPermission: "Only organization owners and administrators can view members.",
    memberName: "Member", memberEmail: "Email", memberRole: "Role", status: "Status",
    active: "Active", inactive: "Inactive", save: "Save", saved: "Role updated successfully.",
    memberLoadFailed: "Could not load organization members.", roleOwner: "Owner", roleAdmin: "Administrator",
    roleManager: "Manager", roleMember: "Member", updating: "Updating…", refresh: "Refresh"
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
    failed: "خطا رخ داد. اتصال API را بررسی و دوباره تلاش کنید.", role: "نقش شما",
    members: "اعضای سازمان", membersHint: "مشاهده اعضا و مدیریت نقش سازمانی آن‌ها.",
    noPermission: "فقط مالک و مدیر سازمان می‌توانند اعضا را مشاهده کنند.",
    memberName: "عضو", memberEmail: "ایمیل", memberRole: "نقش", status: "وضعیت",
    active: "فعال", inactive: "غیرفعال", save: "ذخیره", saved: "نقش با موفقیت تغییر کرد.",
    memberLoadFailed: "بارگذاری اعضای سازمان انجام نشد.", roleOwner: "مالک", roleAdmin: "مدیر",
    roleManager: "سرپرست", roleMember: "عضو", updating: "در حال بروزرسانی…", refresh: "بروزرسانی"
  }
};

export default function App() {
  const [language, setLanguage] = useState<"en" | "fa">(() => localStorage.getItem("openrig-language") === "fa" ? "fa" : "en");
  const t = copy[language];
  const [token, setToken] = useState(() => localStorage.getItem("openrig-token") || "");
  const [user, setUser] = useState<User | null>(null);
  const [orgs, setOrgs] = useState<Org[]>([]);
  const [selected, setSelected] = useState<Org | null>(null);
  const [members, setMembers] = useState<Member[]>([]);
  const [memberBusy, setMemberBusy] = useState(false);
  const [memberError, setMemberError] = useState("");
  const [memberNotice, setMemberNotice] = useState("");
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

  async function loadMembers(org = selected) {
    if (!org || !["owner", "admin"].includes(org.role)) { setMembers([]); return; }
    setMemberBusy(true); setMemberError(""); setMemberNotice("");
    try {
      const data = await request(`/api/v1/organizations/${org.id}/members`);
      setMembers(data.items);
    } catch (e) {
      setMemberError(e instanceof Error ? e.message : t.memberLoadFailed);
    } finally { setMemberBusy(false); }
  }

  useEffect(() => {
    if (token) loadWorkspace().catch(() => signOut());
    // Initial session restoration only.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    setMembers([]);
    setMemberError("");
    setMemberNotice("");
    if (selected && ["owner", "admin"].includes(selected.role)) loadMembers(selected);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selected?.id, token]);

  function signOut() {
    localStorage.removeItem("openrig-token");
    setToken(""); setUser(null); setOrgs([]); setSelected(null); setMembers([]);
  }

  async function submitAuth(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault(); setBusy(true); setError("");
    const form = new FormData(event.currentTarget);
    const payload: Record<string, string> = { email: String(form.get("email")), password: String(form.get("password")) };
    if (mode === "register") payload.full_name = String(form.get("full_name"));
    try {
      const data = await request(`/api/v1/auth/${mode}`, { method: "POST", body: JSON.stringify(payload) });
      if (mode === "register") { setMode("login"); setError("Account created. Please sign in."); }
      else {
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
      await request("/api/v1/organizations", { method: "POST", body: JSON.stringify({ name: String(form.get("name")), slug: String(form.get("slug")).toLowerCase() }) });
      await loadWorkspace(); setShowCreate(false);
    } catch (e) { setError(e instanceof Error ? e.message : t.failed); }
    finally { setBusy(false); }
  }

  async function changeMemberRole(member: Member, role: string) {
    if (!selected || role === member.role) return;
    setMemberBusy(true); setMemberError(""); setMemberNotice("");
    try {
      await request(`/api/v1/organizations/${selected.id}/members/${member.user_id}/role`, {
        method: "PATCH", body: JSON.stringify({ role })
      });
      setMemberNotice(t.saved);
      await loadMembers(selected);
    } catch (e) { setMemberError(e instanceof Error ? e.message : t.failed); }
    finally { setMemberBusy(false); }
  }

  const roleLabel = (role: string) => role === "owner" ? t.roleOwner : role === "admin" ? t.roleAdmin : role === "manager" ? t.roleManager : t.roleMember;

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
          <div className="eyebrow">OPENRIG WORKSPACE</div><h2>{mode === "login" ? t.signIn : t.register}</h2>
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
            <div className="org-grid">{orgs.map(org => <button className={selected?.id === org.id ? "org-card selected" : "org-card"} key={org.id} onClick={() => setSelected(org)}><div className="org-icon"><Building2 size={21}/></div><strong>{org.name}</strong><span>{org.slug}</span><small>{t.role}: {roleLabel(org.role)}</small></button>)}</div>}
          {selected && <div className="selected-banner"><ShieldCheck size={18}/><span>{selected.name} · {roleLabel(selected.role)}</span><span className="scope-tag">Organization scope</span></div>}
          {selected && <section className="members-panel">
            <div className="members-heading"><div><h3><Users size={18}/>{t.members}</h3><p>{t.membersHint}</p></div>
              {["owner", "admin"].includes(selected.role) && <button className="secondary-button refresh-button" onClick={() => loadMembers(selected)} disabled={memberBusy}><RefreshCw size={14}/>{t.refresh}</button>}
            </div>
            {!["owner", "admin"].includes(selected.role) ? <p className="small-muted">{t.noPermission}</p> : memberBusy && members.length === 0 ? <p className="small-muted">{t.loading}</p> : <>
              {memberError && <p className="error-text">{memberError}</p>}
              {memberNotice && <p className="success-text">{memberNotice}</p>}
              <div className="member-table-wrap"><table className="member-table"><thead><tr><th>{t.memberName}</th><th>{t.memberEmail}</th><th>{t.memberRole}</th><th>{t.status}</th></tr></thead>
                <tbody>{members.map(member => {
                  const canEdit = member.role !== "owner" && (selected.role === "owner" || (selected.role === "admin" && member.role !== "admin"));
                  return <tr key={member.user_id}><td><strong>{member.full_name}</strong></td><td>{member.email}</td><td>
                    {canEdit ? <select aria-label={`${t.memberRole}: ${member.full_name}`} value={member.role} disabled={memberBusy} onChange={e => changeMemberRole(member, e.target.value)}>
                      {selected.role === "owner" && <option value="admin">{t.roleAdmin}</option>}
                      <option value="manager">{t.roleManager}</option><option value="member">{t.roleMember}</option>
                    </select> : <span className={`role-pill role-${member.role}`}>{roleLabel(member.role)}</span>}
                  </td><td><span className={member.is_active ? "status-active" : "status-inactive"}>{member.is_active ? t.active : t.inactive}</span></td></tr>;
                })}</tbody></table></div>
            </>}
          </section>}
        </section>
      </main>
    </div>
  );
}

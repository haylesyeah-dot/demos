import { useState, useEffect } from "react";
import {
  LayoutDashboard, Upload, GitMerge, Zap, BarChart2, Code2,
  ChevronRight, CheckCircle, Circle, ArrowRight, Lock,
  RefreshCw, Database, Server, Shield
} from "lucide-react";

const C = {
  bg:      "#04080F",
  surface: "#080E1A",
  card:    "#0C1424",
  border:  "#1A2640",
  gold:    "#D4A843",
  goldLt:  "#F0C96B",
  teal:    "#1BBFA6",
  text:    "#E2D9C8",
  muted:   "#6B7A99",
  purple:  "#A78BFA",
  blue:    "#60A5FA",
  pink:    "#F472B6",
  green:   "#34D399",
  orange:  "#FB923C",
};

const NAV = [
  { id: "overview",     short: "Overview",  Icon: LayoutDashboard },
  { id: "onboard",      short: "Onboard",   Icon: Upload          },
  { id: "graph",        short: "ID Graph",  Icon: GitMerge        },
  { id: "activate",     short: "Activate",  Icon: Zap             },
  { id: "intelligence", short: "Measure",   Icon: BarChart2       },
  { id: "techspec",     short: "Tech Spec", Icon: Code2           },
];

const RMN = [
  { name: "Noon",             color: "#FFC200", reach: "12M users",       format: "Sponsored Products, Display", desc: "UAE/KSA e-commerce leader"       },
  { name: "Carrefour Arabia", color: "#004F9F", reach: "8M loyalty mbrs", format: "In-store + Digital",          desc: "Grocery & general merchandise"   },
  { name: "LuLu Hypermarket", color: "#00843D", reach: "6.4M customers",  format: "Display, Sponsored",          desc: "GCC hypermarket RMN"             },
  { name: "Panda Retail",     color: "#E8453C", reach: "9.1M members",    format: "Offsite + Onsite",            desc: "KSA largest grocery chain"       },
  { name: "Jarir Bookstore",  color: "#CC0000", reach: "4.2M members",    format: "Display, Email",              desc: "Electronics & office RMN"        },
  { name: "Danube Home",      color: "#8B4513", reach: "3.1M shoppers",   format: "Sponsored, CTV",              desc: "Premium grocery & home"          },
];
const DSP = [
  { name: "Google DV360",        color: "#4285F4", reach: "40M+ MENA",    signal: "Customer Match",     type: "DSP",    desc: "Display & Video 360"        },
  { name: "Meta Business",       color: "#0668E1", reach: "35M+ MENA",    signal: "Custom Audience",    type: "Social", desc: "Facebook & Instagram"       },
  { name: "Snapchat",            color: "#FFDD00", reach: "21M KSA",      signal: "Snap Audience",      type: "Social", desc: "No.1 app in KSA"            },
  { name: "TikTok for Business", color: "#FF0050", reach: "18.4M MENA",   signal: "Custom Audience",    type: "Social", desc: "Short-form video leader"    },
  { name: "Amazon DSP",          color: "#FF9900", reach: "10M+ KSA",     signal: "Amazon Audiences",   type: "DSP",    desc: "Amazon demand-side"         },
  { name: "The Trade Desk",      color: "#17E9E0", reach: "Open web",     signal: "UID 2.0",            type: "DSP",    desc: "Open internet DSP"          },
  { name: "Criteo Commerce",     color: "#FF6B2B", reach: "KSA + UAE",    signal: "Commerce Audiences", type: "DSP",    desc: "Commerce media platform"    },
  { name: "STC Ads",             color: "#7B2D8B", reach: "30M KSA subs", signal: "Mobile Identity",    type: "Telco",  desc: "Telecom 1P data network"    },
];
const SOURCES = [
  { id: "crm",     tag: "CRM", label: "CRM / Customer DB",      fields: ["Email","Phone","Customer ID"]        },
  { id: "ecomm",   tag: "SHP", label: "E-commerce Platform",    fields: ["Order ID","Email","Device ID"]       },
  { id: "loyalty", tag: "LYL", label: "Loyalty Programme",      fields: ["Member ID","Email","Mobile"]         },
  { id: "pos",     tag: "POS", label: "Point of Sale",          fields: ["Transaction ID","Phone","Card Hash"] },
  { id: "app",     tag: "APP", label: "Mobile Application",     fields: ["IDFA/GAID","Email","User ID"]        },
  { id: "cdp",     tag: "CDP", label: "CDP / DMP Export",       fields: ["Universal ID","Segment","Score"]     },
];
const SEGMENTS = [
  { name: "High-Value Shoppers",   size: "420K",  score: 92, color: C.gold   },
  { name: "Grocery Loyalists",     size: "1.1M",  score: 87, color: C.teal   },
  { name: "Electronics Intenders", size: "280K",  score: 81, color: C.purple },
  { name: "Ramadan Buyers",        size: "890K",  score: 95, color: C.pink   },
  { name: "Auto In-Market",        size: "145K",  score: 78, color: C.blue   },
  { name: "Pharma & Health",       size: "330K",  score: 84, color: C.green  },
  { name: "Vision 2030 Consumers", size: "660K",  score: 89, color: C.goldLt },
  { name: "KSA New Residents",     size: "88K",   score: 91, color: C.orange },
];

/* ── primitives ─────────────────────────────────────── */
const Badge = ({ label, variant = "gold" }) => {
  const styles = {
    gold:  { color: C.gold,   background: `${C.gold}22`,   border: `1px solid ${C.gold}45`   },
    teal:  { color: C.teal,   background: `${C.teal}20`,   border: `1px solid ${C.teal}40`   },
    muted: { color: C.muted,  background: `${C.muted}15`,  border: `1px solid ${C.border}`   },
  };
  return (
    <span style={{ ...styles[variant], borderRadius: 5, padding: "2px 8px", fontSize: 10, fontWeight: 700, letterSpacing: 0.4, whiteSpace: "nowrap" }}>
      {label}
    </span>
  );
};

const Card = ({ children, gold, teal, style = {} }) => (
  <div style={{
    background: C.card, borderRadius: 13,
    border: `1.5px solid ${gold ? `${C.gold}50` : teal ? `${C.teal}45` : C.border}`,
    padding: "22px 26px",
    boxShadow: gold ? `0 0 28px ${C.gold}0C` : teal ? `0 0 24px ${C.teal}0A` : "none",
    ...style,
  }}>{children}</div>
);

const Divider = ({ margin = "18px 0" }) => <div style={{ height: 1, background: C.border, margin }} />;

const SectionTitle = ({ label, title, sub }) => (
  <div style={{ marginBottom: 26 }}>
    {label && <div style={{ color: C.gold, fontSize: 10, letterSpacing: 3, fontWeight: 700, marginBottom: 8 }}>{label}</div>}
    <div style={{ fontFamily: "'Cinzel', serif", fontSize: 24, fontWeight: 700, color: C.text, marginBottom: 6, lineHeight: 1.2 }}>{title}</div>
    {sub && <div style={{ color: C.muted, fontSize: 13, lineHeight: 1.65, maxWidth: 700 }}>{sub}</div>}
  </div>
);

const MetricCard = ({ value, label, sub, color = C.gold }) => (
  <Card style={{ borderTop: `2px solid ${color}` }}>
    <div style={{ color: C.muted, fontSize: 11, fontWeight: 600, letterSpacing: 0.4, marginBottom: 6 }}>{label}</div>
    <div style={{ fontFamily: "'Cinzel', serif", fontSize: 26, color, fontWeight: 700, marginBottom: 4 }}>{value}</div>
    {sub && <div style={{ color: C.muted, fontSize: 11 }}>{sub}</div>}
  </Card>
);

const ProgBar = ({ pct, color = C.teal, label }) => (
  <div style={{ marginBottom: 10 }}>
    <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 4 }}>
      <span style={{ fontSize: 11, color: C.muted }}>{label}</span>
      <span style={{ fontSize: 11, color, fontWeight: 700 }}>{pct}%</span>
    </div>
    <div style={{ height: 5, background: C.border, borderRadius: 3, overflow: "hidden" }}>
      <div style={{ height: "100%", width: `${pct}%`, background: color, borderRadius: 3 }} />
    </div>
  </div>
);

const Donut = ({ pct, color, size = 64, label }) => {
  const r = (size - 10) / 2; const cx = size / 2;
  const circ = 2 * Math.PI * r;
  return (
    <div style={{ textAlign: "center" }}>
      <svg width={size} height={size} viewBox={`0 0 ${size} ${size}`} style={{ transform: "rotate(-90deg)" }}>
        <circle cx={cx} cy={cx} r={r} fill="none" stroke={C.border} strokeWidth={5} />
        <circle cx={cx} cy={cx} r={r} fill="none" stroke={color} strokeWidth={5}
          strokeDasharray={`${(pct / 100) * circ} ${circ}`} strokeLinecap="round" />
      </svg>
      <div style={{ fontFamily: "'Cinzel', serif", fontSize: 12, color, fontWeight: 700, marginTop: -2 }}>{pct}%</div>
      {label && <div style={{ color: C.muted, fontSize: 10, marginTop: 1 }}>{label}</div>}
    </div>
  );
};

/* mini sparkline */
const Spark = ({ vals, color = C.teal, w = 110, h = 34 }) => {
  const max = Math.max(...vals), min = Math.min(...vals);
  const pts = vals.map((v, i) => `${(i / (vals.length - 1)) * w},${h - ((v - min) / (max - min || 1)) * (h - 4) - 2}`).join(" ");
  return (
    <svg width={w} height={h}><polyline points={pts} fill="none" stroke={color} strokeWidth={1.5} strokeLinejoin="round" strokeLinecap="round" />
      <polyline points={`0,${h} ${pts} ${w},${h}`} fill={`${color}18`} /></svg>
  );
};

/* mini bar chart */
const MiniBar = ({ data, height = 56 }) => {
  const max = Math.max(...data.map(d => d.v));
  const bw = Math.floor(200 / data.length) - 5;
  return (
    <svg width={200} height={height}>
      {data.map((d, i) => {
        const bh = Math.max(3, (d.v / max) * (height - 14));
        return (
          <g key={i}>
            <rect x={i * (bw + 5) + 2} y={height - bh - 12} width={bw} height={bh} rx={2} fill={d.color ?? C.teal} opacity={0.8} />
            <text x={i * (bw + 5) + 2 + bw / 2} y={height - 1} textAnchor="middle" fill={C.muted} fontSize={8} fontFamily="DM Sans">{d.l}</text>
          </g>
        );
      })}
    </svg>
  );
};

/* identity graph svg */
const IDGraphSVG = ({ animate }) => {
  const nodes = [
    { x: 225, y: 52,  label: "Email Hash",  color: C.gold,    r: 13, key: true  },
    { x: 98,  y: 140, label: "Phone Hash",  color: C.gold,    r: 11, key: true  },
    { x: 352, y: 140, label: "Device ID",   color: C.gold,    r: 11, key: true  },
    { x: 44,  y: 240, label: "CRM ID",      color: C.teal,    r: 9,  key: false },
    { x: 162, y: 248, label: "Loyalty ID",  color: C.teal,    r: 9,  key: false },
    { x: 290, y: 248, label: "Cookie",      color: C.teal,    r: 9,  key: false },
    { x: 408, y: 240, label: "IDFA",        color: C.teal,    r: 9,  key: false },
    { x: 225, y: 168, label: "PERSON",      color: "#FFFFFF", r: 20, key: true  },
  ];
  const edges = [[0,7],[1,7],[2,7],[3,1],[4,1],[5,2],[6,2]];
  return (
    <svg width={460} height={300} viewBox="0 0 460 300" style={{ display: "block" }}>
      <defs>
        <radialGradient id="glow" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stopColor={C.teal} stopOpacity="0.2" />
          <stop offset="100%" stopColor={C.teal} stopOpacity="0" />
        </radialGradient>
      </defs>
      {animate && <circle cx={225} cy={168} r={36} fill="url(#glow)" />}
      {edges.map(([a, b], i) => (
        <line key={i} x1={nodes[a].x} y1={nodes[a].y} x2={nodes[b].x} y2={nodes[b].y}
          stroke={animate ? `${C.teal}55` : C.border} strokeWidth={animate ? 1.5 : 0.8}
          strokeDasharray={animate ? "none" : "4 3"} />
      ))}
      {animate && edges.map(([a, b], i) => (
        <circle key={`pk${i}`} r={3} fill={C.gold}>
          <animateMotion dur={`${1.8 + i * 0.22}s`} repeatCount="indefinite"
            path={`M${nodes[a].x},${nodes[a].y} L${nodes[b].x},${nodes[b].y}`} />
        </circle>
      ))}
      {nodes.map((n, i) => (
        <g key={i}>
          {n.key && animate && (
            <circle cx={n.x} cy={n.y} r={n.r + 9} fill="none" stroke={n.color} strokeWidth={0.7} opacity={0.3}>
              <animate attributeName="r" values={`${n.r+4};${n.r+16};${n.r+4}`} dur="2.8s" repeatCount="indefinite" />
              <animate attributeName="opacity" values="0.35;0;0.35" dur="2.8s" repeatCount="indefinite" />
            </circle>
          )}
          <circle cx={n.x} cy={n.y} r={n.r}
            fill={i === 7 ? `${C.teal}22` : C.card}
            stroke={n.color} strokeWidth={i === 7 ? 2.5 : 1.5} />
          {i === 7 && <text x={n.x} y={n.y + 4} textAnchor="middle" fill={C.teal} fontSize={7} fontWeight="700" fontFamily="DM Sans">ID</text>}
          <text x={n.x} y={n.y + n.r + 11} textAnchor="middle"
            fill={i === 7 ? C.teal : C.muted} fontSize={9} fontFamily="DM Sans" fontWeight={i === 7 ? "700" : "400"}>
            {n.label}
          </text>
        </g>
      ))}
    </svg>
  );
};

/* ═══════════════════ SCREENS ═══════════════════════════════════════════ */

const OverviewScreen = ({ nav }) => {
  const pipeline = [
    ["01","Ingest",    "Raw ID Onboarding",    C.gold  ],
    ["02","Normalise", "Schema Harmonisation", C.purple],
    ["03","Hash",      "PII Encryption",       C.blue  ],
    ["04","Graph",     "ID Resolution",        C.teal  ],
    ["05","Enrich",    "Audience Intel",       C.pink  ],
    ["06","Activate",  "Destination Push",     C.gold  ],
  ];
  return (
    <div>
      {/* Hero banner */}
      <div style={{ position: "relative", background: `linear-gradient(135deg, ${C.surface}, #060D18)`, border: `1px solid ${C.border}`, borderRadius: 16, padding: "34px 38px", marginBottom: 18, overflow: "hidden" }}>
        <div style={{ position: "absolute", top: 0, left: 0, right: 0, height: 2, background: `linear-gradient(90deg, transparent, ${C.gold}, ${C.teal}, transparent)` }} />
        <div style={{ maxWidth: 560 }}>
          <div style={{ color: C.gold, fontSize: 10, letterSpacing: 3, fontWeight: 700, marginBottom: 10 }}>SNOWFLAKE-NATIVE IDENTITY RESOLUTION</div>
          <div style={{ fontFamily: "'Cinzel', serif", fontSize: 28, fontWeight: 700, color: C.text, lineHeight: 1.2, marginBottom: 12 }}>
            The Identity Cloud<br /><span style={{ color: C.gold }}>for Saudi Arabia</span>
          </div>
          <div style={{ color: C.muted, fontSize: 13, lineHeight: 1.7, marginBottom: 22 }}>
            Onboard, resolve, and activate your customer identities across KSA's fastest-growing retail media ecosystem. Privacy-safe. PDPL-compliant. Built for Vision 2030.
          </div>
          <div style={{ display: "flex", gap: 10 }}>
            <button onClick={() => nav("onboard")} style={{ background: `linear-gradient(135deg, ${C.gold}, #8B6914)`, color: "#000", border: "none", borderRadius: 9, padding: "11px 24px", fontFamily: "'DM Sans', sans-serif", fontWeight: 700, fontSize: 13, cursor: "pointer" }}>Start Onboarding</button>
            <button onClick={() => nav("graph")} style={{ background: "transparent", color: C.teal, border: `1px solid ${C.teal}50`, borderRadius: 9, padding: "11px 22px", fontFamily: "'DM Sans', sans-serif", fontWeight: 600, fontSize: 13, cursor: "pointer" }}>View ID Graph</button>
          </div>
        </div>
        {/* Floating chart */}
        <div style={{ position: "absolute", right: 32, top: "50%", transform: "translateY(-50%)", display: "flex", flexDirection: "column", gap: 10 }}>
          <div style={{ background: C.card, border: `1px solid ${C.border}`, borderRadius: 10, padding: "12px 16px", minWidth: 200 }}>
            <div style={{ fontSize: 9, color: C.muted, letterSpacing: 1, fontWeight: 600, marginBottom: 8 }}>CHANNEL ROAS</div>
            <MiniBar data={[{l:"STC",v:7.1,color:"#7B2D8B"},{l:"Noon",v:6.2,color:C.gold},{l:"Snap",v:5.8,color:"#FFDD00"},{l:"DV360",v:4.4,color:"#4285F4"},{l:"Meta",v:3.9,color:"#0668E1"}]} height={52} />
          </div>
          <div style={{ background: C.card, border: `1px solid ${C.border}`, borderRadius: 10, padding: "12px 16px" }}>
            <div style={{ fontSize: 9, color: C.muted, letterSpacing: 1, fontWeight: 600, marginBottom: 6 }}>7-WEEK ROAS TREND</div>
            <Spark vals={[3.1,3.4,3.8,4.2,4.0,4.5,4.8]} color={C.teal} w={180} h={36} />
          </div>
        </div>
      </div>

      {/* KPIs */}
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 13, marginBottom: 18 }}>
        {[
          { value: "2.4B+", label: "IDs in Numad Graph",       sub: "Across GCC markets",    color: C.gold   },
          { value: "94.2%", label: "Average Match Rate",        sub: "Industry avg: 68%",     color: C.teal   },
          { value: "42",    label: "Activation Endpoints",      sub: "RMN + DSP networks",    color: C.purple },
          { value: "< 48h", label: "Time to First Activation",  sub: "From raw data upload",  color: C.blue   },
        ].map((m, i) => <MetricCard key={i} {...m} />)}
      </div>

      {/* Pipeline */}
      <Card style={{ marginBottom: 16 }}>
        <div style={{ color: C.muted, fontSize: 9, letterSpacing: 2, fontWeight: 700, marginBottom: 16 }}>END-TO-END IDENTITY PIPELINE</div>
        <div style={{ display: "flex", alignItems: "flex-start" }}>
          {pipeline.map(([num, label, sub, color], i) => (
            <div key={num} style={{ display: "flex", alignItems: "flex-start", flex: 1 }}>
              <div style={{ flex: 1, textAlign: "center" }}>
                <div style={{ width: 40, height: 40, borderRadius: 10, background: `${color}18`, border: `1.5px solid ${color}55`, display: "flex", alignItems: "center", justifyContent: "center", margin: "0 auto 8px", fontFamily: "'Cinzel', serif", fontSize: 12, fontWeight: 700, color }}>{num}</div>
                <div style={{ fontSize: 12, fontWeight: 700, color: C.text, marginBottom: 2 }}>{label}</div>
                <div style={{ fontSize: 10, color: C.muted }}>{sub}</div>
              </div>
              {i < 5 && <ArrowRight size={13} color={`${C.gold}55`} style={{ flexShrink: 0, marginTop: 14 }} />}
            </div>
          ))}
        </div>
      </Card>

      {/* Market tables */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 13 }}>
        <Card gold>
          <div style={{ color: C.gold, fontSize: 9, letterSpacing: 2, fontWeight: 700, marginBottom: 12 }}>KSA MARKET CONTEXT</div>
          {[["Internet users","36.9M"],["Mobile penetration","98.4%"],["E-commerce GMV (2024)","SAR 42B"],["Retail media ad spend","SAR 1.8B"],["Retail media YoY growth","+38%"]].map(([k,v]) => (
            <div key={k} style={{ display: "flex", justifyContent: "space-between", padding: "7px 0", borderBottom: `1px solid ${C.border}` }}>
              <span style={{ fontSize: 12, color: C.muted }}>{k}</span><span style={{ fontSize: 12, color: C.text, fontWeight: 700 }}>{v}</span>
            </div>
          ))}
        </Card>
        <Card teal>
          <div style={{ color: C.teal, fontSize: 9, letterSpacing: 2, fontWeight: 700, marginBottom: 12 }}>NUMAD ADVANTAGE</div>
          {[["Unique identifier types","11"],["Avg IDs per person","3.7"],["Deterministic match rate","94.2%"],["Saudi PDPL compliance","Certified"],["Data residency","KSA me-central-1"]].map(([k,v]) => (
            <div key={k} style={{ display: "flex", justifyContent: "space-between", padding: "7px 0", borderBottom: `1px solid ${C.border}` }}>
              <span style={{ fontSize: 12, color: C.muted }}>{k}</span><span style={{ fontSize: 12, color: C.text, fontWeight: 700 }}>{v}</span>
            </div>
          ))}
        </Card>
      </div>
    </div>
  );
};

const OnboardScreen = ({ nav }) => {
  const [step, setStep] = useState(0);
  const [sel, setSel] = useState([]);
  const [progress, setProgress] = useState(0);
  const [done, setDone] = useState(false);

  useEffect(() => {
    if (step === 3 && !done) {
      let p = 0;
      const iv = setInterval(() => { p += Math.random() * 9 + 3; if (p >= 100) { p = 100; setDone(true); clearInterval(iv); } setProgress(Math.min(p, 100)); }, 200);
      return () => clearInterval(iv);
    }
  }, [step]);

  const STEPS = ["Select Sources","Map Schema","Privacy Config","Ingest & Validate"];
  const TASKS = ["SHA-256 hashing applied to all PII fields","Identity spine building in Snowflake DCR","Cross-device graph stitching","Audience segmentation complete","Graph ready for activation"];

  return (
    <div>
      <SectionTitle label="STEP-BY-STEP WIZARD" title="Data Onboarding" sub="Connect your first-party data sources to the Numad Identity Graph on Snowflake" />
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", marginBottom: 28 }}>
        {STEPS.map((s, i) => (
          <div key={i} style={{ borderTop: `2px solid ${i <= step ? C.gold : C.border}`, paddingTop: 9, paddingRight: 10, transition: "border-color 0.3s" }}>
            <span style={{ fontSize: 12, fontWeight: 600, color: i < step ? C.teal : i === step ? C.gold : C.muted }}>
              {i < step ? "✓ " : `${i+1}. `}{s}
            </span>
          </div>
        ))}
      </div>

      {step === 0 && (
        <div>
          <div style={{ fontSize: 14, fontWeight: 600, color: C.text, marginBottom: 16 }}>Select your data sources</div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3,1fr)", gap: 12, marginBottom: 20 }}>
            {SOURCES.map(src => {
              const on = sel.includes(src.id);
              return (
                <div key={src.id} onClick={() => setSel(p => on ? p.filter(x => x !== src.id) : [...p, src.id])}
                  style={{ background: on ? `${C.gold}0D` : C.card, border: `1.5px solid ${on ? C.gold : C.border}`, borderRadius: 12, padding: "18px 20px", cursor: "pointer", transition: "all 0.2s", position: "relative" }}>
                  {on && <CheckCircle size={13} color={C.teal} style={{ position: "absolute", top: 12, right: 12 }} />}
                  <div style={{ background: `${C.gold}20`, border: `1px solid ${C.gold}35`, borderRadius: 7, padding: "4px 10px", fontSize: 11, fontFamily: "'Cinzel', serif", color: C.gold, fontWeight: 700, display: "inline-block", marginBottom: 10 }}>{src.tag}</div>
                  <div style={{ fontSize: 13, fontWeight: 700, color: C.text, marginBottom: 10 }}>{src.label}</div>
                  <div style={{ display: "flex", flexWrap: "wrap", gap: 5 }}>{src.fields.map(f => <Badge key={f} label={f} variant="muted" />)}</div>
                </div>
              );
            })}
          </div>
          {sel.length > 0 && <button onClick={() => setStep(1)} style={{ background: `linear-gradient(135deg, ${C.gold}, #8B6914)`, color: "#000", border: "none", borderRadius: 9, padding: "11px 26px", fontFamily: "'DM Sans', sans-serif", fontWeight: 700, fontSize: 13, cursor: "pointer" }}>Continue with {sel.length} source{sel.length > 1 ? "s" : ""} →</button>}
        </div>
      )}

      {step === 1 && (
        <div>
          <div style={{ fontSize: 14, fontWeight: 600, color: C.text, marginBottom: 16 }}>Map identity fields to Numad Universal Schema</div>
          <Card style={{ padding: 0, overflow: "hidden", marginBottom: 20 }}>
            <div style={{ display: "grid", gridTemplateColumns: "2fr 28px 2fr 2fr 1.4fr", background: C.surface, padding: "10px 20px", borderBottom: `1px solid ${C.border}` }}>
              {["Your Field","","Numad Field","Namespace","Type"].map((h, i) => <div key={i} style={{ fontSize: 10, color: C.muted, fontWeight: 700, letterSpacing: 0.8 }}>{h}</div>)}
            </div>
            {[["customer_email","email_hash","SHA256_EMAIL","Deterministic"],["mobile_number","phone_hash","SHA256_PHONE","Deterministic"],["user_id","brand_id","BRAND_NS","Deterministic"],["device_uuid","device_id","IDFA_GAID","Probabilistic"],["loyalty_card_no","loyalty_id","LOYALTY_NS","Deterministic"]].map(([y,n,ns,t],i) => (
              <div key={i} style={{ display: "grid", gridTemplateColumns: "2fr 28px 2fr 2fr 1.4fr", padding: "11px 20px", borderBottom: `1px solid ${C.border}`, alignItems: "center" }}>
                <code style={{ background: C.surface, color: C.teal, padding: "3px 7px", borderRadius: 4, fontSize: 11, border: `1px solid ${C.border}` }}>{y}</code>
                <ArrowRight size={12} color={C.gold} />
                <span style={{ fontSize: 12, color: C.teal, fontWeight: 600 }}>{n}</span>
                <code style={{ background: `${C.teal}12`, color: C.teal, padding: "3px 7px", borderRadius: 4, fontSize: 11, border: `1px solid ${C.teal}30` }}>{ns}</code>
                <Badge label={t} variant={t === "Deterministic" ? "teal" : "muted"} />
              </div>
            ))}
          </Card>
          <div style={{ display: "flex", gap: 10 }}>
            <button onClick={() => setStep(0)} style={{ background: "transparent", color: C.muted, border: `1px solid ${C.border}`, borderRadius: 9, padding: "10px 22px", fontFamily: "'DM Sans', sans-serif", fontWeight: 600, fontSize: 13, cursor: "pointer" }}>Back</button>
            <button onClick={() => setStep(2)} style={{ background: `linear-gradient(135deg, ${C.gold}, #8B6914)`, color: "#000", border: "none", borderRadius: 9, padding: "10px 26px", fontFamily: "'DM Sans', sans-serif", fontWeight: 700, fontSize: 13, cursor: "pointer" }}>Confirm Mapping →</button>
          </div>
        </div>
      )}

      {step === 2 && (
        <div>
          <div style={{ fontSize: 14, fontWeight: 600, color: C.text, marginBottom: 16 }}>Privacy & Compliance Configuration</div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginBottom: 20 }}>
            {[["Differential Privacy","Adds calibrated noise to results, preventing reverse-engineering of individual records.","PDPL Required"],["Aggregation Threshold","Minimum cohort size (k≥50) before segment data is surfaced to any partner.","Default: 50"],["Hashing Protocol","SHA-256 with HMAC salt on all PII fields before entering the Snowflake clean room.","SHA-256 + HMAC"],["Saudi PDPL Compliance","Full alignment with the Saudi PDPL and SDAIA framework requirements.","Certified"],["Data Residency — KSA","All compute and storage within Saudi Arabia. Snowflake me-central-1 (Riyadh).","KSA Local"],["Purpose Limitation","Data usage contractually restricted to declared activation purposes only.","Enforced"]].map(([t, d, b]) => (
              <Card key={t} teal style={{ padding: "16px 20px" }}>
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 6 }}>
                  <span style={{ fontSize: 13, fontWeight: 700, color: C.text }}>{t}</span>
                  <Badge label={b} variant="teal" />
                </div>
                <div style={{ fontSize: 11, color: C.muted, lineHeight: 1.6 }}>{d}</div>
              </Card>
            ))}
          </div>
          <div style={{ display: "flex", gap: 10 }}>
            <button onClick={() => setStep(1)} style={{ background: "transparent", color: C.muted, border: `1px solid ${C.border}`, borderRadius: 9, padding: "10px 22px", fontFamily: "'DM Sans', sans-serif", fontWeight: 600, fontSize: 13, cursor: "pointer" }}>Back</button>
            <button onClick={() => setStep(3)} style={{ background: `linear-gradient(135deg, ${C.gold}, #8B6914)`, color: "#000", border: "none", borderRadius: 9, padding: "10px 26px", fontFamily: "'DM Sans', sans-serif", fontWeight: 700, fontSize: 13, cursor: "pointer" }}>Start Ingestion →</button>
          </div>
        </div>
      )}

      {step === 3 && !done && (
        <div style={{ textAlign: "center", padding: "20px 0" }}>
          <RefreshCw size={38} color={C.gold} style={{ marginBottom: 18, animation: "spin 1.1s linear infinite" }} />
          <style>{`@keyframes spin{to{transform:rotate(360deg)}}`}</style>
          <div style={{ fontFamily: "'Cinzel', serif", fontSize: 20, color: C.text, marginBottom: 6 }}>Ingesting & Resolving Identities</div>
          <div style={{ color: C.muted, fontSize: 13, marginBottom: 26 }}>Snowflake native pipeline running inside your clean room</div>
          <div style={{ maxWidth: 440, margin: "0 auto" }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 5 }}>
              <span style={{ fontSize: 12, color: C.muted }}>Processing</span>
              <span style={{ fontSize: 12, color: C.gold, fontWeight: 700 }}>{Math.round(progress)}%</span>
            </div>
            <div style={{ height: 7, background: C.border, borderRadius: 4, overflow: "hidden", marginBottom: 22 }}>
              <div style={{ height: "100%", width: `${progress}%`, background: `linear-gradient(90deg,${C.gold},${C.teal})`, borderRadius: 4, transition: "width 0.25s" }} />
            </div>
            {TASKS.map((t, i) => (
              <div key={i} style={{ display: "flex", alignItems: "center", gap: 10, padding: "7px 0", textAlign: "left" }}>
                {progress > (i + 1) / TASKS.length * 100 ? <CheckCircle size={15} color={C.teal} /> : <Circle size={15} color={C.border} />}
                <span style={{ fontSize: 12, color: progress > (i + 1) / TASKS.length * 100 ? C.text : C.muted }}>{t}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {done && (
        <div style={{ textAlign: "center", padding: "18px 0" }}>
          <div style={{ width: 62, height: 62, borderRadius: "50%", background: `${C.teal}20`, border: `2px solid ${C.teal}`, margin: "0 auto 18px", display: "flex", alignItems: "center", justifyContent: "center" }}>
            <CheckCircle size={26} color={C.teal} />
          </div>
          <div style={{ fontFamily: "'Cinzel', serif", color: C.teal, fontSize: 22, marginBottom: 8 }}>Identity Graph Ready</div>
          <div style={{ color: C.muted, fontSize: 13, maxWidth: 420, margin: "0 auto 26px", lineHeight: 1.65 }}>Your data has been ingested, resolved, and graphed inside the Numad clean room on Snowflake.</div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 11, maxWidth: 540, margin: "0 auto 26px" }}>
            {[["4.2M","IDs Onboarded"],["3.96M","Resolved IDs"],["94.2%","Match Rate"],["12","Segments"]].map(([v,l]) => (
              <div key={l} style={{ textAlign: "center", background: C.card, border: `1px solid ${C.border}`, borderRadius: 10, padding: "13px 8px" }}>
                <div style={{ fontFamily: "'Cinzel', serif", fontSize: 21, color: C.gold }}>{v}</div>
                <div style={{ fontSize: 10, color: C.muted, marginTop: 4 }}>{l}</div>
              </div>
            ))}
          </div>
          <div style={{ display: "flex", gap: 10, justifyContent: "center" }}>
            <button onClick={() => nav("graph")} style={{ background: "transparent", color: C.teal, border: `1px solid ${C.teal}50`, borderRadius: 9, padding: "10px 22px", fontFamily: "'DM Sans', sans-serif", fontWeight: 600, fontSize: 13, cursor: "pointer" }}>View Identity Graph</button>
            <button onClick={() => nav("activate")} style={{ background: `linear-gradient(135deg, ${C.gold}, #8B6914)`, color: "#000", border: "none", borderRadius: 9, padding: "10px 26px", fontFamily: "'DM Sans', sans-serif", fontWeight: 700, fontSize: 13, cursor: "pointer" }}>Activate Audiences →</button>
          </div>
        </div>
      )}
    </div>
  );
};

const GraphScreen = ({ nav }) => {
  const [animated, setAnimated] = useState(false);
  useEffect(() => { const t = setTimeout(() => setAnimated(true), 350); return () => clearTimeout(t); }, []);
  return (
    <div>
      <SectionTitle label="NUMAD GRAPH ENGINE v3.2 — SNOWFLAKE NATIVE" title="Identity Graph" sub="Cross-device, cross-channel identity resolution for the Saudi market" />
      <div style={{ display: "grid", gridTemplateColumns: "3fr 2fr", gap: 16, marginBottom: 16 }}>
        <Card>
          <div style={{ color: C.muted, fontSize: 9, letterSpacing: 2, fontWeight: 700, marginBottom: 14 }}>IDENTITY RESOLUTION NETWORK</div>
          <IDGraphSVG animate={animated} />
        </Card>
        <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
          <Card>
            <div style={{ color: C.muted, fontSize: 9, letterSpacing: 2, fontWeight: 700, marginBottom: 12 }}>GRAPH STATISTICS</div>
            {[["Total Identities","4.2M",C.gold],["Resolved Persons","3.96M",C.teal],["Avg IDs / Person","3.7",C.text],["Deterministic Links","94.2%",C.gold],["Cross-Device Match","81.4%",C.text]].map(([k,v,c]) => (
              <div key={k} style={{ display: "flex", justifyContent: "space-between", padding: "7px 0", borderBottom: `1px solid ${C.border}` }}>
                <span style={{ fontSize: 12, color: C.muted }}>{k}</span>
                <span style={{ fontFamily: "'Cinzel', serif", fontSize: 13, color: c, fontWeight: 700 }}>{v}</span>
              </div>
            ))}
          </Card>
          <Card>
            <div style={{ color: C.muted, fontSize: 9, letterSpacing: 2, fontWeight: 700, marginBottom: 12 }}>ID SIGNAL COVERAGE</div>
            <ProgBar pct={78} color={C.gold}   label="Email"        />
            <ProgBar pct={64} color={C.teal}   label="Mobile"       />
            <ProgBar pct={52} color={C.purple} label="Device ID"    />
            <ProgBar pct={41} color={C.blue}   label="Loyalty Card" />
          </Card>
        </div>
      </div>

      {/* Signal health donuts */}
      <Card style={{ marginBottom: 16 }}>
        <div style={{ color: C.muted, fontSize: 9, letterSpacing: 2, fontWeight: 700, marginBottom: 14 }}>IDENTITY SIGNAL HEALTH</div>
        <div style={{ display: "flex", gap: 28, alignItems: "flex-start" }}>
          <Donut pct={94} color={C.gold}   label="Match Rate"   />
          <Donut pct={81} color={C.teal}   label="Cross-Device" />
          <Donut pct={76} color={C.purple} label="Email Reach"  />
          <Donut pct={64} color={C.blue}   label="Mobile"       />
          <Donut pct={89} color={C.pink}   label="Deterministic"/>
          <div style={{ flex: 1, borderLeft: `1px solid ${C.border}`, paddingLeft: 22 }}>
            <div style={{ fontSize: 11, color: C.muted, marginBottom: 8 }}>Graph last refreshed</div>
            <div style={{ fontFamily: "'Cinzel', serif", fontSize: 14, color: C.text, marginBottom: 4 }}>Daily at 02:00 AST</div>
            <div style={{ color: C.muted, fontSize: 11, marginBottom: 12 }}>Next refresh in 6h 42m</div>
            <Badge label="PDPL Compliant" variant="teal" />
          </div>
        </div>
      </Card>

      <div style={{ color: C.text, fontSize: 13, fontWeight: 700, letterSpacing: 0.4, marginBottom: 13 }}>RESOLVED AUDIENCE SEGMENTS</div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 10 }}>
        {SEGMENTS.map((seg, i) => (
          <div key={i} onClick={() => nav("activate")} style={{ background: C.card, border: `1px solid ${C.border}`, borderLeft: `3px solid ${seg.color}`, borderRadius: 10, padding: "13px 15px", cursor: "pointer" }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 7 }}>
              <span style={{ fontSize: 11, fontWeight: 700, color: C.text, lineHeight: 1.3 }}>{seg.name}</span>
              <span style={{ fontSize: 10, color: seg.color, fontWeight: 700, background: `${seg.color}18`, borderRadius: 3, padding: "1px 5px" }}>{seg.score}</span>
            </div>
            <div style={{ fontFamily: "'Cinzel', serif", fontSize: 19, color: seg.color, fontWeight: 700 }}>{seg.size}</div>
            <div style={{ fontSize: 10, color: C.teal, marginTop: 5 }}>Activate →</div>
          </div>
        ))}
      </div>
    </div>
  );
};

const ActivateScreen = () => {
  const [sel, setSel] = useState([]);
  const [tab, setTab] = useState("rmn");
  const toggle = name => setSel(p => p.includes(name) ? p.filter(x => x !== name) : [...p, name]);
  return (
    <div>
      <SectionTitle label="PRIVACY-SAFE AUDIENCE ACTIVATION" title="Activation Hub" sub="Push resolved audiences to retail media networks and ad tech platforms — no raw data leaves the clean room." />
      <div style={{ display: "flex", borderBottom: `1px solid ${C.border}`, marginBottom: 18 }}>
        {[["rmn","Retail Media Networks"],["dsp","DSP & Ad Tech Platforms"]].map(([id, label]) => (
          <button key={id} onClick={() => setTab(id)} style={{ background: "transparent", border: "none", borderBottom: `2px solid ${tab === id ? C.gold : "transparent"}`, color: tab === id ? C.gold : C.muted, padding: "9px 22px", fontFamily: "'DM Sans', sans-serif", fontWeight: 600, fontSize: 13, cursor: "pointer" }}>{label}</button>
        ))}
      </div>
      <Card style={{ padding: "0 20px" }}>
        {(tab === "rmn" ? RMN : DSP).map((p, i) => {
          const on = sel.includes(p.name);
          return (
            <div key={i} style={{ display: "grid", gridTemplateColumns: "12px 2fr 1.6fr 2fr 88px", gap: 14, padding: "12px 0", borderBottom: `1px solid ${C.border}`, alignItems: "center" }}>
              <div style={{ width: 9, height: 9, borderRadius: "50%", background: p.color }} />
              <div>
                <div style={{ fontSize: 13, fontWeight: 700, color: C.text }}>{p.name}</div>
                <div style={{ fontSize: 11, color: C.muted }}>{p.desc}</div>
              </div>
              <div style={{ fontSize: 11, color: C.muted }}>{p.reach}</div>
              <div style={{ display: "flex", gap: 5, flexWrap: "wrap" }}>
                {tab === "rmn"
                  ? <><Badge label="DCR-Ready" variant="teal" /><Badge label={p.format} variant="muted" /></>
                  : <><Badge label={p.type} variant="muted" /><Badge label={p.signal} variant="teal" /></>}
              </div>
              <button onClick={() => toggle(p.name)} style={{ background: on ? `${C.gold}18` : "transparent", color: on ? C.gold : C.muted, border: `1px solid ${on ? C.gold : C.border}`, borderRadius: 7, padding: "6px 14px", fontSize: 12, fontFamily: "'DM Sans', sans-serif", fontWeight: 600, cursor: "pointer", transition: "all 0.18s" }}>
                {on ? "Selected" : "Select"}
              </button>
            </div>
          );
        })}
      </Card>
      {sel.length > 0 && (
        <Card gold style={{ marginTop: 16 }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
            <div>
              <div style={{ fontSize: 15, fontWeight: 700, color: C.text, marginBottom: 4 }}>{sel.length} destination{sel.length > 1 ? "s" : ""} selected</div>
              <div style={{ fontSize: 12, color: C.muted }}>Hashed audiences pushed via Snowflake DCR — zero raw data exposure</div>
            </div>
            <button style={{ background: `linear-gradient(135deg, ${C.gold}, #8B6914)`, color: "#000", border: "none", borderRadius: 9, padding: "12px 26px", fontFamily: "'DM Sans', sans-serif", fontWeight: 700, fontSize: 14, cursor: "pointer" }}>Launch Activation</button>
          </div>
          <div style={{ display: "flex", gap: 7, flexWrap: "wrap" }}>{sel.map(d => <Badge key={d} label={d} variant="gold" />)}</div>
        </Card>
      )}
    </div>
  );
};

const IntelligenceScreen = () => {
  const channels = [
    { name: "STC Ads",           roas: 7.1, reach: "1.2M",  color: "#7B2D8B" },
    { name: "Noon RMN",          roas: 6.2, reach: "2.1M",  color: C.gold    },
    { name: "Snapchat KSA",      roas: 5.8, reach: "3.4M",  color: "#FFDD00" },
    { name: "Google DV360",      roas: 4.4, reach: "4.2M",  color: "#4285F4" },
    { name: "Meta MENA",         roas: 3.9, reach: "5.1M",  color: "#0668E1" },
  ];
  const maxR = Math.max(...channels.map(c => c.roas));
  return (
    <div>
      <SectionTitle label="CLOSED-LOOP MEASUREMENT" title="Audience Intelligence" sub="Incrementality reporting and campaign measurement — computed inside Snowflake, no raw data shared." />
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4,1fr)", gap: 13, marginBottom: 18 }}>
        {[
          { value: "8.9M",      label: "Total Reach",         sub: "+14.2% vs prior",  color: C.gold   },
          { value: "142K",      label: "Matched Conversions", sub: "+28.4% vs prior",  color: C.teal   },
          { value: "4.8x",      label: "Incremental ROAS",    sub: "+0.6x vs prior",   color: C.purple },
          { value: "SAR 14.2M", label: "Incremental Revenue", sub: "Attribution: 84%", color: C.pink   },
        ].map((m, i) => <MetricCard key={i} {...m} />)}
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
        <Card>
          <div style={{ color: C.muted, fontSize: 9, letterSpacing: 2, fontWeight: 700, marginBottom: 14 }}>ROAS BY CHANNEL</div>
          {channels.map((ch, i) => (
            <div key={i} style={{ marginBottom: 13 }}>
              <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 5 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 7 }}>
                  <div style={{ width: 7, height: 7, borderRadius: "50%", background: ch.color }} />
                  <span style={{ fontSize: 12, color: C.text }}>{ch.name}</span>
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
                  <span style={{ fontSize: 11, color: C.muted }}>{ch.reach}</span>
                  <span style={{ fontFamily: "'Cinzel', serif", fontSize: 13, color: ch.color, fontWeight: 700 }}>{ch.roas}x</span>
                </div>
              </div>
              <div style={{ height: 5, background: C.border, borderRadius: 3, overflow: "hidden" }}>
                <div style={{ height: "100%", width: `${(ch.roas / maxR) * 100}%`, background: ch.color, opacity: 0.8, borderRadius: 3 }} />
              </div>
            </div>
          ))}
          <Divider margin="16px 0 12px" />
          <div style={{ fontSize: 10, color: C.muted, marginBottom: 6 }}>ROAS TREND (7 WEEKS)</div>
          <Spark vals={[3.1,3.4,3.8,4.2,4.0,4.5,4.8]} color={C.teal} w={200} h={38} />
        </Card>
        <Card>
          <div style={{ color: C.muted, fontSize: 9, letterSpacing: 2, fontWeight: 700, marginBottom: 14 }}>INCREMENTALITY MEASUREMENT</div>
          {[["Incremental Conversions","38,420","84.7% of total"],["Incremental Revenue","SAR 14.2M","Attributed to Numad"],["True Lift","+22.4%","vs holdout group"],["Break-even ROAS","1.4x","vs actual 4.8x"],["iROAS","4.1x","Incremental return"]].map(([label, value, note]) => (
            <div key={label} style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", padding: "10px 0", borderBottom: `1px solid ${C.border}` }}>
              <div>
                <div style={{ fontSize: 12, color: C.muted }}>{label}</div>
                <div style={{ fontSize: 10, color: C.border, marginTop: 2 }}>{note}</div>
              </div>
              <div style={{ fontFamily: "'Cinzel', serif", fontSize: 16, color: C.teal, fontWeight: 700 }}>{value}</div>
            </div>
          ))}
          <div style={{ marginTop: 14, background: `${C.teal}0E`, border: `1px solid ${C.teal}30`, borderRadius: 8, padding: "10px 13px", fontSize: 11, color: C.teal, lineHeight: 1.6, display: "flex", gap: 8 }}>
            <Lock size={12} style={{ flexShrink: 0, marginTop: 1 }} />
            Measurement computed inside Snowflake DCR. No raw conversion data shared with any measurement partner.
          </div>
        </Card>
      </div>
    </div>
  );
};

const TechSpecScreen = () => {
  const [tab, setTab] = useState("arch");
  const YAML = `# Numad.AI — Snowflake DCR Collaboration Spec v2.4
# Region: AWS me-central-1 (Riyadh) | PDPL Compliant

collaboration:
  name: numad_identity_cloud_collab
  version: "2.4"
  region: aws_me_central_1
  compliance: [saudi_pdpl, sdaia_framework]
  data_residency: ksa_only

identity_resolution:
  namespaces:
    - { id: SHA256_EMAIL,  type: deterministic }
    - { id: SHA256_PHONE,  type: deterministic }
    - { id: BRAND_NS,      type: deterministic }
    - { id: IDFA_GAID,     type: probabilistic }
    - { id: LOYALTY_NS,    type: deterministic }

privacy_controls:
  differential_privacy:
    enabled: true
    epsilon: 1.0
    mechanism: gaussian_noise
  aggregation_threshold:
    minimum_group_size: 50
  hashing:
    algorithm: sha256
    salt: hmac_sha256
  purpose_limitation:
    allowed_purposes: [audience_matching, measurement, lookalike]
    enforce: true

templates:
  - name: audience_overlap
    output: [overlap_count, overlap_pct]
    privacy: aggregated_only
  - name: campaign_attribution
    output: [matched_conversions, roas, iroas]
    privacy: aggregated_only
  - name: incrementality_measurement
    output: [true_lift_pct, confidence_interval]
    privacy: differential_privacy
  - name: lookalike_expansion
    output: [lookalike_ids, similarity_scores]
    privacy: k_anonymity_50

activation:
  transfer_method: hashed_match_keys_only
  raw_data_exposure: false
  audit_log: enabled`;

  return (
    <div>
      <SectionTitle label="SNOWFLAKE DCR COLLABORATION SPEC" title="Technical Specification" sub="Architecture, collaboration YAML, and API reference for Numad Identity Cloud" />
      <div style={{ display: "flex", borderBottom: `1px solid ${C.border}`, marginBottom: 20 }}>
        {[["arch","Architecture"],["yaml","DCR YAML"],["api","API Reference"]].map(([id,label]) => (
          <button key={id} onClick={() => setTab(id)} style={{ background: "transparent", border: "none", borderBottom: `2px solid ${tab === id ? C.gold : "transparent"}`, color: tab === id ? C.gold : C.muted, padding: "9px 22px", fontFamily: "'DM Sans', sans-serif", fontWeight: 600, fontSize: 13, cursor: "pointer" }}>{label}</button>
        ))}
      </div>

      {tab === "arch" && (
        <div>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14, marginBottom: 14 }}>
            <Card gold>
              <div style={{ color: C.gold, fontSize: 9, letterSpacing: 2, fontWeight: 700, marginBottom: 12 }}>DATA LAYER — SNOWFLAKE</div>
              {[["Clean Room","Snowflake Native DCR"],["Region","AWS me-central-1 (Riyadh)"],["Hashing","SHA-256 + HMAC-SHA256"],["Privacy","Differential Privacy (ε=1.0)"],["Threshold","Aggregation k≥50"],["Compliance","Saudi PDPL / SDAIA"],["Residency","KSA local, no cross-border"]].map(([k,v]) => (
                <div key={k} style={{ display: "flex", justifyContent: "space-between", padding: "6px 0", borderBottom: `1px solid ${C.border}` }}>
                  <span style={{ fontSize: 12, color: C.muted }}>{k}</span><span style={{ fontSize: 12, color: C.text, fontWeight: 600 }}>{v}</span>
                </div>
              ))}
            </Card>
            <Card teal>
              <div style={{ color: C.teal, fontSize: 9, letterSpacing: 2, fontWeight: 700, marginBottom: 12 }}>IDENTITY NAMESPACES</div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 50px", marginBottom: 6 }}>
                {["Namespace","Type","Cov."].map(h => <span key={h} style={{ fontSize: 10, color: C.muted, fontWeight: 700 }}>{h}</span>)}
              </div>
              {[["SHA256_EMAIL","Deterministic","78%"],["SHA256_PHONE","Deterministic","64%"],["BRAND_NS","Deterministic","100%"],["IDFA_GAID","Probabilistic","52%"],["LOYALTY_NS","Deterministic","41%"],["UID2","Deterministic","35%"],["MAID","Probabilistic","48%"]].map(([ns,t,c]) => (
                <div key={ns} style={{ display: "grid", gridTemplateColumns: "1fr 1fr 50px", padding: "6px 0", borderBottom: `1px solid ${C.border}`, alignItems: "center" }}>
                  <code style={{ fontSize: 10, color: C.teal, background: `${C.teal}12`, padding: "2px 6px", borderRadius: 3, display: "inline-block" }}>{ns}</code>
                  <span style={{ fontSize: 11, color: C.muted }}>{t}</span>
                  <span style={{ fontSize: 12, color: C.text, fontWeight: 700 }}>{c}</span>
                </div>
              ))}
            </Card>
          </div>
          <Card>
            <div style={{ color: C.muted, fontSize: 9, letterSpacing: 2, fontWeight: 700, marginBottom: 14 }}>END-TO-END DATA FLOW</div>
            <div style={{ display: "flex", alignItems: "center" }}>
              {[["01","Ingest","Raw 1P data",C.gold],["02","Normalise","Schema map",C.purple],["03","Hash","SHA-256 PII",C.blue],["04","Graph","ID resolution",C.teal],["05","Enrich","Segmentation",C.pink],["06","Activate","DCR push",C.gold]].map(([n,s,sub,col],i,arr) => (
                <div key={n} style={{ display: "flex", alignItems: "center", flex: i < arr.length-1 ? "1 1 0" : "0 0 auto" }}>
                  <div style={{ background: C.surface, border: `1px solid ${C.border}`, borderTop: `2px solid ${col}`, borderRadius: 8, padding: "10px 8px", textAlign: "center", minWidth: 74 }}>
                    <div style={{ fontFamily: "'Cinzel', serif", fontSize: 10, color: col, fontWeight: 700, marginBottom: 3 }}>{n}</div>
                    <div style={{ fontSize: 11, color: C.text, fontWeight: 700 }}>{s}</div>
                    <div style={{ fontSize: 9, color: C.muted }}>{sub}</div>
                  </div>
                  {i < arr.length-1 && <ArrowRight size={12} color={`${C.gold}50`} style={{ flexShrink: 0, margin: "0 3px" }} />}
                </div>
              ))}
            </div>
          </Card>
        </div>
      )}

      {tab === "yaml" && (
        <div style={{ background: C.surface, border: `1px solid ${C.border}`, borderRadius: 12, overflow: "hidden" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "9px 18px", borderBottom: `1px solid ${C.border}`, background: C.card }}>
            <div style={{ display: "flex", gap: 5 }}>
              {["#E8453C",C.gold,C.teal].map(c => <div key={c} style={{ width: 9, height: 9, borderRadius: "50%", background: c }} />)}
            </div>
            <span style={{ fontSize: 11, color: C.muted }}>numad_dcr_collaboration_spec.yaml</span>
            <Badge label="YAML" variant="muted" />
          </div>
          <pre style={{ padding: "20px 24px", margin: 0, fontFamily: "monospace", fontSize: 12, color: C.text, lineHeight: 1.7, maxHeight: 420, overflowY: "auto" }}>
            {YAML.split("\n").map((line, i) => {
              const isComment = line.trim().startsWith("#");
              const isKey = /^\s*[\w_-]+:/.test(line) && !isComment;
              return (
                <div key={i} style={{ color: isComment ? C.muted : isKey ? C.goldLt : C.teal }}>
                  {line}
                </div>
              );
            })}
          </pre>
        </div>
      )}

      {tab === "api" && (
        <Card>
          <div style={{ color: C.gold, fontSize: 9, letterSpacing: 2, fontWeight: 700, marginBottom: 16 }}>REST API ENDPOINTS</div>
          <div style={{ display: "grid", gridTemplateColumns: "72px 2fr 2fr" }}>
            {["Method","Endpoint","Description"].map(h => (
              <div key={h} style={{ fontSize: 10, color: C.muted, fontWeight: 700, letterSpacing: 0.8, padding: "7px 0", borderBottom: `1px solid ${C.border}` }}>{h}</div>
            ))}
            {[["POST","/v1/onboard/initiate","Initiate data onboarding job"],["POST","/v1/onboard/schema-map","Submit field mapping configuration"],["GET","/v1/graph/stats","Retrieve identity graph statistics"],["GET","/v1/graph/segments","List resolved audience segments"],["POST","/v1/activate","Push audience to destination endpoint"],["GET","/v1/measure/roas","Retrieve closed-loop ROAS report"],["GET","/v1/measure/incrementality","Get incrementality measurement"],["POST","/v1/dcr/run-template","Execute a DCR analysis template"]].map(([m,ep,desc],i) => (
              <div key={i} style={{ display: "contents" }}>
                <div style={{ padding: "10px 0", borderBottom: `1px solid ${C.border}` }}><Badge label={m} variant={m==="POST"?"teal":"gold"} /></div>
                <div style={{ padding: "10px 0", borderBottom: `1px solid ${C.border}` }}><code style={{ background: C.surface, color: C.teal, padding: "3px 7px", borderRadius: 4, fontSize: 11, border: `1px solid ${C.border}` }}>{ep}</code></div>
                <div style={{ padding: "10px 0", borderBottom: `1px solid ${C.border}`, fontSize: 12, color: C.muted }}>{desc}</div>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
};

/* ═══════════════════ APP SHELL ══════════════════════════════════════════ */
export default function NumadApp() {
  const [page, setPage] = useState("overview");
  const screens = {
    overview:     <OverviewScreen nav={setPage} />,
    onboard:      <OnboardScreen nav={setPage} />,
    graph:        <GraphScreen nav={setPage} />,
    activate:     <ActivateScreen />,
    intelligence: <IntelligenceScreen />,
    techspec:     <TechSpecScreen />,
  };

  return (
    <div style={{ display: "flex", height: "100vh", background: C.bg, fontFamily: "'DM Sans', sans-serif", overflow: "hidden" }}>
      <style>{`@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=DM+Sans:wght@400;500;600;700&display=swap');*{box-sizing:border-box;margin:0;padding:0}::-webkit-scrollbar{width:5px}::-webkit-scrollbar-track{background:${C.bg}}::-webkit-scrollbar-thumb{background:${C.border};border-radius:3px}`}</style>

      {/* ── SIDEBAR ── */}
      <div style={{ width: 210, background: C.surface, borderRight: `1px solid ${C.border}`, display: "flex", flexDirection: "column", flexShrink: 0, overflowY: "auto" }}>
        {/* Logo */}
        <div style={{ padding: "20px 18px 16px" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 9, marginBottom: 8 }}>
            <div style={{ width: 30, height: 30, background: `linear-gradient(135deg, ${C.gold}, ${C.teal})`, borderRadius: 7, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
              <span style={{ fontFamily: "'Cinzel', serif", fontSize: 14, fontWeight: 900, color: "#000" }}>N</span>
            </div>
            <span style={{ fontFamily: "'Cinzel', serif", fontSize: 14, fontWeight: 700, color: C.text, letterSpacing: 1 }}>
              NUMAD<span style={{ color: C.gold }}>.AI</span>
            </span>
          </div>
          <div style={{ background: C.card, border: `1px solid ${C.border}`, borderRadius: 5, padding: "2px 9px", fontSize: 8, color: C.muted, letterSpacing: 2, fontWeight: 600, display: "inline-block" }}>IDENTITY CLOUD</div>
        </div>

        {/* Nav */}
        <div style={{ padding: "0 10px" }}>
          <div style={{ fontSize: 8, color: C.muted, letterSpacing: 2, fontWeight: 700, padding: "0 8px 8px" }}>NAVIGATION</div>
          {NAV.map(({ id, short, Icon }) => {
            const active = page === id;
            return (
              <button key={id} onClick={() => setPage(id)} style={{ display: "flex", alignItems: "center", gap: 9, width: "100%", padding: "8px 10px", border: "none", borderRadius: 7, cursor: "pointer", textAlign: "left", marginBottom: 2, transition: "all 0.15s", background: active ? `${C.gold}14` : "transparent", borderLeft: `3px solid ${active ? C.gold : "transparent"}`, color: active ? C.gold : C.muted }}>
                <Icon size={14} />
                <span style={{ fontSize: 12, fontWeight: active ? 700 : 500 }}>{short}</span>
                {active && <ChevronRight size={11} style={{ marginLeft: "auto" }} />}
              </button>
            );
          })}
        </div>

        {/* Sidebar visuals */}
        <div style={{ padding: "14px 14px 18px", marginTop: "auto" }}>
          <Divider margin="0 0 14px" />

          {/* Donut graph health */}
          <div style={{ background: C.card, border: `1px solid ${C.border}`, borderRadius: 10, padding: "13px 14px", marginBottom: 10 }}>
            <div style={{ fontSize: 8, color: C.muted, letterSpacing: 2, fontWeight: 700, marginBottom: 10 }}>GRAPH HEALTH</div>
            <div style={{ display: "flex", alignItems: "center", gap: 12, marginBottom: 12 }}>
              <Donut pct={94} color={C.teal} size={54} />
              <div>
                <div style={{ fontFamily: "'Cinzel', serif", fontSize: 18, color: C.gold, fontWeight: 700 }}>4.2M</div>
                <div style={{ fontSize: 10, color: C.muted }}>Resolved IDs</div>
              </div>
            </div>
            <ProgBar pct={78} color={C.gold} label="Email" />
            <ProgBar pct={64} color={C.teal} label="Mobile" />
          </div>

          {/* Mini ROAS sparkline */}
          <div style={{ background: C.card, border: `1px solid ${C.border}`, borderRadius: 10, padding: "12px 14px", marginBottom: 10 }}>
            <div style={{ fontSize: 8, color: C.muted, letterSpacing: 2, fontWeight: 700, marginBottom: 8 }}>iROAS TREND</div>
            <Spark vals={[3.1,3.4,3.8,4.2,4.0,4.5,4.8]} color={C.teal} w={160} h={32} />
            <div style={{ display: "flex", justifyContent: "space-between", marginTop: 6 }}>
              <span style={{ fontSize: 9, color: C.muted }}>7 weeks</span>
              <span style={{ fontFamily: "'Cinzel', serif", fontSize: 13, color: C.gold, fontWeight: 700 }}>4.8x</span>
            </div>
          </div>

          {/* Snowflake status */}
          <div style={{ background: C.card, border: `1px solid ${C.border}`, borderRadius: 10, padding: "11px 14px" }}>
            <div style={{ fontSize: 8, color: C.muted, letterSpacing: 2, fontWeight: 700, marginBottom: 8 }}>SNOWFLAKE STATUS</div>
            {[["Clean Room Active",true],["DCR Spec v2.4",true],["me-central-1 KSA",true],["PDPL Certified",true]].map(([label, ok]) => (
              <div key={label} style={{ display: "flex", alignItems: "center", gap: 7, marginBottom: 6 }}>
                <div style={{ width: 5, height: 5, borderRadius: "50%", background: ok ? C.teal : C.gold, flexShrink: 0 }} />
                <span style={{ fontSize: 10, color: C.text }}>{label}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* ── MAIN ── */}
      <div style={{ flex: 1, overflowY: "auto", padding: "30px 34px" }}>
        {screens[page]}
      </div>
    </div>
  );
}

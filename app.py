import React, { useEffect, useState } from "react";

// Dara Investor Platform — Professional single-file React component
// Tailwind CSS is expected to be available in the host app.
// Purpose: clean, professional investor-facing dashboard that:
// - Shows projects and downloads
// - Presents master deck
// - Provides an AI chat panel (hook points for OpenAI integration)
// - Supports Arabic/English labels and simple branding
// - Includes notes for connecting storage / OpenAI keys

// USAGE NOTES (place in your README / env):
// - Provide file URLs (S3 signed URLs, or your server endpoints). Replace sandbox: links.
// - To integrate OpenAI Chat/Realtime: connect your server-side endpoint that proxies requests
//   and injects OPENAI_API_KEY securely. Call that endpoint from sendMessageToAI() below.
// - For production file downloads use signed URLs and avoid direct filesystem links.

const BRAND = {
  name: "Dara",
  colors: {
    primary: "bg-blue-600",
    accent: "text-blue-600",
  },
  logoAlt: "Dara logo",
};

const initialProjects = [
  {
    id: "kyc",
    title: "KYC Initiative",
    tagline: "AI-Enhanced Sudan Digital Identity",
    description:
      "نظام KYC رقمي مدعوم بالذكاء الاصطناعي للتحقق البيومتري، تحليل المخاطر، وربط المستخدمين بالمؤسسات المالية.",
    files: [
      { name: "KYC_Initiative.pdf", key: "KYC_Initiative.pdf" },
      { name: "KYC_Slides.pptx", key: "KYC_Initiative_Slides.pptx" },
    ],
    tags: ["KYC", "AI", "Compliance"],
  },
  {
    id: "dara-plan",
    title: "Dara Business Plan",
    tagline: "TravelTech + AI Business Plan",
    description:
      "خطة عمل كاملة لشركة دارا تتضمن الرؤية، السوق، نموذج الإيرادات، وخطة التوسع 2025–2027.",
    files: [
      { name: "Dara_BusinessPlan.pdf", key: "Dara_BusinessPlan.pdf" },
      { name: "Dara_Deck.pptx", key: "Dara_Deck.pptx" },
    ],
    tags: ["Business Plan", "Strategy"],
  },
  {
    id: "ndc",
    title: "Sudan NDC Platform",
    tagline: "Proprietary NDC + Payment Integration",
    description:
      "منصة NDC وطنية تدمج محرك عروض ديناميكي، إدارة الطلبات، وربط الدفع المحلي، متوافقة مع معايير IATA.",
    files: [
      { name: "NDC_Platform.pdf", key: "NDC_Platform.pdf" },
    ],
    tags: ["NDC", "Payments", "IATA"],
  },
  {
    id: "doha",
    title: "Doha Office",
    tagline: "Gulf Expansion & Investor Relations",
    description:
      "مكتب تمثيلي في الدوحة لدعم الشراكات الخليجية، التفاوض مع البنوك (QNB)، وجذب المستثمرين.",
    files: [
      { name: "Doha_Office.pdf", key: "Doha_Office.pdf" },
    ],
    tags: ["Expansion", "QNB"],
  },
  {
    id: "master",
    title: "Master Investor Deck",
    tagline: "All Projects — One Investor Package",
    description: "الحزمة الاستثمارية الكاملة: كل المشاريع الأربعة + ملخص الاستثمار وAI Integration.",
    files: [{ name: "Master_Investor_Deck.pptx", key: "Master_Investor_Deck.pptx" }],
    tags: ["Master", "All"],
  },
];

export default function DaraInvestorPlatform() {
  const [projects, setProjects] = useState(initialProjects);
  const [query, setQuery] = useState("");
  const [activeTags, setActiveTags] = useState([]);
  const [selected, setSelected] = useState(null);
  const [showModal, setShowModal] = useState(false);

  // Chat state (AI assistant)
  const [chatLines, setChatLines] = useState([
    { from: "system", text: "مرحبًا بك في منصة المستثمر — اسألني عن أي مشروع." },
  ]);
  const [chatInput, setChatInput] = useState("");
  const [lang, setLang] = useState("ar"); // ar | en

  useEffect(() => {
    // Example: fetch updated file URLs from your server if needed
    // fetch('/api/files').then(...)
  }, []);

  function toggleTag(tag) {
    setActiveTags((prev) => (prev.includes(tag) ? prev.filter((t) => t !== tag) : [...prev, tag]));
  }

  function filtered() {
    return projects.filter((p) => {
      const q = query.trim().toLowerCase();
      const matchesQuery = !q || p.title.toLowerCase().includes(q) || p.description.toLowerCase().includes(q);
      const matchesTags = activeTags.length === 0 || activeTags.every((t) => p.tags.includes(t));
      return matchesQuery && matchesTags;
    });
  }

  function openProject(p) {
    setSelected(p);
    setShowModal(true);
  }

  // Download helper: requests a signed URL from backend then opens it in a new tab.
  async function downloadFile(file) {
    // file can be { url } (legacy) or { key } (preferred)
    try {
      const key = file?.key || null;
      const legacyUrl = file?.url || null;
      if (legacyUrl) {
        window.open(legacyUrl, "_blank");
        return;
      }
      if (!key) return;
      // Call backend to get a short-lived signed URL: /api/signed-url?key=...
      const res = await fetch(`/api/signed-url?key=${encodeURIComponent(key)}`);
      if (!res.ok) throw new Error('failed to get signed url');
      const body = await res.json();
      const signed = body.url;
      if (signed) window.open(signed, "_blank");
    } catch (err) {
      console.error(err);
      alert('تعذر تنزيل الملف. الرجاء المحاولة مرة أخرى أو التواصل مع الدعم.');
    }
  }

  // Chat sender: calls backend proxy /api/ai-chat which must hold OPENAI_API_KEY securely.
  async function sendChat() {
    if (!chatInput.trim()) return;
    const message = chatInput.trim();
    const userLine = { from: "user", text: message };
    setChatLines((c) => [...c, userLine]);
    setChatInput("");

    try {
      const res = await fetch('/api/ai-chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
      });
      if (!res.ok) throw new Error('AI service error');
      const data = await res.json();
      const reply = data.reply || data?.choices?.[0]?.message?.content || 'لا يوجد رد من الخادم';
      setChatLines((c) => [...c, { from: 'assistant', text: reply }] );
    } catch (err) {
      console.error(err);
      setChatLines((c) => [...c, { from: 'assistant', text: 'تعذر الوصول لخدمة الذكاء الاصطناعي الآن.' }]);
    }
  }

  function sendChat() {
    if (!chatInput.trim()) return;
    const userLine = { from: "user", text: chatInput };
    setChatLines((c) => [...c, userLine]);

    // Hook for integration with your backend that calls OpenAI securely.
    // Example (pseudo):
    // fetch('/api/ai-chat', { method: 'POST', body: JSON.stringify({ message: chatInput }) })
    //   .then(res => res.json())
    //   .then(data => setChatLines(c => [...c, { from: 'assistant', text: data.reply }]));

    // For demo, push a friendly placeholder response after short delay.
    setTimeout(() => {
      setChatLines((c) => [...c, { from: "assistant", text: "تم استلام سؤالك — سأعرض خلاصة المشروع أو أجيب استفسارك مباشرةً." }]);
    }, 600);

    setChatInput("");
  }

  function uniqueTags() {
    const s = new Set();
    projects.forEach((p) => p.tags.forEach((t) => s.add(t)));
    return Array.from(s);
  }

  // Professional small components
  const Tag = ({ label, active, onClick }) => (
    <button onClick={onClick} className={`px-3 py-1 text-sm rounded-full border ${active ? "bg-blue-600 text-white" : "bg-white"}`}>
      {label}
    </button>
  );

  const ProjectCard = ({ p }) => (
    <article className="bg-white p-5 rounded-lg shadow hover:shadow-md transition">
      <div className="flex justify-between items-start gap-3">
        <div>
          <h3 className="font-semibold text-lg">{p.title}</h3>
          <p className="text-sm text-gray-600 mt-1">{p.tagline}</p>
        </div>
        <div className="flex flex-col items-end gap-2">
          <div className="text-xs text-gray-500">{p.tags.join(" • ")}</div>
          <div className="flex gap-2">
            <button onClick={() => openProject(p)} className="px-3 py-1 border rounded text-sm">عرض</button>
            <button onClick={() => downloadFile(p.files[0]?.url)} className="px-3 py-1 bg-green-600 text-white rounded text-sm">تحميل</button>
          </div>
        </div>
      </div>
      <p className="mt-3 text-sm text-gray-700">{p.description}</p>
    </article>
  );

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 p-6">
      <header className="max-w-7xl mx-auto flex items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-lg bg-white flex items-center justify-center shadow">
            <svg width="34" height="34" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect width="24" height="24" rx="4" fill="#0b61ff" />
              <text x="50%" y="55%" dominantBaseline="middle" textAnchor="middle" fontSize="10" fill="white">DA</text>
            </svg>
          </div>
          <div>
            <h1 className="text-2xl font-bold">{BRAND.name} — Investor Platform</h1>
            <p className="text-sm text-gray-600">حزمة العرض الاستثمارية • جاهزة للمستثمرين</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="hidden sm:flex items-center gap-2 text-sm text-gray-600">
            <span>اللغة:</span>
            <button onClick={() => setLang("ar")} className={`px-2 py-1 rounded ${lang === "ar" ? "bg-gray-200" : ""}`}>العربية</button>
            <button onClick={() => setLang("en")} className={`px-2 py-1 rounded ${lang === "en" ? "bg-gray-200" : ""}`}>English</button>
          </div>

          <a
            href="sandbox:/mnt/data/Dara_Investment_Files.zip"
            className={`px-4 py-2 ${BRAND.colors.primary} text-white rounded-lg text-sm shadow`}
          >
            تحميل الحزمة كاملة
          </a>

          <button
            onClick={() => {
              const master = projects.find((p) => p.id === "master");
              if (master) downloadFile(master.files[0]?.url);
            }}
            className="px-4 py-2 border rounded-lg text-sm"
          >
            فتح Master Deck
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6">
        <section className="lg:col-span-2">
          <div className="mb-4 flex gap-3 items-center">
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder={lang === "ar" ? "ابحث عن مشروع أو وصف..." : "Search project or description..."}
              className="flex-1 px-4 py-3 border rounded-lg"
            />

            <div className="flex gap-2 flex-wrap">
              {uniqueTags().map((t) => (
                <Tag key={t} label={t} active={activeTags.includes(t)} onClick={() => toggleTag(t)} />
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {filtered().map((p) => (
              <ProjectCard key={p.id} p={p} />
            ))}
          </div>

          <div className="mt-6">
            <h3 className="text-lg font-semibold">ملاحظات التنفيذ السريع</h3>
            <ul className="list-disc list-inside mt-3 text-sm text-gray-700 space-y-2">
              <li>استبدال روابط "sandbox:/mnt/data" بروابط آمنة (S3 signed URLs أو CDN).</li>
              <li>إنشاء نقطة نهاية خلفية لاستدعاء OpenAI بمفتاح مخفي (server-side).</li>
              <li>نشر الواجهة على Vercel / Netlify مع إعداد environment variables.</li>
            </ul>
          </div>
        </section>

        <aside className="bg-white p-4 rounded-lg shadow-sm">
          <h4 className="font-semibold mb-2">AI Assistant</h4>
          <div className="h-60 overflow-auto border rounded p-3 mb-3 bg-gray-50">
            {chatLines.map((c, i) => (
              <div key={i} className={`mb-2 ${c.from === "assistant" ? "text-left" : c.from === "system" ? "text-center text-xs text-gray-500" : "text-right"}`}>
                <div className={`${c.from === "assistant" ? "inline-block bg-white p-2 rounded shadow" : c.from === "user" ? "inline-block bg-blue-600 text-white p-2 rounded" : "text-xs"}`}>
                  {c.text}
                </div>
              </div>
            ))}
          </div>
          <div className="flex gap-2">
            <input value={chatInput} onChange={(e) => setChatInput(e.target.value)} placeholder={lang === "ar" ? "اسأل المساعد..." : "Ask the assistant..."} className="flex-1 px-3 py-2 border rounded" />
            <button onClick={sendChat} className="px-3 py-2 bg-blue-600 text-white rounded">{lang === "ar" ? "أرسل" : "Send"}</button>
          </div>

          <div className="mt-4">
            <h5 className="font-medium">روابط سريعة</h5>
            <ul className="mt-2 text-sm text-gray-600 space-y-1">
              <li>
                <a className="text-blue-600 underline cursor-pointer" onClick={() => downloadFile("sandbox:/mnt/data/Dara_Investment_Files.zip")}>تحميل الحزمة الكاملة (ZIP)</a>
              </li>
              <li>
                <a className="text-blue-600 underline cursor-pointer" onClick={() => downloadFile("sandbox:/mnt/data/Master_Investor_Deck.pptx")}>تحميل Master Deck</a>
              </li>
            </ul>
          </div>

          <div className="mt-4 border-t pt-3 text-xs text-gray-500">
            جاهز للعرض في الاجتماعات — استخدم هذه اللوحة لتحريك النقاش مع المستثمر.
          </div>
        </aside>
      </main>

      {/* Modal */}
      {showModal && selected && (
        <div className="fixed inset-0 bg-black/40 flex items-center justify-center p-4 z-40">
          <div className="bg-white w-full max-w-3xl rounded-lg shadow-lg p-6">
            <div className="flex justify-between items-start">
              <div>
                <h2 className="text-xl font-semibold">{selected.title}</h2>
                <p className="text-sm text-gray-600">{selected.tagline}</p>
              </div>
              <div className="flex gap-2">
                <button onClick={() => { setShowModal(false); setSelected(null); }} className="px-3 py-1 border rounded">إغلاق</button>
              </div>
            </div>

            <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-gray-700">{selected.description}</p>
                <div className="mt-4">
                  <h4 className="font-medium">الملفات</h4>
                  <ul className="mt-2 space-y-2">
                    {selected.files.map((f) => (
                      <li key={f.name} className="flex items-center justify-between bg-gray-50 p-2 rounded">
                        <div className="text-sm">{f.name}</div>
                        <div className="flex gap-2">
                          <button onClick={() => downloadFile(f.url)} className="px-3 py-1 bg-green-600 text-white rounded text-sm">تحميل</button>
                        </div>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              <div>
                <h4 className="font-medium">نقاط سريعة للمستثمر</h4>
                <ul className="list-disc list-inside mt-2 text-sm text-gray-700">
                  <li>جاهزية تقنية + AI</li>
                  <li>توافق مع IATA</li>
                  <li>شراكة محتملة مع QNB</li>
                  <li>خطة نمو 3 سنوات</li>
                </ul>

                <div className="mt-4">
                  <h4 className="font-medium">اتصال سريع</h4>
                  <p className="text-sm text-gray-700">للمستثمرين المهتمين: <span className="font-medium">hamed.mukhtar@daral-sd.com</span></p>
                </div>
              </div>
            </div>

          </div>
        </div>
      )}

      <footer className="max-w-7xl mx-auto mt-8 text-center text-sm text-gray-500">
        Dara — Investor Platform • Prepared with AI • Last updated: {new Date().toLocaleDateString()}
      </footer>
    </div>
  );
}

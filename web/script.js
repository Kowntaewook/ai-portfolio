const NOTION_RESUME_URL = "https://myclassesmadebykwontaewook.notion.site/Forensics-Reverse-Engineer-3679ecccd0ca80efa804da61a8e77967?pvs=74";

let allProjects = [];
let currentFilter = "All";
let currentLang = localStorage.getItem("portfolio_lang") || "ko";

const I18N = {
  ko: {
    "nav.skills": "// \uAE30\uC220",
    "nav.projects": "// \uD504\uB85C\uC81D\uD2B8",
    "nav.timeline": "// \uC774\uB825",
    "nav.contact": "// \uC5F0\uB77D",
    "nav.hire": "\uC9C0\uC6D0 \uBB38\uC758",
    "hero.terminal": "terminal SEC_PROFILE \uCD08\uAE30\uD654 \uC911...",
    "hero.name": "\uAD8C\uD0DC\uC6B1",
    "hero.title": "// \uD3EC\uB80C\uC2DD & \uB9AC\uBC84\uC2A4 \uC5D4\uC9C0\uB2C8\uC5B4",
    "hero.desc": "\uB514\uC9C0\uD138 \uC99D\uAC70 \uC55E\uC5D0\uC11C\uB294 \uCD94\uCE21\uBCF4\uB2E4 \uC0AC\uC2E4\uC744 \uC6B0\uC120\uD569\uB2C8\uB2E4.<br />\uC815\uBC00\uD55C \uBA54\uBAA8\uB9AC \uD3EC\uB80C\uC2DD\uACFC \uBC14\uC774\uB108\uB9AC \uBD84\uC11D\uC744 \uD1B5\uD574 \uBCF4\uC774\uC9C0 \uC54A\uB294 \uC704\uD611\uC758 \uC2E4\uCCB4\uB97C \uADDC\uBA85\uD569\uB2C8\uB2E4.",
    "hero.projects": "\uD504\uB85C\uC81D\uD2B8 \uBCF4\uAE30",
    "hero.resume": "\uC774\uB825 \uBCF4\uAE30",
    "hero.notion": "\uB178\uC158 \uC774\uB825\uC11C",
    "hero.contact": "\uC5F0\uB77D\uD558\uAE30",
    "skills.kicker": "\uC5ED\uB7C9 \uB9E4\uD2B8\uB9AD\uC2A4",
    "projects.kicker": "\uC99D\uAC70 \uC544\uCE74\uC774\uBE0C",
    "timeline.kicker": "\uD65C\uB3D9 \uB85C\uADF8",
    "contact.kicker": "\uC5F0\uACB0 \uC694\uCCAD",
    "contact.desc": "\uC785\uC0AC \uC9C0\uC6D0, \uD504\uB85C\uC81D\uD2B8 \uD611\uC5C5, \uBCF4\uC548 \uBD84\uC11D \uAD00\uB828 \uBB38\uC758\uB97C \uD658\uC601\uD569\uB2C8\uB2E4.",
    "contact.mail": "\uBA54\uC77C \uBCF4\uB0B4\uAE30",
    "contact.blog": "\uBE14\uB85C\uADF8 \uC5F4\uAE30",
    "contact.notion": "\uB178\uC158 \uC774\uB825\uC11C \uC5F4\uAE30",
    "contact.download": "\uC774\uB825\uC11C PDF \uB2E4\uC6B4\uB85C\uB4DC",
    "chat.hello": "\uC548\uB155\uD558\uC138\uC694. \uD3EC\uD2B8\uD3F4\uB9AC\uC624, \uD504\uB85C\uC81D\uD2B8, \uAE30\uC220 \uC2A4\uD0DD, \uC774\uB825\uC11C\uC5D0 \uB300\uD574 \uBB3C\uC5B4\uBCFC \uC218 \uC788\uC2B5\uB2C8\uB2E4.",
    "chat.placeholder": "\uD504\uB85C\uC81D\uD2B8 \uC124\uBA85\uD574\uC918",
    "skill.forensics.desc": "\uB808\uC9C0\uC2A4\uD2B8\uB9AC, \uBA54\uBAA8\uB9AC, \uD30C\uC77C\uC2DC\uC2A4\uD15C, Windows Artifact \uAE30\uBC18 \uBD84\uC11D",
    "skill.reverse.desc": "\uBC14\uC774\uB108\uB9AC \uC815\uC801 \uBD84\uC11D, \uC5B4\uC148\uBE14\uB9AC \uD750\uB984 \uBD84\uC11D, \uC2E4\uD589 \uB85C\uC9C1 \uCD94\uC801",
    "skill.auto.desc": "CTF \uD480\uC774 \uC790\uB3D9\uD654, \uD3EC\uB80C\uC2DD \uBC18\uBCF5 \uBD84\uC11D \uC2A4\uD06C\uB9BD\uD2B8, \uB370\uC774\uD130 \uCC98\uB9AC",
    "skill.network.desc": "\uD328\uD0B7, \uB85C\uADF8, \uBE0C\uB77C\uC6B0\uC800 \uAE30\uB85D, \uD0C0\uC784\uB77C\uC778 \uAE30\uBC18 \uCE68\uD574 \uD750\uB984 \uC7AC\uAD6C\uC131",
    "timeline.c.title": "\uCCAD\uC18C\uB144 IT\uACBD\uC2DC\uB300\uD68C C\uC5B8\uC5B4 \uBD80\uBB38 \uAE08\uC0C1",
    "timeline.c.desc": "\uC800\uC218\uC900 \uD504\uB85C\uADF8\uB798\uBC0D \uC5ED\uB7C9\uACFC \uBB38\uC81C \uD574\uACB0 \uB2A5\uB825\uC744 \uAC80\uC99D\uD588\uC2B5\uB2C8\uB2E4.",
    "timeline.rce.title": "RCE CTF \uD574\uD0B9 \uBC29\uC5B4\uC804 \uC7A5\uB824\uC0C1",
    "timeline.rce.desc": "\uBCF4\uC548 \uB3D9\uC544\uB9AC \uD65C\uB3D9\uACFC CTF \uAE30\uBC18 \uC2E4\uC804 \uBD84\uC11D \uACBD\uD5D8\uC744 \uC313\uC558\uC2B5\uB2C8\uB2E4.",
    "timeline.ai.title": "\uCCAD\uC18C\uB144 IT\uACBD\uC2DC\uB300\uD68C AI \uB370\uC774\uD130\uBD84\uC11D \uBD80\uBB38 \uAE08\uC0C1",
    "timeline.ai.desc": "\uB370\uC774\uD130 \uBD84\uC11D\uACFC AI \uD65C\uC6A9 \uC5ED\uB7C9\uC744 \uD504\uB85C\uC81D\uD2B8\uB85C \uC99D\uBA85\uD588\uC2B5\uB2C8\uB2E4.",
    "timeline.sec.title": "CTF / Bug Bounty / \uD3EC\uB80C\uC2DD \uD504\uB85C\uC81D\uD2B8",
    "timeline.sec.desc": "\uAD6D\uB0B4\uC678 CTF, Bugcrowd VDP, \uCE68\uD574\uC0AC\uACE0 \uBD84\uC11D \uD504\uB85C\uC81D\uD2B8\uB97C \uC9C4\uD589\uD588\uC2B5\uB2C8\uB2E4."
  },
  en: {
    "nav.skills": "// Skills",
    "nav.projects": "// Projects",
    "nav.timeline": "// Timeline",
    "nav.contact": "// Contact",
    "nav.hire": "Hire Me",
    "hero.terminal": "terminal INITIALIZING_SEC_PROFILE...",
    "hero.name": "Kwon Tae Uk",
    "hero.title": "// Forensics & Reverse Engineer",
    "hero.desc": "I prioritize facts over assumptions when handling digital evidence.<br />I investigate hidden threats through memory forensics, artifact analysis, and binary analysis.",
    "hero.projects": "View Projects",
    "hero.resume": "View Resume",
    "hero.notion": "Notion Resume",
    "hero.contact": "Contact",
    "skills.kicker": "CAPABILITY MATRIX",
    "projects.kicker": "EVIDENCE ARCHIVE",
    "timeline.kicker": "ACTIVITY LOG",
    "contact.kicker": "ESTABLISH_CONNECTION",
    "contact.desc": "Open to job applications, project collaboration, and security analysis inquiries.",
    "contact.mail": "Send Mail",
    "contact.blog": "Open Blog",
    "contact.notion": "Open Notion Resume",
    "contact.download": "Download Resume PDF",
    "chat.hello": "Hello. You can ask about my portfolio, projects, skills, and resume.",
    "chat.placeholder": "Tell me about your projects",
    "skill.forensics.desc": "Registry, memory, filesystem, and Windows artifact analysis",
    "skill.reverse.desc": "Static binary analysis, assembly flow analysis, and execution logic tracing",
    "skill.auto.desc": "CTF solving automation, forensic scripts, and data processing",
    "skill.network.desc": "Packet, log, browser history, and timeline-based incident reconstruction",
    "timeline.c.title": "Youth IT Contest C Language Gold Prize",
    "timeline.c.desc": "Verified low-level programming and problem-solving ability.",
    "timeline.rce.title": "RCE CTF Cyber Defense Award",
    "timeline.rce.desc": "Built practical analysis experience through security club and CTF activity.",
    "timeline.ai.title": "Youth IT Contest AI Data Analysis Gold Prize",
    "timeline.ai.desc": "Demonstrated data analysis and AI capability through a project.",
    "timeline.sec.title": "CTF / Bug Bounty / Forensics Projects",
    "timeline.sec.desc": "Participated in CTFs, Bugcrowd VDP reports, and incident analysis projects."
  }
};

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function applyLanguage() {
  document.documentElement.lang = currentLang;

  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.dataset.i18n;
    if (I18N[currentLang][key]) el.textContent = I18N[currentLang][key];
  });

  document.querySelectorAll("[data-i18n-html]").forEach((el) => {
    const key = el.dataset.i18nHtml;
    if (I18N[currentLang][key]) el.innerHTML = I18N[currentLang][key];
  });

  const toggle = document.getElementById("lang-toggle");
  if (toggle) toggle.textContent = currentLang === "ko" ? "EN" : "KO";

  const chatInput = document.getElementById("chat-input");
  if (chatInput) chatInput.placeholder = I18N[currentLang]["chat.placeholder"];
}

function switchLanguage() {
  currentLang = currentLang === "ko" ? "en" : "ko";
  localStorage.setItem("portfolio_lang", currentLang);
  applyLanguage();
}

function getCategory(project) {
  const raw = [project.id, project.title, project.description, ...(project.tags || [])].join(" ").toLowerCase();
  if (raw.includes("cve") || raw.includes("packagekit") || raw.includes("lpe")) return "CVE";
  if (raw.includes("forensic") || raw.includes("uac") || raw.includes("incident")) return "Forensics";
  if (raw.includes("reverse") || raw.includes("reversing") || raw.includes("ida")) return "Reverse";
  if (raw.includes("ctf") || raw.includes("kitsunebi")) return "CTF";
  if (raw.includes("ai agent") || raw.includes("claude")) return "AI Agent";
  return "Security";
}

function renderFilters() {
  const bar = document.getElementById("filter-bar");
  if (!bar) return;

  const filters = ["All", ...new Set(allProjects.map(getCategory))];

  bar.innerHTML = filters.map((name) => `
    <button class="filter-btn ${name === currentFilter ? "active" : ""}" data-filter="${escapeHtml(name)}">
      ${escapeHtml(name)}
    </button>
  `).join("");

  bar.querySelectorAll(".filter-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      currentFilter = btn.dataset.filter;
      renderFilters();
      renderProjects();
    });
  });
}

function renderProjects() {
  const grid = document.getElementById("project-grid");
  const status = document.getElementById("project-status");
  if (!grid) return;

  const projects = currentFilter === "All"
    ? allProjects
    : allProjects.filter((project) => getCategory(project) === currentFilter);

  if (status) status.textContent = `loaded ${allProjects.length} projects from ./data/projects.json`;

  grid.innerHTML = projects.map((project) => {
    const category = getCategory(project);
    const tags = (project.tags || []).slice(0, 6);

    return `
      <article class="project-card" data-id="${escapeHtml(project.id)}">
        <div class="project-meta">${escapeHtml(category)} / ${escapeHtml(project.id)}</div>
        <h3>${escapeHtml(project.title)}</h3>
        <p>${escapeHtml(project.description)}</p>
        <div class="tags">
          ${tags.map((tag) => `<span>${escapeHtml(tag)}</span>`).join("")}
        </div>
      </article>
    `;
  }).join("");

  grid.querySelectorAll(".project-card").forEach((card) => {
    card.addEventListener("click", () => openProject(card.dataset.id));
  });
}

function openProject(id) {
  const project = allProjects.find((p) => p.id === id);
  const modal = document.getElementById("modal");
  const body = document.getElementById("modal-body");
  if (!project || !modal || !body) return;

  const tags = project.tags || [];
  const content = project.content || project.summary || project.description || "";

  body.innerHTML = `
    <div class="project-meta">${escapeHtml(getCategory(project))} / ${escapeHtml(project.id)}</div>
    <h2>${escapeHtml(project.title)}</h2>
    <p>${escapeHtml(project.description)}</p>
    <div class="tags">${tags.map((tag) => `<span>${escapeHtml(tag)}</span>`).join("")}</div>
    <hr style="border-color: rgba(0,217,255,0.18); margin: 28px 0;">
    <pre class="content-pre">${escapeHtml(content)}</pre>
  `;

  modal.classList.remove("hidden");
}

async function loadProjects() {
  const status = document.getElementById("project-status");

  try {
    const response = await fetch("./data/projects.json?ts=" + Date.now(), { cache: "no-store" });
    if (!response.ok) throw new Error("HTTP " + response.status);

    const data = await response.json();
    if (!Array.isArray(data)) throw new Error("projects.json is not an array");

    allProjects = data;
    renderFilters();
    renderProjects();
  } catch (error) {
    console.error("Project load failed:", error);
    if (status) status.textContent = "failed to load ./data/projects.json";
  }
}

function addChatMessage(role, text) {
  const log = document.getElementById("chat-log");
  if (!log) return;

  const msg = document.createElement("div");
  msg.className = "chat-msg " + role;
  msg.textContent = text;
  log.appendChild(msg);
  log.scrollTop = log.scrollHeight;
}

function makeChatReply(input) {
  const q = input.toLowerCase();
  const ko = currentLang === "ko";
  const projectNames = allProjects.length
    ? allProjects.map((p) => "- " + p.title).join("\n")
    : "- D+\n- Linux Forensic Scenario\n- CVE Analysis\n- K!$un3b1\n- K!t$un3b1 Forensics";

  if (q.includes("project") || q.includes("ctf") || q.includes("\uD504\uB85C\uC81D\uD2B8")) {
    return ko
      ? "\uD604\uC7AC \uD3EC\uD2B8\uD3F4\uB9AC\uC624\uC5D0\uB294 \uB2E4\uC74C \uD504\uB85C\uC81D\uD2B8\uAC00 \uB4F1\uB85D\uB418\uC5B4 \uC788\uC2B5\uB2C8\uB2E4.\n\n" + projectNames + "\n\n\uD504\uB85C\uC81D\uD2B8 \uCE74\uB4DC\uB97C \uB204\uB974\uBA74 \uC0C1\uC138 \uB0B4\uC6A9\uC744 \uBCFC \uC218 \uC788\uC2B5\uB2C8\uB2E4."
      : "The portfolio currently contains these projects:\n\n" + projectNames + "\n\nClick a project card to view details.";
  }

  if (q.includes("skill") || q.includes("stack") || q.includes("\uAE30\uC220") || q.includes("\uC2A4\uD0DD")) {
    return ko
      ? "\uC8FC\uC694 \uAE30\uC220\uC740 Digital Forensics, Reverse Engineering, Python \uC790\uB3D9\uD654, Windows/Linux Artifact \uBD84\uC11D, \uB124\uD2B8\uC6CC\uD06C \uBD84\uC11D\uC785\uB2C8\uB2E4."
      : "Main skills include Digital Forensics, Reverse Engineering, Python automation, Windows/Linux artifact analysis, and network analysis.";
  }

  if (q.includes("resume") || q.includes("notion") || q.includes("\uC774\uB825\uC11C") || q.includes("\uB178\uC158")) {
    return ko
      ? "\uB178\uC158 \uC774\uB825\uC11C\uB294 \uC0C1\uB2E8 \uB610\uB294 Contact \uC139\uC158\uC758 \uBC84\uD2BC\uC73C\uB85C \uC5F4 \uC218 \uC788\uC2B5\uB2C8\uB2E4. PDF \uB2E4\uC6B4\uB85C\uB4DC\uB294 web/assets/resume.pdf \uD30C\uC77C\uC744 \uB123\uC73C\uBA74 \uB3D9\uC791\uD569\uB2C8\uB2E4."
      : "You can open the Notion resume from the buttons on the page. PDF download works when web/assets/resume.pdf exists.";
  }

  return ko
    ? "\uD3EC\uD2B8\uD3F4\uB9AC\uC624, \uD504\uB85C\uC81D\uD2B8, \uAE30\uC220 \uC2A4\uD0DD, CTF, \uC774\uB825\uC11C, \uC5F0\uB77D \uBC29\uBC95\uC5D0 \uB300\uD574 \uC9C8\uBB38\uD560 \uC218 \uC788\uC2B5\uB2C8\uB2E4."
    : "You can ask about the portfolio, projects, skills, CTF activity, resume, or contact information.";
}

function setupChatWidget() {
  const open = document.getElementById("chat-open");
  const close = document.getElementById("chat-close");
  const panel = document.getElementById("chat-panel");
  const form = document.getElementById("chat-form");
  const input = document.getElementById("chat-input");

  if (!open || !close || !panel || !form || !input) return;

  open.addEventListener("click", () => panel.classList.toggle("hidden"));
  close.addEventListener("click", () => panel.classList.add("hidden"));

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const text = input.value.trim();
    if (!text) return;

    addChatMessage("user", text);
    input.value = "";

    setTimeout(() => addChatMessage("bot", makeChatReply(text)), 200);
  });
}

function setupResumeDownload() {
  const btn = document.getElementById("resume-download");
  if (!btn) return;

  btn.addEventListener("click", async (event) => {
    event.preventDefault();

    try {
      const res = await fetch("./assets/resume.pdf?ts=" + Date.now(), {
        method: "HEAD",
        cache: "no-store"
      });

      if (res.ok) {
        window.location.href = "./assets/resume.pdf";
        return;
      }
    } catch (_) {}

    alert(currentLang === "ko"
      ? "\uC544\uC9C1 web/assets/resume.pdf \uD30C\uC77C\uC774 \uC5C6\uC2B5\uB2C8\uB2E4. \uB300\uC2E0 \uB178\uC158 \uC774\uB825\uC11C\uB97C \uC5FD\uB2C8\uB2E4."
      : "web/assets/resume.pdf does not exist yet. Opening the Notion resume instead."
    );

    window.open(NOTION_RESUME_URL, "_blank");
  });
}

function setupModal() {
  const close = document.getElementById("modal-close");
  const modal = document.getElementById("modal");

  if (!close || !modal) return;

  close.addEventListener("click", () => modal.classList.add("hidden"));
  modal.addEventListener("click", (event) => {
    if (event.target.id === "modal") modal.classList.add("hidden");
  });
}

function setupCanvas() {
  const canvas = document.getElementById("cyber-bg");
  if (!canvas) return;

  const ctx = canvas.getContext("2d");
  let width = 0;
  let height = 0;
  let particles = [];
  let mouse = { x: null, y: null };

  function resizeCanvas() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;

    const count = Math.min(120, Math.max(55, Math.floor((width * height) / 16000)));
    particles = Array.from({ length: count }, () => ({
      x: Math.random() * width,
      y: Math.random() * height,
      vx: (Math.random() - 0.5) * 0.35,
      vy: (Math.random() - 0.5) * 0.35,
      r: Math.random() * 1.8 + 0.6
    }));
  }

  function drawNetwork() {
    ctx.clearRect(0, 0, width, height);
    ctx.fillStyle = "#000000";
    ctx.fillRect(0, 0, width, height);

    for (const p of particles) {
      p.x += p.vx;
      p.y += p.vy;

      if (p.x < 0 || p.x > width) p.vx *= -1;
      if (p.y < 0 || p.y > height) p.vy *= -1;

      if (mouse.x !== null) {
        const dx = mouse.x - p.x;
        const dy = mouse.y - p.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 170) {
          p.x -= dx * 0.002;
          p.y -= dy * 0.002;
        }
      }

      ctx.beginPath();
      ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      ctx.fillStyle = "rgba(0, 217, 255, 0.75)";
      ctx.fill();
    }

    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const a = particles[i];
        const b = particles[j];
        const dx = a.x - b.x;
        const dy = a.y - b.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < 135) {
          ctx.beginPath();
          ctx.moveTo(a.x, a.y);
          ctx.lineTo(b.x, b.y);
          ctx.strokeStyle = "rgba(0, 217, 255, " + ((1 - dist / 135) * 0.32) + ")";
          ctx.lineWidth = 0.7;
          ctx.stroke();
        }
      }
    }

    requestAnimationFrame(drawNetwork);
  }

  window.addEventListener("resize", resizeCanvas);
  window.addEventListener("mousemove", (event) => {
    mouse.x = event.clientX;
    mouse.y = event.clientY;
  });
  window.addEventListener("mouseleave", () => {
    mouse.x = null;
    mouse.y = null;
  });

  resizeCanvas();
  drawNetwork();
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("lang-toggle")?.addEventListener("click", switchLanguage);

  setupCanvas();
  setupModal();
  setupChatWidget();
  setupResumeDownload();

  applyLanguage();
  loadProjects();
});


// === PROJECT_LANG_PATCH_START ===
const PROJECT_I18N_PATCH = {
  ko: {
    "cve-2026-41651-analysis": {
      "title": "CVE-2026-41651 Pack2TheRoot \ubd84\uc11d",
      "description": "PackageKit\uc758 TOCTOU \ub808\uc774\uc2a4 \ucee8\ub514\uc158\uc73c\ub85c \ubc1c\uc0dd\ud558\ub294 \ub85c\uceec \uad8c\ud55c \uc0c1\uc2b9 \ucde8\uc57d\uc810\uc744 \ubd84\uc11d\ud55c \ud504\ub85c\uc81d\ud2b8\uc785\ub2c8\ub2e4. \ubc84\uadf8 \uccb4\uc778, \uacf5\uaca9 \ud750\ub984, \uce68\ud574 \uc9c0\ud45c, \ud0d0\uc9c0 \uba85\ub839\uc5b4, \ub300\uc751 \ubc29\uc548\uc744 \uc815\ub9ac\ud588\uc2b5\ub2c8\ub2e4.",
      "tags": ["CVE \ubd84\uc11d", "Linux", "\uad8c\ud55c \uc0c1\uc2b9", "PackageKit", "TOCTOU"]
    },
    "d-plus": {
      "title": "D+ \ubd88\ubc95 \uc6f9\uc0ac\uc774\ud2b8 \ubaa8\ub2c8\ud130\ub9c1 \uc2dc\uc2a4\ud15c",
      "description": "\ube14\ub799\ub9ac\uc2a4\ud2b8 \uc6f9\uc0ac\uc774\ud2b8 \ubc29\ubb38 \uae30\ub85d\uc744 \ubaa8\ub2c8\ud130\ub9c1\ud558\uace0, \uc218\uc9d1 \uae30\ub85d\uc744 \uc554\ud638\ud654\ud558\uc5ec \uad00\ub9ac\uc790 \ub300\uc2dc\ubcf4\ub4dc\ub85c \ubcf4\uace0\ud558\ub294 \ud300 \ud504\ub85c\uc81d\ud2b8\uc785\ub2c8\ub2e4. \uc800\ub294 \uc554\ud638\ud654 \ub85c\uc9c1\uacfc \ubc31\uc5d4\ub4dc \uad6c\ud604\uc744 \ub2f4\ub2f9\ud588\uc2b5\ub2c8\ub2e4.",
      "tags": ["Python", "\ubc31\uc5d4\ub4dc", "\uc554\ud638\ud654", "SQLite", "AWS", "\ubcf4\uc548"]
    },
    "kitsunebi-auto-ctf-solver": {
      "title": "K!$un3b1 \uc790\ub3d9 CTF \uc194\ubc84",
      "description": "Claude Agent SDK\uc640 Opus 4.7 \uae30\ubc18\uc73c\ub85c CTF \ubb38\uc81c \ud30c\uc77c\uc744 \uc77d\uace0, \uc2a4\ud06c\ub9bd\ud2b8 \uc791\uc131\uacfc \ub3c4\uad6c \uc2e4\ud589\uc744 \ud1b5\ud574 \ud50c\ub798\uadf8\ub97c \uc790\ub3d9 \ucd94\ucd9c\u00b7\ucc44\uc810\ud558\ub294 \uc5d0\uc774\uc804\ud2b8\uc785\ub2c8\ub2e4.",
      "tags": ["AI \uc5d0\uc774\uc804\ud2b8", "CTF", "\uc790\ub3d9\ud654", "Claude SDK", "Python"]
    },
    "kitsunebi-forensics": {
      "title": "K!t$un3b1 \ud3ec\ub80c\uc2dd CTF \uc2e4\ud5d8",
      "description": "\uc790\ub3d9 CTF \uc194\ubc84\ub97c \ud3ec\ub80c\uc2dd \ubd84\uc57c\uc5d0 \uc801\uc6a9\ud55c \ubca4\uce58\ub9c8\ud06c\uc785\ub2c8\ub2e4. \ud3ec\ub80c\uc2dd \ubb38\uc81c 20\uac1c \uc911 14\uac1c\ub97c \ud574\uacb0\ud558\uc5ec 70%\uc758 \ud574\uacb0\ub960\uacfc \ucd1d 26.15\ub2ec\ub7ec\uc758 \ube44\uc6a9\uc744 \uae30\ub85d\ud588\uc2b5\ub2c8\ub2e4.",
      "tags": ["\ud3ec\ub80c\uc2dd", "CTF", "\ubca4\uce58\ub9c8\ud06c", "\uc790\ub3d9\ud654", "AI \uc5d0\uc774\uc804\ud2b8"]
    },
    "linux-forensic-scenario": {
      "title": "Linux \uce68\ud574\uc0ac\uace0 \ud3ec\ub80c\uc2dd \uc2dc\ub098\ub9ac\uc624 \ubd84\uc11d",
      "description": "UAC \uc544\ud2f0\ud329\ud2b8\ub97c \uae30\ubc18\uc73c\ub85c Linux \uc6cc\ucee4 \uc2dc\uc2a4\ud15c\uc758 SSH \uce68\ud22c, NOPASSWD sudo \uc545\uc6a9, ld.so.preload \ub8e8\ud2b8\ud0b7, \uc740\ub2c9 \ud504\ub85c\uc138\uc2a4, \uc778\uba54\ubaa8\ub9ac \ud398\uc774\ub85c\ub4dc \uc2e4\ud589\uc744 \ubd84\uc11d\ud55c \ud504\ub85c\uc81d\ud2b8\uc785\ub2c8\ub2e4.",
      "tags": ["Linux \ud3ec\ub80c\uc2dd", "UAC", "\ub8e8\ud2b8\ud0b7", "\uce68\ud574\uc0ac\uace0 \ub300\uc751", "journalctl"]
    }
  },
  en: {
    "cve-2026-41651-analysis": {
      "title": "CVE-2026-41651 Pack2TheRoot Analysis",
      "description": "A vulnerability analysis project for PackageKit local privilege escalation caused by a TOCTOU race condition. The report covers the bug chain, exploit flow, IoCs, detection commands, and mitigation.",
      "tags": ["CVE Analysis", "Linux", "LPE", "PackageKit", "TOCTOU"]
    },
    "d-plus": {
      "title": "D+ Illegal Website Monitoring System",
      "description": "A team project that monitors browser history for blacklisted websites and reports encrypted records to an admin dashboard. I worked on encryption and backend logic.",
      "tags": ["Python", "Backend", "Encryption", "SQLite", "AWS", "Security"]
    },
    "kitsunebi-auto-ctf-solver": {
      "title": "K!$un3b1 Auto CTF Solver",
      "description": "An automated CTF-solving agent built with Claude Agent SDK and Opus 4.7. It reads challenge files, writes scripts, executes tools, extracts flags, and compares answers automatically across CTF categories.",
      "tags": ["AI Agent", "CTF", "Automation", "Claude SDK", "Python"]
    },
    "kitsunebi-forensics": {
      "title": "K!t$un3b1 Forensics CTF Experiment",
      "description": "A forensics-focused benchmark for the automated CTF solver. The agent solved 14 out of 20 forensic challenges, achieving a 70 percent solve rate with a total cost of 26.15 dollars.",
      "tags": ["Forensics", "CTF", "Benchmark", "Automation", "AI Agent"]
    },
    "linux-forensic-scenario": {
      "title": "Linux Forensic Scenario Analysis",
      "description": "A Linux incident response project based on UAC artifacts. The analysis covers SSH intrusion, NOPASSWD sudo abuse, ld.so.preload rootkit behavior, hidden processes, and suspicious in-memory payload execution.",
      "tags": ["Linux Forensics", "UAC", "Rootkit", "Incident Response", "journalctl"]
    }
  }
};

function projectLang() {
  return currentLang === "ko" ? "ko" : "en";
}

function localProject(project) {
  const lang = projectLang();
  const translated = PROJECT_I18N_PATCH[lang][project.id] || {};
  return {
    ...project,
    title: translated.title || project.title,
    description: translated.description || project.description,
    tags: translated.tags || project.tags || []
  };
}

function categoryLabel(category) {
  if (currentLang !== "ko") return category;

  const map = {
    "All": "\uc804\uccb4",
    "CVE": "CVE \ubd84\uc11d",
    "Forensics": "\ud3ec\ub80c\uc2dd",
    "Reverse": "\ub9ac\ubc84\uc2f1",
    "CTF": "CTF",
    "AI Agent": "AI \uc5d0\uc774\uc804\ud2b8",
    "Security": "\ubcf4\uc548"
  };

  return map[category] || category;
}

function renderFilters() {
  const bar = document.getElementById("filter-bar");
  if (!bar) return;

  const filters = ["All", ...new Set(allProjects.map(getCategory))];

  bar.innerHTML = filters.map((name) => `
    <button class="filter-btn ${name === currentFilter ? "active" : ""}" data-filter="${safeEscape(name)}">
      ${safeEscape(categoryLabel(name))}
    </button>
  `).join("");

  bar.querySelectorAll(".filter-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      currentFilter = btn.dataset.filter;
      renderFilters();
      renderProjects();
    });
  });
}

function safeEscape(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function renderProjects() {
  const grid = document.getElementById("project-grid");
  const status = document.getElementById("project-status");
  if (!grid) return;

  const projects = currentFilter === "All"
    ? allProjects
    : allProjects.filter((project) => getCategory(project) === currentFilter);

  if (status) {
    status.textContent = currentLang === "ko"
      ? `./data/projects.json\uc5d0\uc11c ${allProjects.length}\uac1c \ud504\ub85c\uc81d\ud2b8 \ub85c\ub4dc \uc644\ub8cc`
      : `loaded ${allProjects.length} projects from ./data/projects.json`;
  }

  grid.innerHTML = projects.map((project) => {
    const localized = localProject(project);
    const category = getCategory(project);
    const tags = (localized.tags || []).slice(0, 6);

    return `
      <article class="project-card" data-id="${safeEscape(project.id)}">
        <div class="project-meta">${safeEscape(categoryLabel(category))} / ${safeEscape(project.id)}</div>
        <h3>${safeEscape(localized.title)}</h3>
        <p>${safeEscape(localized.description)}</p>
        <div class="tags">
          ${tags.map((tag) => `<span>${safeEscape(tag)}</span>`).join("")}
        </div>
      </article>
    `;
  }).join("");

  grid.querySelectorAll(".project-card").forEach((card) => {
    card.addEventListener("click", () => openProject(card.dataset.id));
  });
}

function openProject(id) {
  const project = allProjects.find((p) => p.id === id);
  const modal = document.getElementById("modal");
  const body = document.getElementById("modal-body");

  if (!project || !modal || !body) return;

  const localized = localProject(project);
  const tags = localized.tags || [];
  const content = project.content || project.summary || localized.description || "";

  body.innerHTML = `
    <div class="project-meta">${safeEscape(categoryLabel(getCategory(project)))} / ${safeEscape(project.id)}</div>
    <h2>${safeEscape(localized.title)}</h2>
    <p>${safeEscape(localized.description)}</p>
    <div class="tags">${tags.map((tag) => `<span>${safeEscape(tag)}</span>`).join("")}</div>
    <hr style="border-color: rgba(0,217,255,0.18); margin: 28px 0;">
    <pre class="content-pre">${safeEscape(content)}</pre>
  `;

  modal.classList.remove("hidden");
}

function switchLanguage() {
  currentLang = currentLang === "ko" ? "en" : "ko";
  localStorage.setItem("portfolio_lang", currentLang);

  applyLanguage();
  renderFilters();
  renderProjects();
}

(function forceInitialLangFromUrl() {
  const params = new URLSearchParams(window.location.search);
  const lang = params.get("lang");

  if (lang === "ko" || lang === "en") {
    currentLang = lang;
    localStorage.setItem("portfolio_lang", lang);
  }
})();

document.addEventListener("DOMContentLoaded", () => {
  setTimeout(() => {
    applyLanguage();
    renderFilters();
    renderProjects();
  }, 100);
});
// === PROJECT_LANG_PATCH_END ===
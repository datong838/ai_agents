/**
 * 谛听 Data Integration · 客户演示 Demo
 * 共享导航、图标与轻量交互
 */

const DEMO_VERSION = 'v1.6.5';

const APPEARANCE_KEY = 'aos-appearance';
const APPEARANCE_OPTS = [
  { id: 'light', label: '浅色', icon: 'sun' },
  { id: 'dark', label: '深色', icon: 'moon' },
  { id: 'system', label: '跟随系统', icon: 'monitor' },
];

/** 尽早上色，减少闪烁 */
(function bootstrapAppearance() {
  try {
    const v = localStorage.getItem(APPEARANCE_KEY);
    const pref = v === 'light' || v === 'dark' || v === 'system' ? v : 'dark';
    const resolved =
      pref === 'system'
        ? window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches
          ? 'light'
          : 'dark'
        : pref;
    document.documentElement.setAttribute('data-aos-theme', resolved);
    document.documentElement.setAttribute('data-aos-appearance', pref);
  } catch (_) { /* ignore */ }
})();

/** 侧栏：概览 → 工作台 → AIP → 本体 → 数据 → Apollo（使用优先 · 中文为主） */
const DEMO_PAGES = [
  { id: 'index', href: 'index.html', label: '概览', icon: 'home' },
  { section: '工作台 L3' },
  { id: 'workshop', href: 'workshop.html', label: '应用列表', icon: 'apps' },
  { id: 'workshop-canvas', href: 'workshop-canvas.html', label: '画布编辑', icon: 'layers' },
  { id: 'workshop-module', href: 'workshop-module.html', label: '运营台', icon: 'inbox' },
  { id: 'workshop-object-view', href: 'workshop-object-view.html', label: '知识图谱', icon: 'graph' },
  { id: 'workshop-aip-chat', href: 'workshop-aip-chat.html', label: 'Buddy · 智能助手', icon: 'chat' },
  { id: 'workshop-cop', href: 'workshop-cop.html', label: '态势大屏', icon: 'ontology' },
  { id: 'workshop-publish', href: 'workshop-publish.html', label: '发布入口', icon: 'server' },
  { id: 'workshop-module-interface', href: 'workshop-module-interface.html', label: '模块接口', icon: 'apps' },
  { id: 'workshop-events', href: 'workshop-events.html', label: '事件配置', icon: 'bell' },
  { section: 'AIP 决策引擎' },
  { id: 'agents', href: 'agents.html', label: 'Chatbot Studio', icon: 'chat' },
  { id: 'aip-logic', href: 'aip-logic.html', label: 'AIP 逻辑画布', icon: 'workflow' },
  { id: 'aip-tools', href: 'aip-tools.html', label: 'Agent 工具面板', icon: 'wrench' },
  { id: 'aip-capabilities', href: 'aip-capabilities.html', label: '重能力接入', icon: 'film' },
  { id: 'aip-draft-inbox', href: 'aip-draft-inbox.html', label: 'Draft 审批台', icon: 'inbox' },
  { id: 'aip-evals', href: 'aip-evals.html', label: 'Evals 门控', icon: 'check' },
  { id: 'aip-decision-lineage', href: 'aip-decision-lineage.html', label: '决策谱系', icon: 'git' },
  { id: 'aip-model-providers', href: 'aip-model-providers.html', label: '模型供应商', icon: 'plug' },
  { id: 'aip-model-router', href: 'aip-model-router.html', label: '模型路由', icon: 'spark' },
  { id: 'aip-maturity', href: 'aip-maturity.html', label: '成熟度楼梯', icon: 'stairs' },
  { section: '本体 · 数字孪生' },
  { id: 'ontology', href: 'ontology.html', label: '本体管理（数字孪生）', icon: 'ontology' },
  { id: 'ontology-funnel', href: 'ontology-funnel.html', label: '漏斗管道', icon: 'funnel' },
  { id: 'funnel', href: 'funnel.html', label: 'OKF 行业漏斗', icon: 'spark' },
  { id: 'ontology-graph-health', href: 'ontology-graph-health.html', label: '图谱健康度', icon: 'heart' },
  { id: 'ontology-wiki', href: 'ontology-wiki.html', label: '活知识 Wiki', icon: 'wiki' },
  { id: 'ontology-branches', href: 'ontology-branches.html', label: '分支管理', icon: 'git' },
  { section: '数据集成' },
  { id: 'data-connection', href: 'data-connection.html', label: '数据连接', icon: 'plug' },
  { id: 'data-connection-agents', href: 'data-connection-agents.html', label: '边缘代理', icon: 'server' },
  { id: 'media-sets', href: 'media-sets.html', label: '媒体集', icon: 'film' },
  { id: 'pipeline-list', href: 'pipeline-list.html', label: '管道构建', icon: 'workflow' },
  { id: 'pipeline-proposals', href: 'pipeline-proposals.html', label: '管道提案', icon: 'git' },
  { id: 'schedules', href: 'schedules.html', label: '计划编辑器', icon: 'bell' },
  { id: 'builds', href: 'builds.html', label: '搭建', icon: 'layers' },
  { id: 'dataset', href: 'dataset.html', label: '数据集预览', icon: 'table' },
  { id: 'code-repositories', href: 'code-repositories.html', label: '代码库', icon: 'layers' },
  { id: 'lineage', href: 'lineage.html', label: '数据沿袭', icon: 'git' },
  { id: 'health', href: 'health.html', label: '数据健康', icon: 'heart' },
  { section: '交付 Apollo' },
  { id: 'apollo-hub', href: 'apollo-hub.html', label: 'Hub 舰队', icon: 'server' },
  { id: 'apollo-release', href: 'apollo-release.html', label: 'Release 通道', icon: 'stairs' },
  { id: 'apollo-spoke', href: 'apollo-spoke.html', label: 'Spoke 详情', icon: 'plug' },
  { id: 'apollo-ferry', href: 'apollo-ferry.html', label: 'Ferry 摆渡', icon: 'film' },
  { id: 'apollo-assets', href: 'apollo-assets.html', label: 'FDE 资产包', icon: 'spark' },
  { id: 'apollo-change-mgmt', href: 'apollo-change-mgmt.html', label: '变更审批', icon: 'inbox' },
  { id: 'apollo-config', href: 'apollo-config.html', label: '配置与密钥', icon: 'wrench' },
];

const ICONS = {
  home: '<path stroke-linecap="round" stroke-linejoin="round" d="M3 9.5L12 3l9 6.5V20a1 1 0 01-1 1h-5v-6H9v6H4a1 1 0 01-1-1V9.5z"/>',
  plug: '<path stroke-linecap="round" stroke-linejoin="round" d="M12 22v-5M9 7V2M15 7V2M7 13h10a2 2 0 002-2V7a5 5 0 00-10 0v4a2 2 0 002 2z"/>',
  server: '<rect x="3" y="4" width="18" height="6" rx="1"/><rect x="3" y="14" width="18" height="6" rx="1"/><circle cx="7" cy="7" r="1" fill="currentColor" stroke="none"/><circle cx="7" cy="17" r="1" fill="currentColor" stroke="none"/>',
  workflow: '<circle cx="6" cy="6" r="2"/><circle cx="18" cy="6" r="2"/><circle cx="12" cy="18" r="2"/><path stroke-linecap="round" d="M8 6h8M7 7.5L10 16M17 7.5L14 16"/>',
  layers: '<path stroke-linecap="round" stroke-linejoin="round" d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>',
  table: '<rect x="3" y="5" width="18" height="14" rx="1"/><path d="M3 10h18M9 10v9M15 10v9"/>',
  git: '<circle cx="6" cy="6" r="2"/><circle cx="6" cy="18" r="2"/><circle cx="18" cy="12" r="2"/><path stroke-linecap="round" d="M6 8v8M8 6h5a3 3 0 013 3v0a3 3 0 01-3 3H8"/>',
  spark: '<path stroke-linecap="round" stroke-linejoin="round" d="M12 3l1.5 5.5L19 10l-5.5 1.5L12 17l-1.5-5.5L5 10l5.5-1.5L12 3z"/>',
  heart: '<path stroke-linecap="round" stroke-linejoin="round" d="M4.5 12.5l7.5 7 7.5-7a4.5 4.5 0 10-6.4-6.4L12 7.6l-.6-.5A4.5 4.5 0 004.5 12.5z"/>',
  film: '<rect x="3" y="5" width="18" height="14" rx="1"/><path stroke-linecap="round" d="M7 5v14M17 5v14M3 10h4M17 10h4M3 14h4M17 14h4"/>',
  ontology: '<circle cx="12" cy="12" r="3"/><path stroke-linecap="round" d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
  funnel: '<path stroke-linecap="round" stroke-linejoin="round" d="M4 4h16l-5 7v5l-6 4v-9L4 4z"/>',
  wiki: '<path stroke-linecap="round" d="M4 5h16v14H4zM8 9h8M8 13h5"/>',
  stairs: '<path stroke-linecap="round" stroke-linejoin="round" d="M4 20h4v-4h4v-4h4V8h4"/>',
  wrench: '<path stroke-linecap="round" stroke-linejoin="round" d="M14.7 6.3a1 1 0 000 1.4l1.6 1.6a1 1 0 001.4 0l3.77-3.77a6 6 0 01-7.94 7.94l-6.91 6.91a2.12 2.12 0 01-3-3l6.91-6.91a6 6 0 017.94-7.94l-3.76 3.76z"/>',
  apps: '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>',
  inbox: '<path stroke-linecap="round" stroke-linejoin="round" d="M4 13h4l2 3h4l2-3h4v6H4v-6zM4 13l2-8h12l2 8"/>',
  graph: '<circle cx="6" cy="12" r="2"/><circle cx="18" cy="6" r="2"/><circle cx="18" cy="18" r="2"/><path stroke-linecap="round" d="M8 12h6M15 7.5l-5 3M15 16.5l-5-3"/>',
  chat: '<path stroke-linecap="round" stroke-linejoin="round" d="M21 11.5a8.5 8.5 0 01-8.5 8.5H5l-3 3V11.5A8.5 8.5 0 0110.5 3h2A8.5 8.5 0 0121 11.5z"/>',
  search: '<circle cx="11" cy="11" r="7"/><path stroke-linecap="round" d="M20 20l-3-3"/>',
  bell: '<path stroke-linecap="round" stroke-linejoin="round" d="M15 17h5l-1.4-1.4A2 2 0 0118 14.2V11a6 6 0 10-12 0v3.2c0 .5-.2 1-.6 1.4L4 17h5M10 20a2 2 0 002-2h-2a2 2 0 002 2z"/>',
  chevron: '<path stroke-linecap="round" stroke-linejoin="round" d="M9 5l7 7-7 7"/>',
  back: '<path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7"/>',
  plus: '<path stroke-linecap="round" d="M12 5v14M5 12h14"/>',
  check: '<path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/>',
  sun: '<circle cx="12" cy="12" r="4"/><path stroke-linecap="round" d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
  moon: '<path stroke-linecap="round" stroke-linejoin="round" d="M21 14.5A8.5 8.5 0 1111.5 3 7 7 0 0021 14.5z"/>',
  monitor: '<rect x="3" y="4" width="18" height="12" rx="1"/><path stroke-linecap="round" d="M8 20h8M12 16v4"/>',
};

function svgIcon(name, cls = 'w-4 h-4') {
  const paths = ICONS[name] || ICONS.home;
  return `<svg class="${cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">${paths}</svg>`;
}

function statusDot(status) {
  const colors = {
    ok: 'bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.5)]',
    warn: 'bg-amber-400 shadow-[0_0_8px_rgba(251,191,36,0.4)]',
    err: 'bg-rose-400 shadow-[0_0_8px_rgba(251,113,133,0.4)]',
    run: 'bg-cyan-400 animate-pulse shadow-[0_0_8px_rgba(34,211,238,0.5)]',
  };
  return `<span class="inline-block w-2 h-2 rounded-full ${colors[status] || colors.ok}"></span>`;
}

function getAppearancePref() {
  try {
    const v = localStorage.getItem(APPEARANCE_KEY);
    if (v === 'light' || v === 'dark' || v === 'system') return v;
  } catch (_) { /* ignore */ }
  return 'dark';
}

function resolveTheme(pref) {
  if (pref === 'light' || pref === 'dark') return pref;
  if (typeof window !== 'undefined' && window.matchMedia) {
    return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  }
  return 'dark';
}

function applyAppearance(pref) {
  const resolved = resolveTheme(pref);
  document.documentElement.setAttribute('data-aos-theme', resolved);
  document.documentElement.setAttribute('data-aos-appearance', pref);
  document.documentElement.style.colorScheme = resolved;
  const btn = document.getElementById('aos-appearance-btn');
  if (btn) {
    const opt = APPEARANCE_OPTS.find((o) => o.id === pref) || APPEARANCE_OPTS[1];
    btn.innerHTML = `${svgIcon(opt.icon, 'w-3.5 h-3.5')} 外观`;
  }
  document.querySelectorAll('[data-appearance]').forEach((el) => {
    el.classList.toggle('is-selected', el.dataset.appearance === pref);
  });
}

function setAppearance(pref) {
  try {
    localStorage.setItem(APPEARANCE_KEY, pref);
  } catch (_) { /* ignore */ }
  applyAppearance(pref);
}

function initAppearance() {
  const pref = getAppearancePref();
  applyAppearance(pref);
  if (window.matchMedia) {
    const mq = window.matchMedia('(prefers-color-scheme: light)');
    const onChange = () => {
      if (getAppearancePref() === 'system') applyAppearance('system');
    };
    if (mq.addEventListener) mq.addEventListener('change', onChange);
    else if (mq.addListener) mq.addListener(onChange);
  }
}

function mountAppearanceControl(host) {
  if (!host || host.querySelector('#aos-appearance')) return;
  const wrap = document.createElement('div');
  wrap.id = 'aos-appearance';
  wrap.className = 'aos-appearance';
  wrap.innerHTML = `
    <button type="button" id="aos-appearance-btn" class="aos-appearance-btn" aria-haspopup="menu" aria-expanded="false">外观</button>
    <div class="aos-appearance-menu" role="menu">
      ${APPEARANCE_OPTS.map(
        (o) => `<button type="button" role="menuitemradio" class="aos-appearance-item" data-appearance="${o.id}">
          ${svgIcon(o.icon, 'w-3.5 h-3.5')}<span>${o.label}</span>
          <span class="aos-check">${svgIcon('check', 'w-3.5 h-3.5')}</span>
        </button>`
      ).join('')}
    </div>`;
  host.insertBefore(wrap, host.firstChild);
  const btn = wrap.querySelector('#aos-appearance-btn');
  btn.addEventListener('click', (e) => {
    e.stopPropagation();
    const open = wrap.classList.toggle('is-open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  wrap.querySelectorAll('[data-appearance]').forEach((el) => {
    el.addEventListener('click', (e) => {
      e.stopPropagation();
      setAppearance(el.dataset.appearance);
      wrap.classList.remove('is-open');
      btn.setAttribute('aria-expanded', 'false');
    });
  });
  document.addEventListener('click', () => {
    wrap.classList.remove('is-open');
    btn.setAttribute('aria-expanded', 'false');
  });
  applyAppearance(getAppearancePref());
}

/** 注入全局侧栏 */
function initShell(activeId, breadcrumbs) {
  initAppearance();
  const navEl = document.getElementById('app-nav');
  const bcEl = document.getElementById('app-breadcrumb');
  if (navEl) {
    navEl.innerHTML = DEMO_PAGES.map((p) => {
      if (p.section) {
        return `<div class="aos-nav-section">${p.section}</div>`;
      }
      const active = p.id === activeId;
      return `<a href="${p.href}" class="aos-nav-link${active ? ' is-active' : ''}">${svgIcon(p.icon, 'w-4 h-4 shrink-0')}<span>${p.label}</span></a>`;
    }).join('');
  }
  if (bcEl && breadcrumbs) {
    bcEl.innerHTML = breadcrumbs
      .map((b, i) => {
        if (b.href && i < breadcrumbs.length - 1) {
          return `<a href="${b.href}" class="hover:opacity-80 transition-opacity" style="color:var(--aos-accent)">${b.label}</a>`;
        }
        return `<span class="aos-text">${b.label}</span>`;
      })
      .join(`<span class="aos-faint mx-1.5">${svgIcon('chevron', 'w-3 h-3 inline opacity-50')}</span>`);
  }
  const header = document.querySelector('header');
  if (header) {
    let actions = header.querySelector('.flex.items-center.gap-2, .flex.items-center.gap-3, .flex.gap-2.items-center, .flex.gap-2');
    if (!actions) {
      actions = document.createElement('div');
      actions.className = 'flex items-center gap-2';
      header.appendChild(actions);
    }
    mountAppearanceControl(actions);
  }
}

/** Tab 切换 · 面板可在 tab-group 外（如 main 内），向上找 scope */
function initTabs(containerSelector) {
  document.querySelectorAll(`${containerSelector} [data-tab]`).forEach((btn) => {
    btn.addEventListener('click', () => {
      const group = btn.closest('[data-tab-group]');
      const target = btn.dataset.tab;
      const scope = group.closest('[data-tabs-root]') || group.parentElement;

      group.querySelectorAll('[data-tab]').forEach((t) => {
        const active = t.dataset.tab === target;
        t.classList.toggle('tab-active', active);
        t.classList.toggle('text-gray-400', !active);
        t.classList.toggle('text-gray-100', active);
        t.classList.toggle('font-medium', active);
        t.classList.toggle('border-b-2', active);
        t.classList.toggle('border-cyan-400', active);
        t.classList.toggle('border-transparent', !active);
      });

      scope.querySelectorAll('[data-tab-panel]').forEach((p) => {
        p.classList.toggle('hidden', p.dataset.tabPanel !== target);
      });
    });
  });
}

/** 代理列表选中 */
function initAgentList() {
  document.querySelectorAll('.agent-item').forEach((item) => {
    item.addEventListener('click', () => {
      document.querySelectorAll('.agent-item').forEach((i) => i.classList.remove('active'));
      item.classList.add('active');
      const id = item.dataset.agent;
      document.querySelectorAll('[data-agent-panel]').forEach((p) => {
        p.classList.toggle('hidden', p.dataset.agentPanel !== id);
      });
    });
  });
}

/** 存储路由向导 · 单选与解析路径联动 */
function initStorageRouter() {
  const form = document.getElementById('storage-router-form');
  if (!form) return;

  const targets = form.querySelectorAll('[name="storage-target"]');
  const pathSelect = form.querySelector('#parse-path');
  const hint = form.querySelector('#storage-hint');
  const xlsxWarn = form.querySelector('#xlsx-warn');

  const pathByTarget = {
    dataset: 'structured',
    media_doc: 'unstructured',
    media_sheet: 'unstructured',
    stream: 'timeseries',
  };

  const hints = {
    dataset: 'CSV · JSON · JDBC 表 · API 响应 → Dataset（Text/Parquet）',
    media_doc: 'PDF · 图像 · 音视频 · Word/PPT → Document 型媒体集',
    media_sheet: 'XLSX/XLSM → Spreadsheet 型媒体集（schema: spreadsheet）',
    stream: 'Kafka · IoT · MQTT → 流数据集（Avro）',
    smallfile: '单文件 <128KB 且无需原件预览 → 直入 Dataset，不建 MediaSet（避免元数据碎片）',
  };

  const pathByTargetExt = { ...pathByTarget, smallfile: 'structured' };

  function update() {
    const selected = form.querySelector('[name="storage-target"]:checked');
    if (!selected) return;
    const val = selected.value;
    if (pathSelect) pathSelect.value = pathByTargetExt[val] || 'structured';
    if (hint) hint.textContent = hints[val] || '';
    if (xlsxWarn) xlsxWarn.classList.toggle('hidden', val !== 'media_doc');
  }

  targets.forEach((r) => r.addEventListener('change', update));
  update();
}

/** 同步页 · 读取路由 query 预填 */
function applySyncRoutingParams() {
  const params = new URLSearchParams(window.location.search);
  const target = params.get('target');
  const path = params.get('path');
  const elTarget = document.querySelector('[data-sync-target]');
  const elPath = document.querySelector('[data-sync-path]');
  const elTitle = document.querySelector('[data-sync-title]');
  if (!target) return;

  const labels = {
    dataset: '数据集',
    media_doc: '媒体集 · 文档',
    media_sheet: '媒体集 · 电子表格',
    stream: '流数据集',
  };
  const paths = {
    structured: '结构化 · Apply Schema',
    semistructured: '半结构化 · Explode',
    unstructured: '非结构化 · Doc Intel 五步',
    timeseries: '时序 · Stream + CDC',
  };

  if (elTarget) elTarget.textContent = labels[target] || target;
  if (elPath && path) elPath.textContent = paths[path] || path;
  if (elTitle && target.startsWith('media')) {
    elTitle.textContent = '创建媒体集同步';
  }
}

/** AIP 成熟度楼梯 · WF-AIP-00 */
function initAipMaturity() {
  const root = document.getElementById('maturity-stairs');
  if (!root) return;
  const label = document.getElementById('maturity-label');
  const hint = document.getElementById('maturity-hint');
  const toast = document.getElementById('maturity-toast');
  const hints = {
    1: '适合摸索。固化可复用对话模式后再升 L2。',
    2: '挂 Workshop Agent 组件 → 升 L3；勿直接开 L4。',
    3: '一线试用通过后，再申请 L4（须 Eval 绿 + Draft 默认）。',
    4: 'L4：失败率>5% 自动熔断降 L3；冷模型须预热。须 Eval 绿 + Draft 默认。',
  };
  const labels = {
    1: '○ L1 临时分析',
    2: '◆ L2 任务 Agent',
    3: '◆ L3 Agentic 应用',
    4: '⚠ L4 自动化（熔断护栏）',
  };

  function setLevel(n) {
    root.dataset.level = String(n);
    root.querySelectorAll('[data-mat]').forEach((card) => {
      const on = Number(card.dataset.mat) === n;
      card.classList.toggle('maturity-active', on);
      card.classList.toggle('border-amber-400/50', on);
      card.classList.toggle('bg-amber-400/10', on);
      card.classList.toggle('ring-1', on);
      card.classList.toggle('ring-amber-400/30', on);
      card.classList.toggle('border-white/[0.08]', !on);
      card.classList.toggle('bg-slate-900/50', !on);
    });
    if (label) label.textContent = labels[n] || '';
    if (hint) hint.textContent = hints[n] || '';
  }

  root.querySelectorAll('[data-mat]').forEach((card) => {
    card.addEventListener('click', () => setLevel(Number(card.dataset.mat)));
  });

  const btnL3 = document.getElementById('btn-mark-l3');
  if (btnL3) {
    btnL3.addEventListener('click', () => {
      setLevel(3);
      if (toast) {
        toast.textContent = '已标记 L3：请打开工作台绑定 Agent（Demo → workshop.html）。';
        toast.classList.remove('hidden');
      }
    });
  }
  const btnL4 = document.getElementById('btn-req-l4');
  if (btnL4) {
    btnL4.addEventListener('click', () => {
      setLevel(4);
      if (toast) {
        toast.textContent = 'L4 评审示意：Eval 未绿 → 拦截。若已上线且失败率>5% → 熔断降级 L3。';
        toast.classList.remove('hidden');
        toast.classList.add('text-rose-300');
      }
    });
  }
  const btnBreak = document.getElementById('btn-sim-breaker');
  if (btnBreak && toast) {
    btnBreak.addEventListener('click', () => {
      setLevel(3);
      toast.textContent = '模拟熔断：失败率 7.2% > 5% → 已自动降级到 L3，须人工确认后恢复。';
      toast.classList.remove('hidden');
      toast.classList.add('text-rose-300');
    });
  }
}

/** AIP Agent 工具面板 · WF-AIP-05T */
function initAipTools() {
  const detailRoot = document.getElementById('tool-detail');
  if (!detailRoot) return;

  document.querySelectorAll('[data-tool-card]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const id = btn.dataset.toolCard;
      document.querySelectorAll('[data-tool-card]').forEach((b) => {
        const on = b === btn;
        b.classList.toggle('border-amber-400/40', on);
        b.classList.toggle('bg-amber-400/10', on);
        b.classList.toggle('border-white/[0.08]', !on);
      });
      detailRoot.querySelectorAll('[data-detail]').forEach((p) => {
        p.classList.toggle('hidden', p.dataset.detail !== id);
      });
    });
  });

  const save = document.getElementById('btn-save-tools');
  const toast = document.getElementById('tools-toast');
  const mode = document.getElementById('tool-mode');
  if (save && toast) {
    save.addEventListener('click', () => {
      const m = mode ? mode.value : 'native';
      toast.textContent = `已保存（示意）· 调用模式=${m} · 写路径仍受 Draft / 提交标准约束`;
      toast.classList.remove('hidden');
    });
  }
}

/** AIP Logic 画布轻交互 · WF-AIP-02 */
function initAipLogic() {
  const run = document.getElementById('btn-run-logic');
  const empty = document.getElementById('debug-empty');
  const panel = document.getElementById('debug-panel');
  if (run && empty && panel) {
    run.addEventListener('click', () => {
      empty.classList.add('hidden');
      panel.classList.remove('hidden');
    });
  }
  const autoBtn = document.getElementById('btn-create-auto');
  const autoMsg = document.getElementById('auto-msg');
  if (autoBtn && autoMsg) {
    autoBtn.addEventListener('click', () => {
      autoMsg.textContent = '已预填自动化（示意）：输出=Ontology edits → 提案审核。开放提案约 24h。';
      autoMsg.classList.remove('hidden');
      autoMsg.classList.add('text-amber-200');
    });
  }
  const pub = document.getElementById('btn-publish-logic');
  if (pub) {
    pub.addEventListener('click', () => {
      pub.textContent = '已发布（示意）';
      pub.classList.add('opacity-80');
    });
  }
}

/** 工作台 Inbox · Selection 联动 WF-WS-03 */
function initWorkshopModule() {
  const rows = document.querySelectorAll('[data-order-row]');
  const selEl = document.getElementById('ws-selection');
  const titleEl = document.getElementById('ws-obj-title');
  const metaEl = document.getElementById('ws-obj-meta');
  const scoreEl = document.getElementById('ws-obj-score');
  const shopEl = document.getElementById('ws-obj-shop');
  const toast = document.getElementById('ws-toast');
  if (!rows.length) return;

  const data = {
    'ORD-8821': { title: 'ORD-8821', meta: '类型：Order · 状态：异常', score: '0.91', shop: '店铺A' },
    'ORD-8819': { title: 'ORD-8819', meta: '类型：Order · 状态：异常', score: '0.72', shop: '店铺B' },
    'ORD-8801': { title: 'ORD-8801', meta: '类型：Order · 状态：正常', score: '0.21', shop: '店铺C' },
  };

  function select(id) {
    rows.forEach((r) => {
      const on = r.dataset.orderRow === id;
      r.classList.toggle('bg-sky-400/10', on);
      r.classList.toggle('border-l-2', on);
      r.classList.toggle('border-sky-400', on);
    });
    const d = data[id];
    if (selEl) selEl.textContent = id;
    if (titleEl && d) titleEl.textContent = d.title;
    if (metaEl && d) metaEl.textContent = d.meta;
    if (scoreEl && d) scoreEl.textContent = d.score;
    if (shopEl && d) shopEl.textContent = d.shop;
  }

  rows.forEach((r) => r.addEventListener('click', () => select(r.dataset.orderRow)));
  select('ORD-8821');

  const dimEl = document.getElementById('ws-sel-dims');
  if (dimEl) dimEl.textContent = '3 / 10';

  let lastKey = '';
  const actionBtn = document.getElementById('ws-btn-appeal');
  if (actionBtn && toast) {
    actionBtn.addEventListener('click', () => {
      const id = selEl ? selEl.textContent : 'ORD-8821';
      const key = `appeal:${id}`;
      if (key === lastKey) {
        toast.textContent = `幂等命中：同一 idempotencyKey，不重复执行（ACT-07）`;
        toast.classList.remove('hidden');
        return;
      }
      lastKey = key;
      toast.textContent = `Action「发起申诉」· key=${key} · HITL / Draft Dataset（示意）`;
      toast.classList.remove('hidden');
    });
  }
}

/** 工作台图谱 · 点节点换 Selection WF-WS-04 */
function initWorkshopGraph() {
  const nodes = document.querySelectorAll('[data-graph-node]');
  const sel = document.getElementById('graph-selection');
  const view = document.getElementById('graph-obj-view');
  const modal = document.getElementById('ws-action-modal');
  if (!nodes.length) return;

  const info = {
    pollutant: { name: '污染物 · PM2.5超标事件', wiki: '排放限值 35µg/m³ · 适用《大气法》§42' },
    enterprise: { name: '企业 · 环科示范厂', wiki: '信用代码 91xxxxx · Wiki：排污许可有效期 2027-03' },
    law: { name: '法规 · 大气污染防治法', wiki: '条款 §42–§45 · 行业定制 Wiki 已挂载' },
  };

  nodes.forEach((n) => {
    n.addEventListener('click', () => {
      nodes.forEach((x) => x.classList.remove('ring-2', 'ring-sky-400'));
      n.classList.add('ring-2', 'ring-sky-400');
      const id = n.dataset.graphNode;
      const d = info[id];
      if (sel) sel.textContent = d ? d.name : id;
      if (view && d) {
        view.querySelector('[data-g-name]').textContent = d.name;
        view.querySelector('[data-g-wiki]').textContent = d.wiki;
      }
    });
  });

  const openAct = document.getElementById('btn-open-action');
  const closeAct = document.getElementById('btn-close-action');
  if (openAct && modal) openAct.addEventListener('click', () => modal.classList.remove('hidden'));
  if (closeAct && modal) closeAct.addEventListener('click', () => modal.classList.add('hidden'));
  const submit = document.getElementById('btn-submit-action');
  const toast = document.getElementById('graph-toast');
  let graphKey = '';
  if (submit && toast && modal) {
    submit.addEventListener('click', () => {
      const selName = sel ? sel.textContent : 'obj';
      const key = `case:${selName}`;
      if (key === graphKey) {
        toast.textContent = '幂等：重复提交已忽略（ACT-07）';
        toast.classList.remove('hidden');
        return;
      }
      graphKey = key;
      modal.classList.add('hidden');
      toast.textContent = '立案 Action 已送审（示意）· Draft 隔离 · 非直调 Logic';
      toast.classList.remove('hidden');
    });
  }
  const dimG = document.getElementById('graph-sel-dims');
  if (dimG) dimG.textContent = 'Selection 维 2 / 10';
}

/** Buddy 侧栏 + Assist 浮层 WF-WS-06/07 */
function initWorkshopAip() {
  const chat = document.getElementById('buddy-panel');
  const assist = document.getElementById('assist-popover');
  const chip = document.getElementById('ctx-chip');
  const openBuddy = document.getElementById('btn-open-buddy');
  const openAssist = document.getElementById('btn-open-assist');
  if (openBuddy && chat) {
    openBuddy.addEventListener('click', () => chat.classList.toggle('hidden'));
  }
  if (openAssist && assist) {
    openAssist.addEventListener('click', () => assist.classList.toggle('hidden'));
  }
  document.querySelectorAll('[data-pick-order]').forEach((btn) => {
    btn.addEventListener('click', () => {
      const id = btn.dataset.pickOrder;
      if (chip) chip.textContent = `Selection: ${id}`;
      document.querySelectorAll('[data-pick-order]').forEach((b) => {
        b.classList.toggle('bg-sky-400/15', b === btn);
        b.classList.toggle('border-sky-400/40', b === btn);
      });
    });
  });
  const send = document.getElementById('buddy-send');
  const log = document.getElementById('buddy-log');
  const input = document.getElementById('buddy-input');
  if (send && log && input) {
    send.addEventListener('click', () => {
      const q = input.value.trim() || '这单为啥卡海关？';
      const ctx = chip ? chip.textContent : 'Selection';
      log.innerHTML += `<div class="mt-3"><div class="text-sky-300 text-xs">你 · ${ctx}</div><div class="text-gray-200 text-sm mt-1">${q}</div></div>`;
      log.innerHTML += `<div class="mt-3"><div class="text-amber-300 text-xs">Buddy</div><div class="text-gray-300 text-sm mt-1">已读 Order + Wiki「清关规则」。建议发起申诉 Action（须 HITL）。</div><button type="button" class="mt-2 text-xs text-sky-400 hover:underline" id="buddy-suggest-action">打开申诉表单 →</button></div>`;
      input.value = '';
      const sug = document.getElementById('buddy-suggest-action');
      if (sug) sug.addEventListener('click', () => { window.location.href = 'workshop-module.html'; });
    });
  }
}

window.DemoUI = {
  svgIcon,
  statusDot,
  initShell,
  initTabs,
  initAgentList,
  initStorageRouter,
  applySyncRoutingParams,
  initAipMaturity,
  initAipTools,
  initAipLogic,
  initWorkshopModule,
  initWorkshopGraph,
  initWorkshopAip,
  setAppearance,
  getAppearancePref,
  DEMO_VERSION,
};

#!/usr/bin/env python3
"""
批量刷新所有 HTML 页面的 shell 样式为截图风格 v2.0
只替换 shell 区域的通用 Tailwind 类，保留页面内容不变
"""

import os
import re
from pathlib import Path

HTML_DIR = Path("/Users/ddt/work/projects/ai_agent/docs/palantier/foundry/html")

# 全局替换规则（安全：这些模式主要出现在 shell 区域）
GLOBAL_REPLACES = [
    # body 基础
    ('class="aos-themeable bg-slate-950 text-gray-400 min-h-screen flex"',
     'class="aos-themeable bg-[#0b0e17] text-[#8b92a8] min-h-screen flex"'),

    # aside 容器（匹配所有颜色变体）
    ('class="w-56 shrink-0 border-r border-white/[0.08] bg-slate-900/80 flex flex-col"',
     'class="w-[220px] shrink-0 border-r border-white/[0.055] bg-[#0d111c] flex flex-col"'),

    # aside 品牌区
    ('class="p-4 border-b border-white/[0.08]"',
     'class="px-4 py-3.5 border-b border-white/[0.055]"'),

    # aside 底部
    ('class="p-3 border-t border-white/[0.08] text-xs text-gray-500"',
     'class="px-3 py-2.5 border-t border-white/[0.055] text-[11px] text-[#5c6275]"'),

    # header 高度和 padding
    ('class="h-14 border-b border-white/[0.08] flex items-center justify-between px-6"',
     'class="h-[52px] border-b border-white/[0.055] flex items-center justify-between px-5"'),
    ('class="h-14 border-b border-white/[0.08] bg-slate-950/90 backdrop-blur flex items-center justify-between px-6 shrink-0"',
     'class="h-[52px] border-b border-white/[0.055] bg-[rgba(11,14,23,0.95)] backdrop-blur flex items-center justify-between px-5 shrink-0"'),
    ('class="h-14 border-b border-white/[0.08] flex items-center justify-between px-4 lg:px-6 gap-2 flex-wrap"',
     'class="h-[52px] border-b border-white/[0.055] flex items-center justify-between px-4 lg:px-5 gap-2 flex-wrap"'),

    # 搜索框样式
    ('class="w-64 pl-9 pr-3 py-1.5 rounded-lg bg-slate-900 border border-white/[0.08] text-sm text-gray-300 placeholder-gray-500 focus:outline-none focus:border-cyan-400/40 transition-colors"',
     'class="w-56 pl-8 pr-3 py-[5px] rounded-md bg-[#111522] border border-white/[0.08] text-[13px] text-[#e8eaf0] placeholder-[#5c6275] focus:outline-none focus:border-[rgba(99,179,237,0.3)] transition-colors"'),
    ('class="w-72 pl-9 pr-3 py-1.5 rounded-lg bg-slate-900 border border-white/[0.08] text-sm text-gray-300 placeholder-gray-500 focus:outline-none focus:border-violet-400/40"',
     'class="w-64 pl-8 pr-3 py-[5px] rounded-md bg-[#111522] border border-white/[0.08] text-[13px] text-[#e8eaf0] placeholder-[#5c6275] focus:outline-none focus:border-[rgba(167,139,250,0.3)] transition-colors"'),

    # 品牌文字
    ('class="text-gray-100 text-sm font-medium leading-tight"',
     'class="text-[#e8eaf0] text-[13px] font-medium leading-tight tracking-tight"'),
    ('class="text-gray-500 text-xs leading-snug mt-0.5"',
     'class="text-[#5c6275] text-[11px] leading-snug mt-0.5"'),

    # 面包屑
    ('class="flex items-center text-sm"',
     'class="flex items-center text-[13px]"'),

    # 通知按钮
    ('class="p-2 rounded-lg hover:bg-white/[0.04] transition-colors text-gray-400"',
     'class="p-1.5 rounded-md hover:bg-white/[0.035] transition-colors text-[#8b92a8]"'),

    # 用户头像
    ('class="w-8 h-8 rounded-full bg-gradient-to-br from-cyan-400/30 to-sky-500/20 border border-white/[0.08]"',
     'class="w-7 h-7 rounded-full bg-gradient-to-br from-[rgba(99,179,237,0.3)] to-[rgba(56,189,248,0.15)] border border-white/[0.08]"'),
    ('class="w-8 h-8 rounded-full bg-gradient-to-br from-violet-400/30 to-fuchsia-500/20 border border-white/[0.08]"',
     'class="w-7 h-7 rounded-full bg-gradient-to-br from-[rgba(167,139,250,0.3)] to-[rgba(217,70,239,0.15)] border border-white/[0.08]"'),
    ('class="w-8 h-8 rounded-full bg-gradient-to-br from-amber-400/30 to-orange-500/20 border border-white/[0.08]"',
     'class="w-7 h-7 rounded-full bg-gradient-to-br from-[rgba(251,191,36,0.3)] to-[rgba(249,115,22,0.15)] border border-white/[0.08]"'),

    # 通用文字色替换（在页面内容中也适用）
    ('text-gray-100', 'text-[#e8eaf0]'),
    ('text-gray-500', 'text-[#5c6275]'),
    ('text-gray-300', 'text-[#e8eaf0]'),
    ('text-gray-400', 'text-[#8b92a8]'),
    ('text-gray-600', 'text-[#3d4358]'),

    # 通用边框替换
    ('border-white/[0.08]', 'border-white/[0.055]'),

    # 通用背景替换
    ('bg-slate-950/90 backdrop-blur', 'bg-[rgba(11,14,23,0.95)] backdrop-blur'),
    ('bg-slate-950/50', 'bg-[rgba(11,14,23,0.5)]'),
    ('bg-slate-950/40', 'bg-[rgba(11,14,23,0.4)]'),
    ('bg-slate-950', 'bg-[#0b0e17]'),
    ('bg-slate-900', 'bg-[#111522]'),
    ('bg-slate-900/80', 'bg-[rgba(17,21,34,0.8)]'),
    ('bg-slate-900/50', 'bg-[rgba(17,21,34,0.5)]'),

    # 按钮/徽章中的颜色
    ('text-cyan-400', 'text-[#63b3ed]'),
    ('text-sky-300', 'text-[#7dd3fc]'),
    ('text-sky-400', 'text-[#63b3ed]'),
    ('text-amber-300', 'text-[#fcd34d]'),
    ('text-amber-400', 'text-[#fbbf24]'),
    ('text-violet-300', 'text-[#c4b5fd]'),
    ('text-violet-400', 'text-[#a78bfa]'),
    ('text-emerald-300', 'text-[#6ee7b7]'),
    ('text-emerald-400', 'text-[#34d399]'),
    ('text-rose-300', 'text-[#fda4af]'),
    ('text-rose-400', 'text-[#fb7185]'),

    # 背景色（保留透明度）
    ('bg-cyan-400/10', 'bg-[rgba(99,179,237,0.1)]'),
    ('bg-cyan-400/5', 'bg-[rgba(99,179,237,0.05)]'),
    ('bg-sky-400/10', 'bg-[rgba(99,179,237,0.1)]'),
    ('bg-sky-400/5', 'bg-[rgba(99,179,237,0.05)]'),
    ('bg-amber-400/10', 'bg-[rgba(251,191,36,0.1)]'),
    ('bg-amber-400/5', 'bg-[rgba(251,191,36,0.05)]'),
    ('bg-violet-400/10', 'bg-[rgba(167,139,250,0.1)]'),
    ('bg-violet-400/5', 'bg-[rgba(167,139,250,0.05)]'),
    ('bg-emerald-400/10', 'bg-[rgba(52,211,153,0.1)]'),
    ('bg-emerald-400/5', 'bg-[rgba(52,211,153,0.05)]'),
    ('bg-rose-400/10', 'bg-[rgba(251,113,133,0.1)]'),

    # 边框色
    ('border-cyan-400/20', 'border-[rgba(99,179,237,0.2)]'),
    ('border-cyan-400/30', 'border-[rgba(99,179,237,0.3)]'),
    ('border-cyan-400/40', 'border-[rgba(99,179,237,0.4)]'),
    ('border-sky-400/20', 'border-[rgba(99,179,237,0.2)]'),
    ('border-sky-400/30', 'border-[rgba(99,179,237,0.3)]'),
    ('border-sky-400/40', 'border-[rgba(99,179,237,0.4)]'),
    ('border-amber-400/20', 'border-[rgba(251,191,36,0.2)]'),
    ('border-amber-400/30', 'border-[rgba(251,191,36,0.3)]'),
    ('border-amber-400/40', 'border-[rgba(251,191,36,0.4)]'),
    ('border-violet-400/20', 'border-[rgba(167,139,250,0.2)]'),
    ('border-violet-400/30', 'border-[rgba(167,139,250,0.3)]'),
    ('border-violet-400/40', 'border-[rgba(167,139,250,0.4)]'),
    ('border-emerald-400/20', 'border-[rgba(52,211,153,0.2)]'),
    ('border-emerald-400/30', 'border-[rgba(52,211,153,0.3)]'),
    ('border-rose-400/20', 'border-[rgba(251,113,133,0.2)]'),

    # 阴影
    ('shadow-black/20', 'shadow-[rgba(0,0,0,0.2)]'),
    ('shadow-black/30', 'shadow-[rgba(0,0,0,0.3)]'),
]

# 品牌区图标颜色映射（保留各模块的强调色）
BRAND_ICON_MAP = {
    'bg-cyan-400/10 border border-cyan-400/20': 'bg-[rgba(99,179,237,0.12)] border border-[rgba(99,179,237,0.2)]',
    'bg-amber-400/10 border border-amber-400/20': 'bg-[rgba(251,191,36,0.12)] border border-[rgba(251,191,36,0.2)]',
    'bg-violet-400/10 border border-violet-400/20': 'bg-[rgba(167,139,250,0.12)] border border-[rgba(167,139,250,0.2)]',
    'bg-sky-400/10 border border-sky-400/20': 'bg-[rgba(99,179,237,0.12)] border border-[rgba(99,179,237,0.2)]',
    'text-cyan-400': 'text-[#63b3ed]',
    'text-amber-400': 'text-[#fbbf24]',
    'text-violet-400': 'text-[#a78bfa]',
    'text-sky-400': 'text-[#63b3ed]',
}

def process_file(filepath):
    content = filepath.read_text(encoding='utf-8')
    original = content

    # 应用全局替换
    for old, new in GLOBAL_REPLACES:
        content = content.replace(old, new)

    # 处理品牌区图标（保留颜色差异）
    for old, new in BRAND_ICON_MAP.items():
        content = content.replace(old, new)

    if content != original:
        filepath.write_text(content, encoding='utf-8')
        return True
    return False

def main():
    html_files = sorted(HTML_DIR.glob("*.html"))
    updated = 0
    skipped = 0

    for f in html_files:
        if f.name == "index.html":
            skipped += 1  # index.html 已单独处理
            continue
        try:
            if process_file(f):
                updated += 1
                print(f"  ✓ {f.name}")
            else:
                skipped += 1
        except Exception as e:
            print(f"  ✗ {f.name}: {e}")

    print(f"\n完成：更新 {updated} 个文件，跳过 {skipped} 个文件")

if __name__ == "__main__":
    main()

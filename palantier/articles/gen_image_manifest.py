#!/usr/bin/env python3
"""
扫描 docs/palantier 下全部 Markdown 文件，提取每张截图引用的元数据，
生成 IMAGE_MANIFEST.md 供写文章时按主题检索配图。

用法: python gen_image_manifest.py
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

BASE = Path(__file__).parent.parent  # docs/palantier/
OUTPUT = Path(__file__).parent / "IMAGE_MANIFEST.md"

# 匹配 ![alt](path) 和 <img src="path" alt="alt" ...>
MD_IMG_RE = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
HTML_IMG_RE = re.compile(r'<img\s+[^>]*src=["\']([^"\']+)["\'][^>]*(?:alt=["\']([^"\']*)["\'])?[^>]*>', re.IGNORECASE)
HTML_IMG_RE2 = re.compile(r'<img\s+[^>]*(?:alt=["\']([^"\']*)["\'])?[^>]*src=["\']([^"\']+)["\'][^>]*>', re.IGNORECASE)

# 截图文件扩展名
IMG_EXTS = {'.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp'}

def extract_title(content, filepath):
    """从 Markdown 内容提取文档标题"""
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('# ') and not line.startswith('## '):
            return line[2:].strip()
    # fallback: 用文件名
    return filepath.stem.replace('-', ' ').replace('_', ' ')

def extract_context(lines, line_idx, context_lines=2):
    """提取图片引用前后 N 行的非空文字上下文"""
    before = []
    after = []
    
    # 向前找上下文
    for i in range(line_idx - 1, max(line_idx - context_lines - 1, -1), -1):
        if i < 0:
            break
        text = lines[i].strip()
        if text and not text.startswith('![') and not text.startswith('<img'):
            before.insert(0, text)
            if len(before) >= context_lines:
                break
    
    # 向后找上下文
    for i in range(line_idx + 1, min(line_idx + context_lines + 1, len(lines))):
        text = lines[i].strip()
        if text and not text.startswith('![') and not text.startswith('<img'):
            after.append(text)
            if len(after) >= context_lines:
                break
    
    return before, after

def get_module(filepath):
    """从文件路径推断模块分类"""
    parts = filepath.parts
    # 找到 palantier 后的路径
    try:
        idx = parts.index('palantier')
        rel_parts = parts[idx+1:]
    except ValueError:
        rel_parts = parts
    
    if len(rel_parts) >= 2:
        if rel_parts[0] == 'foundry':
            if len(rel_parts) >= 3 and rel_parts[1] == 'pages':
                # foundry/pages/zh/foundry/<module>/...
                if len(rel_parts) >= 4:
                    return rel_parts[3] if rel_parts[2] == 'foundry' else '/'.join(rel_parts[2:4])
            return rel_parts[1] if len(rel_parts) > 1 else 'foundry'
        elif rel_parts[0] == 'AIP':
            if len(rel_parts) >= 2:
                return f"AIP/{rel_parts[1]}"
            return 'AIP'
        elif rel_parts[0] == '20_tech':
            return 'tech-docs'
        elif rel_parts[0] == 'prddetail':
            return 'prddetail'
        else:
            return rel_parts[0]
    return 'other'

def normalize_img_path(src, md_filepath):
    """将图片引用路径标准化为相对 docs/palantier 的路径"""
    # 去掉可能的 ../
    src = src.replace('\\', '/')
    
    # 如果是绝对路径或 URL
    if src.startswith('http://') or src.startswith('https://'):
        return src, None
    
    # 处理相对路径
    if src.startswith('../') or src.startswith('./'):
        resolved = (md_filepath.parent / src).resolve()
        try:
            rel = resolved.relative_to(BASE.resolve())
            return str(rel), str(resolved)
        except ValueError:
            return src, str(resolved)
    
    return src, None

def scan_markdown(md_path):
    """扫描单个 Markdown 文件，返回所有图片引用"""
    results = []
    try:
        content = md_path.read_text(encoding='utf-8')
    except Exception:
        try:
            content = md_path.read_text(encoding='utf-8', errors='replace')
        except:
            return results
    
    title = extract_title(content, md_path)
    lines = content.split('\n')
    
    # 找到 palantier 后的相对路径
    try:
        rel_path = md_path.relative_to(BASE)
    except ValueError:
        rel_path = md_path
    
    module = get_module(Path(str(rel_path)))
    
    for i, line in enumerate(lines):
        # Markdown 图片
        for match in MD_IMG_RE.finditer(line):
            alt = match.group(1).strip()
            src = match.group(2).strip()
            norm_src, abs_path = normalize_img_path(src, md_path)
            
            # 只关注图片文件
            ext = os.path.splitext(norm_src)[1].lower()
            if ext not in IMG_EXTS:
                continue
            
            before, after = extract_context(lines, i)
            results.append({
                'filename': os.path.basename(norm_src),
                'alt': alt,
                'src': norm_src,
                'doc_title': title,
                'doc_path': str(rel_path),
                'module': module,
                'line': i + 1,
                'context_before': before,
                'context_after': after,
            })
        
        # HTML <img> 图片
        for match in HTML_IMG_RE.finditer(line):
            src = match.group(1).strip()
            alt = (match.group(2) or '').strip() if match.lastindex >= 2 else ''
            norm_src, abs_path = normalize_img_path(src, md_path)
            
            ext = os.path.splitext(norm_src)[1].lower()
            if ext not in IMG_EXTS:
                continue
            
            before, after = extract_context(lines, i)
            results.append({
                'filename': os.path.basename(norm_src),
                'alt': alt,
                'src': norm_src,
                'doc_title': title,
                'doc_path': str(rel_path),
                'module': module,
                'line': i + 1,
                'context_before': before,
                'context_after': after,
            })
        
        for match in HTML_IMG_RE2.finditer(line):
            alt = (match.group(1) or '').strip() if match.lastindex >= 1 else ''
            src = match.group(2).strip()
            norm_src, abs_path = normalize_img_path(src, md_path)
            
            ext = os.path.splitext(norm_src)[1].lower()
            if ext not in IMG_EXTS:
                continue
            
            # 避免重复（HTML_IMG_RE 可能已经匹配）
            if any(r['src'] == norm_src and r['line'] == i + 1 for r in results):
                continue
            
            before, after = extract_context(lines, i)
            results.append({
                'filename': os.path.basename(norm_src),
                'alt': alt,
                'src': norm_src,
                'doc_title': title,
                'doc_path': str(rel_path),
                'module': module,
                'line': i + 1,
                'context_before': before,
                'context_after': after,
            })
    
    return results

def main():
    all_images = []
    md_files = sorted(BASE.rglob("*.md"))
    
    # 排除 articles 目录自身
    md_files = [f for f in md_files if 'articles' not in f.parts]
    
    print(f"Scanning {len(md_files)} markdown files...")
    
    for md_path in md_files:
        images = scan_markdown(md_path)
        all_images.extend(images)
    
    print(f"Found {len(all_images)} image references")
    
    # 按文件名去重（保留首次出现的引用，因为文档引用最完整）
    seen = {}
    unique_images = []
    for img in all_images:
        key = img['filename']
        if key not in seen:
            seen[key] = True
            unique_images.append(img)
    
    print(f"Unique images: {len(unique_images)}")
    
    # 按 module 分组
    by_module = defaultdict(list)
    for img in unique_images:
        by_module[img['module']].append(img)
    
    # 生成 IMAGE_MANIFEST.md
    lines = []
    lines.append("# 截图元数据清单 (IMAGE MANIFEST)")
    lines.append("")
    lines.append(f"> 自动生成 · 共 **{len(unique_images)}** 张唯一截图 · 来源：{len(md_files)} 篇 Markdown 文档")
    lines.append(f"> 生成时间：2026-07-26")
    lines.append("")
    lines.append("## 使用说明")
    lines.append("")
    lines.append("写文章时按模块查找截图。每条记录包含：")
    lines.append("- **文件名**：截图文件名（用于 Markdown 引用）")
    lines.append("- **alt**：原始 alt 文字（截图的官方描述）")
    lines.append("- **文档标题**：截图所在的 Foundry 文档标题")
    lines.append("- **上下文**：文档中引用截图前后的段落（提供画面描述线索）")
    lines.append("- **路径**：截图相对路径")
    lines.append("")
    lines.append("## 按模块分类索引")
    lines.append("")
    
    for module in sorted(by_module.keys()):
        imgs = by_module[module]
        lines.append(f"- **{module}** ({len(imgs)} 张)")
    lines.append("")
    
    # 按模块输出详情
    for module in sorted(by_module.keys()):
        imgs = by_module[module]
        lines.append(f"---")
        lines.append(f"")
        lines.append(f"## 模块: {module} ({len(imgs)} 张)")
        lines.append(f"")
        
        for img in imgs:
            lines.append(f"### {img['filename']}")
            lines.append(f"- **路径**: `{img['src']}`")
            if img['alt']:
                lines.append(f"- **alt**: {img['alt']}")
            lines.append(f"- **文档**: {img['doc_title']} (`{img['doc_path']}`)")
            if img['context_before']:
                ctx = ' | '.join(img['context_before'])
                # 截断过长的上下文
                if len(ctx) > 300:
                    ctx = ctx[:300] + '...'
                lines.append(f"- **上文**: {ctx}")
            if img['context_after']:
                ctx = ' | '.join(img['context_after'])
                if len(ctx) > 300:
                    ctx = ctx[:300] + '...'
                lines.append(f"- **下文**: {ctx}")
            lines.append("")
    
    OUTPUT.write_text('\n'.join(lines), encoding='utf-8')
    print(f"Generated: {OUTPUT}")
    print(f"Total lines: {len(lines)}")
    
    # 同时生成 JSON 版本，便于程序化检索
    json_output = OUTPUT.with_suffix('.json')
    with open(json_output, 'w', encoding='utf-8') as f:
        json.dump({
            'total': len(unique_images),
            'total_references': len(all_images),
            'modules': {m: len(v) for m, v in by_module.items()},
            'images': unique_images,
        }, f, ensure_ascii=False, indent=2)
    print(f"JSON: {json_output}")


if __name__ == '__main__':
    main()

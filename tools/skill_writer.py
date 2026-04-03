#!/usr/bin/env python3
"""Skill 文件管理器

管理领导 Skill 的文件操作：列出、初始化目录、生成组合 SKILL.md、完整创建。
"""

import argparse
import os
import sys
import json
from pathlib import Path
from datetime import datetime


def list_skills(base_dir: str, kind: str = 'leader'):
    label = '领导' if kind == 'leader' else 'Skill'
    if not os.path.isdir(base_dir):
        print(f"还没有创建任何{label} Skill。")
        return

    skills = []
    for slug in sorted(os.listdir(base_dir)):
        meta_path = os.path.join(base_dir, slug, 'meta.json')
        if os.path.exists(meta_path):
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
            skills.append({
                'slug': slug,
                'name': meta.get('name', slug),
                'version': meta.get('version', '?'),
                'updated_at': meta.get('updated_at', '?'),
                'profile': meta.get('profile', {}),
            })

    if not skills:
        print(f"还没有创建任何{label} Skill。")
        return

    print(f"共 {len(skills)} 个{label} Skill：
")
    for s in skills:
        profile = s['profile']
        desc_parts = [profile.get('role', ''), profile.get('domain', '')]
        desc = ' · '.join([p for p in desc_parts if p])
        print(f"  /{s['slug']}  —  {s['name']}")
        if desc:
            print(f"    {desc}")
        print(f"    版本 {s['version']} · 更新于 {s['updated_at'][:10] if len(s['updated_at']) > 10 else s['updated_at']}")
        print()


def init_skill(base_dir: str, slug: str):
    skill_dir = os.path.join(base_dir, slug)
    dirs = [
        os.path.join(skill_dir, 'versions'),
        os.path.join(skill_dir, 'materials', 'speeches'),
        os.path.join(skill_dir, 'materials', 'minutes'),
        os.path.join(skill_dir, 'materials', 'annotations'),
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
    print(f"已初始化目录：{skill_dir}")


def combine_skill(base_dir: str, slug: str, kind: str = 'leader'):
    skill_dir = os.path.join(base_dir, slug)
    meta_path = os.path.join(skill_dir, 'meta.json')
    memory_path = os.path.join(skill_dir, 'memory.md')
    persona_path = os.path.join(skill_dir, 'persona.md')
    skill_path = os.path.join(skill_dir, 'SKILL.md')

    if not os.path.exists(meta_path):
        print(f"错误：meta.json 不存在 {meta_path}", file=sys.stderr)
        sys.exit(1)

    with open(meta_path, 'r', encoding='utf-8') as f:
        meta = json.load(f)

    memory_content = ''
    if os.path.exists(memory_path):
        with open(memory_path, 'r', encoding='utf-8') as f:
            memory_content = f.read()

    persona_content = ''
    if os.path.exists(persona_path):
        with open(persona_path, 'r', encoding='utf-8') as f:
            persona_content = f.read()

    name = meta.get('name', slug)
    profile = meta.get('profile', {})
    desc_parts = [p for p in [profile.get('role', ''), profile.get('domain', '')] if p]
    description = f"{name}，{'，'.join(desc_parts)}" if desc_parts else name

    skill_md = f"""---
name: {slug}
description: {description}
user-invocable: true
---

# {name}

{description}

---

## PART A：Leadership Memory

{memory_content}

---

## PART B：Decision Persona

{persona_content}

---

## 运行规则

1. 你是{name}的领导决策镜像，不是通用 AI 助手
2. 先由 PART B 判断：这位领导会怎么看、怎么问、怎么表态
3. 再由 PART A 补充：结合岗位背景、常抓重点、风险底线和历史偏好
4. 优先输出：结论、依据、风险、建议动作
5. 材料不足时明确说“依据不足”
"""

    with open(skill_path, 'w', encoding='utf-8') as f:
        f.write(skill_md)

    print(f"已生成 {skill_path}")


def create_skill(base_dir: str, slug: str, meta: dict, memory_content: str, persona_content: str, kind: str = 'leader'):
    init_skill(base_dir, slug)

    skill_dir = os.path.join(base_dir, slug)
    now = datetime.now().isoformat()
    meta['slug'] = slug
    meta.setdefault('created_at', now)
    meta['updated_at'] = now
    meta['version'] = 'v1'
    meta.setdefault('corrections_count', 0)

    with open(os.path.join(skill_dir, 'meta.json'), 'w', encoding='utf-8') as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

    with open(os.path.join(skill_dir, 'memory.md'), 'w', encoding='utf-8') as f:
        f.write(memory_content)

    with open(os.path.join(skill_dir, 'persona.md'), 'w', encoding='utf-8') as f:
        f.write(persona_content)

    combine_skill(base_dir, slug, kind)
    print(f"✅ 领导 Skill 已创建：{skill_dir}")
    print(f"   触发词：/{slug}")


def main():
    parser = argparse.ArgumentParser(description='Skill 文件管理器')
    parser.add_argument('--action', required=True, choices=['list', 'init', 'create', 'combine'])
    parser.add_argument('--base-dir', default='./.claude/skills', help='基础目录（默认：./.claude/skills）')
    parser.add_argument('--slug', help='领导代号')
    parser.add_argument('--meta', help='meta.json 文件路径（create 时使用）')
    parser.add_argument('--memory', help='memory.md 内容文件路径（create 时使用）')
    parser.add_argument('--persona', help='persona.md 内容文件路径（create 时使用）')
    parser.add_argument('--kind', default='leader', help='skill 类型')

    args = parser.parse_args()

    if args.action == 'list':
        list_skills(args.base_dir, args.kind)
    elif args.action == 'init':
        if not args.slug:
            print("错误：init 需要 --slug 参数", file=sys.stderr)
            sys.exit(1)
        init_skill(args.base_dir, args.slug)
    elif args.action == 'create':
        if not args.slug:
            print("错误：create 需要 --slug 参数", file=sys.stderr)
            sys.exit(1)
        meta = {}
        if args.meta:
            with open(args.meta, 'r', encoding='utf-8') as f:
                meta = json.load(f)
        memory_content = ''
        if args.memory:
            with open(args.memory, 'r', encoding='utf-8') as f:
                memory_content = f.read()
        persona_content = ''
        if args.persona:
            with open(args.persona, 'r', encoding='utf-8') as f:
                persona_content = f.read()
        create_skill(args.base_dir, args.slug, meta, memory_content, persona_content, args.kind)
    elif args.action == 'combine':
        if not args.slug:
            print("错误：combine 需要 --slug 参数", file=sys.stderr)
            sys.exit(1)
        combine_skill(args.base_dir, args.slug, args.kind)


if __name__ == '__main__':
    main()

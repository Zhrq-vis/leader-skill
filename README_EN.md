<div align="center">

# Leader.skill

> *“Before the real briefing, let the leader review it once.”*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

<br>

Leader.skill distills a leader's decision logic, review habits, reporting preferences, and risk appetite into a reusable AI skill.

Feed it speeches, meeting notes, annotated slides, emails, policies, and project writeups.
It turns them into two runnable modules:
**Part A — Leadership Memory + Part B — Decision Persona**.

Use it to pre-review proposals, rehearse briefings, simulate follow-up questions, and draft leader-style comments.

</div>

---

## Installation

```bash
mkdir -p .claude/skills
git clone https://github.com/YOUR_USERNAME/leader-skill .claude/skills/create-leader
```

## Usage

Run:

```bash
/create-leader
```

Then provide the leader's alias, role background, style description, and source materials.
Invoke the generated skill with `/{slug}`.

## What it can do

- Proposal pre-review
- Briefing rewrite in leader style
- Meeting Q&A simulation
- Leader-comment generation
- Risk and boundary checks

## Data sources

- Speeches and meeting minutes
- Annotated reports / slides
- Emails and chat logs
- Policies and strategic documents
- Your own textual description of the leader

## Credits

Inspired by the broader open AgentSkills ecosystem and person-distillation skill patterns.

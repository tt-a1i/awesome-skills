<p align="center">
  <img src="assets/awesome-skills-hero.png" alt="从浏览器原生演示文稿到响应式交互原型的 Agent Skills 工作流" width="100%">
</p>

<div align="center">

# Awesome Skills

**把“做得好看”变成可复用、可执行、可验证的 Agent 工作流**

让 Agent 不只生成一个视觉草稿，而是交付能打开、能操作、能在真实设备上检查的作品

[![Agent Skills](https://img.shields.io/badge/agent_skills-3-DCF23E?style=flat-square&labelColor=171717)](#skills)
[![Output](https://img.shields.io/badge/output-HTML%20%2F%20CSS%20%2F%20JS-F35B2A?style=flat-square&labelColor=171717)](#两个视觉-skill-怎么选)
[![Runtime](https://img.shields.io/badge/runtime-browser_native-55DDE0?style=flat-square&labelColor=171717)](#质量门)

[**▶ 在线案例：别让一个线程从需求聊到代码写完**](https://verifiable-goal-weekly-share-public.pages.dev)

</div>

## 为什么做这个仓库

很多设计类提示词停在“生成一个看起来不错的页面”。这个仓库更关心完整交付：先读清内容和场景，建立视觉系统，生成真实文件，再用结构检查和浏览器截图验证结果

当前最核心的是两个互补的视觉 Skill：

- `create-html-deck` 负责演示叙事：固定画布、翻页、投屏和不同笔记本视口
- `design-artifact` 负责交互体验：响应式布局、关键状态、操作路径和产品级细节

## 两个视觉 Skill 怎么选

| | [`create-html-deck`](skills/create-html-deck/) | [`design-artifact`](skills/design-artifact/) |
|---|---|---|
| 主要产物 | 浏览器原生演示文稿、周会分享、技术演讲 | Landing page、交互原型、组件探索、产品 Mockup |
| 布局模型 | 1920×1080 固定画布，按视口等比缩放 | 响应式页面或应用布局 |
| 主要操作 | 翻页、键盘导航、演讲与投屏 | 滚动、表单、筛选、状态切换与完整主路径 |
| 重点验证 | 14 英寸 MacBook、常见笔记本、1080p 投影 | 目标视口、窄屏、交互状态、焦点与溢出 |
| 自带能力 | HTML 模板、结构检查器、便携资源约定 | 设计执行流程、结构检查器、产品状态清单 |

简单判断：需要“第几页”和演讲节奏时用 `create-html-deck`；需要滚动、点击和状态变化时用 `design-artifact`

## Skills

### `create-html-deck`

把源材料变成可以直接播放的 HTML 演示文稿，并对笔记本和投影环境做真实验证

- 一张幻灯片只承担一个叙事任务
- 固定 1920×1080 设计画布，不因小屏而改变版式
- 支持方向键、Home、End、Page Up、Page Down 和可见页码
- 使用相对资源路径，HTML 与 `assets/` 可以一起复制和分享
- 自带 [`deck-template.html`](skills/create-html-deck/assets/deck-template.html) 与 [`check_deck.py`](skills/create-html-deck/scripts/check_deck.py)

### `design-artifact`

把设计 Brief 变成可以操作的高保真 HTML 作品，而不是停在风格描述或静态截图

- 先读现有产品、代码、Token 和素材，再决定视觉语言
- 用明确的字体、颜色、间距、边框、动效系统约束结果
- 覆盖默认、加载、空、错误、成功等真正影响体验的状态
- 支持独立 HTML，也支持在真实项目技术栈中落地
- 自带 [`check_artifact.py`](skills/design-artifact/scripts/check_artifact.py) 检查语义壳、资源、ID 和基础可访问性

### `learn-anything`

通过适应性讲解、苏格拉底式追问和主动回忆，帮助学习者建立能复述、能应用的理解

[查看完整 Skill →](skills/learn-anything/SKILL.md)

## 安装

安装整个仓库：

```bash
npx skills@latest add tt-a1i/awesome-skills -g -y
```

只安装一个 Skill：

```bash
npx skills@latest add tt-a1i/awesome-skills --skill create-html-deck -g -y
npx skills@latest add tt-a1i/awesome-skills --skill design-artifact -g -y
```

安装后可以直接这样说：

```text
Use $create-html-deck to turn these notes into a weekly-share deck
Use $design-artifact to turn this brief into a responsive interactive prototype
```

## 质量门

两个视觉 Skill 都把“结构正确”和“视觉正确”分开验证

```bash
python3 skills/create-html-deck/scripts/check_deck.py /absolute/path/to/deck.html
python3 skills/design-artifact/scripts/check_artifact.py /absolute/path/to/artifact.html
```

脚本负责发现缺失资源、重复 ID、关键 HTML 契约和基础可访问性问题；最终仍需在真实浏览器中检查构图、换行、图片裁切、控制台错误和目标视口

## 仓库结构

```text
skills/
├── create-html-deck/
│   ├── SKILL.md
│   ├── assets/deck-template.html
│   └── scripts/check_deck.py
├── design-artifact/
│   ├── SKILL.md
│   └── scripts/check_artifact.py
└── learn-anything/
    └── SKILL.md
```

## Attribution

`design-artifact` 改编自 BadTechBandit 的 `claude-design`，保留其 [MIT License](skills/design-artifact/LICENSE)

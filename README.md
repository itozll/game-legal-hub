# Game Legal Hub

游戏隐私政策和服务条款的独立 Git 仓库。项目根以项目设置为准，各功能子目录独立管理；默认只读取当前项目设置目录。ring-titan 是游戏仓库，game-legal-hub 是协议仓库。

```text
game-legal-hub/
├── docs/
│   ├── .nojekyll            # 禁用 Jekyll，保留静态网页
│   ├── index.html           # 协议中心入口
│   ├── ring-titan/
│   │   ├── zh-CN/
│   │   │   ├── privacy-policy.md
│   │   │   └── terms-of-service.md
│   │   ├── en/
│   │   │   ├── privacy-policy.md
│   │   │   └── terms-of-service.md
│   │   └── README.md
│   └── meowdoku/
│       ├── zh-CN/privacy-policy.md
│       ├── zh-CN/terms-of-service.md
│       ├── en/privacy-policy.md
│       ├── en/terms-of-service.md
│       ├── zh-Hans/privacy-policy.md
│       ├── zh-Hans/terms-of-service.md
│       ├── zh-Hant/privacy-policy.md
│       ├── ja/privacy-policy.md
│       ├── ko/privacy-policy.md
│       ├── es/privacy-policy.md
│       ├── pt/privacy-policy.md
│       ├── privacy/          # 原始多语言网页与资产
│       ├── index.html        # 保留语言入口
│       └── README.md
├── templates/               # zh-CN、en 共用协议模板
├── tools/validate.py
├── registry.json
├── AGENTS.md
└── README.md
```

## 当前内容

| 游戏 | 语言 | 隐私政策 | 服务条款 |
| --- | --- | --- | --- |
| Meow Garden（meowdoku） | en、zh-CN/zh-Hans、zh-Hant、ja、ko、es、pt | 原文迁入，生效日期 2026-10-07 | 中英及 zh-Hans：1.0.0-draft，未生效；其他语言 missing |
| Ring Titan | zh-CN、en | 1.0.0-draft，未生效 | 1.0.0-draft，未生效 |

- [Ring Titan 中文隐私政策](docs/ring-titan/zh-CN/privacy-policy.md) / [English](docs/ring-titan/en/privacy-policy.md)
- [Ring Titan 中文服务条款](docs/ring-titan/zh-CN/terms-of-service.md) / [English](docs/ring-titan/en/terms-of-service.md)
- [Ring Titan 发布核对说明](docs/ring-titan/README.md)
- [Meow Garden 中文服务条款草案](docs/meowdoku/zh-CN/terms-of-service.md) / [English draft](docs/meowdoku/en/terms-of-service.md)
- [Meow Garden 迁移说明](docs/meowdoku/README.md)

## 登记表规则

registry.json 的 schema_version 为 1。games 记录稳定游戏 id、展示名称、来源版本及 locales；每种语言有 privacy-policy、terms-of-service 两项，记录 status、version、updated_date、effective_date 和相对 path。

- published：协议正文已有生效日期；Meow Garden 保留旧协议状态，不代表新站点已上线。
- draft：待发布草案，effective_date 必须为 null，不能作为已生效协议展示。
- missing：未提供该协议，路径、版本及日期均为 null。
- zh-Hans 是 Meow Garden 简体中文兼容别名；两份规范文本必须一致。
- 模板不登记为游戏协议，不可把占位符原样发布。

## 维护与验证

```sh
python -X utf8 tools/validate.py
# 初次迁移还核对原始内容（需要明确授权访问旧仓库）
python -X utf8 tools/validate.py --migration-source ../meowdoku-legal
```

维护规范 Markdown 时同步 registry.json。Meow Garden 兼容网站仍按原方式手工同步 privacy/*.md 和 *.html；验证脚本检查登记数据、日期与状态、链接目标、简体别名、规范文本与兼容文本一致性，以及迁移字节一致性；不代替协议内容及 HTML 正文同步核对。

发布 Ring Titan 前完成其发布核对说明，填入实际主体与联系方式、确认宿主与目标地区、更新生效日期并将中英文状态一起改为 published。

## 发布与旧链接

发布内容位于 docs/，其中 docs/.nojekyll 保留静态网页并禁用 Jekyll。GitHub Pages 设置选择 Deploy from a branch，分支 main，目录 /docs，点击 Save。发布根目录 docs 不出现在 URL 中，也没有 games 路径段。

部署后的预期地址（尚未验证上线）：

- 协议中心：https://itozll.github.io/game-legal-hub/
- Meow Garden：https://itozll.github.io/game-legal-hub/meowdoku/
- 英文隐私网页：https://itozll.github.io/game-legal-hub/meowdoku/privacy/en.html

原 ?lang= 和 ?select=1 行为仍保留。Ring Titan 当前只有 Markdown 草案，没有发布网页；.nojekyll 模式不会自动把 Markdown 转换为 HTML。

旧 https://itozll.github.io/meowdoku-legal/ 及 /privacy/ 链接保留；未删除旧仓库、未修改旧站点或游戏内协议链接。新站点确认可访问后再单独切换入口。

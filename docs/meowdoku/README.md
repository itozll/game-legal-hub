# Meow Garden（meowdoku）协议

2026-10-14 从 meowdoku-legal 迁入。原始版本：6703701f5b2479166c140ef619bb65a46b3e7fad。

- 各语言目录中的 privacy-policy.md 是规范文本，内容逐字节保留；生效日期仍为 2026-10-07。
- zh-CN 为规范简体中文目录；zh-Hans 保留为同内容兼容目录。其余语言为 en、zh-Hant、ja、ko、es、pt、ru；共八种语言（加简体中文兼容别名）。
- privacy/ 与 index.html 保留原有相对地址与语言入口行为，并已加入俄语匹配与选择项。新站点从 /docs 发布后，可在站点的 meowdoku/ 路径访问（URL 不包含 docs 或 games），支持 ?lang=en、?lang=zh-Hant 和 ?select=1。
- 旧仓库没有服务条款。2026-10-14 新增全部已支持语言的服务条款（zh-CN、zh-Hans、zh-Hant、en、ja、ko、es、pt），版本为 1.0.0-draft，effective_date 为 null。新增条款是待发布草案，不属于原协议迁移内容。
- 隐私规范 Markdown 为唯一维护源；修改 docs/meowdoku/{语言}/privacy-policy.md 后运行 python -X utf8 tools/build-meowdoku-privacy.py，再运行 python -X utf8 tools/validate.py 和 node --test tests/meowdoku-privacy-entry.test.cjs。zh-CN 是简体规范源，zh-Hans 及 privacy/*.md、*.html 是同步生成物。
- 旧线上地址 https://itozll.github.io/meowdoku-legal/ 保持不变。本次仅在 meowdoku-cocos 仓库保留旧地址跳转，不修改旧 meowdoku-legal 仓库。

## 2026-10-16 从游戏仓库完成迁移

meowdoku-cocos 的八语言协议、网页生成脚本和路由测试现已迁入本仓库。俄语译文更新日期为 2026-10-14，沿用 2026-10-07 生效日期，条款范围不变；俄语服务条款尚未提供，登记为 missing，不生成虚假条款。

- [迁移来源与 SHA-256 清单](../../references/meowdoku/cocos-migration.json)记录源提交和原始文件摘要；验证时使用 --migration-source ../meowdoku-cocos，可从迁移前 Git 快照核验正文及模板，即使游戏工作区已移除副本也可验证。
- [原始 Word 模板](../../references/meowdoku/用户隐私保护指引设置.docx)移至非发布目录 references/meowdoku/，它不是已生效协议。
- 网页生成脚本位于 tools/build-meowdoku-privacy.py，入口语言匹配测试位于 tests/meowdoku-privacy-entry.test.cjs；测试只依赖本仓库的 registry.json，不要求读取游戏仓库。
- 游戏仓库不再维护协议正文、模板或生成脚本；历史网页只跳转到协议中心，并保留 lang、select 及段落锚点。

## 服务条款草案

- [简体中文](zh-CN/terms-of-service.md) / [繁體中文](zh-Hant/terms-of-service.md) / [English](en/terms-of-service.md) / [日本語](ja/terms-of-service.md) / [한국어](ko/terms-of-service.md) / [Español](es/terms-of-service.md) / [Português](pt/terms-of-service.md) / [简体兼容别名](zh-Hans/terms-of-service.md)
- 本地存档、无账号/云存档/支付、插屏及激励视频奖励等功能描述以本仓库现有隐私政策为依据；本次没有重新核验游戏版本或宿主供应链。
- 开发者名称 gaoguodong 与邮箱 joiky@163.com 来自现有隐私政策；不据此推断注册地、法律实体类型或专属管辖法院。
- 本次仅添加规范 Markdown 草案，未生成服务条款 HTML 或修改现有隐私网页。启用 .nojekyll 时 Markdown 不会自动成为 HTML 页面。

## 服务条款发布核对

1. 核实签约运营主体、服务联系邮箱、实际游戏版本、目标宿主、发布地区及年龄要求。
2. 核实广告奖励展示与发放规则、异常处理及适用平台规则，保持条款与实际功能一致。
3. 结合运营主体及发布地区确认适用法律、消费者权利和争议处理信息，完善依法需要的提示与同意流程。
4. 确认生效日期，更新版本，将已核实的语言状态从 draft 改为 published；按目标地区需要补充翻译与可阅读的 HTML 入口。
5. 不将草案作为已生效协议展示，不以继续使用或观看广告替代依法需要的明确同意。

起草时参考的格式条款与消费者权利规则：[《中华人民共和国民法典》第496—498条](https://www.cac.gov.cn/2020-06/01/c_15925617772683192.htm)、[欧盟委员会不公平合同条款说明](https://commission.europa.eu/law/law-topic/consumer-protection-law/consumer-contract-law/unfair-contract-terms-directive_en)。这些参考不表示已确定本游戏的适用法或已完成所有发行地区审核。

# Ring Titan 发布核对说明

中英文隐私政策与服务条款为 1.0.0-draft，更新于 2026-10-14，尚未生效。registry.json 的 effective_date 为 null。

## 已核实的游戏事实

依据 ring-titan 提交 e1ac50df8a36b37cf4c87001232c06cc72b608da：

- assets/scripts/platform/GameStorage.ts：ring-titan.progress.v1 保存剧情状态与音效，ring-titan.daily.v1 保存每日挑战；使用 Cocos sys.localStorage。
- assets/scripts/core/PuzzleRules.ts：Progress 保存 level、best、coins、sound 与 puzzle；Puzzle 保存圆环、锁扣、操作次数及可选挑战状态。
- assets/scripts/core/DailyChallenge.ts：使用设备本地日期；恢复最多读取最近 120 个日期条目的有效完成记录，不是 Meow Garden 的 UTC 日期或 366 条。
- assets/scripts/gameplay/RingTitan.ts：ring-titan.locale 保存语言选择，默认 en，不自动读取系统语言。
- docs/ADS_DESIGN.md：广告仅为设计，当前未接入 OpenPaaS 广告 SDK。扫描 assets/scripts 未发现账号、云存档、支付或独立分析上报实现。

## 发布前需确认

1. 运营主体及隐私、服务联系方式；不能仅因为同一代码仓库所有者就认定为 Meow Garden 的 gaoguodong / joiky@163.com。
2. 实际发布版本、目标宿主及其隐私政策、运行时数据处理与实际托管方式。
3. 发布地区、年龄要求、必要的同意与消费者权利流程、适用法律和争议处理说明。
4. 游戏内协议入口、发布后的稳定 URL 与中英文展示方式。游戏 UI 当前包含其他语言，隐私协议提供中英西俄；服务条款仍仅提供中英，西俄条款暂缺。
5. 将草案中的待确认内容填入；完成核对后改正式版本和 published 状态，设置真实生效日期，中英文同步。

草案 HTML 阅读页已接入现有 GitHub Pages，入口为 [协议阅读页](index.html)。中英文正文与规范 Markdown 保持一致，草案不作为已生效协议；正式发布前仍须完成上述核对。

## 西班牙语和俄语隐私协议译文（2026-10-20）

基于 2026-10-14 英文草案新增西班牙语和俄语隐私协议及 HTML 阅读页；不新增数据处理事实，不修改原文、生效日期或运营信息。译文仍为 1.0.0-draft，effective_date 为 null，服务条款登记为 missing。原文中英版本和译文需在正式发布前一起核实并同步。

- [Español](es/privacy-policy.html)
- [Русский](ru/privacy-policy.html)

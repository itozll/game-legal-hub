# BlockPop 发布核对说明

四语隐私政策为 1.0.0-draft，更新于 2026-10-28，尚未生效；登记中的 effective_date 为 null。这里只生成草案与阅读页，不把生成文件或推送当作正式协议生效。

## 游戏事实依据

依据 BlockPop 当前开发工作区中 assets/scripts/BlockPopGame.ts 及 docs/openpaas.md；玩法实现尚未提交，不将仅含商城文件的旧提交伪称为代码依据。

- blockpop.classic.v1：棋盘、待放方块、分数、连击、未消除次数和颜色。
- blockpop.best.v1：最高分；blockpop.sound：声音偏好。
- sud.getAppBaseInfo().language：只用于匹配界面语言，不保存语言，不回退设备语言。
- 当前没有登录、支付、广告 SDK、云存档、独立分析或崩溃上报实现。
- wasmUrl 当前为空，未启用远程计算模块下载；未来启用时须核实资源服务来源及访问日志。
- 本地游戏记录与实际宿主、网页托管方的独立处理分开说明，不把本地存储描述成匿名化、加密或绝对安全。

## 发布前必需资料

- 运营主体的法定名称、隐私联系邮箱和实际请求处理渠道；未沿用其他游戏的主体信息。
- 实际发行地区、目标宿主、其政策链接和相关用户、未成年人及同意流程。
- 实际发布版本、数据处理目的与依据、接收方、保存期限、删除机制、托管地区及适用的跨境安排。
- 根据上线版本复核本地与第三方数据流，不能将未来广告或云服务计划写成已经运行的能力。
- 真实生效日期、正式版本号及四语一致性审阅；核实完成后才修改 published 状态。
- 验证商城及游戏内四语链接；游戏内入口当前隐藏，本次不修改游戏场景、组件或发布状态。

## 文件和语言

- [简体中文](zh-CN/privacy-policy.html)
- [English](en/privacy-policy.html)
- [Русский](ru/privacy-policy.html)
- [العربية](ar/privacy-policy.html)

商城 zh-Hans 对应协议目录 zh-CN；英文、俄语、阿拉伯语分别对应 en、ru、ar。服务条款不在本次请求内，四语均登记为 missing，不生成虚构条款。

规范正文为各目录的 privacy-policy.md；HTML 由 tools/build-blockpop-privacy.py 生成。修改正文后重新生成，并用 --check 验证字节一致性。阿拉伯语阅读页使用 lang=ar、dir=rtl，不反转原文字符。阅读页只有标题和正文，不加载外部字体或脚本。

## 官方核对来源

- [GitHub Pages 数据收集](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages#data-collection)：其官方文档说明访问 IP 的安全日志行为；仅在采用该托管服务时适用。
- [GitHub 隐私声明](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement)：第三方自身的处理以其政策为准。
- [ICO 隐私告知内容指南](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/the-right-to-be-informed/what-privacy-information-should-we-provide/)：用于检查运营主体、联系、用途、保留与权利项目是否遗漏；不据此认定英国法律必然适用于尚未确定地区的游戏。

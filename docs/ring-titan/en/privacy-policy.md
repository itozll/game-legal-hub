# Ring Titan Privacy Policy

Status: Draft for publication (not an effective policy)
Version: 1.0.0-draft
Updated: 2026-10-14
Effective date: To be confirmed before publication

## 1 Scope and contact

This policy describes information handling by the current Ring Titan game and its policy website. The operator's identity and privacy contact email must be confirmed and inserted before publication; another game's operator details have not been assumed. See the [publication checklist](../README.md).

The game may run in a browser or host application. The host's own accounts, permissions and processing are governed by its policies. This policy describes the game's processing and does not replace host policies.

## 2 Information saved by the game and its purposes

The current game has no account registration, sign-in, cloud saves or payments. It has not integrated advertising SDKs, separate behavioral analytics or crash reporting. Current code does not actively collect names, profile pictures, phone numbers, government identifiers, contacts, precise location, camera or microphone data.

To resume play and retain settings, the game uses Cocos local storage to save:

- Story progress: current level, best progress, Stardust balance and sound setting.
- Unfinished puzzles: ring angles and removal states, released clips, move counts and other puzzle state.
- Daily challenges: dates, the current attempt, rotation energy, moves, hints, stars and completion records, to resume play and calculate completion streaks.
- Language preferences: the interface language selected by the player.

Daily puzzles use the device's local date and are generated locally without sending dates or progress to developer servers. When restoring daily saves, current code retains valid completion records from at most the latest 120 date entries. The game defaults to English and reads the saved language selection; it currently does not automatically select a language from system settings.

## 3 Storage, use and deletion

These records are stored on the device or in local storage supplied by its runtime. Current implementation has no developer server receiving saves and no feature uploading, selling or publicly disclosing saves. Local storage is not anonymization; people with access to the device or host storage may see game records.

Saves usually remain until you clear the relevant site or host game data, or the runtime removes them. Actual uninstall, backup and restore behavior depends on the platform. Clearing data may permanently remove progress, Stardust and preferences; there is no cloud recovery. You can change sound and language settings in the game and delete local records through browser site data controls or a host's game data removal feature.

If you contact the operator, it uses the contact information and issue details you provide to address the request, retaining them as necessary to resolve it and satisfy applicable legal obligations. Do not proactively send government identifiers or a complete game save.

## 4 Third-party runtimes and future features

Ring Titan currently has not integrated OpenPaaS advertising interfaces. Its advertising design document describes plans, not active advertising or current advertising data processing.

The actual host or distribution platform may independently process account, device or network information. Before publication, verify the target host, its policy links, data categories, purposes, retention, processing locations and user controls. Unverified third-party behavior must not be described as game behavior, and third-party data must not be promised to remain local.

Before introducing advertising, cloud saves, payments or analytics, update this policy, provide required notices and obtain valid consent where required by applicable law. Watching rewarded advertising must not be treated as consent to personalized advertising or tracking.

## 5 Requests and minors

Rights available under applicable law, including access, copies, correction, deletion, withdrawal of consent and complaints, can be requested using the privacy contact stated in the published version. The operator cannot remotely inspect or delete saves existing only on your device and not supplied to it, but can explain local controls. Requests concerning a host's independent processing can also be addressed to that host.

Minors should follow the age requirements of their jurisdiction and host and use the game with guardian guidance. Current code has no age collection or identity verification; this does not establish that every jurisdiction's child protection requirements have been implemented. Obtain guardian consent before processing where legally required; use of the game alone is not that consent.

## 6 Policy website

This repository provides static policies and the legacy Meow Garden language selection script. It includes no analytics scripts, advertising SDKs, tracking pixels, external fonts or reading-tracking cookies. Visiting a policy page does not read game saves.

If hosted on GitHub Pages, GitHub logs and stores visitor IP addresses for security purposes. GitHub is responsible for that processing. See [GitHub Pages data collection](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages#data-collection) and the [GitHub Privacy Statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement). Confirm hosting configuration before publication. Third-party storage locations, retention and international processing depend on their policies and actual services.

## 7 Security and updates

The operator takes reasonable security measures appropriate to its processing. Device and host security also affect local saves. Update the version and date when features or processing change. Continued use does not replace legally required consent. Chinese and English versions should remain consistent; translation differences do not limit rights under applicable law.

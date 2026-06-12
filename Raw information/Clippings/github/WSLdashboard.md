---
title: "owu/wsl-dashboard: A GUI manager for WSL featuring a modern UI — a lightweight, low‑memory, high‑performance dashboard to manage WSL instances."
source: "https://github.com/owu/wsl-dashboard"
author:
published:
created: 2026-06-12
description: "A GUI manager for WSL featuring a modern UI — a lightweight, low‑memory, high‑performance dashboard to manage WSL instances. - owu/wsl-dashboard"
tags:
  - "clippings"
---
## WSL Dashboard

[![WSL Dashboard Logo](https://github.com/owu/wsl-dashboard/raw/main/assets/logo/logo.png)](https://github.com/owu/wsl-dashboard/blob/main/assets/logo/logo.png)

A modern, high-performance, lightweight, and low-memory WSL (Windows Subsystem for Linux) instance management dashboard. Built with Rust and Slint for a premium native experience.

---

```
Notice:​

- This software is not distributed through the Microsoft Store.
- Any application listed there under the same name is unauthorized and may be counterfeit.
- Please do not download it to avoid potential scams.
```

---

I18N: English | [简体中文](https://github.com/owu/wsl-dashboard/blob/main/manual/README_zh_CN.md) | [繁體中文](https://github.com/owu/wsl-dashboard/blob/main/manual/README_zh_TW.md) | [हिन्दी](https://github.com/owu/wsl-dashboard/blob/main/manual/README_hi.md) | [Español](https://github.com/owu/wsl-dashboard/blob/main/manual/README_es.md) | [Français](https://github.com/owu/wsl-dashboard/blob/main/manual/README_fr.md) | [العربية](https://github.com/owu/wsl-dashboard/blob/main/manual/README_ar.md) | [বাংলা](https://github.com/owu/wsl-dashboard/blob/main/manual/README_bn.md) | [Português](https://github.com/owu/wsl-dashboard/blob/main/manual/README_pt.md) | [Русский](https://github.com/owu/wsl-dashboard/blob/main/manual/README_ru.md) | [اردو](https://github.com/owu/wsl-dashboard/blob/main/manual/README_ur.md) | [Bahasa Indonesia](https://github.com/owu/wsl-dashboard/blob/main/manual/README_id.md) | [Deutsch](https://github.com/owu/wsl-dashboard/blob/main/manual/README_de.md) | [日本語](https://github.com/owu/wsl-dashboard/blob/main/manual/README_ja.md) | [Türkçe](https://github.com/owu/wsl-dashboard/blob/main/manual/README_tr.md) | [한국어](https://github.com/owu/wsl-dashboard/blob/main/manual/README_ko.md) | [Italiano](https://github.com/owu/wsl-dashboard/blob/main/manual/README_it.md) | [Nederlands](https://github.com/owu/wsl-dashboard/blob/main/manual/README_nl.md) | [Svenska](https://github.com/owu/wsl-dashboard/blob/main/manual/README_sv.md) | [Čeština](https://github.com/owu/wsl-dashboard/blob/main/manual/README_cs.md) | [Ελληνικά](https://github.com/owu/wsl-dashboard/blob/main/manual/README_el.md) | [Magyar](https://github.com/owu/wsl-dashboard/blob/main/manual/README_hu.md) | [עברית](https://github.com/owu/wsl-dashboard/blob/main/manual/README_he.md) | [Norsk](https://github.com/owu/wsl-dashboard/blob/main/manual/README_no.md) | [Dansk](https://github.com/owu/wsl-dashboard/blob/main/manual/README_da.md) | [Suomi](https://github.com/owu/wsl-dashboard/blob/main/manual/README_fi.md) | [Slovenčina](https://github.com/owu/wsl-dashboard/blob/main/manual/README_sk.md) | [Slovenščina](https://github.com/owu/wsl-dashboard/blob/main/manual/README_sl.md) | [Íslenska](https://github.com/owu/wsl-dashboard/blob/main/manual/README_is.md)

---

## 📑 Table of Contents

## 🌍 Language Support

English, Simplified Chinese, Traditional Chinese, Hindi, Spanish, French, Arabic, Bengali, Portuguese, Russian, Urdu, Indonesian, German, Japanese, Turkish, Korean, Italian, Dutch, Swedish, Czech, Greek, Hungarian, Hebrew, Norwegian, Danish, Finnish, Slovak, Slovenian, Icelandic

## 🚀 Key Features & Usage

- **Modern Native UI**: Intuitive GUI with Dark/Light mode support, smooth animations, and high-performance rendering powered by **Skia**.
- **System Tray Integration**: Full support for system tray minimizing (~10MB RAM usage), double-click to toggle, and a functional right-click menu.
- **Intelligent Startup**: Configure the dashboard to start with Windows, minimize to tray (silent mode with `/silent`), and auto-shutdown distributions on exit.
- **Comprehensive Instance Control**: One-click Start, Stop, Terminate, and Unregister. Real-time status monitoring and detailed insights into disk usage and file locations.
- **Distro Management**: Set as default, migration (Move VHDX to other drives), and export/clone to `.tar` or `.tar.gz` archives.
- **Quick Integration**: Instant launch into Terminal, VS Code, or File Explorer with customizable working directories and startup script hooks.
- **Smart Installation**: Install from Microsoft Store, GitHub, or local files (RootFS/VHDX). Includes a built-in RootFS download helper.
- **Global Safety**: Mutex locks for safe concurrent migration/backup operations and automatic Appx cleanup on removal.
- **Ultra-Low Memory Footprint**: Highly optimized for efficiency. Silent startup (system tray) uses only **~10MB** RAM. Windowed mode usage varies by font complexity: **~18MB** for standard languages (English, German, Spanish, etc.) and **~38MB** for large font languages (Chinese, Japanese, Korean, etc.).
- **Advanced Networking**: Seamless port forwarding management (with automatic firewall rule creation) and global HTTP proxy configuration for unified connectivity.
- **USB Device Management**: Full integration with `usbipd-win` for effortless binding, attaching, and managing of local USB devices across your WSL instances directly from the dashboard UI.

## ⚙️ Configuration & Logs

All configuration is managed through the Settings view:

- Choose the default installation directory for new WSL instances.
- Configure the log directory and log level (Error / Warn / Info / Debug / Trace).
- Pick the UI language or let it follow the system language.
- Toggle dark mode and whether the app can auto-shutdown WSL after operations.
- Configure how often the app checks for updates (daily, weekly, biweekly, monthly).
- Enable automatic startup on system boot (with automatic path repair).
- Set the app to minimize to the system tray on startup for a distraction-free experience.
- Configure the close button to minimize to the system tray instead of exiting.
- Customize the sidebar by toggling the visibility of specific feature tabs.

Log files are written to the configured log directory and can be attached when reporting issues.

## 🖼️ Screenshots

### Home (Light & Dark Mode)

[![](https://github.com/owu/wsl-dashboard/raw/main/assets/screenshot/home.png)](https://github.com/owu/wsl-dashboard/blob/main/assets/screenshot/home.png) [![](https://github.com/owu/wsl-dashboard/raw/main/assets/screenshot/home-dark.png)](https://github.com/owu/wsl-dashboard/blob/main/assets/screenshot/home-dark.png)

[![](https://github.com/owu/wsl-dashboard/raw/main/assets/screenshot/home-settings.png)](https://github.com/owu/wsl-dashboard/blob/main/assets/screenshot/home-settings.png) [![](https://github.com/owu/wsl-dashboard/raw/main/assets/screenshot/home-configs.png)](https://github.com/owu/wsl-dashboard/blob/main/assets/screenshot/home-configs.png)

[![](https://github.com/owu/wsl-dashboard/raw/main/assets/screenshot/usb.png)](https://github.com/owu/wsl-dashboard/blob/main/assets/screenshot/usb.png) [![](https://github.com/owu/wsl-dashboard/raw/main/assets/screenshot/collapsed.png)](https://github.com/owu/wsl-dashboard/blob/main/assets/screenshot/collapsed.png)

### Network

[![](https://github.com/owu/wsl-dashboard/raw/main/assets/screenshot/port-forwarding.png)](https://github.com/owu/wsl-dashboard/blob/main/assets/screenshot/port-forwarding.png) [![](https://github.com/owu/wsl-dashboard/raw/main/assets/screenshot/http-proxy.png)](https://github.com/owu/wsl-dashboard/blob/main/assets/screenshot/http-proxy.png)

### Add Instance & Settings

[![](https://github.com/owu/wsl-dashboard/raw/main/assets/screenshot/add.png)](https://github.com/owu/wsl-dashboard/blob/main/assets/screenshot/add.png) [![](https://github.com/owu/wsl-dashboard/raw/main/assets/screenshot/settings.png)](https://github.com/owu/wsl-dashboard/blob/main/assets/screenshot/settings.png)

### About

[![](https://github.com/owu/wsl-dashboard/raw/main/assets/screenshot/about.png)](https://github.com/owu/wsl-dashboard/blob/main/assets/screenshot/about.png)

## 🎬 Operation Demo

Below is a demonstration of the WSL Dashboard in action:

![WSL Dashboard Demo](https://github.com/owu/wsl-dashboard/raw/main/assets/screenshot/demo.gif)

WSL Dashboard Demo

## 💻 System Requirements

- Windows 10 or Windows 11 with WSL enabled (WSL 2 recommended).
- At least one WSL distribution installed, or permission to install new ones.
- 64-bit CPU; 4 GB RAM or more recommended for smooth multi-distro usage.

## 📦 Installation

### Option 1: Download prebuilt binary

The easiest way to get started is to use the precompiled release:

1. Go to the [GitHub Releases](https://github.com/owu/wsl-dashboard/releases) page.
2. Download the latest `wsldashboard` executable for Windows.
3. Extract (if packaged) and run `wsldashboard.exe`.

No installer is required; the app is a single portable binary.

### Option 2: Build from source

Ensure you have the Rust toolchain (Rust 1.92+ or newer) installed.

1. Clone the repository:
	```
	git clone https://github.com/owu/wsl-dashboard.git
	cd wsl-dashboard
	```
2. Build and run:
	- For development:
		```
		cargo run
		```
		- Optimized release build, using the build script:
		> The build script requires the `x86_64-pc-windows-msvc` toolchain.
		```
		.\build\portable\build.ps1
		```

## 🛠️ Tech Stack & Performance

- **Core**: Implemented in Rust for memory safety and zero-cost abstractions.
- **UI Framework**: Slint with high-performance **Skia** rendering backend.
- **Async Runtime**: Tokio for non-blocking system commands and I/O.
- **Performance Highlights**:
	- **Responsiveness**: Near-instant startup and real-time WSL status monitoring.
		- **Efficiency**: Ultra-low resource usage (see [Key Features](WSLdashboard.md#-key-features--usage) for details).
		- **Portability**: Optimized release build produces a single compact executable.

## ⭐️ Labor of love

If you have found this project useful, I would be grateful if you could leave a star on GitHub. Your endorsement helps it reach a wider audience and is deeply appreciated. It is this encouragement that motivates me to keep building.

## 📄 License

This project is licensed under the GPL-3.0 – see the [LICENSE](https://github.com/owu/wsl-dashboard/blob/main/LICENSE) file for details.

---

Built with ❤️ for the WSL Community.

---

## 🤝 Community Support

A big thank you to the following communities for their support:

- [Rust Programming Language](https://www.rust-lang.org/) - For the powerful and safe programming language
- [Slint | Declarative GUI for Rust, C++, JavaScript & Python](https://slint.dev/) - For the modern UI framework
- [WSL: Windows Subsystem for Linux](https://github.com/microsoft/WSL) - For the amazing Windows Subsystem for Linux
- [Tokio - An asynchronous Rust runtime](https://tokio.rs/) - For the efficient async runtime
- [Windows Developer Community](https://developer.microsoft.com/en-us/windows/community) - For continuous platform improvements
- [Reddit](https://www.reddit.com/) - For global community discussions and support
- [Hacker News](https://news.ycombinator.com/) - For global community discussions and support
- [Linux.do](https://linux.do/) - For popular community for IT professionals
- [V2EX](https://www.v2ex.com/) - For Chinese tech community discussions

Your contributions and feedback make this project possible!
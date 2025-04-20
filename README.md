# SafePM
**A truly private, offline-first, auditable password manager. No cloud. No noise. Just trust.**

SafePM is a minimalist, offline-first password and secrets manager designed with one core belief:

> When it comes to your most sensitive information, trust must be earned—not assumed.

Unlike traditional solutions, SafePM doesn’t ask you to place blind trust in closed-source systems or remote servers. It was built out of personal frustration with the status quo—where convenience often comes at the cost of control and transparency.

SafePM is built for people who value:

- **🛡️ Transparency:** Fully auditable and verifiable — what you see in the code is what runs.
- **🌐 Offline-first:** No remote servers. No telemetry. No hidden network calls.
- **🔐 Strong encryption:** Uses industry-standard AES-256 symmetric encryption.
- **🎛️ Complete control:** Backups are manual, versioned, and portable—you decide where your data lives.
- **🫥 Minimal footprint:** Runs quietly as a CLI tool with no desktop icons or notifications that hint at its presence.

In future versions, SafePM will support encrypted notes, a simple GUI, and extensible secret types—while staying true to its roots of minimalism, privacy, and user agency.

## ⚙️ Installation

To install SafePM, run this command in your terminal:

```shell
bash <(curl -s https://raw.githubusercontent.com/ankurkesharwani/safe-pm/main/get-and-install.sh) "$HOME"
```

## 🚀 Usage

> Work in progress

## 🧭 Philosophy Behind SafePM

SafePM was born out of a simple but strong conviction: you should not have to blindly trust software to protect your most sensitive data. Existing password managers, while convenient, require users to make several trust assumptions—many of which cannot be verified. SafePM challenges that status quo with a fundamentally different approach, rooted in transparency, control, and privacy.

Here’s what sets SafePM apart:

- **Fully Source-Available and Audit-Friendly**
    
    Passwords are too sensitive to leave in the hands of black-box software. SafePM is written in Python, ensuring the exact source code that runs on your machine is human-readable and inspectable. No surprises, no binaries doing who-knows-what, just honest code you can trust.

- **Offline-First by Design**
    
    Unlike other password managers that rely on remote servers to store or sync your data, SafePM works entirely offline. This eliminates any concern over data transmission, server-side encryption, or backend vulnerabilities. You control your data completely.

- **Encryption You Understand**
    
    SafePM uses strong symmetric-key encryption (AES-256). Because the code is open and simple to follow, you know exactly how your passwords are secured. There’s no ambiguity about what kind of cryptography is being used, or whether it’s even being used at all.

- **User-Driven Backups**
    
    SafePM gives you full control over backups. Instead of automatic syncing to a third-party server, you decide when and where to create encrypted, versioned backup files—whether that’s on your personal NAS, cloud storage, or USB drive. No assumptions, just flexibility.

- **Minimal and Unobtrusive**
    
    SafePM is built as a command-line tool that quietly sits on your system, away from prying eyes and desktop clutter. There are no notifications, system tray icons, or unnecessary integrations. Just a simple, powerful tool that stays out of your way—unless you call upon it.

SafePM is not just a password manager. It’s a philosophy-driven tool for those who care deeply about digital sovereignty, privacy, and transparency. This project is for people who’d rather trust code than marketing claims.

## 📅 Roadmap

SafePM is just getting started. Here’s what’s coming next:

**✅ v1.1 – CLI release (now!)**
- Password storage, retrieval, and backup
- AES-256 encryption
- Manual backups

**🛠️ v1.1 – Notes & Secrets**
- Encrypted notes support (e.g., API keys, tokens)

**🖼️ v2.0 – GUI Client**
- Cross-platform lightweight GUI (using PyQt or similar)

## 🤝 Contributing

Contributions are welcome! 
- Found a bug? Open an issue.
- Have an idea? Start a discussion.

## 📜 License

This project is licensed under the MIT License.
You are free to use, modify, and distribute this tool — responsibly.
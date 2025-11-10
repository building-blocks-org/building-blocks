# Presentation Layer Guidelines 🎨

This directory is reserved for **generic, reusable presentation building blocks** only.

---

## ✨ Guidelines

- **Purpose:**
  This layer is for abstractions or patterns that help build presentation adapters (APIs, CLI, UI) and are reusable across many projects.

- **What belongs here?**
  Only reusable patterns or base classes, such as a generic controller interface or serialization utility.

- **What does NOT belong here?**
  - Project-specific endpoints, routes, CLI commands, or templates
  - Concrete adapters for a specific UI or API (e.g., FastAPI, Flask, Typer)

  Place those in your application's presentation layer or in the `/examples` directory.

- **Examples:**
  - A generic controller ABC for web APIs
  - A DTO validation or serialization utility

---

## 📦 Where do concrete presentation adapters go?

Framework- or library-specific presentation code (FastAPI routes, CLI commands, etc.) should **not** be included here.
Instead, place them in your application's presentation layer or in the `/examples` directory of this repository.

---

## 🏗️ Why This Matters

- **Clarity & Cleanliness:**
  Keeps your toolbox focused on reusable, generic presentation logic.
- **Separation:**
  Project-specific code and framework adapters stay with your app or in examples.

---

**If this folder is empty, that’s intentional.**
Add code here only if it is *genuinely reusable* across many projects.

For real-world adapters and usage with frameworks or libraries, see the `/examples` directory.

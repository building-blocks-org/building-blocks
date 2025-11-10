# Infrastructure Layer Guidelines 🏗️

This directory is reserved for **generic, reusable infrastructure building blocks** only.

---

## ✨ Guidelines

- **Purpose:**
  This layer is for abstractions or patterns that help build infrastructure adapters.


- **What belongs here?**
  Only abstractions or base classes that can be used in multiple projects, such as a generic repository base, message bus interface, or encryption contract.

- **What does NOT belong here?**
  - Project-specific adapters (e.g., your app's Postgres repository, Redis cache, RabbitMQ handler)
  - Concrete implementations that depend on frameworks or libraries

  Place those in your application code or in the `/examples` directory.

- **Examples:**
  - A generic repository base class for any storage backend
  - An abstract message publisher interface

---

## 📦 Where do concrete infrastructure adapters go?

Framework- or library-specific adapters (anything dependent on SQLAlchemy, Redis, etc.) should **not** be included here.
Instead, place them in your application's infrastructure layer or in the `/examples` directory of this repository.

---

## 🏗️ Why This Matters

- **Clarity & Cleanliness:**
  Keeps your toolbox focused and reusable.
- **Separation:**
  Framework- and project-specific code lives with your app, keeping the toolbox easy to maintain.

---

**If this folder is empty, that’s intentional.**
Add code here only if it is *genuinely reusable* across many projects.

For real-world adapters and usage with frameworks or libraries, see the `/examples` directory.

# NexusChat (formerly ChatMate-PyQt)

![Python Version](https://img.shields.io/badge/Python-3.12%2B-blue?logo=python&logoColor=white)
![Framework](https://img.shields.io/badge/Framework-PyQt6-green?logo=qt&logoColor=white)
![Architecture](https://img.shields.io/badge/Architecture-Rule--Based-orange)

NexusChat is a premium, lightweight desktop messaging application engineered with Python 3.12+ and PyQt6. Designed as an academic prototype, this project successfully demonstrates that a **strictly rule-based engine**—utilizing standard control flow, dictionary mapping, and string processing—can emulate a modern conversational interface without relying on Machine Learning, LLMs, or NLP toolkits like spaCy/NLTK.

---

## Key Features

* **Strictly Rule-Based Intelligence**: Matches user intent via intelligent string normalization (handling punctuation, whitespaces, and case-insensitivity) against highly optimized dictionary mappings and variation tables.
* **Premium Graphical Interface**: Crafted to rival modern chat clients (Discord, Telegram). Features custom `MessageBubble` widgets, scalable chat scrolling, and fluid animations.
* **Dynamic Theming Engine**: True Dark Mode (black-shaded `#000000`/`#111111`) and a clean Light Mode. Swapping themes dynamically recolors SVG assets and QSS styles in real-time without restarting.
* **Zero-Database Persistence**: Uses a completely localized storage layer, securely writing chat histories, user settings, and application statistics to `.json` files on the disk.
* **Advanced UX Tooling**: 
  * **Typing Indicators**: Simulates real-time processing delays.
  * **Inline Search**: Live text highlighting via `Ctrl+F`.
  * **Import/Export**: Hot-reload capabilities to inject JSON chat logs directly into the running instance.
  * **Toasts**: Non-intrusive, timed pop-up notifications.

---

## Project Architecture & Folder Structure

The application follows a strictly decoupled Model-View-Controller (MVC) architectural pattern, keeping logic, persistence, and presentation separated.

```text
chatbot/
├── main.py                   # Application Entry Point: Bootstraps the app & handles Splash Screens
├── requirements.txt          # Dependencies (PyQt6)
├── gen_svgs.py               # Utility script: Auto-generates fully scalable SVG icons dynamically
│
├── assets/                   
│   └── icons/                # Generated runtime folder housing Light & Dark mode icon sets
│
├── services/                 # Business Logic Layer
│   ├── chat_engine.py        # Resolves queries, normalizes strings, outputs fallback responses
│   └── logger.py             # Global logging configuration outputting to runtime logs/
│
├── storage/                  # Persistence Layer
│   ├── chat_history.py       # Serializes and Deserializes message payloads to history.json
│   ├── settings.py           # Handles UI preferences (Themes, auto-scroll bounds) to settings.json
│   └── statistics.py         # Tracks session analytics (unknown queries, bot responses)
│
├── styles/                   # Presentation Styling Layer
│   ├── dark.qss              # Qt StyleSheet detailing the black-shaded Dark Mode
│   ├── light.qss             # Qt StyleSheet for Light Mode
│   └── theme_manager.py      # Runtime memory-injector applying styles universally
│
├── ui/                       # View & Controller Layer
│   ├── main_window.py        # Central Hub: Instantiates top-header, icons, and coordinates pages
│   ├── chat_page.py          # Primary feed handling user scrolling and message injection
│   ├── about_dialog.py       # System metadata display window
│   ├── settings_dialog.py    # Preferences interface containing import/export logic
│   └── splash_screen.py      # Timed frameless startup loading window
│
└── widgets/                  # Reusable Component Layer
    ├── message_bubble.py     # Responsive, auto-wrapping text frames with avatar positioning
    ├── quick_reply.py        # Clickable chip buttons injected into the chat feed
    ├── toast.py              # Frameless notification engine overlaying the main app
    └── typing_indicator.py   # Animated ellipsis ('...') frame
```

---

## How It Works (Deep Dive)

### 1. The Rule-Based Engine (`chat_engine.py`)
Unlike standard LLMs that encode vectors and calculate cosine similarity, the NexusChat engine relies on **Deterministic Normalization**. 
- **Pre-processing**: When a user inputs "  Hey!! how are you doing?   ", the engine mathematically strips leading/trailing spaces, squashes duplicate spaces, removes all standard punctuation, and forces lowercase. Result: `"hey how are you doing"`.
- **Mapping**: It checks a `variations` dictionary mapping synonyms (`hi`, `hey`) to base intents (`hello`).
- **Response**: If an intent hits, it returns a hardcoded list of responses. If none match, it gracefully fails to a generic prompt.

### 2. Qt's Signal & Slot System
To prevent hard-coupling components (e.g., `SettingsDialog` knowing exactly how `MainWindow` works), the app relies on event broadcasting (`pyqtSignal`). When a user types a message in the input box, it fires a signal that `ChatPage` listens to, ensuring UI rendering threads are never blocked by logic threads.

### 3. File System Layer
Data integrity is handled entirely by Singleton instances within `storage/`. 
If a user flips the "Show Timestamps" toggle, `settings_manager.set()` updates an in-memory dictionary and immediately writes `settings.json` via file I/O operations. `ChatPage` dynamically checks this dictionary during render time, updating the UI safely and locally.

---

## Getting Started

### Prerequisites
- Python 3.12 or newer installed.

### Installation
1. Navigate to the project directory:
   ```bash
   cd chatbot
   ```
2. Setup a virtual environment (Recommended):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Generate the UI assets:
   *(This ensures high-definition SVG icons are tailored correctly to your system)*
   ```bash
   python gen_svgs.py
   ```
5. Launch the application:
   ```bash
   python main.py
   ```

# 🚀 JARVIS AI - QUICK START GUIDE

## ONE-CLICK EXECUTION (Windows)

### First Time Setup

1. **Download/Clone the repository**
   ```bash
   git clone https://github.com/Tommyd01we/jarvis-ai-assistant.git
   cd jarvis-ai-assistant
   ```

2. **Run the build script**
   - Double-click: `run_jarvis.bat`
   - This will:
     - ✅ Check Python installation
     - ✅ Install all dependencies
     - ✅ Build Jarvis.exe
     - ✅ Launch Jarvis AI

### Subsequent Runs

**Option A: Quick Launch (After built)**
- Double-click: `run_jarvis_exe_only.bat`
- Jarvis launches immediately (no rebuild)

**Option B: Direct Execution**
- Navigate to `dist/` folder
- Double-click `Jarvis.exe`

**Option C: Command Line**
```bash
cd dist
Jarvis.exe
```

## 📋 Requirements

- Windows 7, 8, 10, or 11
- Python 3.8+ (for first build only)
- ~500MB disk space
- Internet (first time only, for pip install)

## 🎯 How to Use Jarvis

```
Welcome! I'm Jarvis, your AI assistant.
I learn from every interaction and continuously improve.

You: Hello Jarvis
Jarvis: Hello! I'm Jarvis, your AI assistant. How can I help you today?

You: What is machine learning?
Jarvis: I understand you're asking about machine learning. Let me help with that.

You: That was helpful!
Jarvis: Thank you for your feedback! I've learned from this interaction and will improve.

You: stats
=== Performance Metrics ===
{
  "timestamp": "2026-09-13T09:50:00",
  "total_interactions": 3,
  "knowledge_base_size": 5,
  ...
}

You: exit
```

## 🎮 Commands

- Any text → Jarvis processes and responds
- `stats` → Show performance metrics
- `learn` → Display learned patterns
- `history` → Show last 10 interactions
- `status` → System status
- `export` → Save knowledge base
- `clear` → Clear conversation
- `help` → Show all commands
- `exit` → Quit program

## 📁 File Structure After Build

```
jarvis-ai-assistant/
├── dist/
│   └── Jarvis.exe          ← Your standalone executable!
├── data/
│   ├── knowledge_base.json
│   ├── user_history.json
│   └── performance_metrics.json
├── logs/
│   └── jarvis.log
├── run_jarvis.bat          ← Click to build & run
├── run_jarvis_exe_only.bat ← Click to run (after built)
└── ...
```

## ⚡ Troubleshooting

### "Python not found"
- Install Python from https://www.python.org/
- Make sure to check "Add Python to PATH" during installation

### "Jarvis.exe not found"
- Run `run_jarvis.bat` to build it first
- Wait for build to complete (takes 1-2 minutes)

### "Permission denied"
- Right-click `run_jarvis.bat`
- Select "Run as administrator"

### Slow first startup
- Normal! First launch unpacks files (~3-5 seconds)
- Subsequent launches are instant

## 🔒 Privacy & Security

✅ All processing is local  
✅ No internet connection required (after build)  
✅ No data sent to servers  
✅ Self-contained executable  
✅ No installation needed  

## 🎉 You're All Set!

Double-click `run_jarvis.bat` to start your AI assistant!

---

For more details, see:
- `README.md` - Full project documentation
- `BUILD.md` - Advanced build options

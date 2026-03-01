# OpenClaw Process Monitor Dashboard

A comprehensive real-time dashboard for tracking and managing all your OpenClaw subagents, background processes, and system health.

## 🚀 Features

### 📊 **Real-Time Monitoring**
- **Active Subagents**: Track running AI agents with runtime, model, and task info
- **Background Processes**: Monitor shell processes and coding agents  
- **Scheduled Jobs**: View cron job status and next run times
- **Active Sessions**: See all OpenClaw sessions across channels

### 🎛️ **Agent Control**
- **Start/Stop** subagents and processes
- **Send messages** to active subagents (steering)
- **View logs** in real-time
- **Kill processes** when needed

### 🌐 **Multiple Interfaces**
- **Web Dashboard**: Full-featured browser interface with controls
- **Terminal Dashboard**: Lightweight command-line monitoring
- **JSON API**: Programmatic access to all data
- **Auto-refresh**: Keep data current automatically

## 🏃‍♂️ Quick Start

### **Option 1: Easy Launcher**
```bash
# Make executable and run
chmod +x dashboard/start-monitor.sh
./dashboard/start-monitor.sh
```

### **Option 2: Direct Commands**

**Web Dashboard (Recommended):**
```bash
cd dashboard
python3 web-server.py --port 8080
# Open http://localhost:8080 in browser
```

**Terminal Dashboard:**
```bash
python3 dashboard/monitor.py
```

**One-time Status:**
```bash
python3 dashboard/monitor.py --once
```

**JSON Export:**
```bash
python3 dashboard/monitor.py --mode json --export status.json
```

## 📋 Dashboard Sections

### 🤖 **Active Subagents**
Shows all running AI subagents with:
- Agent name and runtime
- Current model being used
- Token usage and limits
- Task description
- Controls: View Logs, Send Message, Stop

### ⚙️ **Background Processes** 
Monitors long-running background tasks:
- Process name and session key
- Runtime and status
- Working directory
- Controls: View Logs, Kill Process

### ⏰ **Scheduled Jobs (Cron)**
Tracks automated OpenClaw cron jobs:
- Job name and schedule expression
- Next run time
- Enabled/disabled status
- No controls (managed via `openclaw cron` commands)

### 📊 **Active Sessions**
All OpenClaw sessions across channels:
- Channel type (webchat, Discord, etc.)
- Session age and token usage
- Model being used
- Read-only monitoring

## 🎯 **Use Cases**

### **Multi-Agent Orchestration**
Perfect for managing multiple AI agents working in parallel:
```bash
# You can see all agents at once:
- Gaming Research Agent (running 2h 15m)
- CinchIT Build Agent (running 7h 30m) 
- Data Processing Agent (running 45m)
```

### **Development Workflow**
Monitor coding agents and background builds:
```bash
# Track multiple coding projects:
- Claude: Building React frontend
- Pi: Processing CSV data
- Codex: Code review automation
```

### **System Health**
Keep tabs on OpenClaw ecosystem health:
- Session token usage before limits
- Cron job execution status  
- Background process resource usage
- Agent completion notifications

## 🔧 **API Endpoints**

The web server exposes these REST endpoints:

**Data Retrieval:**
- `GET /api/data` - All monitoring data
- `GET /api/subagents` - Active subagents only
- `GET /api/processes` - Background processes only
- `GET /api/cron` - Scheduled jobs only
- `GET /api/sessions` - Active sessions only

**Agent Control:**
- `POST /api/control/subagents/kill` - Stop a subagent
- `POST /api/control/subagents/steer` - Send message to subagent
- `POST /api/control/subagents/logs` - Get subagent logs
- `POST /api/control/processes/kill` - Kill a background process
- `POST /api/control/processes/logs` - Get process logs

**Example API Usage:**
```bash
# Get all data
curl http://localhost:8080/api/data

# Kill a subagent
curl -X POST http://localhost:8080/api/control/subagents/kill \
  -H "Content-Type: application/json" \
  -d '{"id": "agent-id-here"}'

# Send message to subagent
curl -X POST http://localhost:8080/api/control/subagents/steer \
  -H "Content-Type: application/json" \
  -d '{"id": "agent-id-here", "message": "Update your approach"}'
```

## 🚀 **Testing the Dashboard**

To test with your current setup:

1. **Start the web dashboard:**
   ```bash
   cd dashboard
   python3 web-server.py --port 8080
   ```

2. **Open browser to:** http://localhost:8080

3. **You should see:**
   - Your **Gaming Research Agent** (currently running)
   - Any **background processes** (like Claude building CinchIT)
   - All **cron jobs** (weekly audit, daily job hunt, etc.)
   - **Active sessions** (webchat, Discord, etc.)

## 🛠️ **Troubleshooting**

**"Command not found" errors:**
- Make sure OpenClaw is installed: `which openclaw`
- Make sure Python 3 is available: `python3 --version`

**"Connection failed" in web dashboard:**
- Check that the web server is running on correct port
- Try refreshing the page
- Check browser console for errors

**No subagents showing:**
- Run `subagents list` to verify subagents are running
- Check that sessions are active: `openclaw sessions list`

**Permission errors:**
- Make sure scripts are executable: `chmod +x dashboard/*.sh dashboard/*.py`

## 📈 **What's Next**

This dashboard gives you complete visibility and control over your OpenClaw multi-agent ecosystem. Use it to:

- **Monitor long-running builds** (like your CinchIT project)
- **Coordinate multiple AI agents** working in parallel
- **Track system health** and resource usage
- **Debug issues** with logs and process management
- **Scale up** your AI agent workflows confidently

Perfect for power users running complex multi-agent orchestration! 🚀
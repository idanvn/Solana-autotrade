# 🤝 Contributing to SOL Trading Bot

תודה על העניין לתרום לפרויקט! 🎉

## 🚀 איך להתחיל

### 1. Fork + Clone
```bash
# Fork the repo on GitHub, then:
git clone https://github.com/YOUR_USERNAME/Solana_autotrade.git
cd Solana_autotrade
```

### 2. Setup
```powershell
# Create virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Setup .env
Copy-Item .env.example .env
# Edit .env with your test credentials
```

### 3. Create Branch
```bash
git checkout -b feature/your-feature-name
```

---

## 📝 Guidelines

### Code Style
- **Python:** Follow PEP 8
- **Comments:** Hebrew or English (both OK)
- **Docstrings:** English preferred
- **Type hints:** Use where possible

### Commit Messages
```
✅ Good:
- "Add Telegram notifications"
- "Fix price feed cache bug"
- "Improve Docker health check"

❌ Bad:
- "update"
- "fix bug"
- "changes"
```

### Testing
```powershell
# Run the bot in simulation mode
python .\scripts\run_live_bot.py

# Check Docker
.\docker_check.ps1
.\docker_start.ps1
```

---

## 🎯 Areas for Contribution

### High Priority
- [ ] Real trade execution (with safety checks)
- [ ] Multiple trading pairs support
- [ ] Telegram/Discord notifications
- [ ] Web dashboard
- [ ] Backtesting framework

### Medium Priority
- [ ] Better error handling
- [ ] Prometheus metrics
- [ ] More DEX integrations (Raydium, etc.)
- [ ] Advanced trading strategies
- [ ] Unit tests

### Nice to Have
- [ ] Mobile app
- [ ] GUI for configuration
- [ ] Multi-wallet support
- [ ] Tax reporting

---

## 🔒 Security

### Before Submitting:
- [ ] No private keys in code
- [ ] No API keys committed
- [ ] `.env` not included
- [ ] Sensitive data removed from logs

### Security Issues
If you find a security vulnerability:
1. **DO NOT** open a public issue
2. Email: [your-email-here]
3. Include: description, impact, reproduction steps

---

## 📦 Pull Request Process

### 1. Before PR:
```powershell
# Update from main
git checkout main
git pull upstream main
git checkout your-feature-branch
git rebase main

# Test
python .\scripts\run_live_bot.py
```

### 2. PR Checklist:
- [ ] Code works in simulation mode
- [ ] Docker builds successfully
- [ ] Documentation updated
- [ ] No sensitive data
- [ ] Descriptive PR title
- [ ] Clear description of changes

### 3. PR Template:
```markdown
## Changes
- Feature 1
- Fix 2

## Testing
- Tested with Python 3.10
- Docker build OK
- Ran for 24 hours

## Screenshots (if UI changes)
[add screenshots]

## Related Issues
Closes #123
```

---

## 📚 Documentation

Update docs when you:
- Add new features → Update README.md
- Change setup → Update SETUP.md
- Modify Docker → Update DOCKER_README.md
- Fix bugs → Update relevant .md files

---

## 🎨 Code Structure

```
backend/core/
  ├── wallet_manager.py      # Wallet operations
  ├── dynamic_price_feed.py  # Live price fetching
  ├── orca_client.py         # DEX integration
  └── price_monitor.py       # Signal detection

scripts/
  └── run_live_bot.py        # Main bot

docs/
  └── *.md                   # All documentation
```

---

## ❓ Questions?

- Open a Discussion on GitHub
- Check existing Issues
- Read the docs first

---

## 🌟 Recognition

Contributors will be:
- Added to README.md
- Mentioned in release notes
- Appreciated forever! 💙

---

**Thank you for making this project better! 🚀**

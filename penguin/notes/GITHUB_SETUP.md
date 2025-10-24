# GitHub Setup Guide for PENGUIN

## Step 1: Configure Git (One-Time Setup)

Set your git username and email (this will be visible in commit history):

```bash
git config --global user.name "rfrankeb"
git config --global user.email "your-email@example.com"
```

Replace `your-email@example.com` with your actual email address.

## Step 2: Create GitHub Repository

### Option A: Via GitHub Website (Easiest)

1. Go to https://github.com/new
2. Fill in:
   - **Repository name**: `penguin` (or `PENGUIN-stock-tracker`)
   - **Description**: `AI-powered stock analysis platform that aggregates data from thousands of sources`
   - **Visibility**: Choose **Private** (recommended) or Public
   - ⚠️ **DO NOT** check "Initialize this repository with a README" (we already have files)
3. Click **"Create repository"**

### Option B: Via GitHub CLI (gh)

```bash
# Install GitHub CLI if you don't have it
brew install gh

# Login
gh auth login

# Create repo
gh repo create penguin --private --source=. --remote=origin
```

## Step 3: Connect Local Repo to GitHub

After creating the repo on GitHub, you'll see instructions. Use these commands:

```bash
# Add remote origin (replace USERNAME with your GitHub username)
git remote add origin https://github.com/rfrankeb/penguin.git

# Or if you prefer SSH (requires SSH key setup):
git remote add origin git@github.com:rfrankeb/penguin.git
```

## Step 4: Make Your First Commit

```bash
# Add all files (respects .gitignore)
git add .

# Commit with a message
git commit -m "Initial commit: PENGUIN stock tracker PoC with WSB scraper"

# Push to GitHub
git push -u origin main
```

## Step 5: Verify

1. Go to https://github.com/rfrankeb/penguin
2. You should see all your files!

**Important**: The `.env` file with your API keys will NOT be uploaded (protected by `.gitignore`)

---

## Quick Reference: Common Git Commands

```bash
# Check status
git status

# Add specific files
git add filename.py

# Add all changes
git add .

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push

# Pull latest changes
git pull

# View commit history
git log --oneline

# Create a new branch
git checkout -b feature-name

# Switch branches
git checkout main
```

---

## GitHub Authentication Options

### Option 1: HTTPS (Easier, uses personal access token)
1. Go to https://github.com/settings/tokens
2. Generate a new token (classic)
3. Give it `repo` permissions
4. Use the token as your password when pushing

### Option 2: SSH (More secure, no password needed)
1. Generate SSH key:
   ```bash
   ssh-keygen -t ed25519 -C "your-email@example.com"
   ```
2. Add to GitHub:
   - Copy public key: `cat ~/.ssh/id_ed25519.pub`
   - Go to https://github.com/settings/keys
   - Click "New SSH key"
   - Paste your public key

---

## Repository Best Practices

### Branching Strategy
- `main` - Production-ready code
- `develop` - Active development
- `feature/feature-name` - New features
- `fix/bug-name` - Bug fixes

### Commit Message Convention
```
feat: Add Reddit WSB scraper
fix: Fix ticker extraction regex
docs: Update README with setup instructions
refactor: Improve sentiment analysis
test: Add unit tests for scraper
```

### Before Each Commit
1. Check what's changed: `git status`
2. Review changes: `git diff`
3. Make sure `.env` is NOT staged
4. Write a clear commit message

---

## Protecting Secrets

✅ **Already Protected**:
- `.env` (API keys)
- `venv/` (virtual environment)
- `__pycache__/` (Python cache)

⚠️ **Never Commit**:
- API keys
- Passwords
- Private tokens
- Database credentials

If you accidentally commit a secret:
```bash
# Remove from git history (be careful!)
git rm --cached .env
git commit -m "Remove .env from tracking"

# Rotate the exposed credentials immediately!
```

---

## Collaboration Setup (Future)

When you want to collaborate:

1. **Add collaborators**: Settings → Collaborators
2. **Use Pull Requests**: For code review
3. **Create Issues**: Track bugs and features
4. **Use Projects**: Kanban board for tasks

---

## GitHub Actions (CI/CD) - Future Enhancement

Create `.github/workflows/tests.yml` for automated testing:

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.11
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
```

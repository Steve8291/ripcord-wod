# Ripcord WOD

A workout display system for CrossFit Ripcord that automatically fetches and displays the daily Workout of the Day (WOD) from the CrossFit Ripcord leaderboard.

**Live Site:** https://steve8291.github.io/ripcord-wod/

## Project Overview

This project consists of:
- `index.html` - A responsive web page that displays the daily WOD
- `whiteboard.py` - A Python script that fetches WOD data and updates the HTML

The page automatically refreshes every 5 minutes to show the latest workout information.

## How to Fork This Repository

If you want to create your own copy of this repository to customize or contribute, follow these steps:

### Using GitHub Web Interface

1. **Navigate to the repository** on GitHub: https://github.com/Steve8291/ripcord-wod

2. **Click the "Fork" button** in the top-right corner of the page
   - It's located next to the "Star" and "Watch" buttons

3. **Select your account** where you want to fork the repository
   - Choose your personal account or an organization you have access to

4. **Wait for the fork to complete**
   - GitHub will create a copy of the repository under your account
   - The URL will be: `https://github.com/YOUR_USERNAME/ripcord-wod`

5. **Clone your fork** to your local machine:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ripcord-wod.git
   cd ripcord-wod
   ```

6. **Set up the upstream remote** (optional, but recommended for keeping your fork updated):
   ```bash
   git remote add upstream https://github.com/Steve8291/ripcord-wod.git
   git remote -v
   ```

### Using GitHub CLI (gh)

If you have [GitHub CLI](https://cli.github.com/) installed:

```bash
# Fork the repository
gh repo fork Steve8291/ripcord-wod --clone

# This will fork the repo and clone it to your local machine
cd ripcord-wod
```

## Keeping Your Fork Updated

To sync your fork with the original repository:

```bash
# Fetch the latest changes from the upstream repository
git fetch upstream

# Switch to your main branch
git checkout main

# Merge the upstream changes
git merge upstream/main

# Push the updates to your fork
git push origin main
```

## Local Development

To work with this project locally:

1. **Clone the repository** (your fork or the original)
2. **Open `index.html`** in a web browser to view the WOD display
3. **Modify the files** as needed:
   - Edit `index.html` for display changes
   - Edit `whiteboard.py` for data fetching logic

## Python Script Setup

The `whiteboard.py` script requires:
- Python 3
- The `requests` library: `pip install requests`

**Note:** The script is configured for a specific server setup with paths:
- `/usr/local/github/ripcord-wod/` - Repository location
- `/var/cache/ripcord-wod/` - Cache directory

You'll need to adjust these paths if running locally.

## Contributing

1. Fork the repository (see instructions above)
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Commit your changes: `git commit -m "Description of changes"`
5. Push to your fork: `git push origin feature/your-feature-name`
6. Create a Pull Request from your fork to the original repository

## Features

- **Responsive Design**: Adapts to different screen sizes
- **Auto-scaling**: Automatically scales content to fit the viewport
- **Auto-refresh**: Refreshes every 5 minutes to show updated workouts
- **Dark Theme**: Easy-to-read dark background with white text
- **Multi-section Layout**: Displays warm-up, strength, WOD, and mobility sections

## License

This project is available for personal and educational use.

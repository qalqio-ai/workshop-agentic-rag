#!/usr/bin/env bash
# Initialize a fresh local repository and connect it to an EMPTY Git remote.
# Usage: ./init-git-repo.sh <remote-url> [local-directory]

set -euo pipefail

usage() {
  cat <<'USAGE'
Usage:
  ./init-git-repo.sh <remote-url> [local-directory]

Example:
  ./init-git-repo.sh git@github.com:OWNER/REPOSITORY.git workshop-agentic-rag

The remote must be empty. If it already has a README, license, or commit,
clone it first and copy the starter files into the cloned directory.
USAGE
}

if [[ $# -lt 1 || -z "$1" ]]; then
  usage
  exit 2
fi

REMOTE_URL="$1"
if [[ $# -ge 2 && -n "$2" ]]; then
  LOCAL_DIR="$2"
else
  REMOTE_NAME=$(basename "$REMOTE_URL" .git)
  LOCAL_DIR="$REMOTE_NAME"
fi

run_as_admin() {
  if [[ "$EUID" -eq 0 ]]; then
    "$@"
  elif command -v sudo >/dev/null 2>&1; then
    sudo "$@"
  else
    echo "This installer needs administrator access, but sudo was not found." >&2
    echo "Install Git using your operating system's package manager, then rerun." >&2
    return 1
  fi
}

install_git() {
  local os
  os=$(uname -s)

  case "$os" in
    Darwin)
      if command -v brew >/dev/null 2>&1; then
        brew install git
      elif command -v xcode-select >/dev/null 2>&1; then
        echo "Opening the Apple Command Line Tools installer..."
        xcode-select --install || true
        echo "Finish that installation, reopen Terminal, and rerun this script."
        return 1
      else
        echo "Install Git for macOS, then rerun this script." >&2
        echo "Options: install Homebrew and run 'brew install git', or install Apple's Command Line Tools." >&2
        return 1
      fi
      ;;
    Linux)
      if command -v apt-get >/dev/null 2>&1; then
        run_as_admin apt-get update
        run_as_admin apt-get install -y git
      elif command -v dnf >/dev/null 2>&1; then
        run_as_admin dnf install -y git
      elif command -v yum >/dev/null 2>&1; then
        run_as_admin yum install -y git
      elif command -v pacman >/dev/null 2>&1; then
        run_as_admin pacman -S --needed --noconfirm git
      elif command -v zypper >/dev/null 2>&1; then
        run_as_admin zypper install -y git
      elif command -v apk >/dev/null 2>&1; then
        run_as_admin apk add git
      else
        echo "No supported package manager was found. Install Git for your Linux distribution, then rerun." >&2
        return 1
      fi
      ;;
    MINGW*|MSYS*|CYGWIN*)
      echo "This looks like Windows. Git Bash normally includes Git." >&2
      echo "If Git is missing, install Git for Windows, reopen Git Bash, and rerun." >&2
      return 1
      ;;
    *)
      echo "Unsupported operating system: $os" >&2
      echo "Install Git for your operating system, then rerun." >&2
      return 1
      ;;
  esac

  if ! command -v git >/dev/null 2>&1; then
    echo "Git was installed, but this Terminal session cannot find it yet." >&2
    echo "Reopen Terminal and rerun the script." >&2
    return 1
  fi
}

if ! command -v git >/dev/null 2>&1; then
  echo "Git is not installed. Attempting installation..."
  install_git
fi

echo "Using $(git --version)"

# Verify access and make sure this is an empty remote before creating local history.
if ! REMOTE_REFS=$(GIT_TERMINAL_PROMPT=0 git ls-remote "$REMOTE_URL" 2>&1); then
  echo "Could not read the remote repository." >&2
  echo "$REMOTE_REFS" >&2
  echo "Check the remote URL and configure SSH or GitHub authentication, then rerun." >&2
  exit 1
fi

if [[ -n "$REMOTE_REFS" ]]; then
  echo "The remote already contains Git refs (branches or tags)." >&2
  echo "Do not run git init against it; clone it first to avoid unrelated histories:" >&2
  echo "  git clone <remote-url> <local-directory>" >&2
  echo "Then copy the starter files into that cloned directory and commit them." >&2
  exit 1
fi

if [[ ! -d "$LOCAL_DIR" ]]; then
  mkdir -p "$LOCAL_DIR"
fi

if git -C "$LOCAL_DIR" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "Using existing local Git repository at: $LOCAL_DIR"
else
  echo "Initializing local repository at: $LOCAL_DIR"
  git -C "$LOCAL_DIR" -c init.defaultBranch=main init
fi

if git -C "$LOCAL_DIR" rev-parse --verify HEAD >/dev/null 2>&1; then
  echo "The local directory already has commit history." >&2
  echo "This bootstrap is for a fresh repository. Use git clone or connect this repository manually." >&2
  exit 1
fi

git -C "$LOCAL_DIR" branch -M main

if [[ ! -f "$LOCAL_DIR/.gitignore" ]]; then
  cat > "$LOCAL_DIR/.gitignore" <<'GITIGNORE'
# Local secrets and environment files
.env
.env.*
!.env.example

# Common local build and editor files
.DS_Store
.venv/
venv/
__pycache__/
*.py[cod]
node_modules/
dist/
build/
GITIGNORE
fi

if [[ ! -f "$LOCAL_DIR/README.md" ]]; then
  cat > "$LOCAL_DIR/README.md" <<'README'
# Workshop Agentic RAG

Starter repository for the AI-native repository and Agentic RAG workshop.
README
fi

ORIGIN_URL=$(git -C "$LOCAL_DIR" remote get-url origin 2>/dev/null || true)
if [[ -z "$ORIGIN_URL" ]]; then
  git -C "$LOCAL_DIR" remote add origin "$REMOTE_URL"
elif [[ "$ORIGIN_URL" != "$REMOTE_URL" ]]; then
  echo "The local repository already has a different origin:" >&2
  echo "  $ORIGIN_URL" >&2
  echo "This script will not replace it automatically." >&2
  exit 1
fi

# Set a repository-local author only when Git has no configured identity.
if [[ -z "$(git -C "$LOCAL_DIR" config user.name || true)" ]]; then
  read -r -p "Name to use for commits in this repository: " GIT_AUTHOR_NAME
  if [[ -z "$GIT_AUTHOR_NAME" ]]; then
    echo "A commit name is required." >&2
    exit 1
  fi
  git -C "$LOCAL_DIR" config user.name "$GIT_AUTHOR_NAME"
fi

if [[ -z "$(git -C "$LOCAL_DIR" config user.email || true)" ]]; then
  read -r -p "Email to use for commits in this repository: " GIT_AUTHOR_EMAIL
  if [[ -z "$GIT_AUTHOR_EMAIL" ]]; then
    echo "A commit email is required." >&2
    exit 1
  fi
  git -C "$LOCAL_DIR" config user.email "$GIT_AUTHOR_EMAIL"
fi

git -C "$LOCAL_DIR" add -A

if ! git -C "$LOCAL_DIR" rev-parse --verify HEAD >/dev/null 2>&1; then
  git -C "$LOCAL_DIR" commit -m "chore: initialize repository"
elif ! git -C "$LOCAL_DIR" diff --cached --quiet; then
  git -C "$LOCAL_DIR" commit -m "chore: add starter files"
fi

git -C "$LOCAL_DIR" push -u origin main

echo
echo "Repository is initialized and connected."
echo "Local path: $LOCAL_DIR"
echo "Remote:     $REMOTE_URL"
echo "Branch:     main"

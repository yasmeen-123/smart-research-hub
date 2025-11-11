#!/bin/bash

# Git Status Verification Script
# This script checks if your changes are committed and pushed to GitHub

echo "=================================="
echo "   Git Status Verification"
echo "=================================="
echo ""

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ ERROR: Not in a git repository"
    exit 1
fi

echo "📍 Repository Location:"
pwd
echo ""

echo "🌿 Current Branch:"
git branch --show-current
echo ""

echo "📊 Git Status:"
git status --short
if [ -z "$(git status --short)" ]; then
    echo "✅ Working tree is clean (no uncommitted changes)"
else
    echo "⚠️  You have uncommitted changes"
fi
echo ""

echo "📝 Recent Commits:"
git log --oneline -5
echo ""

echo "🔄 Sync Status with GitHub:"
BRANCH=$(git branch --show-current)
UPSTREAM="origin/$BRANCH"

# Check if upstream exists
if git rev-parse "$UPSTREAM" >/dev/null 2>&1; then
    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git rev-parse "$UPSTREAM")
    
    if [ "$LOCAL" = "$REMOTE" ]; then
        echo "✅ Your branch is up to date with GitHub"
    else
        AHEAD=$(git rev-list --count "$UPSTREAM"..HEAD)
        BEHIND=$(git rev-list --count HEAD.."$UPSTREAM")
        
        if [ "$AHEAD" -gt 0 ]; then
            echo "⬆️  You have $AHEAD commit(s) that need to be pushed"
        fi
        
        if [ "$BEHIND" -gt 0 ]; then
            echo "⬇️  You are $BEHIND commit(s) behind GitHub"
        fi
    fi
else
    echo "⚠️  No upstream branch found (branch not pushed yet)"
fi
echo ""

echo "📁 Files in Latest Commit:"
git diff-tree --no-commit-id --name-only -r HEAD | head -10
TOTAL=$(git diff-tree --no-commit-id --name-only -r HEAD | wc -l)
echo "   ... and $TOTAL file(s) total"
echo ""

echo "🌐 GitHub Repository:"
git remote get-url origin 2>/dev/null || echo "No remote configured"
echo ""

echo "=================================="
echo "         SUMMARY"
echo "=================================="

# Summary checks
HAS_CHANGES=$(git status --short | wc -l)
IS_PUSHED=0

if git rev-parse "$UPSTREAM" >/dev/null 2>&1; then
    LOCAL=$(git rev-parse HEAD)
    REMOTE=$(git rev-parse "$UPSTREAM")
    if [ "$LOCAL" = "$REMOTE" ]; then
        IS_PUSHED=1
    fi
fi

if [ "$HAS_CHANGES" -eq 0 ]; then
    echo "✅ All changes are committed"
else
    echo "❌ You have uncommitted changes"
fi

if [ "$IS_PUSHED" -eq 1 ]; then
    echo "✅ All commits are pushed to GitHub"
else
    echo "❌ You have unpushed commits or no upstream"
fi

echo ""
echo "To view your changes on GitHub, visit:"
REPO_URL=$(git remote get-url origin 2>/dev/null)
if [ ! -z "$REPO_URL" ]; then
    # Convert SSH to HTTPS if needed
    REPO_URL=$(echo "$REPO_URL" | sed 's/git@github.com:/https:\/\/github.com\//' | sed 's/\.git$//')
    echo "$REPO_URL/tree/$BRANCH"
fi

echo ""
echo "=================================="

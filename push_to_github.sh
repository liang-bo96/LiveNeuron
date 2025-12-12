#!/bin/bash
# Script to push eelbrain-plotly-viz package to GitHub
# Repository: https://github.com/liang-bo96/eelbrain-plotly-viz

echo "🚀 PUSHING EELBRAIN-PLOTLY-VIZ TO GITHUB"
echo "Repository: https://github.com/liang-bo96/eelbrain-plotly-viz"
echo "=" * 60

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: pyproject.toml not found. Please run this script from the package root directory."
    exit 1
fi

# Initialize git repository if not already done
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Add remote origin if not already added
if ! git remote get-url origin >/dev/null 2>&1; then
    echo "🔗 Adding GitHub remote..."
    git remote add origin https://github.com/liang-bo96/eelbrain-plotly-viz.git
    echo "✅ Remote origin added"
else
    echo "✅ Remote origin already configured"
    echo "   Current remote: $(git remote get-url origin)"
fi

# Stage all files
echo "📦 Staging files..."
git add .

# Show what will be committed
echo ""
echo "📋 Files to be committed:"
git status --porcelain

# Commit changes
echo ""
read -p "💭 Enter commit message (or press Enter for default): " commit_msg
if [ -z "$commit_msg" ]; then
    commit_msg="Initial package release with 453x performance improvement

- Interactive 2D brain visualization using Plotly and Dash
- Optimized batch arrow rendering (453x faster than individual annotations)
- Support for multiple data formats (NDVar, numpy arrays, dictionaries)
- Clean coordinate-free visualization
- Comprehensive test suite and documentation
- Ready for pip installation from GitHub"
fi

echo "💾 Committing changes..."
git commit -m "$commit_msg"

if [ $? -eq 0 ]; then
    echo "✅ Changes committed successfully"
else
    echo "❌ Commit failed. Please check for errors."
    exit 1
fi

# Push to GitHub
echo ""
echo "🌐 Pushing to GitHub..."
echo "Note: You may be prompted for your GitHub credentials"

# Check if main branch exists, if not use master
current_branch=$(git branch --show-current)
if [ -z "$current_branch" ]; then
    echo "🔄 Creating and switching to main branch..."
    git checkout -b main
    current_branch="main"
fi

echo "📤 Pushing to origin/$current_branch..."
git push -u origin $current_branch

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 SUCCESS! Package pushed to GitHub!"
    echo "=" * 60
    echo "✅ Repository: https://github.com/liang-bo96/eelbrain-plotly-viz"
    echo "✅ Installation: pip install git+https://github.com/liang-bo96/eelbrain-plotly-viz.git"
    echo ""
    echo "📋 Next steps:"
    echo "1. Visit: https://github.com/liang-bo96/eelbrain-plotly-viz"
    echo "2. Add a description and topics to your repository"
    echo "3. Test installation: pip install git+https://github.com/liang-bo96/eelbrain-plotly-viz.git"
    echo "4. Share with others!"
    echo ""
    echo "🧪 Test the installation:"
    echo "   pip install git+https://github.com/liang-bo96/eelbrain-plotly-viz.git"
    echo "   python -c \"from eelbrain_plotly_viz import EelbrainPlotly2DViz; print('✅ Package works!')\""
else
    echo ""
    echo "❌ Push failed. Common solutions:"
    echo "1. Check your GitHub credentials"
    echo "2. Make sure you have write access to the repository"
    echo "3. Try: git push origin $current_branch --force (use with caution)"
    exit 1
fi 

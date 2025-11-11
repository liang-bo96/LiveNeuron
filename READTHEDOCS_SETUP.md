# Read the Docs 设置指南

本文档介绍如何在 Read the Docs 上为 LiveNeuron 项目设置在线文档。

## 前提条件

1. ✅ GitHub 账户（你已经有了：https://github.com/liang-bo96/LiveNeuron）
2. ✅ 项目已经推送到 GitHub
3. ⚠️ 需要创建 Read the Docs 账户

## 步骤 1: 准备文件（已完成 ✅）

以下文件已经创建好：

```
LiveNeuronRelease/
├── .readthedocs.yaml          # Read the Docs 配置文件
└── docs/
    ├── conf.py                # Sphinx 配置
    ├── requirements.txt       # 文档构建依赖
    ├── Makefile               # 构建脚本
    ├── index.rst              # 主页
    ├── installation.rst       # 安装指南
    ├── quickstart.rst         # 快速开始
    ├── user_guide.rst         # 用户指南
    ├── api_reference.rst      # API 参考
    ├── examples.rst           # 示例代码
    ├── changelog.rst          # 更新日志
    └── README.rst             # 文档说明
```

## 步骤 2: 推送到 GitHub

将新创建的文档文件推送到 GitHub：

```bash
cd /Users/laoliang/Company/pycharm/mcmaster/LiveNeuronRelease

# 添加所有文档文件
git add .readthedocs.yaml
git add docs/

# 提交
git commit -m "Add Read the Docs documentation"

# 推送到 GitHub
git push origin OPT/displayMode
```

如果你想推送到主分支，可以：

```bash
# 切换到主分支（如果有的话，比如 main 或 master）
git checkout main
git merge OPT/displayMode
git push origin main
```

## 步骤 3: 在 Read the Docs 上注册和导入项目

### 3.1 注册账户

1. 访问 https://readthedocs.org/
2. 点击右上角的 **"Sign Up"**（注册）
3. 选择 **"Sign up with GitHub"**（使用 GitHub 注册）
4. 授权 Read the Docs 访问你的 GitHub 账户

### 3.2 导入项目

1. 登录后，点击右上角的你的用户名，选择 **"My Projects"**
2. 点击 **"Import a Project"**（导入项目）
3. 你会看到你的 GitHub 仓库列表
4. 找到 **"LiveNeuron"** 项目，点击旁边的 **"+"** 按钮
5. 填写项目信息：
   - **Name**: LiveNeuron
   - **Repository URL**: https://github.com/liang-bo96/LiveNeuron
   - **Default branch**: main（或 OPT/displayMode，取决于你想使用哪个分支）
   - **Language**: Python
6. 点击 **"Next"**（下一步）

### 3.3 配置项目（自动完成）

Read the Docs 会自动检测到 `.readthedocs.yaml` 文件并使用它的配置：
- Python 版本: 3.11
- 文档格式: Sphinx
- 构建输出: HTML, PDF, EPUB

## 步骤 4: 构建文档

1. Read the Docs 会自动开始构建文档
2. 在项目页面可以看到构建状态
3. 构建完成后（通常需要 2-5 分钟），点击 **"View Docs"**（查看文档）
4. 你的文档将在以下地址可访问：
   - **https://liveneuron.readthedocs.io/**

## 步骤 5: 配置 Webhook（自动完成）

Read the Docs 会自动在你的 GitHub 仓库上创建 webhook。
这意味着每次你推送代码到 GitHub，文档都会自动重新构建！

## 步骤 6: 配置高级选项（可选）

在 Read the Docs 项目设置中，你可以：

### 6.1 启用版本控制
1. 进入项目的 **"Admin"** → **"Versions"**
2. 选择要构建文档的分支和标签
3. 激活想要的版本

### 6.2 自定义域名（可选）
1. 进入 **"Admin"** → **"Domains"**
2. 添加自定义域名（如 docs.liveneuron.com）
3. 按照说明配置 DNS 记录

### 6.3 配置通知
1. 进入 **"Admin"** → **"Notifications"**
2. 添加邮箱接收构建失败通知

## 步骤 7: 更新项目 README

在你的 GitHub 仓库 README.md 中添加文档徽章：

```markdown
[![Documentation Status](https://readthedocs.org/projects/liveneuron/badge/?version=latest)](https://liveneuron.readthedocs.io/en/latest/?badge=latest)
```

## 步骤 8: 本地测试文档构建

在推送到 GitHub 之前，可以先在本地测试：

```bash
cd /Users/laoliang/Company/pycharm/mcmaster/LiveNeuronRelease

# 安装文档依赖
pip install -r docs/requirements.txt

# 构建 HTML 文档
cd docs
make html

# 查看文档
open _build/html/index.html
```

## 常见问题

### Q: 构建失败怎么办？

A: 
1. 检查 Read the Docs 的构建日志（Build Log）
2. 确认 `docs/requirements.txt` 中的依赖都正确
3. 确认 `.readthedocs.yaml` 配置正确
4. 在本地运行 `make html` 测试是否有错误

### Q: 如何更新文档？

A:
1. 修改 `docs/` 目录下的 `.rst` 文件
2. 提交并推送到 GitHub
3. Read the Docs 会自动重新构建

### Q: 如何查看不同版本的文档？

A:
1. 在文档页面左下角有版本选择器
2. 可以选择不同的分支或标签
3. 在 Read the Docs 项目设置中激活相应版本

### Q: 可以使用 Markdown 而不是 reStructuredText 吗？

A: 可以！已经配置了 `myst-parser`，支持 Markdown：
- 创建 `.md` 文件代替 `.rst` 文件
- 在 `index.rst` 的 `toctree` 中引用时不需要扩展名

## 文档链接

构建完成后，你的文档将在以下位置：

- **主文档**: https://liveneuron.readthedocs.io/
- **PDF 版本**: https://liveneuron.readthedocs.io/_/downloads/en/latest/pdf/
- **EPUB 版本**: https://liveneuron.readthedocs.io/_/downloads/en/latest/epub/

## 文档结构

你的文档包含以下章节：

1. **Installation** - 安装指南
2. **Quick Start** - 快速开始，5 分钟上手
3. **User Guide** - 详细的用户指南
4. **API Reference** - 完整的 API 文档
5. **Examples** - 18 个实用示例
6. **Changelog** - 版本历史和更新日志

## 自动化工作流

现在你有了完整的自动化文档流程：

```
1. 修改代码和文档
   ↓
2. 提交到 Git
   ↓
3. 推送到 GitHub
   ↓
4. GitHub Webhook 触发 Read the Docs
   ↓
5. Read the Docs 自动构建
   ↓
6. 文档自动发布到 https://liveneuron.readthedocs.io/
```

## 下一步

✅ **已完成**:
- 创建 Sphinx 文档结构
- 配置 Read the Docs
- 编写详细文档
- 本地测试构建成功

🚀 **待完成**:
1. 推送文档到 GitHub
2. 在 Read the Docs 上注册账户
3. 导入项目
4. 查看在线文档

## 需要帮助？

如果在设置过程中遇到问题：
- Read the Docs 官方文档: https://docs.readthedocs.io/
- Sphinx 文档: https://www.sphinx-doc.org/
- 联系项目维护者

祝你成功！🎉


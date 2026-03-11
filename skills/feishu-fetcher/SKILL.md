---
name: feishu-fetcher
description: 从飞书媒体目录获取文件、图片等到 nanobot workspace。解决 restrictToWorkspace 安全限制导致无法直接访问外部文件的问题。
---

# 飞书文件获取器

从飞书媒体目录获取文件、图片等到 nanobot workspace。

## 背景

由于 nanobot 的 `restrictToWorkspace` 安全限制，所有文件操作（read_file、write_file、list_dir 等）都被限制在 workspace 目录内。飞书接收的文件自动下载到 `~/.nanobot/media/feishu/` 目录，但无法直接访问。

本 skill 通过 Python 脚本作为"桥梁"，将外部文件复制到 workspace，然后使用常规工具处理。

## 快速工作流

```bash
# 1. 列出可用文件
python skills/feishu-fetcher/scripts/feishu_fetcher.py --list

# 2. 获取指定文件
python skills/feishu-fetcher/scripts/feishu_fetcher.py filename.html

# 3. 获取最新的 HTML 文件
python skills/feishu-fetcher/scripts/feishu_fetcher.py --latest
```

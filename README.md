# Feishu Fetcher 📥

从飞书媒体目录获取文件、图片等到 nanobot workspace。

## 背景

由于 nanobot 的 `restrictToWorkspace` 安全限制，所有文件操作（`read_file`、`write_file`、`list_dir` 等）都被限制在 workspace 目录内。飞书接收的文件自动下载到 `~/.nanobot/media/feishu/` 目录，但无法直接访问。

本 skill 通过 Python 脚本作为"桥梁"，将外部文件复制到 workspace，然后使用常规工具处理。

## 功能

- ✅ 列出飞书媒体目录中的所有文件
- ✅ 按文件类型筛选（图片、文档、HTML 等）
- ✅ 获取最新文件
- ✅ 复制指定文件到 workspace
- ✅ 显示文件详细信息（大小、修改时间）

## 安装

### 1. 克隆本仓库到 nanobot skills 目录

```bash
cd ~/.nanobot/workspace/skills
git clone https://github.com/windmonk/feishu-fetcher.git
```

### 2. 确保 Python 3 可用

```bash
python3 --version
```

## 使用方法

### 列出所有文件

```bash
python3 skills/feishu-fetcher/scripts/feishu_fetcher.py --list
```

输出示例：
```
Feishu Media Directory: ~/.nanobot/media/feishu
Found 3 file(s)

    1. img_v3_02vm_02a1.jpg                       148.4 KB  2026-03-11 22:21:12
    2. img_v3_02vm_6ca3.jpg                       127.9 KB  2026-03-11 17:12:11
    3. img_v3_02vm_a7bc.jpg                       127.9 KB  2026-03-11 17:09:50
```

### 按类型筛选

只列出图片文件：
```bash
python3 skills/feishu-fetcher/scripts/feishu_fetcher.py --list --type image
```

支持的文件类型：
- `image`: 图片文件（png, jpg, jpeg, gif, webp, bmp, svg）
- `html`: HTML 文件
- `pdf`: PDF 文件
- `text`: 文本文件（txt, md）
- `doc`: 文档文件（docx, xlsx, pptx）
- `all`: 所有文件

### 获取最新文件

```bash
python3 skills/feishu-fetcher/scripts/feishu_fetcher.py --latest
```

输出示例：
```
[SUCCESS] Copied: img_v3_02vm_02a1.jpg
   Source: ~/.nanobot/media/feishu/img_v3_02vm_02a1.jpg
   Target: ~/.nanobot/workspace/img_v3_02vm_02a1.jpg
   Size:   148.4 KB
```

### 获取指定文件

```bash
python3 skills/feishu-fetcher/scripts/feishu_fetcher.py img_v3_02vm_02a1.jpg
```

### 指定输出目录

```bash
python3 skills/feishu-fetcher/scripts/feishu_fetcher.py img_v3_02vm_02a1.jpg --output ./downloads/
```

### 显示帮助信息

```bash
python3 skills/feishu-fetcher/scripts/feishu_fetcher.py --help
```

## 工作流程

```
飞书消息 → nanobot 接收 → 下载到 ~/.nanobot/media/feishu/
                     ↓
           feishu-fetcher 脚本
                     ↓
          复制到 ~/.nanobot/workspace/
                     ↓
              nanobot 正常处理
```

## 目录结构

```
feishu-fetcher/
├── README.md              # 项目说明（本文件）
├── SKILL.md               # nanobot skill 元数据
├── .gitignore
├── scripts/
│   └── feishu_fetcher.py  # 主脚本
└── references/
    └── USAGE.md           # 详细使用说明
```

## 技术栈

- Python 3
- 标准库：`shutil`, `pathlib`, `sys`, `argparse`, `datetime`

## 依赖

无需额外依赖，仅使用 Python 标准库。

## 在 nanobot 中使用

本 skill 已集成到 nanobot 框架，可通过以下方式调用：

```python
# 示例：列出飞书文件
exec("python3 skills/feishu-fetcher/scripts/feishu_fetcher.py --list")

# 示例：获取最新文件
exec("python3 skills/feishu-fetcher/scripts/feishu_fetcher.py --latest")
```

## 常见问题

### Q: 为什么需要这个 skill？

A: nanobot 的安全限制禁止访问 workspace 之外的文件。飞书接收的文件保存在 `~/.nanobot/media/feishu/`，需要通过此脚本复制到 workspace 后才能正常处理。

### Q: 文件会被移动还是复制？

A: 文件会被**复制**到 workspace，原始文件保留在飞书媒体目录。

### Q: 支持哪些文件类型？

A: 支持图片、文档、HTML、文本等常见文件类型。使用 `--list --type all` 查看所有文件。

### Q: 如何在 nanobot 配置中启用？

A: 本 skill 已通过 `SKILL.md` 自动注册，无需额外配置。

## 许可证

MIT License

## 作者

[windmonk](https://github.com/windmonk)

## 相关链接

- [nanobot](https://github.com/windmonk/nanobot) - nanobot AI 助手框架
- [Feishu Open Platform](https://open.feishu.cn/) - 飞书开放平台

#!/usr/bin/env python3
"""
Feishu File Fetcher
从飞书媒体目录获取文件到 nanobot workspace
"""
import shutil, pathlib, sys, argparse
from datetime import datetime
from typing import List, Optional

# ===== 配置 =====
# 飞书媒体目录（自动下载的文件存储位置）
FEISHU_MEDIA_DIR = pathlib.Path.home() / ".nanobot" / "media" / "feishu"

# 支持的文件类型分组
FILE_TYPES = {
    "html": ["*.html", "*.htm"],
    "image": ["*.png", "*.jpg", "*.jpeg", "*.gif", "*.webp", "*.bmp", "*.svg"],
    "pdf": ["*.pdf"],
    "text": ["*.txt", "*.md"],
    "doc": ["*.doc", "*.docx"],
    "excel": ["*.xls", "*.xlsx", "*.csv"],
}
# =================


def format_size(size_bytes: int) -> str:
    """格式化文件大小显示"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def format_time(timestamp: float) -> str:
    """格式化时间显示"""
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")


def list_files(pattern: str = "*", source_dir: Optional[pathlib.Path] = None) -> List[pathlib.Path]:
    """列出飞书媒体目录中的文件

    Args:
        pattern: 文件匹配模式，如 "*.html", "*.png", "*"
        source_dir: 源目录，默认为 FEISHU_MEDIA_DIR

    Returns:
        文件路径列表，按修改时间倒序排列
    """
    if source_dir is None:
        source_dir = FEISHU_MEDIA_DIR

    if not source_dir.exists():
        print(f"❌ 飞书媒体目录不存在: {source_dir}")
        return []

    files = sorted(
        source_dir.glob(pattern),
        key=lambda p: p.stat().st_mtime,
        reverse=True
    )

    return files


def print_file_list(files: List[pathlib.Path], show_details: bool = True):
    """打印文件列表

    Args:
        files: 文件路径列表
        show_details: 是否显示详细信息（大小、修改时间）
    """
    if not files:
        print("Directory is empty")
        return

    print(f"Feishu Media Directory: {FEISHU_MEDIA_DIR}")
    print(f"Found {len(files)} file(s)")
    print()

    for i, f in enumerate(files, 1):
        if show_details:
            size = format_size(f.stat().st_size)
            mtime = format_time(f.stat().st_mtime)
            print(f"  {i:3}. {f.name:40} {size:>10}  {mtime}")
        else:
            print(f"  {i:3}. {f.name}")


def fetch_file(filename: str, source_dir: Optional[pathlib.Path] = None,
               dest_dir: Optional[pathlib.Path] = None,
               overwrite: bool = True) -> bool:
    """从源目录复制文件到目标目录

    Args:
        filename: 文件名
        source_dir: 源目录，默认为 FEISHU_MEDIA_DIR
        dest_dir: 目标目录，默认为当前目录
        overwrite: 是否覆盖已存在的文件

    Returns:
        成功返回 True，失败返回 False
    """
    if source_dir is None:
        source_dir = FEISHU_MEDIA_DIR

    if dest_dir is None:
        dest_dir = pathlib.Path.cwd()

    src = source_dir / filename
    dst = dest_dir / filename

    # 检查源目录
    if not source_dir.exists():
        print(f"[ERROR] Source directory does not exist: {source_dir}")
        print(f"   Please check the Feishu media directory path")
        return False

    # 检查源文件
    if not src.exists():
        print(f"[ERROR] Source file does not exist: {src}")
        print(f"   Available files:")
        for f in sorted(source_dir.iterdir())[:10]:
            print(f"   - {f.name}")
        return False

    # 检查目标文件
    if dst.exists() and not overwrite:
        print(f"[WARNING] Target file already exists: {dst}")
        print(f"   Use --overwrite to overwrite or choose another filename")
        return False

    # 创建目标目录
    dest_dir.mkdir(parents=True, exist_ok=True)

    # 复制文件
    try:
        shutil.copy2(src, dst)
        print(f"[SUCCESS] Copied: {filename}")
        print(f"   Source: {src}")
        print(f"   Target: {dst.absolute()}")
        print(f"   Size:   {format_size(dst.stat().st_size)}")
        return True
    except Exception as e:
        print(f"[ERROR] Copy failed: {e}")
        return False


def fetch_latest(pattern: str = "*", source_dir: Optional[pathlib.Path] = None,
                 dest_dir: Optional[pathlib.Path] = None) -> bool:
    """获取匹配模式的最新的文件

    Args:
        pattern: 文件匹配模式
        source_dir: 源目录
        dest_dir: 目标目录

    Returns:
        成功返回 True，失败返回 False
    """
    files = list_files(pattern, source_dir)

    if not files:
        print(f"❌ 没有找到匹配 '{pattern}' 的文件")
        return False

    latest_file = files[0]
    return fetch_file(latest_file.name, source_dir, dest_dir)


def parse_pattern(arg: str) -> str:
    """解析文件类型参数为 glob 模式

    Args:
        arg: 文件类型参数，如 "html", "*.html", "image"

    Returns:
        glob 模式字符串
    """
    if arg in FILE_TYPES:
        # 使用预定义的类型组合
        return FILE_TYPES[arg][0]  # 返回该类型的第一个模式
    elif arg.startswith("*"):
        # 已经是 glob 模式
        return arg
    else:
        # 尝试作为 glob 模式
        return f"*{arg}" if not arg.startswith("*") else arg


def main():
    parser = argparse.ArgumentParser(
        description="从飞书媒体目录获取文件到 nanobot workspace",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --list                           # 列出所有文件
  %(prog)s --list --type "*.html"          # 列出 HTML 文件
  %(prog)s --list --type image             # 列出图片文件
  %(prog)s file.html                        # 获取指定文件
  %(prog)s --latest                        # 获取最新的文件
  %(prog)s --latest --type "*.pdf"         # 获取最新的 PDF 文件
  %(prog)s file.png --dest ./images        # 获取文件到指定目录
        """
    )

    parser.add_argument("filename", nargs="?", help="要获取的文件名")
    parser.add_argument("--list", "-l", action="store_true", help="列出飞书媒体目录中的文件")
    parser.add_argument("--latest", action="store_true", help="获取最新的文件")
    parser.add_argument("--type", "-t", dest="pattern", help="文件类型过滤，如 '*.html', 'image', 'pdf'")
    parser.add_argument("--dest", "-d", dest="dest_dir", help="目标目录（默认当前目录）")
    parser.add_argument("--overwrite", "-o", action="store_true", help="覆盖已存在的文件")
    parser.add_argument("--no-details", action="store_true", help="列表时不显示详细信息")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    args = parser.parse_args()

    # 解析文件类型
    pattern = "*"
    if args.pattern:
        pattern = parse_pattern(args.pattern)

    # 解析目标目录
    dest_dir = pathlib.Path(args.dest_dir) if args.dest_dir else pathlib.Path.cwd()

    # 执行命令
    if args.list:
        files = list_files(pattern)
        print_file_list(files, show_details=not args.no_details)
    elif args.latest:
        success = fetch_latest(pattern, dest_dir=dest_dir)
        sys.exit(0 if success else 1)
    elif args.filename:
        success = fetch_file(args.filename, dest_dir=dest_dir, overwrite=args.overwrite)
        sys.exit(0 if success else 1)
    else:
        # 无参数：显示帮助和文件列表
        parser.print_help()
        print()
        files = list_files()
        if files:
            print_file_list(files[:10], show_details=not args.no_details)
            if len(files) > 10:
                print(f"   ... 还有 {len(files) - 10} 个文件")


if __name__ == "__main__":
    main()

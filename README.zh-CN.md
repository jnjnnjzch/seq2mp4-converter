# SEQ2MP4 转换器

[English](README.md) | 简体中文

一个独立工具，用于将 NorPix `.seq` 文件转换为压缩的 MP4 格式，**压缩率可达 30-100 倍（100fps）或 150-450 倍（30fps）**。它会自动检测硬件加速（NVIDIA NVENC / AMD AMF / Apple VideoToolbox）以加快转换速度，如果没有 GPU 则回退到 CPU。

💡 需要时间戳？虽然此工具处理压缩，但您可以使用 [kiana](https://github.com/jnjnnjzch/kiana_aligner) 以闪电般的速度提取 `.seq` 时间戳 ⚡。它可以在 **仅 10 秒内处理 300GB 数据（100 万+时间戳）**——运行在 10GbE 带宽的极限，在本地 NVMe SSD 上甚至更快！

## 下载
前往 **[Releases](../../releases)** 页面下载适用于您平台的可执行文件：
* **Windows**：`seq2mp4-win.exe`
* **Linux**：`seq2mp4-linux`
* **macOS**：`seq2mp4-mac`（Apple Silicon 和 Intel）

---

## 使用指南

这是一个命令行工具。请使用 **终端**（Linux/macOS）或 **PowerShell / CMD**（Windows）来运行它。

### 🪟 Windows

1.  打开包含下载的 `seq2mp4-win.exe` 的文件夹。
2.  右键单击空白处 -> "在终端中打开"（或在地址栏中输入 `cmd`）。
3.  运行命令：

    ```powershell
    # 基本转换（高质量）
    .\seq2mp4-win.exe "C:\path\to\video.seq"

    # 小文件模式（高压缩）
    .\seq2mp4-win.exe "C:\path\to\video.seq" --mode small
    ```

### 🐧 Linux

1.  在下载文件的目录中打开终端。
2.  授予执行权限（仅首次需要）：
    ```bash
    chmod +x seq2mp4-linux
    ```
3.  运行命令：
    ```bash
    # 基本转换
    ./seq2mp4-linux /path/to/video.seq

    # 小文件模式
    ./seq2mp4-linux /path/to/video.seq --mode small
    ```

### 🍎 macOS

**1. 选择正确的版本：**
* **Apple Silicon（M1/M2/M3...）：** 下载 `seq2mp4-mac-arm64`（推荐）
* **Intel Mac：** 下载 `seq2mp4-mac-x64`

> *注意：如果不确定，在终端中输入 `uname -m`。`arm64` 表示 Apple Silicon，`x86_64` 表示 Intel。*

**2. ⚠️ 首次运行注意事项（安全警告）：**
由于此工具未经 Apple 签名，macOS 默认会阻止它。要绕过此限制：
1.  在 **访达** 中找到下载的文件。
2.  **右键单击**（或按住 Control 单击）文件并选择 **打开**。
3.  在对话框中单击 **打开**。
*（您只需执行一次此操作。）*

**3. 运行工具：**
打开终端并运行以下命令（将文件名替换为您下载的文件名）：

1.  授予执行权限：
    ```bash
    # 替换为您下载文件的实际路径
    chmod +x /path/to/seq2mp4-mac-arm64
    ```

2.  运行转换：
    ```bash
    # 基本转换
    /path/to/seq2mp4-mac-arm64 /path/to/video.seq

    # 小文件模式
    /path/to/seq2mp4-mac-arm64 /path/to/video.seq --mode small
    ```

---

## 命令行选项

| 参数 | 描述 | 默认值 |
| :--- | :--- | :--- |
| `input_file` | 要转换的 `.seq` 文件的路径。 | （必需） |
| `--mode` | 转换预设模式。<br>• `normal`：高质量，文件较大。<br>• `small`：高压缩，文件较小。 | `normal` |
| `--cq` | **（高级）** 覆盖恒定质量值（0-51）。值越低质量越好。 | 自动 |
| `--gop` | **（高级）** 覆盖图片组（关键帧间隔）。 | 自动 |
| `--bf` | **（高级）** 覆盖 B 帧数量。 | 自动 |

### 示例

**1. 高压缩转换（节省空间）：**
```bash
seq2mp4-win.exe input.seq --mode small
```
**2. 自定义质量（例如，手动设置 CQ 为 24）：**

```bash
seq2mp4-win.exe input.seq --mode small --cq 24
```

### 硬件加速支持
工具在启动时会自动检测您的硬件：

- NVIDIA：使用 `h264_nvenc`
- AMD：使用 `h264_amf`
- macOS：使用 `h264_videotoolbox`（M1/M2/M3/M4 和 Intel）
- CPU：使用 `libx264`（如果未找到 GPU，则回退）

## 许可证
本项目采用 GPLv3 许可证。

## 致谢与声明
* **NorPix**：`.seq` 文件格式是 NorPix 的专有格式。此工具使用 [pims](https://github.com/soft-matter/pims) 进行互操作，不包含任何 NorPix 专有代码。
* **FFmpeg**：此工具捆绑/使用 FFmpeg。FFmpeg 采用 LGPLv2.1/GPLv2+ 许可证。详情请参阅 [FFmpeg 许可证](https://ffmpeg.org/legal.html)。

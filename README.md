# SEQ2MP4 Converter

A standalone tool to convert NorPix `.seq` files to compressed MP4 using FFmpeg. It automatically detects hardware acceleration (NVIDIA NVENC / AMD AMF) to speed up conversion, falling back to CPU if no GPU is available.

## Download
Go to the **[Releases](../../releases)** page to download the executable for your platform:
* **Windows**: `seq2mp4-win.exe`
* **Linux**: `seq2mp4-linux`

---

## Usage Guide

This is a command-line tool. Please use **Terminal** (Linux) or **PowerShell / CMD** (Windows) to run it.

### 🪟 Windows

1.  Open the folder containing the downloaded `seq2mp4-win.exe`.
2.  Right-click empty space -> "Open in Terminal" (or type `cmd` in the address bar).
3.  Run the command:

    ```powershell
    # Basic conversion (High Quality)
    .\seq2mp4-win.exe "C:\path\to\video.seq"

    # Small size mode (High Compression)
    .\seq2mp4-win.exe "C:\path\to\video.seq" --mode small
    ```

### 🐧 Linux

1.  Open terminal in the directory where you downloaded the file.
2.  Grant execution permission (first time only):
    ```bash
    chmod +x seq2mp4-linux
    ```
3.  Run the command:
    ```bash
    # Basic conversion
    ./seq2mp4-linux /path/to/video.seq

    # Small size mode
    ./seq2mp4-linux /path/to/video.seq --mode small
    ```

---

## Command Line Options (参数详解)

| Argument | Description | Default |
| :--- | :--- | :--- |
| `input_file` | Path to the `.seq` file to convert. | (Required) |
| `--mode` | Conversion preset mode.<br>• `normal`: High quality, larger file size.<br>• `small`: High compression, smaller file size. | `normal` |
| `--cq` | **(Advanced)** Override Constant Quality value (0-51). Lower is better quality. | Auto |
| `--gop` | **(Advanced)** Override Group of Pictures (Keyframe interval). | Auto |
| `--bf` | **(Advanced)** Override B-Frames count. | Auto |

### Examples

**1. Convert with high compression (Save space):**
```bash
seq2mp4-win.exe input.seq --mode small
```
**2. Custom Quality (e.g., set CQ to 24 manually):**

```bash
seq2mp4-win.exe input.seq --mode small --cq 24
```

### Hardware Acceleration Support
The tool automatically detects your hardware on startup:

- NVIDIA: Uses h264_nvenc
- AMD: Uses h264_amf
- CPU: Uses libx264 (Fallback if no GPU found)

## License
This project is licensed under the GPLv3 License.

## Acknowledgments & Credits
* **NorPix**: `.seq` file format is proprietary to NorPix. This tool uses [pims](https://github.com/soft-matter/pims) for interoperability and does not contain any NorPix proprietary code.
* **FFmpeg**: This tool bundles/uses FFmpeg. FFmpeg is licensed under the LGPLv2.1/GPLv2+. Please refer to the [FFmpeg License](https://ffmpeg.org/legal.html) for details.
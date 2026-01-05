# SEQ2MP4 Converter

A standalone tool to convert NorPix `.seq` files to compressed MP4 using FFmpeg **with 30x-100x (100fps) or 150x-450x (30fps) compress rate**. It automatically detects hardware acceleration (NVIDIA NVENC / AMD AMF / Apple VideoToolbox) to speed up conversion, falling back to CPU if no GPU is available.

💡 Need the timestamps? While this tool handles compression, you can use [kiana](https://github.com/jnjnnjzch/kiana_aligner) to extract `.seq` timestamps at lightning speed ⚡. It can process **300GB of data (1M+ timestamps) in just 10s**—running at the limit of 10GbE bandwidth and even faster on local NVMe SSDs!

## Download
Go to the **[Releases](../../releases)** page to download the executable for your platform:
* **Windows**: `seq2mp4-win.exe`
* **Linux**: `seq2mp4-linux`
* **macOS**: `seq2mp4-mac` (Apple Silicon & Intel)

---

## Usage Guide

This is a command-line tool. Please use **Terminal** (Linux/macOS) or **PowerShell / CMD** (Windows) to run it.

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

### 🍎 macOS

**1. Choose the correct version:**
* **Apple Silicon (M1/M2/M3...):** Download `seq2mp4-mac-arm64` (Recommended)
* **Intel Mac:** Download `seq2mp4-mac-x64`

> *Note: If you are unsure, type `uname -m` in Terminal. `arm64` means Apple Silicon, `x86_64` means Intel.*

**2. ⚠️ First Run Notice (Security Warning):**
Since this tool is not signed by Apple, macOS will block it by default. To bypass this:
1.  Locate the downloaded file in **Finder**.
2.  **Right-click** (or Control-click) the file and select **Open**.
3.  Click **Open** in the dialog box.
*(You only need to do this once.)*

**3. Running the tool:**
Open Terminal and run the following commands (replace the filename with the one you downloaded):

1.  Grant execution permission:
    ```bash
    # Replace with the actual path to your downloaded file
    chmod +x /path/to/seq2mp4-mac-arm64
    ```

2.  Run the conversion:
    ```bash
    # Basic conversion
    /path/to/seq2mp4-mac-arm64 /path/to/video.seq

    # Small size mode
    /path/to/seq2mp4-mac-arm64 /path/to/video.seq --mode small
    ```

---

## Command Line Options

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

- NVIDIA: Uses `h264_nvenc`
- AMD: Uses `h264_amf`
- MacOS: Uses `h264_videotoolbox` (M1/M2/M3/M4 & Intel)
- CPU: Uses `libx264` (Fallback if no GPU found)

## License
This project is licensed under the GPLv3 License.

## Acknowledgments & Credits
* **NorPix**: `.seq` file format is proprietary to NorPix. This tool uses [pims](https://github.com/soft-matter/pims) for interoperability and does not contain any NorPix proprietary code.
* **FFmpeg**: This tool bundles/uses FFmpeg. FFmpeg is licensed under the LGPLv2.1/GPLv2+. Please refer to the [FFmpeg License](https://ffmpeg.org/legal.html) for details.

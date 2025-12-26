# scripts/download_ffmpeg.py
import os
import sys
import platform
import urllib.request
import zipfile
import tarfile
import shutil

def download_and_extract():
    system = platform.system().lower()
    base_dir = os.path.abspath("binaries") # 确保是绝对路径
    
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    os.makedirs(base_dir)

    print(f"检测到构建环境: {system}")

    if "windows" in system:
        # 下载 Windows 版 (Gyan.dev)
        url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        zip_path = "ffmpeg.zip"
        print(f"正在下载 Windows FFmpeg: {url} ...")
        urllib.request.urlretrieve(url, zip_path)
        
        print("解压中...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall("temp_ffmpeg")
        
        # 找到 bin/ffmpeg.exe 并移动
        for root, dirs, files in os.walk("temp_ffmpeg"):
            if "ffmpeg.exe" in files:
                shutil.move(os.path.join(root, "ffmpeg.exe"), os.path.join(base_dir, "ffmpeg.exe"))
                break
        print(f"FFmpeg 已就位: {os.path.join(base_dir, 'ffmpeg.exe')}")

    elif "linux" in system:
        # 下载 Linux 版 (John Van Sickle 静态构建)
        url = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
        tar_path = "ffmpeg.tar.xz"
        print(f"正在下载 Linux FFmpeg: {url} ...")
        urllib.request.urlretrieve(url, tar_path)
        
        print("解压中...")
        with tarfile.open(tar_path, "r:xz") as tar:
            tar.extractall("temp_ffmpeg")
            
        # 找到 ffmpeg 并移动
        for root, dirs, files in os.walk("temp_ffmpeg"):
            if "ffmpeg" in files:
                shutil.move(os.path.join(root, "ffmpeg"), os.path.join(base_dir, "ffmpeg"))
                break
        
        # 赋予执行权限
        os.chmod(os.path.join(base_dir, "ffmpeg"), 0o755)
        print(f"FFmpeg 已就位: {os.path.join(base_dir, 'ffmpeg')}")

if __name__ == "__main__":
    download_and_extract()
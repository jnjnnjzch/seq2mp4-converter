import os
import sys
import platform
import urllib.request
import zipfile
import tarfile
import shutil

def download_and_extract():
    system = platform.system().lower()
    base_dir = os.path.abspath("binaries")
    
    # Clean up previous downloads
    if os.path.exists(base_dir):
        shutil.rmtree(base_dir)
    os.makedirs(base_dir)

    print(f"Detected build environment: {system}")

    if "windows" in system:
        # Download Windows FFmpeg (Gyan.dev)
        url = "https://github.com/GyanD/codexffmpeg/releases/download/4.4.1/ffmpeg-4.4.1-essentials_build.zip"        
        zip_path = "ffmpeg.zip"
        print(f"Downloading Windows FFmpeg from: {url} ...")
        
        try:
            # Add User-Agent to avoid 403 Forbidden on some runners
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(zip_path, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
        except Exception as e:
            print(f"Download failed: {e}")
            sys.exit(1)
        
        print("Extracting zip file...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall("temp_ffmpeg")
        
        # Find and move ffmpeg.exe
        found = False
        for root, dirs, files in os.walk("temp_ffmpeg"):
            if "ffmpeg.exe" in files:
                src = os.path.join(root, "ffmpeg.exe")
                dst = os.path.join(base_dir, "ffmpeg.exe")
                print(f"Moving {src} -> {dst}")
                shutil.move(src, dst)
                found = True
                break
        
        if not found:
            print("Error: ffmpeg.exe not found in the downloaded zip!")
            sys.exit(1)

        print(f"FFmpeg setup complete: {os.path.join(base_dir, 'ffmpeg.exe')}")

    elif "linux" in system:
        # Download Linux FFmpeg (BtbN - with NVENC)
        url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-linux64-gpl.tar.xz"
        tar_path = "ffmpeg.tar.xz"
        print(f"Downloading Linux FFmpeg (BtbN - with NVENC): {url} ...")
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(tar_path, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
        except Exception as e:
            print(f"Download failed: {e}")
            sys.exit(1)
        
        print("Extracting tar.xz file...")
        with tarfile.open(tar_path, "r:xz") as tar:
            tar.extractall("temp_ffmpeg")
            
        # Find and move ffmpeg
        found = False
        for root, dirs, files in os.walk("temp_ffmpeg"):
            if "ffmpeg" in files:
                src = os.path.join(root, "ffmpeg")
                dst = os.path.join(base_dir, "ffmpeg")
                print(f"Moving {src} -> {dst}")
                shutil.move(src, dst)
                found = True
                break
        
        if not found:
            print("Error: ffmpeg binary not found in the downloaded tarball!")
            sys.exit(1)
        
        # Make executable
        os.chmod(os.path.join(base_dir, "ffmpeg"), 0o755)
        print(f"FFmpeg setup complete: {os.path.join(base_dir, 'ffmpeg')}")

    elif "darwin" in system:
        # Download Mac FFmpeg (Evermeet)
        url = "https://evermeet.cx/ffmpeg/getrelease/zip"
        zip_path = "ffmpeg_mac.zip"
        print(f"Downloading Mac FFmpeg (Evermeet): {url} ...")

        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response, open(zip_path, 'wb') as out_file:
                shutil.copyfileobj(response, out_file)
        except Exception as e:
            print(f"Download failed: {e}")
            sys.exit(1)
        
        print("Extracting zip file...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall("temp_ffmpeg")
            
        src = os.path.join("temp_ffmpeg", "ffmpeg")
        dst = os.path.join(base_dir, "ffmpeg")
        
        if os.path.exists(src):
            print(f"Moving {src} -> {dst}")
            shutil.move(src, dst)
            os.chmod(dst, 0o755) # 赋予执行权限
            print(f"FFmpeg setup complete: {dst}")
        else:
            print("Error: ffmpeg binary not found in extracted files")
            sys.exit(1)

if __name__ == "__main__":
    download_and_extract()
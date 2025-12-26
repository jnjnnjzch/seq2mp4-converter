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
        url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
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
        # Download Linux FFmpeg (John Van Sickle static build)
        url = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
        tar_path = "ffmpeg.tar.xz"
        print(f"Downloading Linux FFmpeg from: {url} ...")
        
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

if __name__ == "__main__":
    download_and_extract()
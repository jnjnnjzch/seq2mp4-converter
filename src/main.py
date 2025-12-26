import sys
import os
import subprocess
import argparse
import platform
from pims import NorpixSeq

def get_resource_path(relative_path):
    """资源路径定位，兼容 PyInstaller 和开发环境"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def get_ffmpeg_binary():
    """根据操作系统自动选择 ffmpeg 文件名"""
    system_name = platform.system().lower()
    filename = "ffmpeg.exe" if "windows" in system_name else "ffmpeg"
    
    # 优先找打包在内的
    bundled_path = get_resource_path(filename)
    if os.path.exists(bundled_path):
        return bundled_path
    
    # 开发环境/系统环境 fallback
    return filename

def check_encoder_availability(ffmpeg_bin, encoder_name):
    """
    通过生成 1 帧空白视频来测试编码器是否真的可用（驱动是否正常）。
    返回: True (可用) / False (驱动不支持或报错)
    """
    try:
        # 构建一个极小的测试命令：
        # -f lavfi -i color=c=black:s=64x64:d=0.1  -> 生成 0.1秒 64x64 的黑屏
        # -c:v encoder_name                      -> 尝试使用指定的编码器
        # -f null -                              -> 输出扔进黑洞，不写文件
        cmd = [
            ffmpeg_bin, 
            '-hide_banner', '-loglevel', 'error',
            '-f', 'lavfi', '-i', 'color=c=black:s=64x64:d=0.1',
            '-c:v', encoder_name,
            '-f', 'null', '-'
        ]
        
        # 运行测试
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False
    except Exception:
        return False

def detect_encoders(ffmpeg_bin):
    """
    通过运行 ffmpeg -encoders 探测可用硬件编码器。
    返回一个 dict，例如 {'nvidia': True, 'amd': False}
    """
    available = {'nvidia': False, 'amd': False}
    try:
        # 运行 ffmpeg -encoders
        cmd = [ffmpeg_bin, '-hide_banner', '-encoders']
        # Windows下如果不屏蔽 stdin 可能会卡住
        result = subprocess.run(cmd, capture_output=True, text=True, input="")
        output = result.stdout

        if "h264_nvenc" in output:
            available['nvidia'] = True if check_encoder_availability(ffmpeg_bin, 'h264_nvenc') else False
        if "h264_amf" in output:  # AMF 是 AMD 的主要接口
            available['amd'] = True if check_encoder_availability(ffmpeg_bin, 'h264_amf') else False
        # Linux 下 AMD 有时也用 vaapi，这里为了简化逻辑优先 check amf
        # 如果需要更通用的 Linux AMD 支持，可以检测 h264_vaapi
        if "h264_videotoolbox" in output:
            available['mac_vt'] = True if check_encoder_availability(ffmpeg_bin, 'h264_videotoolbox') else False
            
    except Exception as e:
        print(f"警告: 无法探测编码器支持情况 ({e})，将默认使用 CPU。")
    
    return available

def get_encoding_params(hardware_type, mode, user_args):
    """生成编码参数"""
    cmd = []
    
    # --- 预设定义 ---
    # Normal: 默认高质量
    # Small:  高压缩率
    presets = {
        'normal': {'cq': 20, 'gop': -1, 'bf': -1, 'preset': 'quality'}, 
        'small':  {'cq': 28, 'gop': 2000, 'bf': 3,  'preset': 'quality'}
    }
    config = presets.get(mode, presets['normal']).copy()

    # 用户覆盖
    if user_args.cq is not None: config['cq'] = user_args.cq
    if user_args.gop is not None: config['gop'] = user_args.gop
    if user_args.bf is not None: config['bf'] = user_args.bf
    
    print(f"检测到的硬件加速: {hardware_type.upper()}")

    if hardware_type == 'nvidia':
        cmd.extend(['-c:v', 'h264_nvenc'])
        cmd.extend(['-cq', str(config['cq'])])
        # N卡 preset: p1-p7 (p7最慢质量最好)
        n_preset = 'p7' if config['preset'] == 'speed' else 'p4'
        cmd.extend(['-preset', n_preset])
        
    elif hardware_type == 'amd':
        cmd.extend(['-c:v', 'h264_amf'])
        # AMF 的质量控制通常用 -rc cqp -qp_i X -qp_p X
        # 这里简化处理，尝试使用 -qvbr_quality_level 或通用的 -q
        # 注意: AMF 参数随版本变动很大，这里使用较通用的 rc=cqp 模式
        cmd.extend(['-rc', 'cqp']) 
        cmd.extend(['-qp_i', str(config['cq'])])
        cmd.extend(['-qp_p', str(config['cq'])])
        # AMD preset: speed, balanced, quality
        cmd.extend(['-quality', config['preset']])

    elif hardware_type == 'mac_vt':
        cmd.extend(['-c:v', 'h264_videotoolbox'])
        # 映射质量参数: 
        # 用户输入的 cq 是 0-51 (越小越好)
        # VideoToolbox 的 -q:v 是 1-100 (越大越好)
        # 我们做一个简单的转换
        if mode == 'small':
            # 对应高压缩 (cq=28) -> VideoToolbox q=50 左右
            q_val = 50
        else:
            # 对应高质量 (cq=20) -> VideoToolbox q=75 左右
            q_val = 75
        # 如果用户手动指定了 cq，我们尝试映射一下
        if user_args.cq is not None:
            # 简单线性映射: 0(cq) -> 100(q), 51(cq) -> 0(q)
            q_val = int(100 - (user_args.cq * 2))
            q_val = max(1, min(100, q_val)) # 限制在 1-100

        cmd.extend(['-q:v', str(q_val)])

    else:
        # CPU Fallback
        cmd.extend(['-c:v', 'libx264'])
        cmd.extend(['-crf', str(config['cq'])])
        c_preset = 'veryslow' if config['preset'] == 'quality' else 'medium'
        if mode == 'small': c_preset = 'veryfast' # 压缩模式下 CPU 也要快点
        cmd.extend(['-preset', c_preset])

    # 通用参数
    if config['gop'] > 0: cmd.extend(['-g', str(config['gop'])])
    if config['bf'] > 0:  cmd.extend(['-bf', str(config['bf'])])
    
    cmd.extend(['-pix_fmt', 'yuv420p'])
    return cmd

def process_video(input_file, mode, args):
    ffmpeg_bin = get_ffmpeg_binary()
    
    # 1. 探测硬件 (仅在需要时)
    # 逻辑：优先 N 卡，其次 A 卡，最后 CPU
    encoders = detect_encoders(ffmpeg_bin)
    if encoders['nvidia']:
        hardware = 'nvidia'
    elif encoders['amd']:
        hardware = 'amd'
    elif encoders['mac_vt']: # 使用 get 防止旧字典报错
        hardware = 'mac_vt'
    else:
        hardware = 'cpu'

    # 2. 读取 SEQ
    try:
        video = NorpixSeq(input_file)
    except Exception as e:
        print(f"错误: 无法读取文件 {input_file} - {e}")
        return

    # 3. 构建路径
    base_name = os.path.splitext(input_file)[0]
    suffix = "-converted-small.mp4" if mode == 'small' else "-converted.mp4"
    output_file = f"{base_name}{suffix}"

    # 4. 构建 FFmpeg 命令
    width = video.frame_shape[1]
    height = video.frame_shape[0]
    input_fmt = 'gray' if len(video.frame_shape) == 2 else 'rgb24'
    
    base_cmd = [
        ffmpeg_bin, '-y',
        '-f', 'rawvideo', '-vcodec', 'rawvideo',
        '-s', f"{width}x{height}", '-pix_fmt', input_fmt,
        '-r', str(video.frame_rate),
        '-i', '-'
    ]
    
    enc_cmd = get_encoding_params(hardware, mode, args)
    full_cmd = base_cmd + enc_cmd + [output_file]

    print(f"[{mode.upper()}] 开始转码 -> {output_file}")
    
    try:
        proc = subprocess.Popen(full_cmd, stdin=subprocess.PIPE)
        for i, frame in enumerate(video):
            proc.stdin.write(frame.tobytes())
        
        proc.stdin.close()
        proc.wait()
        print("\n完成。")
    except Exception as e:
        print(f"\n转码失败: {e}")
        if proc: proc.kill()

def main():
    parser = argparse.ArgumentParser(description="SEQ to MP4 Converter")
    parser.add_argument("input_file", help="Input .seq file")
    parser.add_argument("--mode", choices=['normal', 'small'], default='normal')
    parser.add_argument("--cq", type=int, help="Override Constant Quality (0-51)")
    parser.add_argument("--gop", type=int, help="Override GOP size")
    parser.add_argument("--bf", type=int, help="Override B-Frames")
    
    args = parser.parse_args()
    
    process_video(args.input_file, args.mode, args)

if __name__ == "__main__":
    main()
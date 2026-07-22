#!/usr/bin/python3
"""CIMG → raw 解码器。CIMG 格式: 64B主头 + N×(64B块头 + 数据块)"""
import sys, os, struct

def cimg_to_raw(in_path, out_path):
    with open(in_path, 'rb') as f:
        magic = f.read(4)
        if magic != b'CIMG':
            # 不是 CIMG，直接当 raw 拷贝
            f.seek(0)
            with open(out_path, 'wb') as o:
                o.write(f.read())
            return
        f.read(8)  # skip version + header_size
        total_chunks = struct.unpack('<I', f.read(4))[0]
        f.seek(64)  # 跳过 64B 主头
        with open(out_path, 'wb') as o:
            for _ in range(total_chunks):
                chunk_header = f.read(64)
                data_size = struct.unpack('<I', chunk_header[4:8])[0]
                o.write(f.read(data_size))
    print(f"  cimg2raw: {os.path.basename(in_path)} ({total_chunks} chunks) -> {out_path}")

if __name__ == '__main__':
    cimg_to_raw(sys.argv[1], sys.argv[2])

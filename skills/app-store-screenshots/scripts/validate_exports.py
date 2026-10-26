#!/usr/bin/env python3
"""Inspect an upload directory using only Python's standard library.

Structural checks only: does not decode pixels or validate ICC profile content.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import sys
import zlib


def inspect_png(path):
    data = path.read_bytes()
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError("not a PNG file")
    offset = 8
    chunks = []
    header = None
    while offset < len(data):
        if len(data) - offset < 12:
            raise ValueError("truncated chunk header")
        length = struct.unpack_from(">I", data, offset)[0]
        kind = data[offset + 4:offset + 8]
        end = offset + 12 + length
        if end > len(data):
            raise ValueError("truncated chunk payload")
        payload = data[offset + 8:offset + 8 + length]
        checksum = struct.unpack_from(">I", data, offset + 8 + length)[0]
        if zlib.crc32(kind + payload) & 0xFFFFFFFF != checksum:
            raise ValueError("CRC mismatch in " + kind.decode("ascii", errors="replace"))
        if not chunks and kind != b"IHDR":
            raise ValueError("IHDR must be the first chunk")
        if kind == b"IHDR":
            if header is not None or length != 13:
                raise ValueError("invalid or repeated IHDR")
            header = struct.unpack(">IIBBBBB", payload)
        chunks.append(kind)
        offset = end
        if kind == b"IEND":
            if length != 0 or offset != len(data):
                raise ValueError("invalid IEND or trailing bytes")
            break
    if not chunks or chunks[-1] != b"IEND" or b"IDAT" not in chunks or header is None:
        raise ValueError("missing image data or IEND")
    width, height, depth, color_type, compression, filter_method, interlace = header
    legal_depths = {0: {1, 2, 4, 8, 16}, 2: {8, 16}, 3: {1, 2, 4, 8}, 4: {8, 16}, 6: {8, 16}}
    if not width or not height or depth not in legal_depths.get(color_type, set()):
        raise ValueError("invalid PNG dimensions or color format")
    if compression != 0 or filter_method != 0 or interlace not in (0, 1):
        raise ValueError("unsupported PNG header values")
    return {
        "file": path.name,
        "width": width,
        "height": height,
        "bit_depth": depth,
        "color_type": color_type,
        "has_alpha_or_transparency": color_type in (4, 6) or b"tRNS" in chunks,
        "srgb_chunk_present": b"sRGB" in chunks,
        "icc_chunk_present": b"iCCP" in chunks,
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path, help="one locale/device PNG directory; non-recursive")
    parser.add_argument("--size", required=True, help="expected pixels, e.g. 1206x2622 (verify current requirements)")
    parser.add_argument("--count", required=True, type=int, help="expected number of PNGs")
    parser.add_argument("--manifest", type=Path, help="optional JSON report, including errors on failure")
    args = parser.parse_args()
    match = re.fullmatch(r"([1-9][0-9]*)x([1-9][0-9]*)", args.size)
    if not match or args.count < 1:
        parser.error("--size must be WIDTHxHEIGHT and --count must be positive")
    if not args.directory.is_dir():
        parser.error("directory does not exist")
    if args.manifest and args.manifest.suffix.lower() != ".json":
        parser.error("manifest must use a .json filename")
    expected = tuple(map(int, match.groups()))
    paths = sorted(p for p in args.directory.iterdir() if p.is_file() and p.suffix.lower() == ".png")
    errors = []
    images = []
    if len(paths) != args.count:
        errors.append(f"Expected {args.count} PNGs, found {len(paths)}")
    for path in paths:
        try:
            info = inspect_png(path)
            images.append(info)
            if (info["width"], info["height"]) != expected:
                errors.append(f"{path.name}: wrong size {info['width']}x{info['height']}")
            if info["has_alpha_or_transparency"]:
                errors.append(f"{path.name}: alpha channel or transparency is present")
        except (OSError, ValueError, struct.error) as exc:
            errors.append(f"{path.name}: {exc}")
    report = {
        "directory": str(args.directory.resolve()),
        "expected_size": list(expected),
        "expected_count": args.count,
        "structural_checks_passed": not errors,
        "limitations": "Does not decode pixels, validate ICC contents, or perform visual/upload verification.",
        "images": images,
        "errors": errors,
    }
    if args.manifest:
        args.manifest.parent.mkdir(parents=True, exist_ok=True)
        args.manifest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Gán nhãn sơ bộ (pre-label) ảnh train bằng model YOLO pretrained trên COCO.

Kết quả chỉ là bản nháp để import vào CVAT rồi sửa tay:
- COCO không có lớp `van` -> xe van sẽ bị gán thành car/truck, phải tự đổi.
- Xe nhỏ ở xa, xe che nhau thường bị sót hoặc box lỏng -> phải kiểm tra từng ảnh.

Đầu ra (đều nằm trong outputs/, đã bị .gitignore):
- outputs/prelabels/<ảnh>.txt              nhãn YOLO thô
- outputs/prelabels_cvat_yolo11.zip        import vào CVAT bằng định dạng "YOLO 1.1"

Cài đặt:  pip install ultralytics
Chạy:     python tools/prelabel_yolo.py
"""

from __future__ import annotations

import argparse
import zipfile
from pathlib import Path

# Thứ tự lớp phải khớp data.yaml: 0 car, 1 truck, 2 bus, 3 van
CLASS_NAMES = ["car", "truck", "bus", "van"]
# COCO id -> id của lab
COCO_TO_LAB = {2: 0, 7: 1, 5: 2}  # car, truck, bus


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--images", default="dataset/images/train")
    parser.add_argument("--out", default="outputs/prelabels")
    parser.add_argument("--zip", default="outputs/prelabels_cvat_yolo11.zip")
    parser.add_argument("--model", default="yolo26x.pt", help="model càng lớn càng chính xác (n/s/m/l/x)")
    parser.add_argument("--conf", type=float, default=0.35, help="ngưỡng tin cậy")
    parser.add_argument("--imgsz", type=int, default=1280, help="ảnh lớn giúp bắt xe nhỏ ở xa")
    args = parser.parse_args()

    from ultralytics import YOLO

    image_dir = Path(args.images)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    images = sorted(p for ext in ("*.jpg", "*.jpeg", "*.png") for p in image_dir.glob(ext))
    if not images:
        raise SystemExit(f"Không tìm thấy ảnh trong {image_dir}")

    model = YOLO(args.model)
    counts = [0] * len(CLASS_NAMES)

    for image in images:
        result = model.predict(
            source=str(image),
            conf=args.conf,
            imgsz=args.imgsz,
            classes=list(COCO_TO_LAB),
            agnostic_nms=True,  # tránh 1 xe vừa có box car vừa có box truck
            verbose=False,
        )[0]
        lines = []
        for cls, box in zip(result.boxes.cls.tolist(), result.boxes.xyxyn.tolist()):
            lab_id = COCO_TO_LAB[int(cls)]
            x1, y1, x2, y2 = (min(max(v, 0.0), 1.0) for v in box)
            w, h = x2 - x1, y2 - y1
            if w <= 0 or h <= 0:
                continue
            lines.append(f"{lab_id} {(x1 + x2) / 2:.6f} {(y1 + y2) / 2:.6f} {w:.6f} {h:.6f}")
            counts[lab_id] += 1
        (out_dir / f"{image.stem}.txt").write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
        print(f"{image.name}: {len(lines)} box")

    # Gói theo định dạng CVAT "YOLO 1.1"
    zip_path = Path(args.zip)
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("obj.names", "\n".join(CLASS_NAMES) + "\n")
        zf.writestr(
            "obj.data",
            f"classes = {len(CLASS_NAMES)}\ntrain = data/train.txt\nnames = data/obj.names\nbackup = backup/\n",
        )
        zf.writestr("train.txt", "".join(f"data/obj_train_data/{img.name}\n" for img in images))
        for image in images:
            zf.write(out_dir / f"{image.stem}.txt", f"obj_train_data/{image.stem}.txt")

    print("\nTổng số box:", ", ".join(f"{n}={c}" for n, c in zip(CLASS_NAMES, counts)))
    print(f"Nhãn thô: {out_dir}")
    print(f"File import CVAT (YOLO 1.1): {zip_path}")


if __name__ == "__main__":
    main()

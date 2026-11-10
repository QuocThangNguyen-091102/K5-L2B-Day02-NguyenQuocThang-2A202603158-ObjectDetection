# Báo cáo cá nhân — Ngày 2 Object Detection

## 1. Thông tin học viên

- Họ tên: Nguyễn Quốc Thắng 
- MSSV: 2A202603158
- Email: quocthang9112@gmail.com
- Lớp: K5-2b
- Link repo bài làm: https://github.com/QuocThangNguyen-091102/K5-L2B-DAY02-NguyenQuocThang-2A202603158-ObjectDetection
- Link Colab đã chạy: https://colab.research.google.com/drive/135zsq_BMrnzm0vmr2gQM_LHHPzEAh_cv?hl=vi#scrollTo=Dwe27ER4SzyM

## 2. Schema và mini guideline

Chi tiết ở [GUIDELINE_MINI.md](../../GUIDELINE_MINI.md). Guideline được hoàn thiện sau khi gán nhãn, ghi lại các quy tắc đã dùng.

Cách áp dụng schema: gán theo loại xe, không theo trạng thái (xe đỗ vẫn gán). Xe bị che hoặc cắt khung vẫn gán nếu nhận ra loại, box chỉ bao phần nhìn thấy. Xe quá nhỏ không xác định được lớp thì bỏ qua.

Các ca mơ hồ đã quyết định:

- `drive_014`: xe đỏ cỡ giữa minivan và minibus → `van`, vì thân hộp và ngắn hơn hẳn xe buýt trong cùng ảnh.
- `drive_014`: xe cứu hộ → `truck`, vì là xe chuyên dụng có cabin riêng, không chở khách.
- `drive_028`: xe đỗ ven đường bị cây che một phần → gán `car` cho từng xe nhận ra được.
- `drive_008`: xe buýt nối toa → một box `bus` cho cả xe.

Cần giảng viên làm rõ:

- Ranh giới van và minibus.
- Gold có vẻ dùng mã lớp khác README: ở `drive_008`, `drive_014` xe buýt được gán lớp 3, xe van lớp 1, xe tải lớp 2.
- Phạm vi gán xe đỗ ven đường: gold `drive_028` chỉ có 3 box.

## 3. Annotation và self-QC

- Số file nhãn train: 50 (không có file rỗng), tổng 1086 box: car 924, truck 30, bus 97, van 35.
- Kết quả checker và lỗi đã xử lý: `check_yolo_labels.py` đạt 50/50. Trên Windows script báo `UnicodeEncodeError` khi in tiếng Việt, chạy lại với `PYTHONIOENCODING=utf-8` thì đạt; nội dung nhãn không có lỗi.
- Danh sách ít nhất 10 ảnh đã rà bằng mắt (vẽ box lên ảnh để xem): `drive_001`, `drive_002`, `drive_008`, `drive_014`, `drive_018`, `drive_021`, `drive_028`, `drive_036`, `drive_044`, `drive_049`.
- Lỗi bỏ sót/box/class phát hiện khi rà và cách sửa:
  - Box nhìn chung sát xe, xe bị che hoặc cắt khung đều có box.
  - `drive_049`: xe MPV trắng ở cuối ảnh bị gán `truck`, đúng ra là `car` hoặc `van`; xe van trắng ở góc trên trái bị gán `car`.
  - `drive_044`: xe xám thân hộp giữa ảnh gán `car`, có thể là `van`.
  - `drive_001`, `drive_018`, `drive_028`: gán nhiều xe đỗ ven đường và xe nhỏ ở xa. Em giữ theo README (xe đỗ vẫn gán) nhưng đây là nguồn chính của box thừa so với gold.
  - Các lỗi trên phát hiện sau khi đã khóa nhãn, em ghi lại và không sửa (không rework, xem mục 4).
- Commit khóa nhãn ban đầu: `fd1870a` (Add YOLO labels for 50 train images).

## 4. Gold QC và rework

| Chỉ số | Trước sửa | Sau sửa nếu có |
|---|---:|---:|
| TP | 480 | không rework |
| FP | 606 | |
| FN | 173 | |
| Precision | 0.442 | |
| Recall | 0.7351 | |
| F1 | 0.552 | |
| mean_iou_of_matches | 0.8507 | |
| passed | false | |

Kết quả đầy đủ ở [outputs/annotation_evaluation.json](../../outputs/annotation_evaluation.json).

Mean IoU đạt (0.85 ≥ 0.70) nên box khá sát. F1 chưa đạt (0.552 < 0.80), chủ yếu do precision thấp: em vẽ 1086 box trong khi gold có 653.

Em không rework nhãn vì đây là buổi đầu thực hành gán nhãn. Thay vào đó em mở lại ảnh để tìm nguyên nhân:

- Lệch lớp: đặt nhãn của em cạnh gold trên `drive_008` và `drive_014` thì thấy gold gán xe buýt là lớp 3 (`van`), xe van là lớp 1 (`truck`), xe tải/xe cứu hộ là lớp 2 (`bus`). Em gán theo bảng schema trong README. Trên cả 50 ảnh, 52/54 box `van` của gold trùng vị trí với box `bus` của em. Nếu quy đổi lớp của em theo cách gán của gold thì F1 là 0.650 và recall là 0.865 (chỉ tính lại để kiểm tra, không sửa file nhãn).
- Box thừa: kể cả sau khi quy đổi vẫn còn khoảng 520 FP. Phần lớn là xe đỗ ven đường và xe nhỏ ở xa mà gold không gán, ví dụ `drive_028` gold có 3 box còn em có 20. Nhãn của em có 22 box nhỏ hơn 0.05% diện tích ảnh, gold chỉ có 1.
- Nhãn ban đầu được tạo bằng pre-label YOLO (COCO) rồi sửa tay trong CVAT. Model pre-label bắt được nhiều xe nhỏ nên em giữ lại nhiều box hơn phạm vi của gold.

## 5. Kết quả YOLO

- Runtime, GPU/CPU, phiên bản Ultralytics và Torch: Google Colab, GPU (`device: 0`), Ultralytics 8.4.208 (đọc từ checkpoint). Phiên bản Torch và tên GPU không có trong các file đã tải về từ Colab nên em không ghi.
- Các tham số thay đổi so với notebook nếu có và lý do: không thay đổi (yolo26n.pt, 50 epoch, imgsz 640, batch -1, seed 20260909)
- Đường dẫn best checkpoint trong phiên chạy: `/content/Day2-Lab/outputs/yolo26_runs/vehicle_annotation/weights/best.pt` (best rơi vào epoch 1)

| Chỉ số trên 10 ảnh eval | Giá trị |
|---|---:|
| Precision | 0.411 |
| Recall | 0.230 |
| mAP50 | 0.272 |
| mAP50–95 | 0.202 |

AP50 theo lớp (từ [BoxPR_curve.png](assets/yolo26_runs/vehicle_eval/BoxPR_curve.png)): car 0.739, truck 0.239, bus 0.008, van 0.103.

Kết quả Colab: [ảnh dự đoán trên eval](assets/eval_predictions/visuals/), [log train results.csv](assets/yolo26_runs/vehicle_annotation/results.csv), [biểu đồ train](assets/yolo26_runs/vehicle_annotation/results.png), [confusion matrix](assets/yolo26_runs/vehicle_eval/confusion_matrix.png).

Ví dụ cụ thể:

- [drive_052](assets/eval_predictions/visuals/drive_052.jpg): xe buýt 2 tầng ở giữa ảnh được dự đoán `bus` 0.51, nhưng nhãn eval gán xe này là `van` nên bị tính sai lớp. Các xe con đỗ bên trái được nhận đúng `car`.
- [drive_056](assets/eval_predictions/visuals/drive_056.jpg): xe SUV tối màu giữa đường bị dự đoán `van` 0.95 và xe đỏ phía dưới bị dự đoán `van` 0.89, trong khi nhãn eval là `car`.

Trả lời bốn câu hỏi cuối notebook:

1. Lớp nào recall thấp nhất? Ảnh nào minh họa?

   `van` và `bus` đều có recall bằng 0 theo [confusion matrix](assets/yolo26_runs/vehicle_eval/confusion_matrix.png). `van` đáng chú ý hơn vì có 12 vật thể trong eval mà không nhận đúng cái nào (11 cái bị dự đoán thành `bus`). Ví dụ [drive_052](assets/eval_predictions/visuals/drive_052.jpg): xe buýt 2 tầng có nhãn `van`, model dự đoán `bus`. `car` có recall cao nhất (84/94).

2. Nếu mAP50 cao nhưng mAP50–95 thấp, cần kiểm điều gì trên box?

   Khi đó box tìm đúng vật thể nhưng chưa sát, nên cần kiểm tra các cạnh box: box lỏng, lấn nền, hoặc lệch vài pixel ở xe nhỏ. Ở bài này mAP50 (0.272) và mAP50–95 (0.202) chênh không nhiều, và mean IoU của nhãn là 0.85, nên vấn đề chính không nằm ở độ sát của box mà ở việc nhận sai lớp.

3. Lỗi class nào có thể liên quan guideline? Dữ kiện nào hỗ trợ nhận xét?

   Lỗi `bus`/`van`. Em gán xe buýt là `bus` theo README, nhưng nhãn eval (và gold train) gán xe buýt là `van`. Dữ kiện: confusion matrix có 11 vật thể `van` bị dự đoán thành `bus`; AP50 của bus chỉ 0.008 và van 0.103; trên tập train, 52/54 box `van` của gold trùng với box `bus` của em. Lỗi này đến từ cách hiểu schema khác nhau giữa nhãn của em và gold, không phải do model.

4. Vì sao không dùng 10 ảnh eval để train? Vai trò validation của chúng trong notebook là gì?

   Nếu train trên eval thì model đã thấy đáp án, chỉ số đo trên eval sẽ cao giả và không cho biết model làm tốt thế nào trên ảnh mới. Trong notebook, eval được dùng làm tập validation: sau mỗi epoch model được đo trên eval và `best.pt` là epoch có điểm cao nhất (ở đây là epoch 1). Vì eval đã được dùng để chọn checkpoint nên nó cũng không phải test set độc lập.

## 6. Khó khăn và cách xử lý

| Bước/thời điểm | Lỗi quan sát | Cách đã thử | Kết quả/còn thiếu |
|---|---|---|---|
| Gán nhãn (CP2) | Model pre-label COCO không có lớp `van`, xe van bị gán thành car/truck | Import pre-label vào CVAT rồi sửa lớp bằng tay | Đã sửa tay, nhưng vẫn giữ nhiều box xe nhỏ ở xa từ pre-label |
| Self-QC (CP3) | `check_yolo_labels.py` báo `UnicodeEncodeError` khi in tiếng Việt trên terminal Windows | Chạy lại với biến môi trường `PYTHONIOENCODING=utf-8` | Checker đạt 50/50, lỗi chỉ nằm ở phần in ra màn hình |
| Gold QC (CP5) | F1 = 0.552, chưa đạt ngưỡng 0.80 | Đặt nhãn của em cạnh gold trên `drive_008`, `drive_014`, `drive_028` | Tìm ra lệch mã lớp bus/van/truck và box thừa ở xe đỗ/xe nhỏ; không rework, cần giảng viên xác nhận mã lớp |
| Train (CP6) | `best.pt` rơi vào epoch 1, mAP dao động mạnh giữa các epoch | Giữ nguyên tham số notebook, xem `results.csv` và confusion matrix | Nguyên nhân có thể do lệch lớp giữa nhãn train và nhãn eval, cộng với dữ liệu chỉ 50 ảnh |

## 7. Tự đánh giá theo rubric

| Tiêu chí | Hiện trạng |
| --- | --- |
| Hoàn thành và định dạng YOLO | Đủ 50 file, checker đạt |
| Đầy đủ vật thể | Recall so với gold là 0.735 (0.865 nếu quy đổi lớp); gán thừa nhiều xe đỗ và xe nhỏ ở xa so với gold |
| Độ bám sát và hình học box | Mean IoU 0.85, đạt |
| Phân lớp nhất quán | Gán theo bảng schema README; lệch với gold ở bus/van/truck, chưa được giảng viên xác nhận bên nào đúng |
| Mini guideline và quyết định mơ hồ | Có định nghĩa lớp, quy tắc box và 4 ca mơ hồ; guideline hoàn thiện sau khi gán nhãn, không phải trước như yêu cầu CP1 |
| Gold-set annotation QC | Có file đánh giá, chưa đạt F1; không rework nhưng có phân tích nguyên nhân |
| Pipeline YOLO và phân tích | Colab chạy xong, không dùng eval để train, có metrics, ảnh eval và nhận xét. Lưu ý: train khi nhãn chưa qua ngưỡng gold |

Điều kiện bắt buộc: đủ file nhãn và checker đạt, có gold-set evaluation, không dùng eval để train và không sửa gold.

## 8. Công cụ AI và tài liệu tham khảo

- Claude (Claude Code): viết script `tools/prelabel_yolo.py` để pre-label; so sánh nhãn của em với gold để tìm nguyên nhân F1 thấp; vẽ box lên ảnh để rà 10 ảnh ở mục 3; soạn nháp `GUIDELINE_MINI.md` và các mục của báo cáo. Em đã mở lại ảnh để kiểm tra các ca mơ hồ, các ví dụ và số liệu được nêu trong báo cáo.
- Model pre-label: YOLO26x pretrained trên COCO (Ultralytics), chỉ dùng tạo nhãn nháp; toàn bộ nhãn được kiểm tra và sửa tay trong CVAT.
- Công cụ: CVAT để gán nhãn, Google Colab để train.
- Tài liệu: tài liệu Ultralytics (docs.ultralytics.com).

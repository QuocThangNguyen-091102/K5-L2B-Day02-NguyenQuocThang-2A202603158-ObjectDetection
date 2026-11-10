# Mini guideline — bài làm cá nhân

> Điền nội dung này trước khi bắt đầu gán nhãn. Giữ lại các quyết định sau khi self-QC.
>
> Ghi chú: em hoàn thiện guideline sau khi gán nhãn (commit `fd1870a`), ghi lại các quy tắc đã dùng khi gán.

## Định nghĩa lớp

| Lớp | Định nghĩa của bạn | Ví dụ/điểm phân biệt |
| --- | --- | --- |
| `car` | Xe con 4 bánh chở người | sedan, SUV, taxi, bán tải nhỏ; xe đang đỗ vẫn là car |
| `truck` | Xe chở hàng hoặc xe chuyên dụng, cabin tách riêng với thùng phía sau | xe tải, xe ben, đầu kéo, xe cứu hộ |
| `bus` | Xe chở khách cỡ lớn, thân dài, nhiều cửa sổ | buýt thành phố, buýt 2 tầng, buýt nối toa |
| `van` | Xe thân hộp, cao hơn xe con nhưng ngắn hơn xe buýt | van chở hàng, minivan kiểu Hiace/Transit |

## Quy tắc chung

- Box bám sát vật thể nghĩa là: box chạm mép ngoài phần thân xe nhìn thấy, không lấy bóng, mặt đường hay xe bên cạnh; mỗi xe một box.
- Vật thể bị che khuất: vẫn gán, box quanh phần nhìn thấy nếu còn nhận ra loại xe.
- Vật thể bị cắt bởi rìa ảnh: box chạm rìa ảnh, không đoán phần bên ngoài.
- Vật thể rất nhỏ/mơ hồ: gán nếu còn xác định được lớp (box nhỏ nhất khoảng 8–12 px); không xác định được thì bỏ qua.

## Ghi lại quyết định cho ít nhất ba ca mơ hồ

| Ảnh | Tình huống | Quyết định cuối | Lý do theo schema |
| --- | --- | --- | --- |
| `drive_014` | Xe đỏ ở rìa phải, cỡ giữa minivan và minibus | `van` | Thân hộp, ngắn hơn hẳn xe buýt trong cùng ảnh. Chưa chắc chắn, cần hỏi giảng viên |
| `drive_014` | Xe cứu hộ có cần kéo phía sau | `truck` | Không chở khách, có cabin và khung chuyên dụng; gần nhất với xe chở hàng |
| `drive_028` | Nhiều xe đỗ ven đường, bị cây che một phần | `car` cho từng xe | Lớp theo loại xe, không theo trạng thái; xe đỗ vẫn gán |
| `drive_008` | Xe buýt nối toa | 1 box `bus` | Hai khoang là một xe nên chỉ một box |

## Cần giảng viên làm rõ

- Ranh giới van và minibus (ca `drive_014`).
- Gold có vẻ dùng mã lớp khác README: ở `drive_008`, `drive_014` xe buýt là lớp 3, xe van là lớp 1, xe tải là lớp 2.
- Gold `drive_028` chỉ có 3 box, không gán xe đỗ ven đường. Cần xác nhận phạm vi gán.

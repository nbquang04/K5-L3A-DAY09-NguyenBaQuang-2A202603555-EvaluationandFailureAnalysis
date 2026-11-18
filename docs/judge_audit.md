# Judge audit

FAIL là positive class: TP là lỗi được phát hiện, FN là lỗi bị bỏ sót.

| Tiêu chí | n | κ | Precision | Recall | TP/FP/FN/TN | Đạt floors? | Quyết định |
|---|---|---|---|---|---|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.800 | 24/4/6/66 | Có | Đủ chuẩn cho tone trong phạm vi replay |
| helpful | 100 | 0.375 | 1.000 | 0.300 | 9/0/21/70 | Không | Loại khỏi gate |

Floors: κ≥0.6, P≥0.8, R≥0.7. Helpful bỏ sót 21/30 lỗi; precision cao không bù được recall thấp. Tỷ lệ lỗi tone quan sát 0.28, hiệu chỉnh Rogan–Gladen 0.30; helpful 0.09 → 0.30. Hiệu chỉnh tỷ lệ không sửa quyết định từng case và không cứu judge yếu thành gate.

## Audit bất đồng từ CSV công khai

Người phụ trách duyệt thủ công: **Nguyễn Bá Quang (NguyenBaQuang)**.
Trạng thái: chờ người phụ trách xác nhận các nhận định trong bảng.

Nhận định dưới đây đối chiếu reply và note của nhãn người; không phải một vòng gán nhãn độc lập mới.

| Case | Judge | Human | Ai đúng và vì sao? | Sửa rubric |
|---|---|---|---|---|
| H-008 | PASS | FAIL | Human: cách xưng em và từ nha quá suồng sã theo chuẩn CS. | Phân biệt thân thiện với suồng sã; đưa ví dụ xưng hô. |
| H-017 | PASS | FAIL | Human theo note khách lớn tuổi: gọi bạn và dùng nha không phù hợp. | Truyền ngữ cảnh khách; nếu thiếu tuổi thì ghi bất định thay vì suy đoán. |
| H-029 | PASS | FAIL | Human: không cần nhắn thêm mang giọng ra lệnh. | Chấm toàn câu, không chỉ từ Dạ/vui lòng. |
| H-042 | FAIL | PASS | Human: câu ngắn nhưng lịch sự và đủ thông tin. | Không bắt buộc xin lỗi khi thông báo hoàn thành. |
| H-051 | FAIL | PASS | Human: từ refund được chuẩn CS cho phép. | Whitelist từ chuyên môn, không phạt tiếng Anh tự động. |
| HL-015 | PASS | FAIL | Human: reply 55.000đ nhưng note ledger 40.000đ. | Tách factual correctness khỏi văn phong; so tiền bằng code. |
| HL-016 | PASS | FAIL | Human: lời xin lỗi dài không sửa sai tiền 55.000 so với 35.000đ. | Không thưởng độ dài; yêu cầu bằng chứng ledger. |
| HL-020 | PASS | FAIL | Human: nói 90.000 thay vì 120.000đ. | Dùng reply_amount_correct, không nhờ judge tính tiền. |
| HL-028 | PASS | FAIL | Human: nói 50.000 thay vì 35.000đ. | Lịch sự không được bù sai nghiệp vụ. |
| HL-035 | PASS | FAIL | Human: lặp xin lỗi nhưng sai 50.000 so với 35.000đ. | Thêm ví dụ đối nghịch cùng giọng văn, khác độ đúng. |

## Tái kiểm tra

Chạy trong src: `python -m lab9.judge --csv data/eval/judge_tone_public.csv --audit 5` trả 0; thay bằng judge_helpful_public.csv trả 1, đây là kết quả đúng.

Sau khi sửa rubric cần nhãn người trên tập held-out mới và calibration lại; không khẳng định rubric đã sửa làm tăng accuracy. CSV replay công khai không đại diện người dùng thật. Judge tone đạt chuẩn nhưng chưa được đưa vào gate tiền/approval.

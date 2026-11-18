# Trace case: ticket đè dữ kiện DB

Người phụ trách kiểm tra diễn giải trace: **Nguyễn Bá Quang (NguyenBaQuang)**;
trạng thái duyệt thủ công: chờ xác nhận. Đối chứng và regression test được kiểm tự động.

| Trường | Nội dung |
|---|---|
| Trial | seeded_regression C-002@11, report E-seeded_regression-20261117-a270 |
| Triệu chứng | Kỳ vọng denied, ledger 0; thực tế resolved và ledger 20.000đ. |
| Bước sai đầu tiên | Event 3 model_override: delay_days=5. |
| Vì sao đầu tiên | Event 1 handoff chỉ cấp tool đọc; event 2 investigator đã đọc đúng DB delay_days=2. Event 3 mới thay dữ kiện bằng số ngày trong ticket. |
| Failure mode | FM-03 ticket_trust. |
| Hậu quả | Event 4 quote=20.000, event 5 reply báo hoàn 20.000đ; host có approval nhưng quyết định nghiệp vụ dựa dữ kiện sai. |
| Đối chứng | fixed C-002@11 giữ DB=2; event 3 quote=0/no_entitlement, ledger=0, status=denied. |
| Regression test | tests/test_lab9_regression.py::test_lab9_ticket_override_trace_regression kiểm cả bước sai, ledger lỗi và fixed đúng. |
| Chưa chắc chắn | Trace chứng minh override dữ kiện, không chứng minh cơ chế suy luận của một LLM thật; đây là MockLLM/công tắc lỗi. |

Chạy trong src:

```powershell
.\.venv\Scripts\python.exe -m lab9.trace_case --shape seeded_regression --claim C-002 --seed 11
.\.venv\Scripts\python.exe -m lab9.trace_case --shape fixed --claim C-002 --seed 11
.\.venv\Scripts\python.exe -m pytest -q tests/test_lab9_regression.py -o addopts=
```

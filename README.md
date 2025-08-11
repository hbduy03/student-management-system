# Hệ thống quản lý sinh viên
# Giới thiệu
Hệ thống quản lý sinh viên được phát triển bằng Django Framework, hỗ trợ nhiều vai trò khác nhau, có bốn nhóm chính:
- Django Admin: quản lý cấp cao, toàn quyền với hệ thống.
- School Admin: quản lý trường học, giảng viên, và sinh viên.
- Teacher: quản lý lớp được phân công, nhập điểm sinh viên.
- Student: Xem thông tin.

# Các công nghệ sử dụng:
- Backend: Django 5.x, Python 3.x
- Database: Sqlite
- Frontend: Html,Css,Js (Django Template)
- Xác thực, phân quyền: AbtractUser, Auth.

# Cấu trúc chung của thư mục:
<img width="560" height="526" alt="image" src="https://github.com/user-attachments/assets/9c37fc4c-f5a1-4ece-a74b-fafa5db42f45" />

# Các tính năng chính: 
Hệ thống hỗ trợ CRUD (Create – Read – Update – Delete) cho các đối tượng:
- Phân quyền cho người dùng: Tự động gán quyền khi tạo tài khoản, có 3 nhóm chính: admins, teachers, students
- Quản lý các đối tượng của trường học:
  + Teacher: Quản lý thông tin giảng viên, phân công giảng dạy và chủ nhiệm các lớp
  + Student: Quản lý thông tin học sinh, lớp học
  + Department:Quản lý các khoa thuộc trong trường.
  + Major: Quản lý các ngành thuộc khoa đó.
  + Subject: Quản lý các môn học.
  + Subject Details: Quản lý điểm số của sinh viên theo từng lớp học phần.
  + Classroom: Quản lý lớp học gốc của giảng viên chủ nhiệm và các sinh viên.
  + ClassSection: QUản lý các lớp học phần thuộc về lớp gốc.
- Quản lý điểm số::
  + Giảng viên thuộc về lớp học phần đó nhập điểm lên hệ thống
  + Hệ thống nhận là lưu điểm số.
  + Hệ thống tự động chấm điểm (Overrall,GPA) , phân loại (rank) và chấm sinh viên đủ tiêu chí qua môn (Passed)
-  Hệ thống thông háo:
  + Gửi thông báo tới từng người dùng.
  +  Cho phép đánh dấu đã đọc hoặc xóa thông báo.
  + Hiển thị thông báo trực tiếp trên giao diện dashboard.

# Hình ảnh minh họa:
<img width="1916" height="968" alt="image" src="https://github.com/user-attachments/assets/2b68085f-6866-4d10-b296-5b895b3c74c6" />

    + Lưu ý: Vì đây là đố án Django đầu tiên của tôi và thời gian có giới hạn, nên tôi đã nhờ sự can thiệp của Chatbot để viết backend (Cụ thể phần ClassSection). Vì vậy, hãy thông cảm cho tôi và tôi mong bạn tìm được hữu ích từ đồ án này. Cảm ơn bạn vì đã dành thời gian xem qua.

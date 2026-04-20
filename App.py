from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)

# Dữ liệu 35 câu hỏi trắc nghiệm từ tài liệu ôn tập Lịch sử 11
questions = [
    {"id": 1, "question": "Bốn câu thơ trong 'Thiên Nam Ngữ Lục' nói về cuộc khởi nghĩa nào?", "options": ["Khúc Thừa Dụ", "Lý Bí", "Hai Bà Trưng", "Phùng Hưng"], "answer": "Hai Bà Trưng"},
    {"id": 2, "question": "Câu nói 'Tôi chỉ muốn cưỡi cơn gió mạnh, đạp luồng sóng dữ...' là của ai?", "options": ["Bà Triệu (Triệu Thị Trinh)", "Bà Trưng Trắc", "Nữ tướng Bùi Thị Xuân", "Công chúa Lê Ngọc Hân"], "answer": "Bà Triệu (Triệu Thị Trinh)"},
    {"id": 3, "question": "Khởi nghĩa Lam Sơn (1418-1427) diễn ra trong bối cảnh nào?", "options": ["Đại Việt bị nhà Nguyên cai trị", "Đại Việt bị nhà Minh đô hộ", "Đại Việt bị chia cắt làm hai Đàng", "Đại Việt có độc lập, chủ quyền"], "answer": "Đại Việt bị nhà Minh đô hộ"},
    {"id": 4, "question": "Sau khi lên ngôi và lập ra nhà Hồ, Hồ Quý Ly đã thực hiện chính sách gì?", "options": ["Kháng chiến chống quân Xiêm", "Tạo ra cục diện Nam-Bắc triều", "Mở rộng lãnh thổ về phía Nam", "Thực hiện nhiều chính sách cải cách"], "answer": "Thực hiện nhiều chính sách cải cách"},
    {"id": 5, "question": "Năm 1397, Hồ Quý Ly ban hành chính sách hạn điền nhằm mục đích gì?", "options": ["Chia ruộng cho dân nghèo", "Hạn chế sở hữu ruộng đất quy mô lớn của tư nhân", "Bảo vệ sức kéo nông nghiệp", "Xóa bỏ gian dối về ruộng đất"], "answer": "Hạn chế sở hữu ruộng đất quy mô lớn của tư nhân"},
    {"id": 6, "question": "Dưới triều Hồ, những tôn giáo nào bị suy giảm vai trò và vị trí?", "options": ["Nho giáo và đạo giáo", "Phật giáo và Đạo giáo", "Hin-đu giáo và Hồi giáo", "Đạo Thiên chúa và Phật giáo"], "answer": "Phật giáo và Đạo giáo"},
    {"id": 7, "question": "Mô hình hành chính nào thuộc thời Lê sơ sau cải cách của Lê Thánh Tông?", "options": ["Đạo, lộ, phủ, châu, hương, giáp, xã", "Đạo thừa tuyên, phủ, huyện, châu, xã", "Lộ, trấn, đạo, phủ, châu, giáp, xã", "Lộ, hương, đạo, phủ, châu, huyện, xã"], "answer": "Đạo thừa tuyên, phủ, huyện, châu, xã"},
    {"id": 8, "question": "Bộ luật nào có nhiều điểm mới và tiến bộ nhất thời phong kiến?", "options": ["Hình luật", "Hình thư", "Quốc triều hình luật", "Hoàng Việt luật lệ"], "answer": "Quốc triều hình luật"},
    {"id": 9, "question": "Dưới thời vua Lê Thánh Tông, quan lại được tuyển chọn chủ yếu qua:", "options": ["Dòng dõi tôn thất", "Tiến cử", "Giáo dục – khoa cử", "Đề cử"], "answer": "Giáo dục – khoa cử"},
    {"id": 10, "question": "Năm 1471, vua Lê Thánh Tông chia đất nước thành bao nhiêu đạo thừa tuyên?", "options": ["10 đạo", "11 đạo", "12 đạo", "13 đạo thừa tuyên và phủ Trung Đô"], "answer": "13 đạo thừa tuyên và phủ Trung Đô"},
    {"id": 11, "question": "Để phát triển kinh tế, vua Lê Thánh Tông đã ban hành chính sách gì?", "options": ["Lập quan Hà đê sứ và quan quân điền", "Cho đào kênh máng, đắp đê 'quai vạc'", "Lập quan Hà đê sứ và đắp đê 'quai vạc'", "Chế độ lộc điền và chế độ quân điền"], "answer": "Chế độ lộc điền và chế độ quân điền"},
    {"id": 12, "question": "Để tôn vinh người đỗ đại khoa, vua Lê Thánh Tông đã:", "options": ["Phong làm quan đại thần", "Dựng bia đá ở Văn Miếu", "Cấp bằng Thạc sĩ", "Cử làm thầy đồ"], "answer": "Dựng bia đá ở Văn Miếu"},
    {"id": 13, "question": "Bộ máy nhà nước phong kiến hoàn chỉnh nhất dưới triều vua nào?", "options": ["Lý Thái Tổ", "Trần Thánh Tông", "Lê Thái Tông", "Lê Thánh Tông"], "answer": "Lê Thánh Tông"},
    {"id": 14, "question": "Kế sách nào của Ngô Quyền được nhà Trần kế thừa năm 1288?", "options": ["Tiên phát chế nhân", "Đánh thành diệt viện", "Vườn không nhà trống", "Đóng cọc trên sông Bạch Đằng"], "answer": "Đóng cọc trên sông Bạch Đằng"},
    {"id": 15, "question": "Câu nói 'vua tôi đồng tâm, anh em hòa mục' khẳng định bài học nào?", "options": ["Truyền thống đánh giặc", "Kết hợp yêu nước và sản xuất", "Phát huy sức mạnh đại đoàn kết dân tộc", "Chiến thuật bao vây"], "answer": "Phát huy sức mạnh đại đoàn kết dân tộc"},
    {"id": 16, "question": "Ý nghĩa lớn nhất của chiến thắng Bạch Đằng năm 938 là gì?", "options": ["Buộc quân Nam Hán từ bỏ mộng xâm lược", "Nâng cao vị thế khu vực", "Mở ra thời đại độc lập, tự chủ lâu dài", "Bài học khoan thư sức dân"], "answer": "Mở ra thời đại độc lập, tự chủ lâu dài"},
    {"id": 17, "question": "Sử cũ viết quân Xiêm 'sợ quân Tây Sơn như sợ cọp' chứng tỏ điều gì?", "options": ["Lính Xiêm vô cùng sợ hãi", "Cách đánh tài tình của Tây Sơn", "Khẳng định uy tín và sức mạnh của Tây Sơn", "Quân Xiêm không dám sang xâm lược"], "answer": "Khẳng định uy tín và sức mạnh của Tây Sơn"},
    {"id": 18, "question": "'Bạch Đằng nhất trận hỏa công...' nói về sự kiện nào?", "options": ["Chiến thắng Bạch Đằng 1288", "Chi Lăng – Xương Giang 1427", "Ngọc Hồi – Đống Đa 1789", "Rạch Gầm – Xoài Mút 1785"], "answer": "Chiến thắng trên sông Bạch Đằng năm 1288"},
    {"id": 19, "question": "Nguyên nhân quyết định thắng lợi của khởi nghĩa Lam Sơn là gì?", "options": ["Tương quan lực lượng có lợi", "Quân Minh thiếu quyết tâm", "Nghĩa quân có kỷ luật cao", "Nhân dân có lòng yêu nước, quyết tâm đuổi giặc"], "answer": "Nhân dân Việt Nam có lòng yêu nước, quyết tâm đuổi giặc"},
    {"id": 20, "question": "Điểm khác biệt của KN Lam Sơn so với kháng chiến chống Tống thời Lý là:", "options": ["Diễn ra qua hai giai đoạn", "Diễn ra khi đất nước đã mất độc lập", "Đông đảo nhân dân tham gia", "Có nhiều tướng giỏi"], "answer": "Diễn ra khi đất nước đã mất độc lập"},
    {"id": 21, "question": "Đặc điểm nổi bật nhất của các cuộc KN thời Bắc thuộc là gì?", "options": ["Không có người lãnh đạo", "Diễn ra liên tục và mạnh mẽ", "Kết quả đều thắng lợi", "Chỉ có nhân dân tham gia"], "answer": "Diễn ra liên tục và mạnh mẽ"},
    {"id": 22, "question": "'Tướng sĩ một lòng phụ tử...' thể hiện truyền thống nào?", "options": ["Truyền thống đoàn kết", "Truyền thống yêu nước", "Truyền thống hiếu học", "Truyền thống hiếu thảo"], "answer": "Truyền thống đoàn kết"},
    {"id": 23, "question": "Nghệ thuật quân sự nào thời Lý được kế thừa trong KN Lam Sơn?", "options": ["Tiên phát chế nhân", "Chủ động kết thúc chiến tranh", "Thanh dã", "Đánh nhanh thắng nhanh"], "answer": "Chủ động kết thúc chiến tranh"},
    {"id": 24, "question": "Nguyên nhân chủ quan chung dẫn đến thắng lợi các cuộc KN là gì?", "options": ["Tinh thần yêu nước, đoàn kết của nhân dân", "Sự mất đoàn kết của kẻ thù", "Địa hình phức tạp", "Vũ khí hiện đại"], "answer": "Tinh thần yêu nước, đoàn kết của nhân dân"},
    {"id": 25, "question": "Nội dung phản ánh tính đại chúng trong cải cách giáo dục của Hồ Quý Ly?", "options": ["Dạy chữ Nôm cho cung nữ", "Tổ chức kì thi đông người đỗ", "Mở trường học ở các lộ, phủ, châu", "Sửa đổi chế độ thi cử"], "answer": "Mở trường học ở các lộ, phủ, châu"},
    {"id": 26, "question": "Điểm tiến bộ trong cải cách của Hồ Quý Ly là gì?", "options": ["Nho giáo là tư tưởng chủ đạo", "Giáo dục phát triển", "Thể hiện tinh thần dân tộc, ý thức tự cường", "Xác lập quân chủ tập quyền"], "answer": "Thể hiện tinh thần dân tộc, ý thức tự cường"},
    {"id": 27, "question": "Bài học quan trọng nhất từ sự thất bại của nhà Hồ là gì?", "options": ["Tập hợp sức mạnh đoàn kết toàn dân tộc", "Xây dựng quân đội hùng mạnh", "Xây dựng công trình phòng thủ", "Đoàn kết với láng giềng"], "answer": "Tập hợp sức mạnh đoàn kết toàn dân tộc, sự ủng hộ của nhân dân"},
    {"id": 28, "question": "Nội dung nào SAI về kết quả cải cách của Hồ Quý Ly?", "options": ["Nâng cao tiềm lực quốc phòng", "Giúp nông dân có thêm ruộng", "Đề cao văn hóa dân tộc", "Giữ vững độc lập dài lâu"], "answer": "Giữ vững nền độc lập dài lâu cho dân tộc"},
    {"id": 29, "question": "Nhận định nào ĐÚNG về cuộc cải cách của Hồ Quý Ly?", "options": ["Đáp ứng được yêu cầu lịch sử", "Chưa đáp ứng yêu cầu lịch sử", "Giữ được độc lập", "Không thoát khỏi khủng hoảng và không giữ được độc lập"], "answer": "Thực hiện cuộc cải cách trên nhiều lĩnh vực, phần nào đáp ứng được yêu cầu lịch sử"},
    {"id": 30, "question": "Mục đích cải cách hành chính của vua Lê Thánh Tông là gì?", "options": ["Tăng cường quyền lực hoàng đế", "Giải quyết khủng hoảng", "Biến nước ta thành cường quốc", "Chuẩn bị chống ngoại xâm"], "answer": "Tăng cường quyền lực của hoàng đế và củng cố bộ máy nhà nước"},
    {"id": 31, "question": "Chức năng của lục Bộ dưới thời Lê Thánh Tông là gì?", "options": ["Giúp việc lục Tự", "Giám sát lục Khoa", "Cơ quan cao cấp chủ chốt", "Phụ trách quân sự"], "answer": "Cơ quan cao cấp chủ chốt trong triều đình"},
    {"id": 32, "question": "Đặc điểm cuộc cải cách dưới triều vua Lê Thánh Tông là gì?", "options": ["Có tính kế thừa", "Có sự nối tiếp", "Có tính liên thông", "Có tính đồng bộ từ trung ương đến địa phương"], "answer": "Có tính đồng bộ từ trung ương đến địa phương"},
    {"id": 33, "question": "Điểm tương đồng trong tuyển chọn quan lại thời Lê Thánh Tông với hiện nay?", "options": ["Có năng lực và phẩm chất tốt", "Có năng lực, xuất thân dòng tộc", "Ưu tiên con em quan lại", "Chú trọng người có công"], "answer": "có năng lực và phẩm chất tốt"},
    {"id": 34, "question": "Cải cách của Lê Thánh Tông đã khắc phục được hạn chế nào?", "options": ["Tranh giành địa vị hoàng tử", "Cấu kết của đại thần", "Bóc lột của quan địa phương", "Sự chuyên quyền và nguy cơ cát cứ"], "answer": "Sự chuyên quyền và nguy cơ cát cứ"},
    {"id": 35, "question": "Mô hình quân chủ thời Lê sơ ảnh hưởng thế nào đến giai đoạn sau?", "options": ["Mô hình thử nghiệm", "Trở thành khuôn mẫu cho các triều đại về sau", "Nền móng phong kiến", "Hình mẫu thí điểm"], "answer": "Trở thành khuôn mẫu cho các triều đại về sau"}
]

# Giao diện HTML tích hợp sẵn
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ôn Tập Lịch Sử 11 - HKII</title>
    <style>
        body { background-color: #f4f7f6; font-family: 'Arial', sans-serif; padding: 20px; color: #333; }
        .container { max-width: 800px; margin: 0 auto; background: #fff; padding: 30px; border-radius: 12px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        h1 { text-align: center; color: #1a73e8; }
        .question-card { border: 1px solid #e1e4e8; padding: 15px; margin-bottom: 15px; border-radius: 8px; border-left: 5px solid #1a73e8; }
        .option-label { display: block; padding: 10px; cursor: pointer; border-radius: 5px; margin: 5px 0; border: 1px solid #eee; }
        .option-label:hover { background: #f0f7ff; }
        #btn-submit { width: 100%; padding: 15px; background: #28a745; color: white; border: none; border-radius: 8px; font-size: 18px; cursor: pointer; position: sticky; bottom: 10px; }
        .correct { background: #d4edda !important; border-color: #c3e6cb !important; }
        .wrong { background: #f8d7da !important; border-color: #f5c6cb !important; }
        .hidden { display: none; }
        #result-box { text-align: center; padding: 20px; background: #e8f0fe; border-radius: 10px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>ÔN TẬP LỊCH SỬ 11</h1>
        <div id="result-box" class="hidden">
            <h2 id="final-score"></h2>
            <button onclick="location.reload()">Làm lại bài</button>
        </div>
        <div id="quiz-area">
            {% for q in quiz %}
            <div class="question-card" id="q-{{ q.id }}">
                <p><strong>Câu {{ loop.index }}: {{ q.question }}</strong></p>
                {% for opt in q.options %}
                <label class="option-label">
                    <input type="radio" name="q{{ q.id }}" value="{{ opt }}"> {{ opt }}
                </label>
                {% endfor %}
                <p class="feedback hidden" style="font-weight:bold;"></p>
            </div>
            {% endfor %}
            <button id="btn-submit">Nộp Bài & Xem Đáp Án</button>
        </div>
    </div>
    <script>
        document.getElementById('btn-submit').onclick = function() {
            let answers = {};
            document.querySelectorAll('.question-card').forEach(card => {
                let id = card.id.split('-')[1];
                let selected = card.querySelector('input:checked');
                answers[id] = selected ? selected.value : null;
            });
            fetch('/submit', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(answers)
            })
            .then(res => res.json())
            .then(data => {
                window.scrollTo(0, 0);
                document.getElementById('result-box').classList.remove('hidden');
                document.getElementById('final-score').innerText = `Kết quả: ${data.score} / ${data.total}`;
                data.details.forEach(item => {
                    let card = document.getElementById('q-' + item.id);
                    let fb = card.querySelector('.feedback');
                    fb.classList.remove('hidden');
                    if (item.correct) {
                        card.classList.add('correct');
                        fb.innerText = "Đúng!"; fb.style.color = "green";
                    } else {
                        card.classList.add('wrong');
                        fb.innerText = "Sai. Đáp án: " + item.right_answer; fb.style.color = "red";
                    }
                });
            });
        };
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, quiz=questions)

@app.route('/submit', methods=['POST'])
def submit():
    user_data = request.json
    score = 0
    details = []
    for q in questions:
        is_correct = (user_data.get(str(q['id'])) == q['answer'])
        if is_correct: score += 1
        details.append({"id": q['id'], "correct": is_correct, "right_answer": q['answer']})
    return jsonify({"score": score, "total": len(questions), "details": details})

if __name__ == '__main__':
    app.run(debug=True)

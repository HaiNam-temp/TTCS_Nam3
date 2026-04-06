const express = require("express");
const app = express();
const PORT = process.env.PORT || 3000;
const cors = require("cors");
app.use(cors());
app.use(express.json());

const data = [
  {
    id: "post_12345",
    name: "RESTful có gì khó????",
    title: "Xây dựng RESTful API chuẩn mực",
    slug: "xay-dung-restful-api-chuan-muc",
    summary: "Bài viết tóm tắt các nguyên tắc thiết kế API...",
    author_name: "Nguyễn Văn A",
    published_at: "2026-03-29T10:00:00Z",
  },
  {
    id: "post_12346",
    name: "Database ở quanh ta thôi.",
    title: "Tối ưu hóa query database",
    slug: "toi-uu-hoa-query-database",
    summary: "Các kỹ thuật index và cache để tăng tốc độ truy vấn...",
    author_name: "Trần Thị B",
    published_at: "2026-03-28T15:30:00Z",
  },
];
app.get("/posts", (req, res) => {
  let dataResponse = [];
  for (let i = 0; i < data.length; i++) {
    dataResponse.push({
      id: data[i].id,
      name: data[i].name,
      title: data[i].title,
    });
  }
  return res.json(dataResponse);
});

app.get("/post/:id", (req, res) => {
  const { id } = req.params;

  let inputIndex = id;

  let dataResponse = data.find((b) => b.id === inputIndex);
  return res.json(dataResponse);
});

app.use((err, req, res, next) => {
  console.error(err.stack);
  res.st  atus(500).json({ error: "Lỗi server" });
});

app.listen(PORT, () => {
  console.log(`Server chạy tại: http://localhost:${PORT}`);
});
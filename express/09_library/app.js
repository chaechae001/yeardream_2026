// Express 서버의 중심

// 1. Express 가져오기
// 2. .env 읽기 (PORT, MongoDB URI, SECRET)
// 3. DB 연결
// 4. Express 앱 생성
// 5. JSON 사용할 수 있게 설정
// 6. 라우터 연결
// 7. 서버 실행

// 필요한 도구 가져오기
const express = require("express");
const dotenv = require("dotenv");  // 환경변수(.env)를 사용할 수 있게 해주는 도구
const connectDB = require("./db");  // db.js 불러옴

// 2. 서버설정 및 데이터베이스 연결
dotenv.config();  // .env 파일에 숨겨둔 비밀번호, 포트 번호 등을 읽어서 process.env에 채워넣음
const app = express();  // 불러온 express 도구를 실행 -> app이라는 이름의 서버 객체를 만듬
connectDB();  // 불러왔던 데이터베이스 연결 코드 실행 (MongDB 등과 연결)

// 3. 클라이언트(사용자) 데이터 이해하기
// 사용자가 서버로 데이터를 보낼 때 보통 JSON 형태를 많이 사용
app.use(express.json());  // 서버가 알아서 JSON 데이터를 읽기 쉬운 형태로 변환

// 4. 라우팅 설정 (길안내)
const authRouter = require("./routes/auth");
app.use("/api/auth", authRouter);

const booksRouter = require("./routes/books");
app.use("/api/books", booksRouter);

// 누군가 브라우저 주소창에 서버의 기본주소(/)로 접속 했을 때, 어떻게 반응??
app.get("/", (req, res) =>{
    res.send("Library Server");  // 사용자가 접속하면 화면에 "Library Server" 글자를 띄워(send) 보내줌
});

// 5. 서버 켜기 (실행)
const PORT = process.env.PORT;  // 환경변수에서 서버를 열 문(Port) 번호를 가져옴
// app.listen(...) : 서버를 켜서 접속을 기다리게 하는 핵심 명령어
app.listen(PORT, ()=>{
    console.log(`Server running on ${PORT}`);
})

// 1. npm install express mongodb cors

const express = require("express");
const app = express();
const cors = require('cors');
const connectDB = require('./db');

// middle ware
// Cross Domain Policy (JS를 이용한 서로 다른 도메인에서 하는 통신을 막는다.)
// 그래서 특정 IP에 대해서 허용해 주는 기능
app.use(cors());
app.use(express.json());  // BODY로 보내는 JSON 형태로 받기

// DB 접속 먼저
connectDB();

app.all('/', (req, res)=>{
    res.send('/member를 이용해 join, list, get update, delete');
});

app.listen(80, ()=> console.log('http://localhost'));

// npm install express jsonwebtoken bcrypt
// express, JWT, 암호화 관련
// bcrypt (해쉬 암호화 모듈)

const express = require("express");
const app = express();
const jwt = require("jsonwebtoken");
const crypto = require("crypto");

// 로그인할 때 id, pw필요
app.use(express.json());
// app.use(cors());  // 설치하면 가능

// 64비트 크기로 Byte를 뽑아낸다 -> hex(16진수)로 변환
const KEY = crypto.randomBytes(64).toString("hex");
console.log('sign key : ' + KEY);

app.post('/login', (req, res)=>{
    // req.body에서 id, pw 받아옴
    const {id, pw} = req.body;
    console.log(`${id}와 ${pw}를 이용해 db 안에 회원이 있는 지 확인`);
    // 로그인 했다고 가정합시다.
    // jwt는 토큰을 만들 때 반드시 sign 해야함!!
    // 토큰 생성 (payload, key, expire)
    // expiresIn : '1s', '1m', '1h', '1d', '1w', '1y' 사용 가능
    const token = jwt.sign({id, pw}, KEY, {expiresIn: '30m'});
    res.json({'success': true, 'token': token});
});

app.post('/check', (req, res)=>{
    const headers = req.headers;
    console.log('headers', headers);
    const token = headers.authorization;

    if (token == null) {
        return res.json({'loginYN':false, 'msg': '토큰이 없습니다.'});
    }
    console.log('test...')

    // token을 뭐로 판단? key!
    try{
        const info = jwt.verify(token, KEY);
        console.log('info', info);
        // 요청했던 일을 한다.
        return res.json({'loginYN':true, 'data':'추가작업 결과'});
    }catch (e){
        // 만료된 토큰이라면 에러가 발생한다.
        return res.json({'loginYN':false, 'msg': '유효하지 않은 토큰입니다.'});
    }
});

app.listen(80, ()=>{console.log('http://localhost')});
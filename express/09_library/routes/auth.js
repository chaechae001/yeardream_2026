// 회원가입 API
// 1. 사용자가 보낸 email, password, name을 받기
// 2. 같은 email이 있는 지 확인
// 3. password 암호화
// 4. User를 MongoDB에 저장

const express = require("express");
const bcrypt = require("bcrypt");
const User = require("../models/User");

const jwt = require("jsonwebtoken");

const router = express.Router();

// 회원가입
// POST /api/auth/register
router.post("/register", async (req,res)=>{
    try {
        // 1. 사용자가 요청 body로 보낸 값을 가져옴
        const {email, password, name} = req.body;

        // 2. 같은 이메일을 가진 사용자가 있는 지 확인
        const existingUser = await User.findOne({email});
        if(existingUser) {
            return res.status(400).json({
                msg: "이미 사용 중인 이메일입니다."
            });
        }

        // 3. 비밀번호를 암호화
        const hashedPassword = await bcrypt.hash(password, 10);  // 10은 salt rounds 값

        // 4. 새로운 사용자 생성
        const user = await User.create({
            email,
            password: hashedPassword,
            name,
        })

        // 5. 회원가입 성공 응답
        res.status(201).json({
            msg: "회원가입이 완료되었습니다.",
            user: {
                id: user._id,
                email: user.email,
                name: user.name,
                role: user.role,
            },
        });
    } catch (error){
        console.error(error);
        res.status(500).json({
            msg: "서버 오류가 발생했습니다."
        });
    }
});

// 로그인
// POST /api/auth/login

router.post("/login", async(req, res)=>{
    try {
        // 1. 사용자가 보낸 email, password 가져오기
        const {email, password} = req.body;

        // 2. 이메일로 회원 찾기
        const user = await User.findOne({email});

        // 3. 회원 없다면 로그인 실패
        if (!user) {
            return res.status(401).json({
                msg: "이메일 또는 비밀번호가 올바르지 않습니다."
            });
        }

        // 4. 입력한 비밀번호와 DB에 저장된 암호화 비밀번호를 비교
        const isMatch = await bcrypt.compare(password, user.password);
        if (!isMatch) {
            return res.status(401).json({
                msg: "이메일 또는 비밀번호가 올바르지 않습니다."
            });
        }

        // 5. JWT 생성
        const token = jwt.sign(
            {
                id: user._id,
                role: user.role,
            },
            process.env.SECRET,
            {
                expiresIn: "1h",
            }
        );

        // 6. 로그인 성공
        res.json({
            msg: "로그인 성공",
            token,
        });
    } catch (error) {
        console.error(error);
        res.status(500).json({
            msg: "서버 오류가 발생했습니다.",
        });
    }
});



module.exports = router;
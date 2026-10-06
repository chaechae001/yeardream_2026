// JWT 인증 미들웨어
// 역할
// 사용자가 보낸 JWT -> 정상 토큰인 지 확인 -> 토큰 안의 사용자 정보 추출 -> req.user에 저장

const jwt = require("jsonwebtoken");

const verifyToken = (req, res, next) =>{
    try {
        // Authorization 헤더를 가져옴
        const authHeader = req.headers.authorization;

        // Authorization 헤더가 없다면, 인증 실패
        if(!authHeader){
            return res.status(401).json({
                msg: "인증 토큰이 필요합니다."
            });
        }

        // 보통 Header의 형식
        // Bearer eyJhbGci.....
        const token = authHeader.split(" ")[1];  // 토큰 값만 가져옴

        // JWT 검증
        const decoded = jwt.verify(token, process.env.SECRET);

        // 토큰 안의 사용자 정보를 req.user에 저장
        req.user = decoded;

        // 다음 미들웨어 or route로 이동
        next();
    } catch(error) {
        return res.status(401).json({
            msg: "유효하지 않은 토큰입니다.",
        })
    }
};

// ADMIN 권한 확인
const requireAdmin = (req, res, next) =>{
    // verifyToken을 통과했다면, req.user가 존재
    if(req.user.role !== "ADMIN") {
        return res.status(403).json({
            msg: "관리자만 접근할 수 있습니다."
        });
    }
    next();
};

module.exports = {
    verifyToken,
    requireAdmin,
};
// Node.js -> MongoDB 연결

// DB 연결해야되는데...??
// 1. mongoose가 필요
// 2. MongoDB 주소가 필요
// 3. mongoose.connect() 사용

const mongoose = require("mongoose");

const connectDB = async ()=> {
    try {
        // process : Node.js에서 현재 실행중인 Node.js 프로세스에 대한 정보와 제어를 제공하는 전역객체
        // Node.js 환경 어디서든 따로 불러오지(import/require) 않고 사용할 수 있습니다.
        await mongoose.connect(process.env.Mongo_URI);
        console.log("MongoDB 연결 성공");
    } catch (error) {
        console.error(error);
    }
};

module.exports = connectDB;
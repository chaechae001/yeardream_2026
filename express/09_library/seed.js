// ============================================================
// seed.js
// 테스트용 도서 10권을 MongoDB에 한 번에 등록하는 파일
// 실행 방법:
// node seed.js
// ============================================================

const mongoose = require("mongoose");
const dotenv = require("dotenv");
const Book = require("./models/Book");

// .env 환경변수 사용
dotenv.config();

// ============================================================
// 테스트용 도서 데이터 10권
// ============================================================

const books = [
    {
        title: "클린 코드 (Clean Code)",
        author: "로버트 C. 마틴",
        isbn: "9788966260959",
        category: "개발"
    },
    {
        title: "리팩터링 2판",
        author: "마틴 파울러",
        isbn: "9791162241882",
        category: "개발"
    },
    {
        title: "모던 자바스크립트 Deep Dive",
        author: "이웅모",
        isbn: "9791158392238",
        category: "개발"
    },
    {
        title: "코어 자바스크립트",
        author: "정재남",
        isbn: "9791158391720",
        category: "개발"
    },
    {
        title: "객체지향의 사실과 오해",
        author: "조영호",
        isbn: "9788998139766",
        category: "개발"
    },
    {
        title: "HTTP 완벽 가이드",
        author: "데이빗 구를리",
        isbn: "9788966261208",
        category: "네트워크"
    },
    {
        title: "혼자 공부하는 컴퓨터 구조+운영체제",
        author: "강민철",
        isbn: "9791169210287",
        category: "CS"
    },
    {
        title: "자바 ORM 표준 JPA 프로그래밍",
        author: "김영한",
        isbn: "9788960777330",
        category: "개발"
    },
    {
        title: "그림으로 배우는 구조적 SQL",
        author: "아사이 아츠시",
        isbn: "9791158390129",
        category: "데이터베이스"
    },
    {
        title: "Do it! 점프 투 파이썬",
        author: "박응용",
        isbn: "9791163034735",
        category: "개발"
    }
];


// ============================================================
// MongoDB에 더미 데이터 저장
// ============================================================

async function seedBooks() {

    try {
        // 1. MongoDB 연결
        await mongoose.connect(process.env.MONGO_URI);
        console.log("MongoDB 연결 성공");


        // 2. 기존 books 데이터를 모두 삭제
        // 테스트를 깔끔하게 다시 시작하기 위한 코드
        await Book.deleteMany({});
        console.log("기존 도서 데이터 삭제 완료");


        // 3. 도서 10권 한 번에 저장
        await Book.insertMany(books);
        console.log("도서 10권 등록 완료");


    } catch (error) {
        console.error("더미 데이터 등록 실패:", error);

    } finally {
        // 4. MongoDB 연결 종료
        await mongoose.connection.close();
        console.log("MongoDB 연결 종료");
    }
}


// 함수 실행
seedBooks();
const express = require("express");
const Book = require("../models/Book");
const {verifyToken, requireAdmin} = require("../middleware/auth");
const router = express.Router();


// 도서 입고 (ADMIN만 가능)
// POST /api/books
router.post("/", verifyToken, requireAdmin, async(req, res)=>{
    try {
        console.log("req.params =", req.params);
        console.log("req.body =", req.body);
        console.log("req.user =", req.user);
        // 사용자가 보낸 도서 정보 가져오기
        const {
            title,
            author,
            isbn,
            category
        } = req.body;

        // 같은 ISBN 책이 있는 지 확인
        const existingBook = await Book.findOne({isbn});
        if(existingBook) {
            return res.status(400).json({
                msg: "이미 등록된 ISBN입니다."
            });
        }

        // 새로운 도서 생성
        const book = await Book.create({
            title,
            author,
            isbn,
            category,
        });

        res.status(201).json({
            msg: "도서가 등록되었습니다.",
            book,
        })
    } catch (error) {
        console.error(error);
        return res.status(500).json({
            msg: "서버 오류가 발생했습니다."
        });
    }
});


// 도서 조회 (전체 도서 목록 반환)
// GET /api/books
router.get("/", async(req, res) =>{
    try {
        const books = await Book.find();
        res.json(books);
    } catch (error) {
        console.error(error);
        res.status(500).json({
            msg: "서버 오류가 발생했습니다.",
        });
    }
});

// 도서 상세 (ISBN으로 단일 도서 상세 및 대출자 정보 조회)
// GET /api/books/:isbn
router.get("/:isbn", async(req, res) => {
    try {
        // URL에서 isbn값 가져오기
        const {isbn} = req.params;
        // ISBN이 같은 책 찾기
        // Book.borrowedBy가 참조하고 있는 User의 name, email 정보를 함께 가져옴
        const book = await Book.findOne({isbn}).populate("borrowedBy", "name email");

        // 해당 ISBN의 도서가 없으면
        if(!book){
            return res.status(404).json({
                msg: "도서를 찾을 수 없습니다."
            });
        }
        // 조회 성공
        res.json(book);
    } catch(error) {
        console.error(error);
        res.status(500).json({
            msg: "서버 오류가 발생했습니다."
        });
    }
});


// 도서 수정/대출 (도서 정보 수정 및 대출/반납 상태 변경)
// PUT /api/books/:isbn
router.put("/:isbn", verifyToken, requireAdmin, async (req, res)=>{
    try {
        const {isbn} = req.params;
        const {
            title,
            author,
            category,
            status,
            borrowedBy
        } = req.body;

        // ISBN으로 도서 검색
        const book = await Book.findOne({isbn});

        if(!book) {
            return res.status(404).json({
                msg: "도서를 찾을 수 없습니다."
            });
        }
        // 값이 들어온 경우, 일반 도서 정보 수정
        if(title !== undefined) {
            book.title = title;
        }
        if(author !== undefined) {
            book.author = author;
        }
        if(category !== undefined) {
            book.category = category;
        }

        // 대출 처리
        if (status === "LENT") {
            // 이미 대출 중이면
            if (book.status === "LENT") {
                return res.status(400).json({
                    msg: "이미 대출 중인 도서입니다."
                });
            }

            // 대출할 사람의 User ObjectId가 필요
            if(!borrowedBy) {
                return res.status(400).json({
                    msg: "대출자 정보가 필요합니다."
                });
            }

            // 상태 변경
            book.status = "LENT";

            // 대출자의 User ObjectId 저장
            book.borrowedBy = borrowedBy;
        }

        // 반납 처리
        if (status === "AVAILABLE") {
            // 현재 대출 중인 책이 아니면 반납 처리 필요 없음
            if(book.status !== "LENT") {
                return res.status(400).json({
                    msg: "현재 대출 중인 도서가 아닙니다."
                });
            }

            // 다시 대출 가능 상태로 변경
            book.status = "AVAILABLE";
            // 대출자 정보 제거
            book.borrowedBy = null;
        }

        // MongoDB 변경 내용 저장
        await book.save();

        // 수정된 책을 다시 조회
        // populate()으로 대출자 정보까지 함께 반환
        const updatedBook = await Book.findById(book._id).populate("borrowedBy", "name email");

        res.status(200).json({
            msg: "도서 정보가 수정되었습니다.",
            book: updatedBook
        });
    } catch (error) {
        console.error(error);
        return res.status(500).json({
            msg: "서버 오류가 발생했습니다."
        });
    }
});


// 도서 폐기 (ADMIN만 가능)
// DELETE /api/books/:isbn

router.delete("/:isbn", verifyToken, requireAdmin, async(req, res)=>{
    try {
        const {isbn} = req.params;

        // ISBN으로 삭제할 도서 찾기
        const book = await Book.findOne({ isbn });

        // 도서가 없으면 삭제할 수 없음
        if (!book) {
            return res.status(404).json({
                msg: "도서를 찾을 수 없습니다."
            });
        }

        // 대출 중인 도서는 폐기하지 못하게 처리
        if (book.status === "LENT") {
            return res.status(400).json({
                msg: "대출 중인 도서는 폐기할 수 없습니다."
            });
        }

        // 실제 MongoDB에서 도서 삭제
        await Book.findOneAndDelete({ isbn });


        // 삭제 성공 응답
        res.json({
            msg: "도서가 폐기되었습니다."
        })
    } catch (error) {
        console.error(error);
        return res.status(500).json({
            msg: "서버 오류가 발생했습니다."
        });
    }
});



module.exports = router;
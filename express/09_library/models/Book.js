const mongoose = require("mongoose");

const bookSchema = new mongoose.Schema(
    {
        title: {
            type: String,
            required: true,
        },

        author: {
            type: String,
            required: true,
        },

        isbn: {
            type: String,
            required: true,
            unique: true,
        },

        category: {
            type: String,
            required: true,
        },

        status: {
            type: String,
            enum: ["AVAILABLE", "LENT"],
            default: "AVAILABLE",
        },

        borrowedBy: {
            type: mongoose.Schema.Types.ObjectId,  // User모델의 _id(ObjectId)를 저장
            ref: "User",
            default: null,  // 아무도 빌리지 않았다면, null
        },
    }
);

const Book = mongoose.model("Book", bookSchema);

module.exports = Book;
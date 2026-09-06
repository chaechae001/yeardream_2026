const mongoose = require("mongoose");

const userSchema = new mongoose.Schema({
    email: {
        type: String,
        required: true,
        unique: true,  // 중복금지
    },

    password: {
        type: String,
        required: true
    },

    name: {
        type: String,
        required: true
    },

    role: {
        type: String,
        enum: ["USER", "ADMIN"],  // 지정된 값만 허용
        default: "USER"  // 기본값
    }
});

module.exports = mongoose.model("User", userSchema);
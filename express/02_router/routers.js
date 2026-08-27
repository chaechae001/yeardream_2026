const express = require('express');
const router = express.Router();    // app의 router 기능만 수행 (app과 동일한 역할)

router.get('/hello', (req, res)=>{
    console.log('Router Module, GET!!');
    res.send('Router Module, GET!!');
});

router.post('/hello', (req, res)=>{
    console.log('Router Module, POST!!');
    res.send('Router Module, POST!!');
});

// router에 등록된 걸 공유함
module.exports = router;
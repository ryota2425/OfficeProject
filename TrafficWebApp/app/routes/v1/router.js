// index.js
// api のまとめ役
// 自作したそれぞれの api を読み込む

// モジュールの読み込み
var express = require('express');
var router = express.Router();

// app.jsで localhost:3000/api/v1/~で apiを呼び出せるように設定した
// localhost:3000/api/v1/configで ./searchData.jsが読み込まれる
// 付け足し可能
router.use('/config', require('./searchData.js'));

// routerをモジュールとして扱う
// app.jsで読み込めるようにする
module.exports = router;

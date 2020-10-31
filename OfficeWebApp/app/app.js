// app.js
// サーバの役割
// apiや htmlのルーティングを設定

// モジュールの読み込み
var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var basicAuth = require('basic-auth-connect');


// ミドルウェアの設定
app.use(bodyParser.urlencoded({
    extended: true
}));
app.use(bodyParser.json({
    extended: true,
    limit: '10mb' // データ容量が大きくて「request entity too large」と怒られた
}));


// Basic認証の設定
var factory_auth = basicAuth('factory', 'factorypass');
app.use(factory_auth)


// apiのルーティング (./routes/v1/index.jsをルーターに設定)
// ./routes/vi の中に自作した apiを配置する
var router = require('./routes/v1/router.js');
// localhost:3000/api/v1/~ で apiを呼び出せるようにする
// 例えば、localhost:3000/api/v1/rits/campus にアクセスすると立命館大学のキャンパス一覧が取得できるイメージ
app.use('/api/v1/', router);


// テンプレートエンジンを使用するディレクトリを宣言
app.set('views', __dirname + '/views');
// 静的ファイル読み込みの宣言 (/public ディレクトリのファイルをロード可能にする)
app.use(express.static(__dirname + '/public'));
// 静的ファイル読み込みの宣言 (/../../Data ディレクトリ内ののファイルを /video_data パス・プレフィックスからロード可能にする)
app.use('/video_data', express.static(__dirname + '/../../Data'))


// トップページ
app.get('/', (req, res) => {
    res.render('top.ejs')
});


// リアルタイム動画再生
app.get('/realtimevideo_byId/:id', (req, res) => {
    res.render('realtimevideo_byId.ejs', {
        MachineId: req.params.id
    });
});


// 指定された時刻の動画を再生
app.get('/video/:MachineId/:year/:month/:day/:hour/:minute', (req, res) => {
    res.render('video.ejs', {
        MachineId: req.params.MachineId,
        year: req.params.year,
        month: req.params.month,
        day: req.params.day,
        hour: req.params.hour,
        minute: req.params.minute
    })
})


// サーバを起動
var port = process.env.PORT || 8080;
app.listen(port);
console.log("To view your app, open this link in your browser: http://localhost:" + port + "/");

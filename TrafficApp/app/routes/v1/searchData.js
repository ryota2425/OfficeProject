// searchData.js
// ElasticSearchからデータを検索して返す

// モジュールの読み込み
var express = require('express');
var router = express.Router();
const fs = require('fs');
const csvSync = require('csv-parse/lib/sync');
var path = require('path');


router.get('/machine_name_list', function (reqFromHtml, resToHtml) {
    // csvファイル読み込み
    const file = path.join(__dirname, './../../../csv/machine.csv');
    var data = fs.readFileSync(file);
    var csvRes = csvSync(data);

    var machineInfo = [];
    for (var i = 1; i < csvRes.length; i++) {
        machineInfo.push({
            machineId: Number(csvRes[i][0]),
            name: csvRes[i][1],
            utc: csvRes[i][2]
        });
    }

    resToHtml.json({
        result: machineInfo
    });
});

router.post('/video_file_name_list/:dirPath', function (reqFromHtml, resToHtml) {
    const dirPath = path.join(__dirname, './../../../../Data/record/') + reqFromHtml.params.dirPath.split('-').join('/')
    fs.readdir(dirPath, function(err, files) {
        if (err) {
            resToHtml.json({
                result: []
            });
        } else {
            var fileList = files.filter(function(file) {
                return path.extname(file) == '.mp4';
            })
            resToHtml.json({
                result: fileList
            });
        }
    });
});


// routerをモジュールとして扱う
// router.jsで読み込めるようにする
module.exports = router;

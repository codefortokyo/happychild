function cmanGetOk() {
    navigator.geolocation.getCurrentPosition(
        function (result) {
            let latitude = result.coords.latitude;
            let longitude = result.coords.longitude;
            document.getElementById("latitude").value = latitude;
            document.getElementById("longitude").value = longitude;

            $('select#ward option').remove();
            $('select#station option').remove();
            $.ajax({
                url: '/api/v1/location/near',
                dataType: 'json',
                data: {latitude: latitude, longitude: longitude},
                success: function (dataArray) {
                    $.each(dataArray.wards, function (i) {
                       $('#ward').append($('<option>', {
                           value: dataArray.wards[i].id,
                           text: dataArray.wards[i].name
                       }))
                    });
                    $.each(dataArray.stations, function (i) {
                       $('#station') .append($('<option>', {
                           value: dataArray.stations[i].id,
                           text: dataArray.stations[i].name
                       }))
                    });

                    document.getElementById('city').value = dataArray.selected_city_id;
                    document.getElementById('ward').value = dataArray.selected_ward_id;

                    $('#city').selectpicker('refresh');
                    $('#ward').selectpicker('refresh');
                    $('#station').selectpicker('refresh');
                }
            })
    });

}

function cmanGetErr(argErr) {
    var wErrMsg = "";
    switch (argErr.code) {
        case 1 :
            wErrMsg = "位置情報の利用が許可されていません";
            break;
        case 2 :
            wErrMsg = "デバイスの位置が判定できません";
            break;
        case 3 :
            wErrMsg = "タイムアウトしました";
            break;
    }
    if (wErrMsg == "") {
        wErrMsg = argErr.message;
    }

    document.getElementById("getErrMag").innerHTML = wErrMsg;
}

function cmanPosGet(url) {
    if (typeof navigator.geolocation === 'undefined') {
        document.getElementById("getErrMag").innerHTML = 'ブラウザが位置情報取得に対応していません';
        return false;
    }

    var wOptions = {
        "enableHighAccuracy": true,                       // true : 高精度
        "timeout": 10000,                                 // タイムアウト : ミリ秒
        "maximumAge": 0                                  // データをキャッシュ時間 : ミリ秒
    };

    // --- 位置取得 --------------------------------------------------------------------------------
    navigator.geolocation.getCurrentPosition(cmanGetOk,   // 位置取得成功時に実行される関数
        cmanGetErr,  // 位置取得失敗時に実行される関数
        wOptions);  // オプション
}

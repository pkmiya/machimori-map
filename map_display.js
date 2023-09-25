// タイル関係
var t_pale = L.tileLayer('http://cyberjapandata.gsi.go.jp/xyz/pale/{z}/{x}/{y}.png', {
    attribution: "<a href='http://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html' target='_blank'>国土地理院</a>"
});

var t_ort = L.tileLayer('http://cyberjapandata.gsi.go.jp/xyz/ort/{z}/{x}/{y}.jpg', {
    attribution: "<a href='http://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html' target='_blank'>国土地理院</a>"
});

var o_std = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© <a href="http://osm.org/copyright">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'
});
1
var Map_BaseLayer = {
    // "MIERUNE地図 color": m_color,
    // "MIERUNE地図 mono": m_mono,
    "地理院地図 淡色": t_pale,
    "地理院地図 航空写真": t_ort,
    "OpenStreetMap 標準": o_std
};

var map = L.map('map', {
    center: [32.504405, 130.604782],  // 八代を中心に設定
    zoom: 13,
    zoomControl: true,
    layers: [t_pale]
});

L.control.layers(Map_BaseLayer, null, {
    collapsed: true
}).addTo(map)


var occur_info = []; // マーカー情報を格納する配列
var occur_contents = [];  // ポップアップで表示する内容
var occur_lat = [];  // 緯度
var occur_lon = [];  // 経度

var safeguard_info = [];     // まもるいえマーカー情報
var safeguard_contents = []; // まもるいえ表示内容
var safeguard_lat = [];  // まもるいえ緯度
var safeguard_lon = [];  // まもるいえ経度
var safeguard_img = [];  // まもるいえ写真

$.ajaxSetup({ async: false });   //同期通信(json取ってくるまで待つ)
$.getJSON("map_data.json", function (data) {
    len = data.length;
    for (var i = 0; i < len; i++) {
        if (data[i].kind == 0) {
            occur_contents.push(data[i].time)
            occur_lat.push(data[i].lat);
            occur_lon.push(data[i].lon);
        }
        else{
            safeguard_contents.push(data[i].time)
            safeguard_lat.push(data[i].lat);
            safeguard_lon.push(data[i].lon);
            safeguard_img.push(data[i].img);
        }
    }
});
$.ajaxSetup({ async: true });

// GeoJSON形式で複数個のマーカーを設定する
// 不審者出没
for (var i = 0; i < occur_lat.length; i++) {
    occur_info.push({     // 1つのマーカーの情報を格納する
        "type": "Feature",
        "properties": {
            "popupContent": occur_contents[i]
        },
        "geometry": {
            "type": "Point",
            "coordinates": [occur_lon[i], occur_lat[i]]
        }
    });
}

// GeoJSON形式で複数個のマーカーを設定する
// こどもをまもるいえ
for (var i = 0; i < safeguard_lat.length; i++) {
    safeguard_info.push({     // 1つのマーカーの情報を格納する
        "type": "Feature",
        "properties": {
            "popupContent": safeguard_contents[i] + "<br><br><img src=" + safeguard_img[0] + "width='200' height='200'></img>"
        },
        "geometry": {
            "type": "Point",
            "coordinates": [safeguard_lon[i], safeguard_lat[i]]
        }
    });
}

var occur_flag = 0;
var safeguard_flag = 0;
var danger_flag = 0;

var occur_tile;
var safeguard_tile;
var danger_tile = [];
// var danger_tile = L.layerGroup();

// 不審者出没表示
function occur_appear() {
    if (occur_flag == 1) {
        occur_flag = 0;
        occur_disappear();
    }
    else {
        occur_flag = 1;
        // クリックしたらポップアップが出るように設定する
        occur_tile = L.geoJson(occur_info,
            {
                onEachFeature: function (feature, layer) {
                    if (feature.properties && feature.properties.popupContent) {
                        layer.bindPopup(feature.properties.popupContent);
                    }
                },
                // オリジナル画像を設定する
                pointToLayer: function (feature, latlng) {
                    var myIcon = L.icon({
                        iconUrl: 'marker-red.png',  // 画像のURI
                        iconSize: [25, 41],         // 画像のサイズ設定
                        iconAnchor: [12, 40],       // 画像の位置設定
                        popupAnchor: [0, -40]       //　　ポップアップの表示を開始する位置設定
                    });
                    return L.marker(latlng, { icon: myIcon });  // マーカーに画像情報を設定
                }
            });
        occur_tile.addTo(map);
    }
}

// 不審者出没非表示
function occur_disappear() {
    map.removeLayer(occur_tile);

}

// まもるいえ表示
function safeguard_appear() {
    if (safeguard_flag == 1) {
        safeguard_flag = 0;
        safeguard_disappear();
    }
    else {
        safeguard_flag = 1;
        // クリックしたらポップアップが出るように設定する
        safeguard_tile = L.geoJson(safeguard_info,
            {
                onEachFeature: function (feature, layer) {
                    if (feature.properties && feature.properties.popupContent) {
                        layer.bindPopup(feature.properties.popupContent);
                    }
                },
                // オリジナル画像を設定する
                pointToLayer: function (feature, latlng) {
                    var myIcon = L.icon({
                        iconUrl: 'mamoruie.png',  // 画像のURI
                        iconSize: [40, 40],         // 画像のサイズ設定
                        iconAnchor: [12, 40],       // 画像の位置設定
                        popupAnchor: [0, -40]       //　　ポップアップの表示を開始する位置設定
                    });
                    return L.marker(latlng, { icon: myIcon });  // マーカーに画像情報を設定
                }
            });
        safeguard_tile.addTo(map);
    }
}

// まもるいえ非表示
function safeguard_disappear() {
    map.removeLayer(safeguard_tile);
}

// 危険エリア表示
function danger_appear() {
    if (danger_flag == 1) {
        danger_flag = 0;
        danger_disappear();
    }
    else {
        danger_flag = 1;

        for (var i = 0; i < occur_lat.length; i ++ ){
            danger_tile[i] = L.circle([occur_lat[i], occur_lon[i]], 500,{ // 位置と半径
                // radius: 1000,
                color: 'blue',
                fillColor: '#399ade',
                fillOpacity: 0.5,
                weight: 0  // 枠線の太さ
            }).addTo(map);

            /*
            danger_tile.addLayer(L.circle([lat[i], lon[i]], 500,{
                // radius: 1000,
                color: 'blue',
                fillColor: '#399ade',
                fillOpacity: 0.5,
                weight: 0  // 枠線の太さ
            }));
            
            var overlay = {
                "Circle": danger_tile,
            }
            //layersコントロールのオーバーレイに設定
            L.control.layers(null, overlay).addTo(map);
            */
        }
    }
}

// 危険エリア非表示
function danger_disappear() {
    for (var i = 0; i < occur_lat.length; i++) {
        map.removeLayer(danger_tile[i]);
    }
}

// ページ読み込み時に実行
window.onload = function () {
    occur_appear();
    safeguard_appear();
    danger_appear();
}
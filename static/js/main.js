var attributes = ["秃头", "刘海", "黑发", "金发", "棕发", "浓眉", "眼镜", "男性", "微笑", "胡子", "无胡", "肤色", "年轻"];
var attributes_key = ["0.4", "0.2", "-1.0", "0.8", "0.4", "0.6", "-0.6", "-0.8", "1.0", "0.8", "0.4", "0.4", "0.2"];
var attributes_map = {
    "-1.0": 0,
    "-0.8": 1,
    "-0.6": 2,
    "-0.4": 3,
    "-0.2": 4,
    "0.0": 5,
    "0.2": 6,
    "0.4": 7,
    "0.6": 8,
    "0.8": 9,
    "1.0": 10
}
var count = 10
var counts = Array.apply(null, Array(attributes.length)).map(() => 0);


function ishow(obj) {
    document.getElementById("cover-" + obj.id).style.visibility = "visible";
}

function ihidden(obj) {
    document.getElementById("cover-" + obj.id).style.visibility = "hidden";
}


function getImg(element) {
    var id = element.id
    var img = document.getElementById('img');
    img.src = "../static/img/" + id + ".png";
}

function getImgList() {
    var imgs = document.getElementById('imgs')
    var html = "";
    for (var i = 0; i < count; i++) {
        html += '<li type="button" id="'
            + i
            + '"  onclick="getImg(this)"><a href="javascript:void(0);"><img src="../static/img/'
            + i
            + '.png">图片'
            + i + '</a></li>'
    }
    imgs.innerHTML = html
}

getImgList()

function drawSidebar() {
    var sidebars = document.getElementById('sidebars')
    var html = '';
    for (var i = 0; i < attributes.length; i++) {
        html += '<div class="sidebar"><p>'
            + attributes[i]
            + ':</p><div class = "sidebar-right" ><div id ="ionrange_'
            + i
            + '"></div></div></div>';
    }
    sidebars.innerHTML = html;
    sidebarValue(counts);
}


function sidebarValue(counts) {
    for (var i = 0; i < attributes_key.length; i++) {
        var id = "#ionrange_" + i.toString();
        var state1 = false
        var state2 = false
        if (i == 12) {
            state1 = true
        }
        if (counts[i] == 2) state2 = true
        $(id).ionRangeSlider({
            grid: state1,
            disable: state2,
            from: attributes_map[attributes_key[i]],
            values: [
                "-1.0", "-0.8", "-0.6", "-0.4", "-0.2", "0.0", "0.2", "0.4", "0.6", "0.8", "1.0"
            ],
            onChange: function (data) {
                attributes_key[parseInt(data.input.context.id.substring(9, 11))] = data.from_value.toString()
            },
            onFinish: function (data) {
                counts[parseInt(data.input.context.id.substring(9, 11))] = 1;
                var num = checkNum(counts)
                if (num >= 4) drawSidebar()
            }
        })
    }
}

function checkNum(arr) {
    var num = 0
    for (var i = 0; i < arr.length; i++) {
        if (arr[i] == 1) num++;
        else arr[i] = 2
    }
    return num
}

drawSidebar()

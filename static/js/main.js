var attributes = ["秃头", "刘海", "黑发", "金发", "棕发", "浓眉", "眼镜", "男性", "微笑", "胡子", "无胡", "肤色", "年轻"];
var attributes_eng = ["Bald", "Bangs", "Black_Hair", "Blond_Hair", "Brown_Hair", "Bushy_Eyebrows", "Eyeglasses", "Male",
    "Mouth_Slightly_Open", "Mustache", "No_Beard", "Pale_Skin", "Young"];
var attributes_value = Array.apply(null, Array(attributes.length)).map(() => "0.0");
var copy_att_value = Array.apply(null, Array(attributes.length)).map(() => "0.0");
var counts = Array.apply(null, Array(attributes.length)).map(() => 0);
var attribute_level = ["-1", "-0.8", "-0.6", "-0.4", "-0.2", "0", "0.2", "0.4", "0.6", "0.8", "1"];
var count = 10;
var datas = {
    "input_image": '000001.jpg',
    "atts": [],
    "level": []
}

var image_id = 1

function ishow(obj) {
    document.getElementById("cover-" + obj.id).style.visibility = "visible";
}

function ihidden(obj) {
    document.getElementById("cover-" + obj.id).style.visibility = "hidden";
}

function strToList(str) {
    return str.split(',')
}


function getAtt() {
    $.ajax({
        type: "POST",
        url: "/images",
        cache: false,
        dataType: 'json',
        data: {'data': JSON.stringify(datas)},
        error: function (XMLHttpRequest) {
            attributes_value = strToList(XMLHttpRequest.responseText);
            copy_att_value = strToList(XMLHttpRequest.responseText);
            drawSidebar(attributes_value)
        },
        success: function (XMLHttpRequest) {
            var img = document.getElementById('img');
            img.src = "../static/out/1.png" + "?temp=" + Math.random()
        }

    });
}

function getImg(element) {
    image_id = element.id
        console.log(image_id)
    showImg('img', image_id)
    showImg('cover-img', image_id)
    counts = Array.apply(null, Array(attributes.length)).map(() => 0);
    datas['input_image'] = "00000" + image_id + ".jpg";
    datas['atts'] = [];
    datas['level'] = [];
    getAtt();
}

function showImg(tap_id, img_id) {
    var tap = document.getElementById(tap_id);
    tap.src = "../static/img/00000" + img_id + ".jpg";
}

function getImgList() {
    var imgs = document.getElementById('imgs')
    var html = "";
    for (var i = 1; i < count; i++) {
        html += '<li type="button" id="'
            + i
            + '"  onclick="getImg(this)"><a href="javascript:void(0);"><img src="../static/img/00000'
            + i
            + '.jpg">图片'
            + i + '</a></li>'
    }
    imgs.innerHTML = html
    getAtt()
}

getImgList()


function drawSidebar(arr) {
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
    sidebarValue(arr);
}


function sidebarValue(arr) {
    for (var i = 0; i < arr.length; i++) {
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
            from: attribute_level.indexOf(arr[i]),
            values: [
                "-1.0", "-0.8", "-0.6", "-0.4", "-0.2", "0", "0.2", "0.4", "0.6", "0.8", "1.0"
            ],
            onChange: function (data) {
                attributes_value[parseInt(data.input.context.id.substring(9, 11))] = data.from_value.toString();
                changeAtt(data.from_value, data.input.context.id.substring(9, 11))
                getAtt()
            },
            onFinish: function (data) {
                counts[parseInt(data.input.context.id.substring(9, 11))] = 1;
                var num = checkNum(counts)
                if (num >= 3) drawSidebar(attributes_value)
            }
        })
    }
}

function changeAtt(value, num) {
    var i = findHave(datas["atts"], attributes_eng[num])
    if (i == 100) {
        datas["atts"].push(attributes_eng[num])
        datas["level"].push(value)
    }
    else datas["level"][i] = value
}

function findHave(arr, value) {
    var state = 100
    for (var i = 0; i < arr.length; i++) {
        if (arr[i] == value) state = i;
    }
    return state
}

function checkNum(arr) {
    var num = 0
    for (var i = 0; i < arr.length; i++) {
        if (arr[i] == 1) num++;
        else arr[i] = 2
    }
    return num
}

function freshSidebar() {
    counts = Array.apply(null, Array(attributes.length)).map(() => 0);
    drawSidebar(copy_att_value)
    datas['atts'] = [];
    datas['level'] = [];
    showImg('img', image_id)
}


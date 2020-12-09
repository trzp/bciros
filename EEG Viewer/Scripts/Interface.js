

//滑块 1-20
//1-10 -> 0.1-1
//10-20 -> 1-10

var plotgain = 1;
var client = new CySocketClient(cyHost, cyPort, "bciros");

var gainlabel = document.getElementById("GainLabel");


//滑条调节增益
//var slider = document.getElementById('myRange');
//slider.oninput = function(e)
//{
//    var eegRes = document.getElementById("CyRes");
//    if(this.value <= 10)
//    {
//        plotgain = this.value*0.1;
//    }
//    else
//    {
//        plotgain = this.value - 10;
//    }
//    eegRes.innerHTML = plotgain;
//}

//按钮调节增益
document.getElementById('GainInc').onclick = function(e)
{
    plotgain *= 1.25;
//    gainlabel.innerText = plotgain;
//    console.log(plotgain)
}

document.getElementById('GainDec').onclick = function(e)
{
    plotgain *= 0.8;
//    gainlabel.innerText = plotgain;
//    console.log(plotgain)
}


//窗口尺寸改变事件,更新画布尺寸和绘图偏移量
window.onresize = function(e)
{
    relayout();
}


window.onload = function(e)
{
    relayout();
}


//web连接按钮绑定
document.getElementById('cyConnect').onclick = function(e)
{
    //websocket客户端
    client = new CySocketClient(cyHost, cyPort, "bciros");
    var cyHost = document.getElementById('cyHost').value;
    var cyPort = document.getElementById('cyPort').value;

    if (cyHost == null) { var cyHost = "127.0.0.1"; }
    if (cyPort == null) { var cyPort = "54123"; }

    client.connect(cyHost, cyPort);
}


//web断开连接绑定
document.getElementById('cyDisconnect').onclick = function(e)
{
    client.sendData("bciros:::Disconnect");
}

//数据记录按钮
document.getElementById('cyStartRecord').onclick = function(e)
{
    client.sendData("bciros:::RecordStart:::" + document.getElementById('cyRecordFile').value);
}

//停止数据记录按钮
document.getElementById('cyStopRecord').onclick = function(e)
{
    client.sendData("bciros:::RecordStop");
}


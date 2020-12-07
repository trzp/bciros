

//滑块 1-20
//1-10 -> 0.1-1
//10-20 -> 1-10

var plotgain = 1;
var client = new CySocketClient(cyHost, cyPort, "bciros");

var slider = document.getElementById('myRange');
slider.oninput = function(e)
{
    var eegRes = document.getElementById("CyRes");
    if(this.value <= 10)
    {
        plotgain = this.value*0.1;
    }
    else
    {
        plotgain = this.value - 10;
    }
    eegRes.innerHTML = plotgain;
}


//窗口尺寸改变事件,更新画布尺寸
window.onresize = function(e)
{
    resizeCanvas();
}

window.onload = function(e)
{
    resizeCanvas();
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


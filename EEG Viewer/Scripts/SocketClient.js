
//eeg通道数 默认绘制500个点
var eegchnum = 8;
var eeg = [];
var sock_data = [];

for(i=0;i<eegchnum;i++)
{
    tm = [];
    for(j=0;j<500;j++)
    {
        tm[j] = 0;
    }
    eeg[i] = tm;
}

//全局变量
//网络连接参数
var cyHost = document.getElementById('cyHost').value;
var cyPort = document.getElementById('cyPort').value;
if (cyHost == null) { var cyHost = "127.0.0.1"; }
if (cyPort == null) { var cyPort = "54123"; }

var delimiter = ",";


function CySocketClient(ip,port,query)
{
    var _this = this;
    this.socket = '';

    this.connect = function(myIP, myPORT)
    {
        if (this.socket != '')
        {
            return;
        }

        this.socket = new WebSocket('ws://'+myIP+':'+myPORT+'/'+query);

        this.socket.onopen = function()
        {
            console.log('socket Open');
        }

        this.socket.onmessage = function(event)
        {
            data = event.data;
            data = data.split("<head>");
            sock_data = data[1].split("<split>");
            for(i=0;i<eegchnum;i++)
            {
                tm = sock_data[i].split(delimiter);
                for(j=0;j<tm.length;j++)
                {
                    eeg[i].push(parseInt(tm[j]))
                }
                
                eeg[i] = eeg[i].slice(-500,)
            }
        }

        this.socket.onclose = function(event)
        {
            if (this.socket == '') { return; }
        }
    }

    
    this.sendData = function (data)
    {
        if (this.socket == '') { return; }
        this.socket.send(data);
    }
    
    this.close = function()
    {
        if (this.socket == '') { return; }
        this.socket.close();
    }
}


//绘图画布
var cyCanvas = document.getElementById('eegCanvas');
var ctx = cyCanvas.getContext('2d');
ctx.strokeStyle = "rgb(255,0,0)";
ctx.fillStyle = "rgb(255,0,0)";

var canvasWidth    = cyCanvas.width;
var canvasHeight   = cyCanvas.height;

var yoffset = [];   //绘制多路曲线时每条曲线的偏移量
var xscale = 2;
var line_size = 1;

var colors = ["#FF1493","#B03060","#2E8B57","#FF00FF","#8A2BE2","#00FA9A","#EE0000","#FF6347","#8B2323","#FFC125","#FF1493","#B03060","#2E8B57","#FF00FF","#8A2BE2","#00FA9A","#EE0000","#FF6347","#8B2323","#FFC125"];


var ch_checkboxs = document.getElementsByName("channels");
ch_checkboxs.onclick = function(e)
{
    relayout();
}

function relayout() 
{
    cyCanvas.width   = (document.getElementById('canvasPane').offsetWidth );
    cyCanvas.height  = (document.getElementById('canvasPane').offsetHeight);
    
    canvasWidth = cyCanvas.width;
    canvasHeight = cyCanvas.height;
    
    //统计有多少个待显示的通道
    num = 0;
    for(i=0;i<eegchnum;i++)
    {
        if(ch_checkboxs[i].checked)
        {
            num ++;
        }
    }
    
    //分割
    if (num==0)
    {
        unit = 0;
        uunit = 0;
    }
    else
    {
        unit = Math.round(canvasHeight/num);
        uunit = Math.round(canvasHeight/(2*num));
    
    }

    
    indx = 0;
    for (i=0;i<eegchnum;i++)
    {
        if (ch_checkboxs[i].checked)
        {
            off = uunit + unit*indx;
            indx ++;
            yoffset[i] = off;
        }
    }

    xscale = canvasWidth/500;
}


function clearScreen()
{
    ctx.clearRect(0,0,cyCanvasWidth,canvasWidth,canvasHeight);
}

function plot()
{
    ctx.clearRect(0,0,canvasWidth,canvasHeight);
    ctx.lineWidth= line_size;

    
    data = eeg.concat();  //deep clone
    for(i=0;i<eegchnum;i++)
    {
        if (ch_checkboxs[i].checked)
        {
            x0 = 0;
            ctx.strokeStyle=colors[i];
            ctx.beginPath();
            ctx.moveTo(x0,yoffset[i]);
            dat = data[i];
            for(j=0;j<dat.length;j++)
            {
                x0 += xscale;
                ctx.lineTo(x0,dat[j] * plotgain + yoffset[i]);
            }
            ctx.stroke();
            ctx.closePath();
        }
        
    }
    
}

setInterval("plot()",100);
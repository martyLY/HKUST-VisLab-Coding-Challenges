// 开始的XY
const canvasStartX = 100
const canvasStartY = 50
// 方块开始的XY
const contentWidth = 1250
const contentHeight = 1300
const rectStartX = contentWidth/11/2 + canvasStartX
const rectStartY = contentHeight/13/2 + canvasStartY
// 方块的宽高
const rectWidth = contentWidth/11-10 //140
const rectHeight = contentHeight/13-10 // 90
const month = ['January','February','March','April','May','June','July','August','September','October','November','December']
// const color = ['#5e4fa1','#3287bc','#66c1a4','#aadca3','#e5f497','#fdfdbe','#fcdf8a','#fbad61','#f36d43','#d43e4f','#9d0142']
const color = ['#aadca3','#e5f497','#fdfdbe','#fcdf8a','#fbad61','#f36d43','#d43e4f','#9d0142']
const canvas = document.querySelector('canvas')
// canvas.style.backgroundColor = '#ccc'
canvas.width = contentWidth + canvasStartX
canvas.height = contentHeight + canvasStartY
const ctx = canvas.getContext('2d') //一个 CanvasRenderingContext2D 对象，使用它可以绘制到 Canvas 元素中
// 绘画坐标
ctx.moveTo(canvasStartX,canvasStartY)
ctx.lineTo(canvas.width,canvasStartY);
ctx.moveTo(canvasStartX,canvasStartY)
ctx.lineTo(canvasStartX,canvas.height);
for (let i=1;i<13;i++) {
  ctx.moveTo(canvasStartX-5, canvasStartY + (canvas.height-canvasStartY)/13*i)
  ctx.lineTo(canvasStartX, canvasStartY + (canvas.height-canvasStartY)/13*i);
  ctx.font = "15px bold 黑体";
  ctx.textAlign="right";
  ctx.fillText(month[i-1], canvasStartX-5, canvasStartY + (canvas.height-canvasStartY)/13*i+4);
}
for (let i=1;i<11;i++) {
  ctx.moveTo(canvasStartX + (canvas.width-canvasStartX)/11*i,canvasStartY-5)
  ctx.lineTo(canvasStartX + (canvas.width-canvasStartX)/11*i,canvasStartY);
  ctx.font = "15px bold 黑体";
  ctx.textAlign="left";
  ctx.fillText(2007+i, canvasStartX + (canvas.width-canvasStartX)/11*i-15, canvasStartY-10);
}
ctx.textAlign="right";
ctx.fillText('0', canvas.width, 280);
ctx.fillText('40', canvas.width, 570);
// 绘画标量
for (let i=0;i<color.length;i++) {
  ctx.fillStyle = color[i]
  ctx.fillRect(canvas.width-rectWidth/5,300+i*rectHeight/3,rectWidth/5,rectHeight/3);
}
ctx.strokeStyle='#000'
ctx.stroke();
// 读取csv文件
Papa.parse('./temperature_daily.csv', {
  download: true,
  complete: function(results){
    const oldData = results.data
    var data = {
      '2008': [[],[],[],[],[],[],[],[],[],[],[],[]],
      '2009': [[],[],[],[],[],[],[],[],[],[],[],[]],
      '2010': [[],[],[],[],[],[],[],[],[],[],[],[]],
      '2011': [[],[],[],[],[],[],[],[],[],[],[],[]],
      '2012': [[],[],[],[],[],[],[],[],[],[],[],[]],
      '2013': [[],[],[],[],[],[],[],[],[],[],[],[]],
      '2014': [[],[],[],[],[],[],[],[],[],[],[],[]],
      '2015': [[],[],[],[],[],[],[],[],[],[],[],[]],
      '2016': [[],[],[],[],[],[],[],[],[],[],[],[]],
      '2017': [[],[],[],[],[],[],[],[],[],[]]
    }
    // 遍历数组拿到对应的年份
    oldData.forEach(item => {
      let arr=item[0].split("-")
      // 如果年份大于2007
      if (arr[0]>2007) {
        arr[1]<10 && (arr[1] = arr[1]%10)
        data[arr[0]][arr[1]-1].push([item[1], item[2]])
      }
    })
    const max = document.getElementById('max')
    const min = document.getElementById('min')
    // 最高温度点击
    max.onclick = function () {
      draw(data, true)
    }
    // 最低温度点击
    min.onclick = function () {
      draw(data, false)
    }
    // 默认绘画最低温度
    draw(data, false)


  }
})

function draw(data, isMax) {
  let x = 0
  let y = 0
  for (let key in data) {
    for (let items in data[key]) {
      y>=12 && (y=0)
      drawRects(rectStartX + rectWidth*x+(10*x),rectStartY + rectHeight*y+(10*y),data[key][items],(x+2008),(y+1),isMax)
      y++
    }
    x++
  }
}


function drawRects(x, y, data, year, month, isMax) {
  let maxArr = []
  let minArr = []
  for (let i=0;i<data.length-1;i++) {
    maxArr.push(data[i][0])
    minArr.push(data[i][1])
  }
  // 求最大值
  let max = Math.max.apply(Math,maxArr)
  // 求最小值
  let min = Math.min.apply(Math,minArr)
  // 方块的颜色
  ctx.fillStyle = isMax ? color[Math.floor(max/5)] : color[Math.floor(min/5)];
  // 绘画方块
  ctx.fillRect(x,y,rectWidth,rectHeight);

  for (let i=0;i<data.length-1;i++) {
    // 绘画折线图
    ctx.beginPath()
    ctx.strokeStyle='#2C3E50'
    ctx.moveTo(x+i*3.5,y-data[i][0]*2+90)
    ctx.lineTo(x+(i+1)*3.5,y-data[i+1][0]*2+90)
    ctx.stroke();
    ctx.beginPath()
    ctx.strokeStyle='#3287bc'
    ctx.moveTo(x+i*3.5,y-data[i][1]*2+90)
    ctx.lineTo(x+(i+1)*3.5,y-data[i+1][1]*2+90)
    ctx.stroke();
  }
  const div = document.createElement('div')
  div.classList = 'clickDiv'
  div.style.left = x + 'px'
  div.style.top = y +30+ 'px'
  div.style.width = rectWidth + 'px'
  div.style.height = rectHeight + 'px'
  div.setAttribute('data-year',year)
  month<10 && (month='0'+month)
  div.setAttribute('data-month',month)
  // 点击方块
  div.onclick = function () {
    let text = document.getElementById('text')
    // 点击方块对应的文字
    text.innerText = 'Date: '+this.getAttribute('data-year')+'-'+this.getAttribute('data-month')+', '+'max: '+max+' min: '+min
    text.style.left = x+rectWidth  + 'px'
    text.style.top = y+rectHeight + 'px'
    text.classList.remove('hide')
  }
  document.body.appendChild(div)
}


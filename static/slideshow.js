
    var img=document.getElementById('img');

    var images=['example1.jpe','example2.jpe','example3.jpe']
    var x=0;
    function slide(){
    if(x>images.lenght) {
    x=x+1;
    } else {
    x=1;
    }
    img.innerHTML="<img scr="+images[x-1]+">";
    }
    setInterval(slide,2000);

imagesN=13
function show(s){
	var ul=document.getElementById("showul");
		imagesN=s;
	if (imagesN>20){
		imagesN=13;
	}

	switch(imagesN){
		case 13:
			ul.style.backgroundImage="url('/static/images/13.jpg')";
			document.getElementById("l8").style.color="black";
			document.getElementById("l1").style.color="red";
			break;
		case 14:
			ul.style.backgroundImage="url('/static/images/14.jpg')";
			document.getElementById("l1").style.color="black";
			document.getElementById("l2").style.color="red";
			break;
		case 15:
			ul.style.backgroundImage="url('/static/images/15.jpg')";
			document.getElementById("l2").style.color="black";
			document.getElementById("l3").style.color="red";
			break;
		case 16:
			ul.style.backgroundImage="url('/static/images/16.jpg')";;
			document.getElementById("l3").style.color="black";
			document.getElementById("l4").style.color="red";
			break;
		case 17:
			ul.style.backgroundImage="url('/static/images/17.jpg')";;
			document.getElementById("l4").style.color="black";
			document.getElementById("l5").style.color="red";
			break;
		case 18:
			ul.style.backgroundImage="url('/static/images/18.jpg')";;
			document.getElementById("l5").style.color="black";
			document.getElementById("l6").style.color="red";
			break;
		case 19:
			ul.style.backgroundImage="url('/static/images/19.jpg')";;
			document.getElementById("l6").style.color="black";
			document.getElementById("l7").style.color="red";
			break;
		case 20:
			ul.style.backgroundImage="url('/static/images/20.jpg')";;
			document.getElementById("l7").style.color="black";
			document.getElementById("l8").style.color="red";
			break;
	}
	imagesN++;
}
setInterval("show(imagesN)",2000);
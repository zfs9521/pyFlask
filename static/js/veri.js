$(document).ready(function() {
		var authCode;
    	randomCode=$(".VeriSpan");//获取验证码出现的方框dom
    	function createCode() {
		    authCode="";//设置这个为空变量，然后往里面添加随机数
		    var authCodeLength=4;//随机数的长度
		    randomArray=[0,1,2,3,4,5,6,7,8,9,'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R', 'S','T','U','V','W','X','Y','Z'];
		    //创建一个数组，随机数从里面选择四位数或者更多
		    for(var i=0;i<authCodeLength;i++){
		        var index=Math.floor(Math.random()*36);//随机取一位数
		        authCode +=randomArray[index];//取四位数，并+相连
		    }
		    // console.log(authCode);//取到四位随机数之后，跳出循环
		    randomCode.text(authCode);//将四位随机数赋值给验证码出现的方框
		    // console.log(randomCode.val());
		}
		createCode();
		$("#button1").click(function(){
   			// alert("hehahhahah");
			var s=randomCode.text();
			ver=$(".VeriIn");
			if(s!=ver.val()){
				ver.val("error");				}
			});

});
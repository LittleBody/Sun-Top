$(document).ready(function(){
    $("button.myshare").bind('click',function(){
        $.get('/filemanage/myshare/', function(redata){
	    if (redata == "no"){
		alert("请先登录");
	    }
	    else{
		window.location.href = '/filemanage/share/';
	    }
	}, "json");
    });
    
})

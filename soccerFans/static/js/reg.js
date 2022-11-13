$(document).ready(function(){
		
	$("#reg_btn").click(function(){
		
		if($("#username").val()==""){
			alert("username is empty!");
			return;
		}
		
		
		if($("#password").val()==""){
			alert("password is empty !");
			return;
		}

		
		if($("#password").val()!=$("#again").val()){
			alert("password is not same!");
			return;
		}
		
		
		$("#form").submit();
		
	});
	
});
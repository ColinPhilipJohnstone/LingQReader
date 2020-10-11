// JavaScript Document
jQuery(".alticon").hover( function (){
	jQuery(this).children('.hiddenicon').css('display','block');
});

			function newest()
			{
				$('#f-newest').hide();
				$('#f-popler').show();
				$('#mysearbtn').val('f-newest');
				$('#mysearbtn').html('Newest <span class="cart-marg caret"></span> <span class="sr-only">Toggle Dropdown</span>');
			}
			function popler()
			{
				$('#f-newest').show();
				$('#f-popler').hide();
				$('#mysearbtn').val('f-most-popular');
				$('#mysearbtn').html('Most Popular <span class="cart-marg caret"></span> <span class="sr-only">Toggle Dropdown</span>');
			}
			
			
			

$('.alticon')
    .bind('mouseover',function(event){
        jQuery(this).children('.hiddenicon').css('display','block');
    })
    .bind('mouseleave', function(e) {
        jQuery(this).children('.hiddenicon').css('display','none');
    });
jQuery("a[data-action='delete-package']").on('click', function (e){
	e.preventDefault();
	$del_id = $(this).attr('id');
	var r=confirm($(this).data('confirm'));
	if (r==true){
	  	var goodtogo = base_url+"iconsets/icon-set-delete/";
		$.ajax({
			type: "POST",
			url: goodtogo,
			data: {id:$del_id},
			success: function (msg){
				if (msg == '1'){
					alert("You have successfully delete the Icon Set.");
					window.location.href = base_url + 'iconsets/manage-icons';
				}else{
					alert("Unable to remove. Please try later.");
				}
				return false;
			}
		});
	}
	return false;
});
/*$(document).on('submit','#searchForm',function(){
   // code
	
	$(this).closest("form").attr("action", "http://www.myiconfinder.com/search/"+$('#searchtext').val()+"/"+$('#mysearbtn').val());
});*/
$('#searchForm').submit(function(e){
   // code
	//e.preventDefault();
	//e.stopPropagation();
	var $listItems = $(".autosuggest ul li");
	var $selected = $listItems.filter('.li-select'),$current;
	if ($selected.length){
			e.preventDefault();
			e.stopPropagation();
			$('#searchtext').val($selected[0].innerText);
			$('#autosuggest').html('');
			return;
		}
	$(this).closest("form").attr("action", "http://www.myiconfinder.com/search/"+$('#searchtext').val()+"/"+$('#mysearbtn').val());
});

$('#autosuggest').hover(function(e){
	$(".autosuggest ul li").removeClass("li-select");
});

$('#searchtext').keyup(function (e) {
    if (e.keyCode == 27 || e.keyCode == 13) {
        $('#autosuggest').html('');
        return;
    }
	
	var $listItems = $(".autosuggest ul li");
	var $selected = $listItems.filter('.li-select'),$current;
	
	
	$listItems.removeClass('li-select');
	if (e.keyCode == 40)
	{
		//li:hover
		if ( ! $selected.length || $selected.is(':last-child') ) {
            $current = $listItems.eq(0);
        }
        else {
            $current = $selected.next();
        }
		$current.addClass('li-select');
		return;
	}
	else if ( e.keyCode  == 38 ) // Up key
    {
        if ( ! $selected.length || $selected.is(':first-child') ) {
            $current = $listItems.last();
        }
        else {
            $current = $selected.prev();
        }
		$current.addClass('li-select');
		return;
    }
	
    var input = $('#searchtext').val();
    if (input.length <= 1 || input.slice(-1) == " ")
        return;
    //	return;
    $.ajax({
        type: "get",
        url: 'http://www.myiconfinder.com/search/get_tags',
        data: { q: input },
        async: true,
        success: function (data) {
            var outWords = $.parseJSON(data);
            $('#autosuggest').html('');
            var res = '<ul id="as_ul">';
            for (x = 0; x < outWords.length; x++) {

                var li = '<li class=""><a href="#" data="' + outWords[x] + '" name="' + (x + 1) + '"><span class="tl"> </span><span class="tr"> </span><span>' + outWords[x] + '</span></a></li>';
                //            $('#auto').prepend('<div>'+outWords[x]+'</div>'); //Fills the #auto div with the options
                res += li;
            }
            res += '</ul>';
            $('#autosuggest').css("position", 'absolute');
            $('#autosuggest').css("width", $('#searchtext').innerWidth());
       //     $('#autosuggest').css("left", $('searchtext').left());
         //   $('#autosuggest').css("top", $('searchtext').top());
            
            $('#autosuggest').prepend(res);


            /*    for(x = 0; x < outWords.length; x++){
                    $('#auto').prepend('<div>'+outWords[x]+'</div>'); //Fills the #auto div with the options
                }*/
        }
    });
});

$(document).on('click', ".autosuggest ul li a", function (e) {
    e.preventDefault();
    e.stopPropagation();
    $('#searchtext').val(e.currentTarget.innerText);
    $('#autosuggest').html('');
});
$(document).bind('click',function (e) {
	if (e.target.innerHTML != "Search")
    	$('#autosuggest').html('');
});

jQuery("a.favorite").on('click', function (e){
	e.preventDefault();
	var a_obj = $(this);
	$fav_id = $(this).attr('id');
	fav = $fav_id.split("-");
	var goodtogo = base_url+"icon/favorite/"+fav[1];
	$.ajax({
		type: "GET",
		url: goodtogo,
		success: function (msg){
			if (msg == '1'){
				a_obj.addClass('active');
			}else if (msg == '0'){
				a_obj.removeClass('active');
			} else {
			    jQuery('#loginModalQuick').modal('show');
				//alert('Please loggedin to add this icon in favorites');
			}
			return false;
		}
	});
	return false;
});
jQuery(document).on('click', "a.fav-link", function (e) {
    e.preventDefault();
    var a_obj = $(this);
    $fav_id = $(this).attr('id');
    fav = $fav_id.split("-");
    var goodtogo = base_url + "icon/favorite_set/" + fav[1];
    $.ajax({
        type: "GET",
        url: goodtogo,
        success: function (msg) {
            if (msg == '1') {
                a_obj.addClass('active');
            } else if (msg == '0') {
                a_obj.removeClass('active');
            } else {
                jQuery('#loginModalQuick').modal('show');
                //alert('Please loggedin to add this icon in favorites');
            }
            return false;
        }
    });
    return false;
});

function hideinfo(a) {
	a.fadeOut("fast");
}
function hideallinfo() {
    hideinfo($(document).find(".infomenu"));
}
function loadinfo() {
    document.onclick = hideallinfo;
    $(document).unbind("click", ".infolink");
    jQuery(document).on('click',".infolink", function (e){
		e.preventDefault();
		hideinfo(jQuery(document).find(".infomenu"));
		$icon_slug = $(this).attr('id').split("~");
		var goodtogo = base_url + "iconsets/icon-set-information/";
		setTimeout(function () {
		    // Do something after 5 seconds
		    $("#infomenu-" + $icon_slug[1]).css('display', 'block');
		    return false;
		}, 50);
		
		/*$.ajax({
			type: "POST",
			url: goodtogo,
			data: {slug:$icon_slug[0]},
			success: function (msg){
				if (msg != '0'){
					//$("#infomenu-"+$icon_slug[1]).css('display','block');
				//	$("#infomenu-"+$icon_slug[1]).html(msg);
				}else{
					alert("Unable to get information. Please try later.");
				}
				return false;
			}
		})*/;
		return false;
	});  
    return false;
}
function scrollToTopReady() {
    $(document).on('scroll', function () {

        if ($(window).scrollTop() > 100) {
            $('.scroll-top-wrapper').addClass('show');
        } else {
            $('.scroll-top-wrapper').removeClass('show');
        }
    });

    $('.scroll-top-wrapper').on('click', scrollToTop);
}
function scrollToTop() {
    verticalOffset = typeof (verticalOffset) != 'undefined' ? verticalOffset : 0;
    element = $('body');
    offset = element.offset();
    offsetTop = offset.top;
    $('html, body').animate({ scrollTop: offsetTop }, 500, 'linear');
}
function signUpData(){
	jQuery(".alert-danger").html('').fadeOut('slow');
	jQuery("#signupModal.modal").css("height","");
	jQuery("#SignUpModalQuick.modal").css("height","");
	var str = '';
	if(jQuery("#id_password_registration").val()==""){
		str = 'Please enter password.';
	}
	if(jQuery("#id_user_email").val()==""){
		str = 'Please enter email address.';
	}
	if(jQuery("#id_username").val()==""){
		str = 'Please enter username.';
	}
	if(jQuery("#id_user_lname").val()==""){
		str = 'Please enter last name.';
	}
	if(jQuery("#id_user_fname").val()==""){
		str = 'Please enter first name.';
	}
	if(str != ''){
		jQuery(".alert-danger").html(str).fadeIn('slow');
		jQuery("#signupModal.modal").css("height",jQuery("#signupModal.modal").height()+(jQuery(".alert").height()+50));
		jQuery("#SignUpModalQuick.modal").css("height",jQuery("#SignUpModalQuick.modal").height()+(68));
		return false;
	}else{
		var goodtogo = base_url+"user/sign-up-done/";
		var data_str = jQuery("#frmSignUp").serializeArray(); // Serialize the data for the POST-request
		$.ajax({
			type: "POST",
			url: goodtogo,
			data: data_str,
			success: function (msg){
				if (msg == '1'){ // If a message is sent, the user thanks�
					window.location.href = base_url + 'user/dashboard';
				}else{
					jQuery(".alert").html(msg).fadeIn('slow');
					jQuery("#signupModal.modal").css("height",jQuery("#signupModal.modal").height()+(jQuery(".alert").height()+50));
					jQuery("#SignUpModalQuick.modal").css("height",jQuery("#SignUpModalQuick.modal").height()+(68));
					return false;
				}
				return false;
			}
		});
	}
}
function loginData(){
	jQuery(".alert").html("").fadeOut('slow');
	jQuery("#loginModal.modal").css("height","");
	jQuery("#loginModalQuick.modal").css("height","");
	$str = '';
	if(jQuery("#id_email_address").val()==""){
		$str = 'The email and password were incorrect.';
	}
	if(jQuery("#id_password").val()==""){
		$str = 'The email and password were incorrect.';
	}
	if($str != ''){
		jQuery(".alert").html($str).fadeIn('slow');
		jQuery("#loginModal.modal").css("height",jQuery("#loginModal.modal").height()+(jQuery(".alert").height()+50));
		jQuery("#loginModalQuick.modal").css("height",jQuery("#loginModalQuick.modal").height()+(jQuery(".alert").height()+50));
		return false;
	}else{
		var goodtogo = base_url+"user/login-check/";
		var str = jQuery("#login_form").serializeArray(); // Serialize the data for the POST-request
		$.ajax({
			type: "POST",
			url: goodtogo,
			data: str,
			success: function (msg){
				if (msg == '1'){ // If a message is sent, the user thanks�
					window.location.href = base_url + 'user/dashboard';
				}else{
					jQuery(".alert").html(msg).fadeIn('slow');
					jQuery("#loginModal.modal").css("height",jQuery("#loginModal.modal").height()+(jQuery(".alert").height()+50));
					jQuery("#loginModalQuick.modal").css("height",jQuery("#loginModalQuick.modal").height()+(jQuery(".alert").height()+50));
					return false;
				}
				return false;
			}
		});
	}
}
function nextStep(){
	$str = '';
	if($("#icon_set").val()==""){
		$str += 'Name of icon set is required. Please enter a value.';
	}
	if($("#author").val()==""){
		if($str != ''){
			$str += '<br />';
		}
		$str += 'Name of the author is required. Please enter a value.';
	}
	if($str != ''){
		$('.alert-danger').html($str).css('display','block');
		return false;
	}else{
		var goodtogo = site_url+"iconsets/next-step";
		var str = $("#frmIcon").serializeArray(); // Serialize the data for the POST-request
		$.ajax({
			type: "POST",
			url: goodtogo,
			data: str,
			success: function (msg){
				if (msg == '1'){ // If a message is sent, the user thanks�
					$("#step1").hide();
					$("#step2").show();
				}
				return false;
			}
		});
	}
}
function nextStepToNew() {
    var rows = $('#allfiledata tr').length ;
    if (rows <= 5) {
		alert("please upload atleast 6 icons");
        return;
    }
    $("#step1").show();
    $("#step2").hide();
	$.post(site_url+"iconsets/thumbnail",$("#frmIcon").serializeArray(),function (data){
		$('#icon_set_img').val(data);
		var temp = '<div class="col-sm-2 col-sm-offset-3" id="icon_set_image"><span class="preview" id="icon_set_image"><img class="center-block" src="/uploads/'+data+'"><span class="overlay" style="display: none;"><span class="updone">100%</span></span></span><div class="progress" id="icon_set_image"><span style="width: 100%;"></span></div></div><div id="clearboth" style="clear:both"></div></div>';
		$("#thumbnail-image").html(temp);
	});
}
function backStep(){
	//backStep
	$("#step2").show();
    $("#step1").hide();
}
function congrats() {
	window.location = "http://www.myiconfinder.com/iconsets/upload_icon_set";
}
function testsubmitFullForm() {
    $str = '';
    if ($("#icon_set").val() == "") {
        $str += 'Name of icon set is required. Please enter a value.';
    }
    if ($("#author").val() == "") {
        if ($str != '') {
            $str += '<br />';
        }
        $str += 'Name of the author is required. Please enter a value.';
    }
    if ($str != '') {
        $('.alert-danger').html($str).css('display', 'block');
        return false;
    } else {
        var goodtogo = site_url + "iconsets/testpostForm";
        var str = $("#frmIcon").serializeArray(); // Serialize the data for the POST-request
        $.ajax({
            type: "POST",
            url: goodtogo,
            data: str,
            success: function (msg) {
             //   if (msg == '1') { // If a message is sent, the user thanks�
                    $("#step1").hide();
                    $("#step2").hide();
					$("#step3").show();
              //  }
				
                return false;
            }
        });
    }
}
function submitFullForm() {
    $str = '';
    if ($("#icon_set").val() == "") {
        $str += 'Name of icon set is required. Please enter a value.';
    }
    if ($("#author").val() == "") {
        if ($str != '') {
            $str += '<br />';
        }
        $str += 'Name of the author is required. Please enter a value.';
    }
    if ($str != '') {
        $('.alert-danger').html($str).css('display', 'block');
        return false;
    } else {
        var goodtogo = site_url + "iconsets/postForm";
        var str = $("#frmIcon").serializeArray(); // Serialize the data for the POST-request
        $.ajax({
            type: "POST",
            url: goodtogo,
            data: str,
            success: function (msg) {
             //   if (msg == '1') { // If a message is sent, the user thanks�
                    $("#step1").hide();
                    $("#step2").hide();
					$("#step3").show();
              //  }
				
                return false;
            }
        });
    }
}
function getUrlParameter(sParam) {
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++) {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam) {
            return sParameterName[1];
        }
    }
}
function finalStep(){
	$str = '';
	if($("#icon_url").val()=="" && $("#user_file_uploaded").val()==""){
		$str += 'Link to compressed file with icons.<br />Please enter a valid url in http://website.com format.';
	}
	if($str != ''){
		$('.error_list').html($str);
		$('.alert').css('display','block');
		return false;
	}else{
		$('.alert').css('display','none');
		document.forms['frmIcon_2'].action = site_url+"iconsets/submission-close";
		document.forms['frmIcon_2'].submit();
	}
}
jQuery( document ).ready(function() {
	jQuery('#loginQuick, .loginQuick').on('click', function(e){
		e.preventDefault();
		jQuery('#loginModalQuick').modal('show');
	});
	$('#myDropdown').on({
	    "click": function (e) {
	        e.stopPropagation();
	    }
	});
	jQuery('#uripopup').on('click', function (e) {
	    e.preventDefault();
	    $.ajax({
	        type: "GET",
	        url: $('#uripopup').attr("href"),
	       // datatype: "image",
	        success: function (data) {
	         /*   canvas = document.createElement('canvas');
	            imag = new Image;
	            imag.src = img;
	            canvas.width = imag.width;
	            canvas.height = imag.height;
	            // Get '2d' context and draw the image.
	            ctx = canvas.getContext("2d");
	            ctx.drawImage(imag, 0, 0);
	            // Get canvas data URL
	            data = canvas.toDataURL();
                */
	             
	            $('.datauri').val(data);
	            
	            jQuery('#modalu').modal('show');
	        }
	    });
	    
	});
	jQuery('#SignUpQuick').on('click', function(e){
		e.preventDefault();
		jQuery('#SignUpModalQuick').modal('show');
	});
	jQuery('#SignUpQuick1').on('click', function (e) {
	    e.preventDefault();
	    jQuery('#SignUpModalQuick').modal('show');
	});
	jQuery('#SignUpQuick2').on('click', function (e) {
	    e.preventDefault();
	    jQuery('#loginModalQuick').modal('hide');
	    jQuery('#SignUpModalQuick').modal('show');
	});
	loadinfo();
	scrollToTopReady();
	jQuery(".search-fiters-left ul.dropdown-menu li a").on('click', function(){
		$(".search-fiters-left .btn:first-child").html($(this).children('em').text()+'<span class="caret"></span>');
	});
	$(function() {
		$('.search-fiters label').on("click", function() {
			var bg_class = $(this).children('input').attr('id');
			$('.icon').removeClass("white");
			$('.icon').removeClass("black");
			$('.icon').removeClass("transparent");
			$('.icon').addClass(bg_class);
		});
	});
	jQuery(".filter-menu > li > a").on('click', function (e){
		e.preventDefault();
		$filter_menu_id = $(this).attr('id');
		window.document.location = $(this).attr("href");//;base_url+'search/'+$("#query_term").val()+'/'+getUrlParameter('sid')+'/l:='+$filter_menu_id;
	});
	var downloadButtonSelector = jQuery("div.buttons > div.btn-group > a.png");
    //dropdown-menu
	var downloadButtonSelector1 = jQuery("ul.dropdown-menu a.uri");
	//downloadlink
	var downloadButtonSelector2 = jQuery("ul.dropdown-menu a.downloadlink");
	var downloadLinkSelector = jQuery("div.buttons").children('p').children('a:first-child');
	jQuery('#uri2').on('click', function (event) {
	    event.preventDefault();
	   // var str = event.currentTarget.attr("href");
	    $.ajax({
	        type: "GET",
	        url: $('#uri2').attr("href"),
	        // datatype: "image",
	        success: function (data) {
	            /*   canvas = document.createElement('canvas');
                   imag = new Image;
                   imag.src = img;
                   canvas.width = imag.width;
                   canvas.height = imag.height;
                   // Get '2d' context and draw the image.
                   ctx = canvas.getContext("2d");
                   ctx.drawImage(imag, 0, 0);
                   // Get canvas data URL
                   data = canvas.toDataURL();
                   */

	            $('.datauri').val(data);

	            jQuery('#modalu').modal('show');
	        }
	    });
	});
	jQuery('#uri1').on('click', function (event) {
	    event.preventDefault();
	  //  var str = event.currentTarget.attr("href");
	    $.ajax({
	        type: "GET",
	        url: $('#uri1').attr("href"),
	        // datatype: "image",
	        success: function (data) {
	            /*   canvas = document.createElement('canvas');
                   imag = new Image;
                   imag.src = img;
                   canvas.width = imag.width;
                   canvas.height = imag.height;
                   // Get '2d' context and draw the image.
                   ctx = canvas.getContext("2d");
                   ctx.drawImage(imag, 0, 0);
                   // Get canvas data URL
                   data = canvas.toDataURL();
                   */

	            $('.datauri').val(data);

	            jQuery('#modalu').modal('show');
	        }
	    });
	});
	jQuery("#512").on('click', function(e){
		
		jQuery("#preview_image").hide().attr("src",jQuery(this).data('value')).fadeIn('slow');
		downloadButtonSelector.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/download/") + "~" + jQuery('#icon_id').val());
		downloadButtonSelector1.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/downloaduri/") + "~" + jQuery('#icon_id').val());
		downloadButtonSelector2.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/download/") + "~" + jQuery('#icon_id').val());
		downloadLinkSelector.attr("href",jQuery(this).data('value').replace("/uploads/iconsets/","/icon/download/")+"~"+jQuery('#icon_id').val());
		//jQuery("#preview_image").focus();
	});
	jQuery("#256").on('click', function(){
		jQuery("#preview_image").hide().attr("src",jQuery(this).data('value')).fadeIn('slow');
		downloadButtonSelector.attr("href",jQuery(this).data('value').replace("/uploads/iconsets/","/icon/download/")+"~"+jQuery('#icon_id').val());
		downloadButtonSelector1.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/downloaduri/") + "~" + jQuery('#icon_id').val());
		downloadButtonSelector2.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/download/") + "~" + jQuery('#icon_id').val());
		downloadLinkSelector.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/download/") + "~" + jQuery('#icon_id').val());
	});
	jQuery("#128").on('click', function(){
		jQuery("#preview_image").hide().attr("src",jQuery(this).data('value')).fadeIn('slow');
		downloadButtonSelector.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/download/") + "~" + jQuery('#icon_id').val());
		downloadButtonSelector1.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/downloaduri/") + "~" + jQuery('#icon_id').val());
		downloadButtonSelector2.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/download/") + "~" + jQuery('#icon_id').val());
		downloadLinkSelector.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/download/") + "~" + jQuery('#icon_id').val());
	});
	jQuery("#64").on('click', function(){
		jQuery("#preview_image").hide().attr("src",jQuery(this).data('value')).fadeIn('slow');
		downloadButtonSelector.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/download/") + "~" + jQuery('#icon_id').val());
		downloadButtonSelector1.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/downloaduri/") + "~" + jQuery('#icon_id').val());
		downloadButtonSelector2.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/download/") + "~" + jQuery('#icon_id').val());
		downloadLinkSelector.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/download/") + "~" + jQuery('#icon_id').val());
	});
	jQuery("#48").on('click', function(){
		jQuery("#preview_image").hide().attr("src",jQuery(this).data('value')).fadeIn('slow');
		downloadButtonSelector.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/download/") + "~" + jQuery('#icon_id').val());
		downloadButtonSelector1.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/downloaduri/") + "~" + jQuery('#icon_id').val());
		downloadButtonSelector2.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/download/") + "~" + jQuery('#icon_id').val());
		downloadLinkSelector.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/download/") + "~" + jQuery('#icon_id').val());
	});
	jQuery("#32").on('click', function(){
		jQuery("#preview_image").hide().attr("src",jQuery(this).data('value')).fadeIn('slow');
		downloadButtonSelector.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/download/") + "~" + jQuery('#icon_id').val());
		downloadButtonSelector1.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/downloaduri/") + "~" + jQuery('#icon_id').val());
		downloadButtonSelector2.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/download/") + "~" + jQuery('#icon_id').val());
		downloadLinkSelector.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/download/") + "~" + jQuery('#icon_id').val());
	});
	jQuery("#24").on('click', function(){
		jQuery("#preview_image").hide().attr("src",jQuery(this).data('value')).fadeIn('slow');
		downloadButtonSelector.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/download/") + "~" + jQuery('#icon_id').val());
		downloadButtonSelector1.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/downloaduri/") + "~" + jQuery('#icon_id').val());
		downloadButtonSelector2.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/download/") + "~" + jQuery('#icon_id').val());
		downloadLinkSelector.attr("href",jQuery(this).data('value').replace("/uploads/iconsets/","/icon/download/")+"~"+jQuery('#icon_id').val());
	});
	jQuery("#20").on('click', function(){
		jQuery("#preview_image").hide().attr("src",jQuery(this).data('value')).fadeIn('slow');
		downloadButtonSelector.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/download/") + "~" + jQuery('#icon_id').val());
		downloadButtonSelector1.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/downloaduri/") + "~" + jQuery('#icon_id').val());
		downloadButtonSelector2.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/download/") + "~" + jQuery('#icon_id').val());
		downloadLinkSelector.attr("href",jQuery(this).data('value').replace("/uploads/iconsets/","/icon/download/")+"~"+jQuery('#icon_id').val());
	});
	jQuery("#16").on('click', function(){
		jQuery("#preview_image").hide().attr("src",jQuery(this).data('value')).fadeIn('slow');
		downloadButtonSelector.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/download/") + "~" + jQuery('#icon_id').val());
		downloadButtonSelector1.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/downloaduri/") + "~" + jQuery('#icon_id').val());
		downloadButtonSelector2.attr("href", jQuery(this).data('value').replace("/uploads/iconsets/", "/icon/download/") + "~" + jQuery('#icon_id').val());
		downloadLinkSelector.attr("href",jQuery(this).data('value').replace("/uploads/iconsets/","/icon/download/")+"~"+jQuery('#icon_id').val());
	});
});
$(document).ready(function(){
    var config = {    
         sensitivity: 1, 
         interval: 0,  
         over: doOpen,  
         timeout: 0,   
         out: doClose      
    };
    
    function doOpen() {
        $(this).addClass('hover');
        $('ul',this).show();
    }
 
    function doClose() {
        $(this).removeClass('hover');
        $('ul',this).hide();
    }

    $('#nav li').hoverIntent(config);
    
    $('#malLogin').fancybox({
    	'hideOnContentClick' : false,
    	'hideOnOverlayClick' : true,
    	'width' : 260,
    	'height' : 200,
    	'autoScale'			: true,
        'autoDimensions'	: false,
    	'onComplete' : function() { $("#loginUsername").focus(); }
    });
    
    $('.Lightbox_AddEdit').fancybox({
    	'width'				: 990,
		'height'			: '85%',
        'autoScale'			: true,
        'autoDimensions'	: true,
        'transitionIn'		: 'none',
		'transitionOut'		: 'none',
		'type'				: 'iframe'
    });
    
    $('.Lightbox_Small').fancybox({
    	'width'				: 400,
		'height'			: 400,
        'autoScale'			: true,
        'autoDimensions'	: true,
        'transitionIn'		: 'none',
		'transitionOut'		: 'none',
		'type'				: 'iframe'
    });
    
    $('.Lightbox_Pic').fancybox({
        'autoScale'			: true,
        'autoDimensions'	: true,
        'transitionIn'		: 'none',
		'transitionOut'		: 'none'
    });
    
    // search bar
    $('#topSearchText').focus(function() {
		if ($(this).val() == 'Search') {
			$(this).val('');
			$(this).css('color','#000000');
		}
	});
	
	$('#topSearchText').blur(function() {
		if ($(this).val() == '') {
			$(this).val('Search');
			$(this).css('color','#777777');
		}
	});
	
	load_img_tags();

});

function logoutMAL()
{
	$.ajax({
	  type: 'POST',
	  url: '/logout.php',
	  data: 'logout=1',
	  success: function() { window.location = '/'; }
	});
}

function searchShowAdv()
{
	if (document.getElementById("advSearch").style.display == "none")
		document.getElementById("advSearch").style.display = "block";
	else
		document.getElementById("advSearch").style.display = "none";
}

function fav_clicker(iORr,favType,favID)
{
	// add
	var iUrl = [];
	iUrl[1] = 't=13&aid='; // anime
	iUrl[2] = 't=38&mid='; // manga
	iUrl[3] = 't=42&cid='; // character
	iUrl[4] = 't=47&vaid='; // va
	
	// remove
	var rUrl = [];
	rUrl[1] = 't=14&aid='; // anime
	rUrl[2] = 't=39&mid='; // manga
	rUrl[3] = 't=43&cid='; // character
	rUrl[4] = 't=48&vaid='; // va
	
	var ajaxURL = '';
	if (iORr == 1) // add
		ajaxURL = iUrl[favType];
	else
		ajaxURL = rUrl[favType];
	
	var url = "/includes/ajax.inc.php?s=1&"+ajaxURL+favID;
	$.get(url, function(data)
		{
		document.getElementById("favOutput").innerHTML = data;
		}
	);
}

function ts_selection()
{
	document.getElementById("topSearchText").focus();
}

function ts_subSearch(val)
{
	if (val == 5) // IE crap
		{
		var url_array = [];
		url_array[0] = '/anime.php?q=';
		url_array[1] = '/manga.php?q=';
		url_array[2] = '/character.php?q=';
		url_array[3] = '/fansub-groups.php?q=';
		url_array[4] = '/clubs.php?action=find&cn=';
		url_array[5] = '/users.php?q=';
		url_array[6] = '/people.php?q=';
		
		var curText = document.getElementById("topSearchText").value; 
		var curVal = document.getElementById("topSearchValue").value;
		//document.location = url_array[curVal]+curText;
		window.location = url_array[curVal]+curText;
		return false;
		//alert('test2');
		}
	else
		return false;
}

function ts_checkEnter(e)
	{
			/*
		var key;
		 if(window.event)
			  key = window.event.keyCode;     //IE
		 else
			  key = e.which;     //firefox
		*/
		var keyCode = e.keyCode ? e.keyCode : e.which ? e.which : e.charCode;
		 if (keyCode == 13)
			{
			ts_subSearch(5);
			return false;
			}
		 else
			return true;
	}
	
function load_img_tags() {
	$('img.userimg').each(function() {
		var imgObj = $(this);
		var imgUrl = $(this).data('src');
		if ($(this).attr('src') == undefined) {
			$('<img>', {
				src: imgUrl,
				error: function() { console.log('Cannot load user image: ' + imgUrl); },
				load: function() { imgObj.attr('src', imgUrl); }
				});
			}
		});
	}
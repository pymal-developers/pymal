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

	$('#topSearchText').on('keyup', function() {
	var tsButton = $('#searchBar input[type=image]');
	if ($(this).val().length>1) {
		tsButton.addClass('ok');
		} else {
		tsButton.removeClass('ok');
		}
	});

	$('#topSearchValue').on('change', function() {
		$('#topSearchText').focus();
	});

	var search_url_array = [];
	search_url_array[0] = '/anime.php?q=';
	search_url_array[1] = '/manga.php?q=';
	search_url_array[2] = '/character.php?q=';
	search_url_array[3] = '/fansub-groups.php?q=';
	search_url_array[4] = '/clubs.php?action=find&cn=';
	search_url_array[5] = '/users.php?q=';
	search_url_array[6] = '/people.php?q=';

	$('form#searchBar').on('submit', function() {
		var curText = $('#topSearchText').val();
		var curVal = $('#topSearchValue').val();
		if (curText.length>1 && curText!='Search') {
			window.location = search_url_array[curVal]+curText;
		}
		return false;
	});
	
	
	$('.min2chars').on('keyup', function() {
		var objBut = $(this).closest('form').find('input[type=submit]');
		if ($(this).val().length > 1) {
			objBut.removeClass('notActive');
			} else {
			objBut.addClass('notActive');
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
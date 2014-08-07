$(document).ready(function(){
	$('.Anime_Gallery').fancybox({
		'titlePosition' 	: 'over'
	});

    $('a.viewOpEdMore').click(function(){
        var _this = $(this);

        $('#'+_this.data('use')).toggle();

        if (_this.html() == 'more')
        {
            _this.html('less');
        }
        else
        {
            _this.html('more');
        }
    });
});


function buyAnime(element) {
    var $element = jQuery(element),
        formElement = $element.data('form-id');

    jQuery('#' + formElement).submit();
}

function myinfo_updateInfo(entry_id)
{
	var nscore = document.getElementById("myinfo_score").value;
	var nstatus = document.getElementById("myinfo_status").value;
	var nepsseen = document.getElementById("myinfo_watchedeps").value;
	var naid = document.getElementById("myinfo_anime_id").value;
	var curstats = document.getElementById("myinfo_curstatus").value;

	//var url = "/includes/ajax.inc.php?t=62&aid="+aid+"&alistid="+entry_id+"&score="+score+"&status="+status+"&epsseen="+epsseen;
	document.getElementById("myinfoDisplay").innerHTML = '<img src="http://cdn.myanimelist.net/images/xmlhttp-loader.gif" align="center">';
	$.post("/includes/ajax.inc.php?t=62", {aid:naid,alistid:entry_id,score:nscore,status:nstatus,epsseen:nepsseen,astatus:curstats}, function(data)
			{
			document.getElementById("myinfoDisplay").innerHTML = data;
	 		}
		);
}

function checkEps()
{
	var totalEps = document.getElementById("curEps").innerHTML;
	if (document.getElementById("myinfo_status").value == 2)
		document.getElementById("myinfo_watchedeps").value = totalEps;
}

function myinfo_toggleAdd()
{
	var myobj = document.getElementById("addtolist");
	$("#addtolist").toggle("slow");
	$("#addclicker").toggle();
}

function showHideSimilarImages(totalImages)
{
	for(i=1;i<=totalImages;i++)
		{
		$("#simimg"+i).toggle();
		}
}

function getRecommendation(arid,arsid)
{
	var simObj = document.getElementById("simaid"+arsid);
	$(simObj).toggle();
	//simObj.style.display = 'block';
	/*
	simObj.innerHTML = '<img src="http://cdn.myanimelist.net/images/xmlhttp-loader.gif"> Loading recommendations...';
	$.get("../includes/ajax.inc.php?t=27&arid="+arid+"&arsid="+arsid, function(data)
		{
		simObj.innerHTML = data;
		}
	);
	*/
}

function myinfo_addtolist(anime_id)
{
	var nscore = document.getElementById("myinfo_score").value;
	var nstatus = document.getElementById("myinfo_status").value;
	var nepsseen = document.getElementById("myinfo_watchedeps").value;

	//var url = "&aid="+anime_id+"&score="+score+"&status="+status+"&epsseen="+epsseen;
	document.getElementById("myinfoDisplay").innerHTML = '<img src="http://cdn.myanimelist.net/images/xmlhttp-loader.gif" align="center">';
	$.post("/includes/ajax.inc.php?t=61", {aid:anime_id,score:nscore,status:nstatus,epsseen:nepsseen}, function(data)
			{
			document.getElementById("myinfoDisplay").innerHTML = '';
			document.getElementById("addtolist").innerHTML = data;
	 		}
		);
}

function showFSGComment(fsg_id)
{
	$("#fsgComments"+fsg_id).toggle("slow");
}

function doedit()
{
	$("#editdiv").toggle("slow");
}

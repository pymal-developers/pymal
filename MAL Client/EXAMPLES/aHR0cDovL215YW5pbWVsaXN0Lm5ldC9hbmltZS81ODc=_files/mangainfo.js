$(document).ready(function(){
	$('.Manga_Gallery').fancybox({
		'titlePosition' 	: 'over'
	});
});

function myinfo_updateInfo()
{
	var dScore = document.getElementById("myinfo_score").value;
	var dStatus = document.getElementById("myinfo_status").value;
	var dChapters = document.getElementById("myinfo_chapters").value;
	var dVolumes = document.getElementById("myinfo_volumes").value;
	var manga_id = document.getElementById("myinfo_manga_id").value;
	
	document.getElementById("myinfoDisplay").innerHTML = '<img src="http://cdn.myanimelist.net/images/xmlhttp-loader.gif" align="center">';
	$.post("/includes/ajax.inc.php?t=34", {mid:manga_id,score:dScore,status:dStatus,chapters:dChapters,volumes:dVolumes},function(data) {
		document.getElementById("myinfoDisplay").innerHTML = data;
	});
}

function checkComp()
{
	var totalChaps = document.getElementById("totalChaps").innerHTML;
	var totalVols = document.getElementById("totalVols").innerHTML;
	
	if (document.getElementById("myinfo_status").value == 2)
		{
		document.getElementById("myinfo_chapters").value = totalChaps;
		document.getElementById("myinfo_volumes").value = totalVols;
		}
}

function myinfo_toggleAdd()
{
	var myobj = document.getElementById("addtolist");
	$("#addtolist").toggle("slow");
	$("#addclicker").toggle();
}

function myinfo_addtolist(manga_id)
{
	var dScore = document.getElementById("myinfo_score").value;
	var dStatus = document.getElementById("myinfo_status").value;
	var dChapters = document.getElementById("myinfo_chapters").value;
	var dVolumes = document.getElementById("myinfo_volumes").value;
	var manga_id = document.getElementById("myinfo_manga_id").value;
	
	$.post("/includes/ajax.inc.php?t=49", {mid:manga_id,score:dScore,status:dStatus,chapters:dChapters,volumes:dVolumes},function(data) {
		document.getElementById("myinfoDisplay").innerHTML = '';
		document.getElementById("addtolist").innerHTML = data;
	 });
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
	/*
	simObj.style.display = 'block';
	simObj.innerHTML = '<img src="http://cdn.myanimelist.net/images/xmlhttp-loader.gif"> Loading recommendations...';
	$.get("../includes/ajax.inc.php?t=27&arid="+arid+"&arsid="+arsid, function(data)
		{
		simObj.innerHTML = data;
		}
	);
	*/
}

function doedit()
{
	$("#editdiv").toggle("slow");
}

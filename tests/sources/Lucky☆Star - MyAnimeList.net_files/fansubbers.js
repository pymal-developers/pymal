

function fsg_setVote(voteType,fsg_id,anime_id,type)
{
	var goodbadVar;
	if (type == 1) // anime page
		goodbadVar = fsg_id;
	else // fansubber page
		goodbadVar = anime_id;
	
	var text;
	if (voteType == 2) // bad
		{
		text = "didn\'t like";
		}
	else
		text = "liked";
	
	if (voteType == 3)
	{
		//var fsg_url = "&fsgid="+fsg_id+"&value="+voteType+"&aid="+anime_id;
		$.post('/includes/ajax.inc.php?t=19', {fsgid:fsg_id,value:voteType,aid:anime_id} , function(data)
			{
			document.getElementById("good"+goodbadVar).src = '/images/good-off.gif';
			document.getElementById("bad"+goodbadVar).src = '/images/bad-off.gif';
			}
		);
	}
	else
	{	
		var fsgHtml = '<div style="font-family: verdana, arial; font-size: 11px; text-align: center;"><span id="explain">Please explain in short detail why you '+text+' this group\'s subbing performance (255 chars max).</span><div style="margin-top: 5px;"><textarea id="fsgcomm" class="textarea" rows="3" cols="40"></textarea></div><div style="margin-top: 5px;"><input type="button" value="Remove Vote" class="inputButton" onclick="fsg_cancelVote(3,'+fsg_id+','+anime_id+',2)">&nbsp;&nbsp;<input type="button" onclick="fsg_makeComment('+fsg_id+','+anime_id+','+type+','+voteType+');" value="Submit Vote" class="inputButton"></div>';
		
		$.fancybox({
			'content'			: fsgHtml,
	        'autoScale'			: true,
	        'autoDimensions'	: true
		});
		
		if (voteType == 1) // good
			{
			document.getElementById("good"+goodbadVar).src = '/images/good-on.gif';
			document.getElementById("bad"+goodbadVar).src = '/images/bad-off.gif';
			}
		else if (voteType == 2) // bad
			{
			document.getElementById("bad"+goodbadVar).src = '/images/bad-on.gif';
			document.getElementById("good"+goodbadVar).src = '/images/good-off.gif';
			}
	}
	
}

function fsg_cancelVote(voteType,fsg_id,anime_id,type)
{
	var conf = confirm("Are you sure?");
	
	if (conf) {
		var goodbadVar;
		if (type == 1) // anime page
			goodbadVar = fsg_id;
		else // fansubber page
			goodbadVar = anime_id;
		
		fsg_setVote(voteType,fsg_id,anime_id,type);
		$.fancybox.close();
	}
}

function fsg_makeComment(fsg_id,anime_id,type,votetype)
{
	var goodbadVar;
	if (type == 1) // anime page
		goodbadVar = fsg_id;
	else // fansubber page
		goodbadVar = anime_id;
	
	document.getElementById("explain").innerHTML = "Please wait...";
	
	//var fsg_url = "&fsgid="+fsg_id+"&value="+votetype+"&aid="+anime_id+"&comment="+$("#fsgcomm").val();
	$.post("/includes/ajax.inc.php?t=19", {fsgid:fsg_id,value:votetype,aid:anime_id,comment:$("#fsgcomm").val()}, function(data)
		{
			$.fancybox.close();
		}
	);
	
	
}
var timeStamp=Date();var xmlLoaderImage='http://cdn.myanimelist.net/images/xmlhttp-loader.gif';$(function(){$('div.postActions a.deletePost').live('click',function(){var thisObj=$(this);thisObj.hide();var confirmObj=thisObj.parent().find('span.confirmDelete');confirmObj.show();});$('div.postActions a.yes').live('click',function(){var thisObj=$(this);var confirmDiv=thisObj.parent();var msgId=thisObj.data('msgid');$.ajax({type:'POST',url:'/includes/ajax.inc.php?t=84',data:'msgId='+msgId,dataType:'json',success:function(data){if(data.error==null)
{confirmDiv.html('Deleted');$('#forumMsg'+msgId).hide('slow');}
else
{alert('Error: '+data.error);}}});});$('div.postActions a.no').live('click',function(){var thisObj=$(this);thisObj.parent().hide();thisObj.parent().parent().find('a.deletePost').show();});$('#postReply').click(function(){$('#postIndicator').show();var topicId=$('#topicId').val();$.ajax({type:'POST',url:'/includes/ajax.inc.php?t=82',data:'topicId='+topicId+'&messageText='+encodeURIComponent($('#messageText').val())+'&totalReplies='+$('#totalReplies').val(),success:function(data){if(data.html==null){if(data.error!=null){alert(data.error);}
else{alert('There was an error posting, please try again.');}}
else{var extra='';if(data.moreposts){var plural='';if(data.moreposts>1)
plural='s have';else
plural=' has';extra='<div class="goodresult">'+data.moreposts+' post'+plural+' been added since your last page refresh. <a href="?topicid='+topicId+'&goto=newpost">Go to new post</a>.</div>';}
$('.forum_boardrowspacer').last().after(extra+data.html);$('#messageText').val('');$('#quickReply').hide();load_img_tags();}
$('#postIndicator').hide();},dataType:'json'});});$('#showQuickReply').click(function(){$('#quickReply').toggle();$('#messageText').focus();});});function quoteEm(msgId)
{$('#quickReply').show();var username=$('#messageuser'+msgId).children().children().html();$.ajax({type:'POST',url:'/includes/quotetext.php',data:'msgid='+msgId,success:function(data){$('#messageText').val($('#messageText').val()+"[quote="+username+"]"+data+"[/quote]");}});$('#messageText').focus();}
function ignoreBoard(boardid,inVal)
{document.getElementById("iBoardId").innerHTML='<img src="'+xmlLoaderImage+'">';$.get("/includes/ajax.inc.php?t=16&val="+inVal+"&ibid="+boardid+"&timestamp="+timeStamp,function(data)
{if(inVal==2)
document.getElementById("iBoardId").innerHTML="<a href='javascript:void(0);' onclick='ignoreBoard("+boardid+",1);'>Ignore Board</a>";else
document.getElementById("iBoardId").innerHTML="<a href='javascript:void(0);' onclick='ignoreBoard("+boardid+",2);'>Un-ignore Board</a>";});}
function ignoreTopic(topicid,idName,cVal)
{$.get("/includes/ajax.inc.php?t=1&val="+cVal+"&id="+topicid+"&timestamp="+timeStampeStamp,function(data)
{$('#'+idName).toggle();});}
function ignoreTopicinThread(topicid)
{document.getElementById("ignoreThreadText").innerHTML='<img src="'+xmlLoaderImage+'">';$.get("/includes/ajax.inc.php?t=1&id="+topicid+"&timestamp="+timeStamp,function(data)
{if(data==1)
$('#ignoreThreadText').html("<a href='javascript:void(0);' onclick='ignoreTopicinThread("+topicid+",1);'>Hid Topic</a>");else if(data==2)
$('#ignoreThreadText').html("<a href='javascript:void(0);' onclick='ignoreTopicinThread("+topicid+",2);'>Removed Hide</a>");else
$('#ignoreThreadText').html('Too Many');});}
function watchTopic(topicid)
{document.getElementById("watchText").innerHTML='<img src="'+xmlLoaderImage+'">';$.get("/includes/ajax.inc.php?t=69&topic_id="+topicid+"&timestamp="+timeStamp,function(data)
{document.getElementById("watchText").innerHTML=data;});}
function topicview_watchTopic(topicid)
{var topicObj=document.getElementById("wt"+topicid);$.get("/includes/ajax.inc.php?t=69&topic_id="+topicid+"&timestamp="+timeStamp,function(data)
{var myRegExp=/Watching/;var matchPos=data.search(myRegExp);if(matchPos!=-1)
{topicObj.innerHTML='<img src="http://cdn.myanimelist.net/images/watch_y.gif" title="You are watching this topicd">';}
else
{topicObj.innerHTML='<img src="http://cdn.myanimelist.net/images/watch_n.gif" title="You are not watching this topic">';}});}
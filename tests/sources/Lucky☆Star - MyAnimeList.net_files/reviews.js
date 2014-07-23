function voteReview(review_id,value)
{$("#revhelp_output_"+review_id).html("Thanks! One moment please...");$.post("/includes/ajax.inc.php?t=72",{id:review_id,val:value},function(data)
{$("#revhelp_output_"+review_id).html(data);if(value==1)
{var helpful_val=eval($("#rhelp"+review_id).html());$("#rhelp"+review_id).html(helpful_val+1);}
var total_val=eval($("#rtotal"+review_id).html());$("#rtotal"+review_id).html(total_val+1);});}
function reviewToggleText(id)
{if($('#review'+id).css('display')=='inline'){$('#review'+id).hide();$('#reviewToggle'+id).html('read more');}
else{$('#review'+id).show();$('#reviewToggle'+id).html('show less');}}
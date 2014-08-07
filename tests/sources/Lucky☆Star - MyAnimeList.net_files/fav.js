function addRemoveFavorite(obj,fav_id,type_id)
{var parentObj=$(obj).parent();parentObj.html('Saving...');$.post("/includes/ajax.inc.php?t=80",{id:fav_id,type:type_id},function(data)
{parentObj.html(data);});}
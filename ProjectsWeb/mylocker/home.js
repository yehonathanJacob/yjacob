function ScrollTo(element){
  $('html, body').stop().animate({ scrollTop: $(element).offset().top - $("#top").css("height").replace("px",'')-10}, 900);
}
var lockIco;var unlockIco;var psinput;var txinput;var id;
var ty;var ps;var de;var nul;
function falock(Obj){
lockIco=$(Obj);
id= lockIco.attr("id");
id = id.replace("lock", "");
unlockIco = $('#Unlock'+id);
psinput = $('#'+id);
txinput = $('#tx'+id);
lockIco.hide(0);
unlockIco.show(0);
psinput.show(500);
txinput.show(500);
}
function faunlock(Obj){
unlockIco=$(Obj);
id= unlockIco.attr("id");
id = id.replace("Unlock", "");
lockIco = $('#lock'+id);
psinput = $('#'+id);
txinput = $('#tx'+id);
unlockIco.hide(0);
lockIco.show(0);
psinput.hide(500);
txinput.hide(500);
}
function fafloppy(Obj){
id = $(Obj).attr('id');
id = id.replace("ok",'');
ty = $('#tr'+id+' .type input').val();
ps = $('#tr'+id+' .ps input').val();
de = $('#tr'+id+' .ps textarea').val();
nul = $('#null').val();
$.post("Update.php",{
      nul:nul,
      upid:id,
      upty:ty,
      upps:ps,
      upde:de
  }, function(response){
    if(response == "True")
      alert("Saved");
    else
      {
      alert('Error:\n'+response);          
      }
});
}
function fatrash(Obj){
if (confirm('Do you wan\'t to delete this item?')) {
  id = $(Obj).attr('id');
  id = id.replace("dele",'');
  nul = $('#null').val();
  $.post("DeletePs.php",{
      nul:nul,
      Dlid:id,
  }, function(response){
    if(response == "True")
    {
      $( "#tr"+id ).remove();
      alert("Deleted")
    }      
    else
      {
      alert('Error:\n'+response);          
      }
});
}
}

$('.fa-floppy-o').click(function(){fafloppy(this)});
$('.fa-trash-o').click(function(){fatrash(this)});
$('.fa-unlock-alt').click(function(){faunlock(this)});
$('.fa-lock').click(function(){falock(this)});

var stSearch = "";
$('#topBar #SearchB').click(function(){
stSearch = $(this).parent().find('input[name="Search"]').val().toLowerCase();
$('tbody tr').each(function(){
if($(this).find('.type input').val().toLowerCase().indexOf(stSearch)<0)
	$(this).hide();
else
	$(this).show();
        });
});
$('#topBar #Refresh').click(function(){location.reload();});
var bar= $('#topBar #ControlBar');
$('#topBar #ControlI').click(function(){
   if(bar.css('display') == 'block')
   {
      $('#topBar #ControlI').css({transform: 'rotate(-360deg)'});
      bar.slideUp(800);
   }else{
      $('#topBar #ControlI').css({transform: 'rotate(360deg)'});
      bar.slideDown(800);
   }
});

$('#NewPsB').click(function(){
  if ($('#AddNewPS').css('display') == 'none'){
    if($('table').css("width").replace("px","")*1.4<$('body').css("width").replace("px","")){
      $('table').animate({ marginLeft : "0"}, 800,function () {
        $('#AddNewPS').slideToggle('medium', function() {    
          $(this).css('display','inline-block');    
        });
      });
    }else{
      $('#AddNewPS').slideToggle('medium', function() {    
        $(this).css('display','inline-block');
      });
    }
    ScrollTo($('#AddNewPS'));
  }else{
    $('#AddNewPS').slideUp(800,function(){
      if($('table').css("width").replace("px","")*1.4<$('body').css("width").replace("px","")){
        $('table').animate({ marginLeft : "16%"}, 800);
      }
    });
    ScrollTo($("#topBar"));
  }
});
var NewTy;var NewPs;var NewRePs;var NewDetails;
function AdNePs(){
NewTy = $('#AddNewPS').parent().find('input[name="Type"]').val();
NewPs = $('#AddNewPS').parent().find('input[name="Ps"]').val();
NewRePs = $('#AddNewPS').parent().find('input[name="RePs"]').val();
NewDetails = $('#AddNewPS form textarea').val();
nul = $('#null').val();
if(NewTy!=""&&NewPs!=""&&NewRePs!=""&&confirm('Are you sure you confirm all the details?'))
{
  if(NewPs==NewRePs){
  $.post("Insert.php",{
      nul:nul,
      NewTy:NewTy,
      NewPs:NewPs,
      NewRePs:NewRePs,
      NewDetails:NewDetails
  }, function(response){
    if(response.indexOf("True")>=0)
		{	
      NewId = response.replace("True","");
      NewData = '<tr id="tr'+NewId+'">';
      NewData+= '<td class="Control" title="Control Button"><i id="ok'+NewId+'" class="fa fa-floppy-o"></i><i id="dele'+NewId+'" class="fa fa-trash-o"></i></td>';
      NewData+= '<td class="type" title="Type"><input type="text" name="TypeText" value="'+NewTy+'"></td>';
      NewData+= '<td class="ps" title="Password"><i id="lockPs'+NewId+'" class="fa fa-lock"></i><i id="UnlockPs'+NewId+'" class="fa fa-unlock-alt"></i><input id="Ps'+NewId+'" type="text" value="'+NewPs+'"><textarea id="txPs'+NewId+'">'+NewDetails+'</textarea></td>';
      NewData+= '</tr>';
      $("tbody").append(NewData);
			alert("Added");
      $('.fa-floppy-o').click(function(){fafloppy(this)});
      $('.fa-trash-o').click(function(){fatrash(this)});
      $('.fa-unlock-alt').click(function(){faunlock(this)});
      $('.fa-lock').click(function(){falock(this)});
		}      
    else
      {
        alert('Error:\n'+response);          
      }
    });
  }else{alert("Your Password and RePassword Dosn't matches");}
}else{
  alert("Please confirm all the details");
}
}
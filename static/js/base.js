(function(){
  "use strict";
  $(function(){$('[data-toggle="tooltip"]').tooltip();});
  $(function(){
    if(window.addEventListener){
      window.addEventListener('DOMContentLoaded', CopyAcross, false);
    }else{
      window.attachEvent('onclick', CopyAcross);
    }
  });
})();

function CopyAcross(f){
  if(f.checked){
    var f_id_arr = f.id.split('#');
    var f_id = f_id_arr[0];
    var f_src = f_id_arr[1];
    var f_trg = f_id_arr[2];
    if(f_id=='src2translit'){
      document.getElementsByName(f_trg)[0].value = document.getElementsByName(f_src)[0].value;
    }
    if(f_id=='src2root'){
      document.getElementsByName(f_trg)[0].value = document.getElementsByName(f_src)[0].value;
    }
    if(f_id=='translit2src'){
      document.getElementsByName(f_trg)[0].value = document.getElementsByName(f_src)[0].value;
    }
    if(f_id=='phoneMic2phoneTic'){
      document.getElementsByName(f_trg)[0].value = document.getElementsByName(f_src)[0].value;
    }
    if(f_id=='phoneTic2phoneMic'){
      document.getElementsByName(f_trg)[0].value = document.getElementsByName(f_src)[0].value;
    }
  }
};

function MutexCheckbox(f){
  if(f.checked){
    // Unchecking others if checked…
    var f_info = f.name.split('-');
    var f_num = f_info[1];
    var chckbx_list = document.getElementsByClassName('MutexCheckbox');
    Array.prototype.forEach.call(chckbx_list, function(targ_chckbx){
      var targ_chckbx_info = targ_chckbx.name.split('-');
      var targ_chckbx_num = targ_chckbx_info[1];
      if(f.id === targ_chckbx.id) return;
      if(f_num !== targ_chckbx_num) return;
      if(targ_chckbx.checked){
        targ_chckbx.checked = false;
      }
    });
  }
};

function ExcludeRows(){
  var notswad_chckbx_list = document.getElementsByClassName('notswad_checkbox');
  Array.prototype.forEach.call(notswad_chckbx_list, function(notswad_chckbx_elem){
    if(notswad_chckbx_elem.checked) {
      var target = notswad_chckbx_elem.parentElement;
      while(target.tagName !== 'TR' && target !== null){
        target = target.parentElement;
      }
      if(target !== null){
        target.style.display = "none";
      }
    }
  });
}

function MirrorCognateCheckboxes(cbox){
  var checked = cbox.checked
    , cld = cbox.dataset.mirror
    , cboxList = document.getElementsByClassName('loan_event');
  Array.prototype.forEach.call(cboxList, function(c){
    if(cld === c.dataset.mirror){
      if(c.checked !== checked){
        c.checked = checked;
      }
    }
  });
}
function val_form(){
    var pass1=document.getElementById('pass1').value;
    var pass2=document.getElementById('pass2').value;
    if(pass1==pass2){
        document.getElementById('pass1').style.borderColor="rgba(17, 25, 138, 0.658)";
        document.getElementById('pass2').style.borderColor="rgba(17, 25, 138, 0.658)";
        document.getElementById('error').innerHTML="";
    }
    else{
        document.getElementById('pass1').style.borderColor="red";
        document.getElementById('pass2').style.borderColor="red";
        document.getElementById('error').innerHTML="Both passwords are not matched.";
        document.getElementById('passwordDiv').style.marginBottom="30px";
        return false;
    }

    if(document.querySelectorAll('input[type="radio"]:checked').length==0)
    {
        alert("Select atleast one subject !!!");
        return false;
    }
    alert("Registration completed. login now.");
    return true;
}

/*

{% if total_sub > 1 %}
    var checkRadio = document.querySelector('input[name="subjects"]:checked');
    if(checkRadio != null) {
        var subjects = document.getElementsByTagName('input');
        var sub_id;
        for (var i = 0; i < subjects.length; i++) {
            if (subjects[i].type === 'radio' && subjects[i].checked) {
                sub_id = subjects[i].value;
            }
        }
        fill_attendance(id, sub_id);
        hide_btn(id);
    }
    else{
        alert("Select atleast one subject !!!");	
    }
{% else %}

*/
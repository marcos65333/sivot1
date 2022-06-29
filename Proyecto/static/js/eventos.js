var eventcheck = document.querySelector('input[name=checkbox]');
var button = document.getElementById('button');
var form = document.forms['form'];

button.disabled = true;

    eventcheck.addEventListener( 'change', function() {
    if(this.checked) {
        button.disabled = false
    } else {
        button.disabled = true 
    } });


document.getElementById("RegisterForm").reset();

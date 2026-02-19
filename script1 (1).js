function validateForm(){

let name = document.getElementById("name").value;
let prn = document.getElementById("prn").value;
let contact = document.getElementById("contact").value;
let email = document.getElementById("email").value;
let password = document.getElementById("password").value;

document.getElementById("nameErr").innerHTML="";
document.getElementById("PRNErr").innerHTML="";
document.getElementById("contactErr").innerHTML="";
document.getElementById("emailErr").innerHTML="";
document.getElementById("passErr").innerHTML="";

let valid = true;

if(name.length < 4){
    document.getElementById("nameErr").innerHTML="Minimum 4 characters";
    valid = false;
}

if(prn.length != 10 || isNaN(prn)){
    document.getElementById("PRNErr").innerHTML="Enter valid 10 digit number";
    valid = false;
}

if(contact.length != 10 || isNaN(contact)){
    document.getElementById("contactErr").innerHTML="Enter valid 10 digit number";
    valid = false;
}


if(email == ""){
    document.getElementById("emailErr").innerHTML="Email required";
    valid = false;
}

if(password.length < 6){
    document.getElementById("passErr").innerHTML="Minimum 6 characters";
    valid = false;
}

if(valid){
    alert("Form Submitted Successfully!");
    return true;
}else{
    alert("Fix errors!");
    return false;
}

}

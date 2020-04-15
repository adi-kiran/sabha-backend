function sendJSON(){ 
               
    full_name = document.getElementById("fname").value; 
    username = document.getElementById("uname").value; 
    password = document.getElementById("pwd").value; 
       
    let xhr = new XMLHttpRequest(); 
    let url = "http://localhost:5000/api/user/add"; 

    xhr.open("POST", url, true); 
    xhr.setRequestHeader("Content-Type", "application/json"); 
    xhr.onreadystatechange = function () { 
        if (this.readyState === 4 && this.status === 200) { 
            console.log(this.responseText);
            $('.toast').toast('show');
        }
        else{
            console.log(this.responseText);
        }
    }; 
    
    var data = JSON.stringify({ "full_name": full_name, "username": username , "password": password }); 
    xhr.send(data); 
} 
function login(){ 
    
    username = document.getElementById("uname"); 
    password = document.getElementById("pwd"); 
       
    // Creating a XHR object 
    let xhr = new XMLHttpRequest(); 
    let url = "localhost:5000/api/user/signin"; 

    // open a connection 
    xhr.open("POST", url, true); 

    // Set the request header i.e. which type of content you are sending 
    xhr.setRequestHeader("Content-Type", "application/json"); 

    // Create a state change callback 
    xhr.onreadystatechange = function () { 
        if (xhr.readyState === 4 && xhr.status === 200) { 

            // Do the necesssary action

        } 
    }; 

    // Converting JSON data to string 
    var data = JSON.stringify({"username": username.value , "password": password.value }); 

    // Sending data with the request 
    xhr.send(data); 
} 
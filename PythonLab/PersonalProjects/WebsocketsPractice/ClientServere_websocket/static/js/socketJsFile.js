var socket = null;
$(function() {
  socket = new WebSocket(`${websocket_protocol}://${base_url}/socketHandler`);
  socket.onopen = () => socket.send(JSON.stringify({"name":UserName}));

  socket.onmessage = function(message) {
    var data = JSON.parse(message.data);
    if (data['status'] === 'NewID'){
        $('#UserID')[0].innerText = data['ID'];
        UserId = data['ID'];
    }
    else if (data['status'] === 'Message'){
        var div = document.createElement("DIV");
        div.setAttribute("data-aos","fade-up");
        div.classList.add("message_box_container");
        if (data['UserId'] === UserId)
            div.classList.add("self");
        div.innerHTML = `<div class='message_box_header'><div class='header_label'>From:</div><div class='sender_name'>${data['UserName']}</div></div><div class='message_box_body'><p>${data['Content']}</p></div>`;
        $("#OutputMessages")[0].appendChild(div);
        window.scrollTo(0,document.body.scrollHeight);
    }
    else if(data['status'] === 'Login'){
        var OutUserName = data['UserName'];
        var OutUserStatus = data['StatusMessage'];
        var OutUserIcon = (OutUserStatus === 'sign_in')? `enter <i class="fas fa-sign-in-alt"></i>`:`left <i class="fas fa-sign-out-alt"></i>` ;
        var divStatus = document.createElement("DIV");
        divStatus.setAttribute("data-aos","fade-up");
        divStatus.classList.add("login_info_container");
        divStatus.classList.add(OutUserStatus);
        divStatus.innerHTML = `<div class="login_info_box"><div class="login_info_name">${OutUserName}</div><div class="login_info_status">${OutUserIcon}</div></div>`;
        $("#OutputMessages")[0].appendChild(divStatus);
        window.scrollTo(0,document.body.scrollHeight);
    }
  };
  $("form").submit(function(event) {
    var data = {"content" : $('#messageInput')[0].value};
    $('#messageInput')[0].value = "";
    socket.send(JSON.stringify(data));
    event.preventDefault();
  });
});
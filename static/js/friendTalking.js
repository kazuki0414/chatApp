$(document).ready(function(){

    debugger;

    var friendId = $('#friendId').val();
    var userId = $('#userId').val();

        $.ajax({
            url: '/getMessage/',
            data: {
                'friendId': friendId,
                'userId' : userId
            },
            dataType: 'json',
            success: function (data) {
                if (data.allmessage) {

                    list = JSON.parse(data.allmessage);

                    for(let i=0; i < list.talkmessage.length; i++){

                        if(list.talkmessage[i].touser == $('#friendId').val()){
                            $('.talkview').append($('<div>').append(list.talkmessage[i].message).attr('class', 'talkmyuserview'));
                        }
                        else{
                            $('.talkview').append($('<div>').append(list.talkmessage[i].message).attr('class', 'talkfriendview'));
                        }
                    }
                }
            }
        });


  
  
    //---------- This assigns an onclick event to each tab link("a" tag) and passes a parameter to the showHideTab() function
        
      $('#messagesubmit').click(function(e){

        var message = $('#id_username').val();
        var friendId = $('#friendId').val();
        var userId = $('#userId').val();

        // alert(message);

        $.ajax({
            url: '/messageSubmit/',
            data: {
                'message': message,
                'friendId': friendId,
                'userId' : userId
            },
            dataType: 'json',   
            success: function (data) {
                if (data.message) {

                     $('.talkfriendview').remove();
                     $('.talkmyuserview').remove();

                    list = JSON.parse(data.allmessage);

                    for(let i=0; i < list.talkmessage.length; i++){

                        if(list.talkmessage[i].touser == $('#friendId').val()){
                            $('.talkview').append($('<div>').append(list.talkmessage[i].message).attr('class', 'talkmyuserview'));
                        }
                        else{
                            $('.talkview').append($('<div>').append(list.talkmessage[i].message).attr('class', 'talkfriendview'));
                        }
                    }
                }
            }
        });
        
      });
      
     
  });//end ready
$(document).ready(function() {
  $('#game-form').submit(function(){
    $.ajax({
      type:$(this).attr('method'),
      url: $(this).attr('action'),
      data: $(this).serialize(),
      success: function(response){
        if (response.hasOwnProperty('game_name')){
          $('#url').html("<h5>" +
              "game " +
              response.game_name +
              " has been created, share it with this URL:</h5> <h5><a href=" +
              response.url +
              ">" +
              response.url +
              "</a></h5>")
        }
        else{
          alert(response)
        }
      },
      error: function(response){
        alert('something went wrong, please try again');
      }
    });
    return false;
  });
});

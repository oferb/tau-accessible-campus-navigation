// TODO(avital): Change to fetch: https://developers.google.com/web/updates/2015/03/introduction-to-fetch - DONE
// TODO(avital): Fix bug with prev that only second click works - DONE
// TODO: Load all jsons on page load
// TODO: Visualize location in geolocation.html (or create link to a map)
// TODO: Experiment with geolocation.html to see accuracy in practice. Note that there is high accuracy mode.

function getDataFromJason() {
  var choose_json = document.getElementById("roadSelector").selectedIndex;
  var file_name =  `/roads/${choose_json}.json`;
  fetch(file_name)
    .then(response => response.json())
    .then(mydata => data = mydata)
    .catch(error => console.log("Opps, Something went wrong!", err));

  /*
  var rawFile = new XMLHttpRequest();
  rawFile.overrideMimeType("application/json");
  rawFile.open("GET", file_name, true);
  rawFile.onreadystatechange = function() {
      if (rawFile.readyState === 4 && rawFile.status == "200") {
          callback(rawFile.responseText);
      }
  }
  rawFile.send(null);
  */
}

var curr_index = 0;
var next_step_instruction = document.getElementById('step_view');
var data;
/*TODO:
document.addEventListener('DOMContentLoaded', (event) => {
    getDataFromJason();
});
*/
function refresh_steps() {
  var data = getDataFromJason();

  /* Brian Experiment to add google map on page
  curr_index = 0;
  var colors = [];
    function initialize() {
      var map = new google.maps.Map(
        document.getElementById("map_canvas"), {
          zoom: 13,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        });
      var bounds = new google.maps.LatLngBounds();
      map.fitBounds(bounds);
    }
    google.maps.event.addDomListener(window, "load", initialize);
  */
  /*
    readTextFile(function(text){
     data = JSON.parse(text);
    });
  */
  next_step_instruction.innerHTML = data[curr_index % data.length].text;
}

function move_to_next_step() {
  curr_index += 1;
  next_step_instruction.innerHTML = data[curr_index % data.length].text;
}

function move_to_previous_step() {
  curr_index -= 1;
  if (curr_index < 0) {
    curr_index += data.length;
  }
  next_step_instruction.innerHTML = data[curr_index % data.length].text;
}
//Avital : tmp
function check_git(){
  //check if git works
}

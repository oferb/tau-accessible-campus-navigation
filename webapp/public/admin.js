// TODO: Experiment with geolocation.html to see accuracy in practice. Note that there is high accuracy mode.
// TODO(ram): Add summaries to jsons and then show them in summary page
// TODO(sharon): Add הגעת ליעד to the end of every route.
// TODO: Ask Zhana if back navigation is fine or we need back buttons
// -done-TODO(reem, guy, daniel): Add url for each page using the History API: https://developer.mozilla.org/en-US/docs/Web/API/History_API history.pushState(0, "title 1", "/navigation4")
// TODO(guy, reem): Load correct page based on url
// TODO(bar): Do we need mockJson1.json and road1.json?
// TODO(adi) - done: Add numbering to אבן דרך
// TODO(ram): Align buttons to bottom in summary page
// TODO: playpause should focus on current location
// TODO(): lan, lon is switched in jsons: 0, 6, 17, 19
// TODO(): Design logo for TAU Walks and add it to the main page
// TODO: Change google maps to dark mode design
// TODO(): Change the textarea element in Review Page to seperate blocks per milestone (all blocks are one after the other by order) 

let admin_console_page;
let all_paths_map_page;
let current_json;
let curr_index = 0;
let data;
let coords = [];

window.onload = function(){
  all_paths_map_page = document.getElementById("all_paths_map_page");
  admin_console_page = document.getElementById("admin_console_page");
};

let from_list=[];
let to_list=[];
let jsons =[];
fetch("/jsons")
  .then(response =>  (response.json()))
  .then(json => get_navigate_json_list(json))
  .then(navigate_lists=>update_from_to_list(navigate_lists))
  .then(response => populate_select("from", from_list))
  .then(response => populate_select("to", to_list))
  
function populate_select(target, source_list){
  select = document.getElementById(target);
  for (var i = 0; i < source_list.length; i++){
      var opt = document.createElement('option');
      opt.value = source_list[i];
      opt.innerHTML = source_list[i];
      select.appendChild(opt);
  }
  select.value = source_list[0];
}

function update_from_to_list(navigate_lists){
    from_list.push(...Object.keys(navigate_lists[0]));
    to_list.push(...Object.keys(navigate_lists[0]));
    var tmp = from_list[from_list.length-1];
    from_list[from_list.length-1] = from_list[0];
    from_list[0] = tmp;
}

function get_navigate_json_list(json_list){
  let to_dictionary = {};
  from_dictionary = get_direction_dictionary(json_list, "from");
  return [from_dictionary, to_dictionary];
}

function get_direction_dictionary(json_list, direction){
  let direction_dictionary = {};
  jsons.push(...json_list);
  for (json of json_list) { 
    if (json[direction] in direction_dictionary){
      direction_dictionary[json[direction]].push(json)
    } else {
       direction_dictionary[json[direction]] = [json]
    }
  }
  return direction_dictionary;
}

function goto_all_paths_map_page(){
  hide_all_pages();
  all_paths_map_page.hidden = false;
  var mymap;
  mymap = L.map('map')
  L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoiYnJpYW5nMTMiLCJhIjoiY2thYjliMjBiMG4yczJ6b2lodmszdjByayJ9.CpAh_9lzEsl9WW1Lo_zneg'
  }).addTo(mymap);
  mymap.locate({setView: true, maxZoom: 16});
  var marker;
  for (json of jsons.slice(0,2)){
    data = json["data"];
    for (index = 0; index < data.length; index++) { 
    current_step = data[index];
    next_step = data[index+1];
    coords.push(new L.LatLng(parseFloat(current_step.lat), parseFloat(current_step.lon)));
    // coords.push([parseFloat(current_step.lat), parseFloat(current_step.lon)]);
    marker = L.marker([current_step.lat, current_step.lon]).addTo(mymap);
    marker.bindPopup(current_step.text);
    }
    var line = new L.polyline(coords).addTo(mymap);  
  }
}


function hide_all_pages() {
  admin_console_page.hidden = true;
  all_paths_map_page.hidden = true;
}

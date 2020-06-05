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

let path_selector;
let path_navigator;
let path_review_page;
let current_json;
let curr_index = 0;
let data;
let next_step_instruction;
let milestone_title;
let milestone_index = 1;

window.onload = function(){
  path_selector = document.getElementById("path_selector_page");
  path_navigator = document.getElementById("path_navigator_page");
  path_review_page = document.getElementById("path_review_page");
  next_step_instruction = document.getElementById('step_view');
  milestone_title = document.getElementById('milestone-title');
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

function get_navigate_json_list(json_list){
  let to_dictionary = {};

  from_dictionary = get_direction_dictionary(json_list, "from");
  return [from_dictionary, to_dictionary];
}

function update_from_to_list(navigate_lists){
    from_list.push(...Object.keys(navigate_lists[0]));
    to_list.push(...Object.keys(navigate_lists[0]));
    var tmp = from_list[from_list.length-1];
    from_list[from_list.length-1] = from_list[0];
    from_list[0] = tmp;
    
}


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


function goto_nav_page(){
  from_place = document.getElementById("from").value;
  to_place = document.getElementById("to").value;
  history.pushState(0, "","/nav_page");
  for (json of jsons){
    if(from_place === to_place){
      return;
    }
  }

  goto_path_navigator();
  var mymap;
  data = get_path_json()["data"];
  mymap = L.map('map')

  L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    maxZoom: 18,
    id: 'mapbox/streets-v11',
    tileSize: 512,
    zoomOffset: -1,
    accessToken: 'pk.eyJ1IjoiYnJpYW5nMTMiLCJhIjoiY2thYjliMjBiMG4yczJ6b2lodmszdjByayJ9.CpAh_9lzEsl9WW1Lo_zneg'
  }).addTo(mymap);

      // placeholders for the L.marker and L.circle representing user's current position and accuracy    
    var current_position, current_accuracy;

    function on_location_found(e) {
      // if position defined, then remove the existing position marker and accuracy circle from the map
      if (current_position) {
          mymap.removeLayer(current_position);
          mymap.removeLayer(current_accuracy);
      }

      var radius = e.accuracy / 2;
      current_position = L.marker(e.latlng).addTo(mymap)
        .bindPopup("You are within " + radius + " meters from this point").openPopup();

      current_accuracy = L.circle(e.latlng, radius).addTo(mymap);
    }

    function on_location_error(e) {
      alert(e.message);
    }

    mymap.on('locationfound', on_location_found);
    mymap.on('locationerror', on_location_error);

    // wrap mymap.locate in a function    
    function locate() {
      mymap.locate({setView: true, maxZoom: 16});
    }
    locate();
    // call locate every 20 seconds... forever
    setInterval(locate, 20000);
    
  var marker;
  
  for (index = 0; index < data.length-1; index++) { 
    console.log("index: " + index);
    current_step = data[index];
    next_step = data[index+1];
    L.polygon([[current_step.lat, current_step.lon], [next_step.lat, next_step.lon] ]).addTo(mymap);
    marker = L.marker([current_step.lat, current_step.lon]).addTo(mymap);
    marker.bindPopup(current_step.text);
  }
  marker = L.marker([data[data.length-1].lat, data[data.length-1].lon]).addTo(mymap);
  marker.bindPopup(data[data.length-1].text);
  next_step_instruction.innerHTML = data[curr_index % data.length].text;
  // if((data[data.length-1].lat == current_step.lat)&&(data[data.length-1].lon == current_step.lon)){
  //    next_step_instruction.innerHTML = 'הגעת ליעד';
  // }
  var milestone_counter_elem = document.createTextNode(" " + milestone_index);
  milestone_title.appendChild(milestone_counter_elem);
}


function goto_review_page() {
  history.pushState(0, "","/review_page");
  goto_path_review_page();
}

function get_path_json(){
  from_place = document.getElementById("from").value;
  to_place = document.getElementById("to").value;
  for (json of jsons){
    if(json["from"] === from_place && json["to"] === to_place){
      return json;
    }
  }
}

function hide_all_pages() {
  path_navigator.hidden = true;
  path_selector.hidden = true;
  path_review_page.hidden = true;
}

function goto_path_selector(){
  history.pushState(0, "","/path_selector");
  hide_all_pages();
  path_selector.hidden = false;
}

function goto_path_navigator(){
  hide_all_pages();
  path_navigator.hidden = false;
}

function goto_path_review_page(){
  hide_all_pages();
  path_review_page.hidden = false;
  on_screen_info();
}

function add_milestone_counter(index) {
  if (index > 0 && index < data.length){   
    var milestone_counter_elem = document.createTextNode(" " + index);
    milestone_title.replaceChild(milestone_counter_elem, milestone_title.childNodes[1]);
  }
}

function move_to_next_step() {
  if (curr_index < data.length-1) {
    curr_index += 1;
  }
  history.pushState(0, "","/path_nav/nav"+curr_index.toString());
  next_step_instruction.innerHTML = data[curr_index % data.length].text;
  milestone_index += 1;
  add_milestone_counter(milestone_index);
}

function move_to_previous_step() {
  if (curr_index > 0) {
    curr_index -= 1;
  }
  history.pushState(0, "","/path_nav/nav"+curr_index.toString());
  next_step_instruction.innerHTML = data[curr_index % data.length].text;
  milestone_index -= 1;
  add_milestone_counter(milestone_index);
}

function on_screen_info(){
  data = get_path_json();
  let text = '';
  for(let i = 0; i < data.data.length; i++){
    text = `${text} ${data.data[i].text}`;
    if(i != data.data.length - 1)
      text += '\n';
  }
  document.getElementById("textarea").value = text;
}

// TODO(guy, reem): Load correct page based on url



let path_selector;
let path_nav_page;
let data;
let path_data_navigator = [];
var building_to_name = {
  "main_gate": "שער ראשי",
  "gilman": "גילמן",
  "dan_david": "דן דוד",
};

window.onload = function(){
  path_selector = document.getElementById("path_selector_page");
  path_nav_page = document.getElementById("path_nav_page");
};


let jsons =[];
fetch("/jsons")
  .then(response =>  (response.json()))
  .then((response) => {
    jsons = response;
    populate_select("to"); 
    populate_select("from");
  });
  
// function get_direction_dictionary(json_list, direction){
//   let direction_dictionary = {};
//   jsons.push(...json_list);
  
//   for (json of json_list) { 
//     if (json[direction] in direction_dictionary){
//       direction_dictionary[json[direction]].push(json)
//     } else {
//        direction_dictionary[json[direction]] = [json]
//     }
//   }
//   return direction_dictionary;
// }

// function get_navigate_json_list(json_list){
//   from_dictionary = get_direction_dictionary(json_list, "from");
//   return from_dictionary;
// }

function populate_select(target){
  let target_list=Object.keys(building_to_name);
  select = document.getElementById(target);
  


  for (var i = 0; i < target_list.length; i++){
      var opt = document.createElement('option');
      opt.value = target_list[i];
      console.log(target);
      console.log(i);
      if (target === "to" && i === 1){
        console.log("Hello");
        opt.selected = true;
      }      
      opt.innerHTML = building_to_name[target_list[i]];
      select.appendChild(opt);
  }
  // select.value = target_list[0];  
}

function goto_nav_page() {
  from_place = document.getElementById("from").value;
  to_place = document.getElementById("to").value;
  for (json of jsons){
    if(from_place === to_place){
      return;
    }
  }
  history.pushState(0, "","/nav_page");
  hide_all_pages();
  path_nav_page.hidden = false;
  on_screen_info();
}

function get_path_json(){
  from_place = document.getElementById("from").value;
  to_place = document.getElementById("to").value;
  for (json of jsons){
    if(json["from_id"] === from_place && json["to_id"] === to_place){
      return json;
    }
  }
}

function hide_all_pages() {
  path_selector.hidden = true;
  path_nav_page.hidden = true;
}

function goto_path_selector(){
  history.pushState(0, "","/");
  hide_all_pages();
  path_selector.hidden = false;
}

function on_screen_info(){
  data = get_path_json();
  to_word_hebrew = " אל "
  document.getElementById("path_title").innerHTML = data["from"] + to_word_hebrew + data["to"]
  let parent = document.getElementById("steps_parent");
  parent.querySelectorAll('*').forEach(n => n.id!="p1" ? n.remove() : void(0));
  let child = document.getElementById("p1");
  for (let i = 0; i < data.data.length; i++){
    let text = `${data.data[i].text}`;
    parent.insertBefore(getTextElement(text), child);
  }
  let text = "הִגַּעְתָּ לְיַעַד";
  parent.insertBefore(getTextElement(text), child);
}

function getTextElement(text){
  let div_element = document.createElement("div");
  let p_element = document.createElement("p");
  div_element.appendChild(p_element);
  div_element.classList.add("description");
  div_element.classList.add("milestone");
  p_element.style.fontSize = "calc(30px + 2.8vw)";
  p_element.display = "block";
  let node = document.createTextNode(text);
  p_element.appendChild(node);
  return div_element;
}

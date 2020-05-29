var el = document.querySelector('input[type="text"]');

let Keyboard = window.SimpleKeyboard.default;

let myKeyboard = new Keyboard({
  onChange: input => onChange(input),
  onKeyPress: button => onKeyPress(button),
  mergeDisplay: true,
  // preventMouseDownDefault: true,
  layoutName: "default",
  layout: {
    default: [
      "q w e r t y u i o p",
      "a s d f g h j k l",
      "{shift} z x c v b n m {backspace}",
      "{numbers} {space} {ent}"
    ],
    shift: [
      "Q W E R T Y U I O P",
      "A S D F G H J K L",
      "{shift} Z X C V B N M {backspace}",
      "{numbers} {space} {ent}"
    ],
    numbers: ["1 2 3", "4 5 6", "7 8 9", "{abc} 0 {backspace}"]
  },
  display: {
    "{numbers}": "123",
    "{ent}": "return",
    "{escape}": "esc ⎋",
    "{tab}": "tab ⇥",
    // "{backspace}": "⌫",
    "{backspace}": "del",
    "{capslock}": "caps lock ⇪",
    // "{shift}": "⇧",
    "{shift}": "shift",
    "{controlleft}": "ctrl ⌃",
    "{controlright}": "ctrl ⌃",
    "{altleft}": "alt ⌥",
    "{altright}": "alt ⌥",
    "{metaleft}": "cmd ⌘",
    "{metaright}": "cmd ⌘",
    "{abc}": "ABC"
  }
});

function handleShift() {
  let currentLayout = myKeyboard.options.layoutName;
  let shiftToggle = currentLayout === "default" ? "shift" : "default";

  myKeyboard.setOptions({
    layoutName: shiftToggle
  });
}

function handleNumbers() {
  let currentLayout = myKeyboard.options.layoutName;
  let numbersToggle = currentLayout !== "numbers" ? "numbers" : "default";

  myKeyboard.setOptions({
    layoutName: numbersToggle
  });
}

function onChange(input) {
  document.querySelector(".mapboxgl-ctrl-geocoder--input").value = input;
  console.log("Input changed", input);
  triggerEvent(el, 'keydown');

  // autoCompleteListenerX(input)
}

function onKeyPress(button) {
  console.log("Button pressed", button);
  if (button === "{shift}" || button === "{lock}") handleShift();
  if (button === "{numbers}" || button === "{abc}") handleNumbers();

  if(button == "{ent}"){
    console.log("Enter Pressed.");
    closeKeyboard();
  }
}

let keyboardStatus = 'closed';
function openKeyboard() {
  if(keyboardStatus != 'closed'){
    return;
}
myKeyboard.clearInput();
sKeyboard.style.display = 'block';
keyboardStatus = 'open';
}
function closeKeyboard() {
    if(keyboardStatus != 'open'){
        return;
    }
    myKeyboard.clearInput();
    sKeyboard.style.display = 'none';
    keyboardStatus = 'closed';
    // closeSearchBox();
    // clearOldSuggestions();
}

// let searchBar = 'closed';
function initKeyboardListener(){
  document.getElementsByClassName('mapboxgl-ctrl-geocoder')[0].addEventListener('transitionstart', function(){
    let status=true;
    status = document.getElementsByClassName('mapboxgl-ctrl-geocoder')[0].classList.contains('mapboxgl-ctrl-geocoder--collapsed');
    if(status == true){
      closeKeyboard();
    }
    else {
      openKeyboard();
    }
  });
}
// document.getElementsByClassName('mapboxgl-ctrl-geocoder')[0].addEventListener('transitionstart', function(){
//   let status=true;
//   status = document.getElementsByClassName('mapboxgl-ctrl-geocoder')[0].classList.contains('mapboxgl-ctrl-geocoder--collapsed');
//   if(status == true){
//     closeKeyboard();
//   }
//   else {
//     openKeyboard();
//   }
// });

// document.getElementsByClassName('mapboxgl-ctrl-geocoder--input')[0].addEventListener('blur', function(){
//   closeKeyboard();
// })

function triggerEvent(el, type){
  if ('createEvent' in document) {
       // modern browsers, IE9+
       var e = document.createEvent('HTMLEvents');
       e.initEvent(type, false, true);
       el.dispatchEvent(e);
   } else {
       // IE 8
       var e = document.createEventObject();
       e.eventType = type;
       el.fireEvent('on'+e.eventType, e);
   }
}


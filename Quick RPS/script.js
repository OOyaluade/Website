// function for picking all html emements to listen to 

function possibleChoices() {
    const choices = document.querySelectorAll('.selection button')
    return choices
}

// functionm for randomly selecting computers choice 
function compChoiceSelector(func) {
    const possibleOptions = func()
    const selectedchoice = Math.floor(Math.random() * possibleOptions.length);
    return possibleOptions[selectedchoice].innerHTML
}

// function to listen to user selection

function userChoiceSelector(func){
    const userOption =  func()
    userOption.forEach(choices => {
        choices.addEventListener('click', getClicked)
        
    });
}

// function to determin if computer choice and user choice match
function getClicked(event) {
    const userClickedChoice = event.target.textContent || event.target.value;
    
    switch (userClickedChoice) {
        case compChoice:
            console.log('correct');
            document.getElementById('message').innerHTML=`Your guessed right: ${userClickedChoice}`
            break;
        default:
            console.log('incorrect');

            document.getElementById('message').innerHTML=`Your guessed wrong: The correct answer is ${compChoice}`

        }

    }




const compChoice = compChoiceSelector(possibleChoices);
console.log(`This is the ${compChoice}`)
const userChoice = userChoiceSelector(possibleChoices);



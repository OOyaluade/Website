



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
var compChoice = compChoiceSelector(possibleChoices);
console.log(`Comp selected: ${compChoice}`)
let lives = 5;

function getClicked(event) {
    const userClickedChoice = event.target.textContent || event.target.value;

    
    switch (userClickedChoice) {
        case compChoice:
            console.log('correct');
            document.getElementById('message').innerHTML=`Your guessed right: ${userClickedChoice}`
            gameContinue(0);
            break;
            default:
                console.log('incorrect');
                
                document.getElementById('message').innerHTML=`Your guessed wrong: The correct answer is ${compChoice}`
                lives -= 1;
                gameContinue(lives);
                break;
            }
    document.getElementById('attempts').innerHTML=`Lives left: ${lives}`
    // console.log(`Comp selected: ${compChoice}`)
}




function gameContinue(lives ){
    if (lives <= 0 )  {
        const userOption = possibleChoices();
        userOption.forEach(choice => {
            choice.disabled = true;
        })
        
        
        document.getElementById('message').innerHTML = 'Game Over! No lives left.';
        
        
    }
    else{
        
        compChoice = compChoiceSelector(possibleChoices);
        console.log(`Comp selected: ${compChoice}`)
    };
}

userChoiceSelector(possibleChoices);
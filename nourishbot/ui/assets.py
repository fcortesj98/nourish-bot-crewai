"""Static UI assets (CSS, JavaScript, copy and example inputs) for the Gradio app."""

from __future__ import annotations

from nourishbot.settings import EXAMPLES_DIR

CSS = """
.title {
    font-size: 1.5em !important;
    text-align: center !important;
    color: #FFD700;
}

.text {
    text-align: center;
}
"""

# Typewriter-style welcome banner injected at page load.
JS = """
function createGradioAnimation() {
    var container = document.createElement('div');
    container.id = 'gradio-animation';
    container.style.fontSize = '2em';
    container.style.fontWeight = 'bold';
    container.style.textAlign = 'center';
    container.style.marginBottom = '20px';
    container.style.color = '#eba93f';

    var text = 'Welcome to your AI NourishBot!';
    for (var i = 0; i < text.length; i++) {
        (function(i){
            setTimeout(function(){
                var letter = document.createElement('span');
                letter.style.opacity = '0';
                letter.style.transition = 'opacity 0.1s';
                letter.innerText = text[i];

                container.appendChild(letter);

                setTimeout(function() {
                    letter.style.opacity = '0.9';
                }, 50);
            }, i * 250);
        })(i);
    }

    var gradioContainer = document.querySelector('.gradio-container');
    gradioContainer.insertBefore(container, gradioContainer.firstChild);

    return 'Animation created';
}
"""

INSTRUCTIONS = [
    "Upload an image of your fridge content, enter your dietary restriction (if you have any!) "
    "and select a workflow type 'recipe' then click 'Analyze' to get recipe ideas.",
    "Upload an image of a complete dish, leave dietary restriction blank and select a workflow "
    "type 'analysis' then click 'Analyze' to get nutritional insights.",
    "You can also select one of the examples provided to autofill the input sections and click "
    "'Analyze' right away!",
]

EXAMPLES = [
    [str(EXAMPLES_DIR / "food-1.jpg"), "vegan", "recipe"],
    [str(EXAMPLES_DIR / "food-2.jpg"), "", "analysis"],
    [str(EXAMPLES_DIR / "food-3.jpg"), "keto", "recipe"],
    [str(EXAMPLES_DIR / "food-4.jpg"), "", "analysis"],
]

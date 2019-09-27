document.addEventListener('DOMContentLoaded', function(event) {
    const button = document.getElementById('randomize');
    const cards = document.getElementById('cards');
    const url = 'https://nv1gwscvf9.execute-api.us-west-2.amazonaws.com/default/DominionRandomizer/'

    button.addEventListener('click', (event) => {
        if (cards.children.length > 0) {
            cards.children[0].remove()
        }

        fetch(url).then((response) => response.json()).then((data) => {
            let ul = document.createElement('ul');
            for (var i = 0; i < data.length; i++) {
                let li = document.createElement('li');
                let text = document.createTextNode(data[i]);
                li.appendChild(text);
                ul.appendChild(li);
            }
            cards.appendChild(ul);
        })
    }, false);
});
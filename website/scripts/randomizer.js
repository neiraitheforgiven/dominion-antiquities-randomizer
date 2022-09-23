document.addEventListener("DOMContentLoaded", function (event) {
    const form = document.forms[0];
    const cards = document.getElementById("cards");
    const url =
        "https://nv1gwscvf9.execute-api.us-west-2.amazonaws.com/default/DominionRandomizer/";

    form.addEventListener(
        "submit",
        (event) => {
            event.preventDefault();
            const pyodide = globalThis.pyodide;
            const randomizer = globalThis.randomizer;

            if (cards.children.length > 0) {
                cards.children[0].remove();
            }

            var data = {
                sets: [],
                options: {},
            };

            for (var i = 0; i < form.sets.elements.length; i++) {
                let checkbox = form.sets.elements[i];

                if (checkbox.className == "set" && checkbox.checked) {
                    data.sets.push(checkbox.value);
                } else {
                    data.options[checkbox.name] = checkbox.checked;
                }
            }

            for (var i = 0; i < form.moreOptions.elements.length; i++) {
                let checkbox = form.moreOptions.elements[i];

                data.options[checkbox.name] = checkbox.checked;
            }

            let proxy = randomizer.RandomizeDominion(data.sets, data.options)
            let cardData = proxy.toJs();
            let ul = document.createElement("ul");
            for (var i = 0; i < cardData.length; i++) {
                let li = document.createElement("li");
                let text = document.createTextNode(cardData[i]);
                li.appendChild(text);
                ul.appendChild(li);
            }
            cards.appendChild(ul);
            cards.scrollIntoView({ behavior: "smooth" });
        },
        false
    );
});

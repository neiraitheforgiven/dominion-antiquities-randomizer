document.addEventListener("DOMContentLoaded", function (event) {
    const form = document.forms[0];
    const cards = document.getElementById("cards");
    const handleExtras = (i, cardData, extraElements) => {
        let h3 = document.createElement("h3");
        let headerText = document.createTextNode(cardData[i]);
        h3.appendChild(headerText);
        i++;

        let ul = document.createElement("ul");
        for (var j = i; j < cardData.length; j++) {
            let li = document.createElement("li");
            let text = document.createTextNode(cardData[j]);
            li.appendChild(text);
            ul.appendChild(li);
        }

        extraElements.push(h3);
        extraElements.push(ul);
    };

    form.addEventListener(
        "submit",
        async (event) => {
            event.preventDefault();
            const pyodide = globalThis.pyodide;

            if (cards.children.length > 0) {
                for (var i = cards.children.length - 1; i >= 0; i--) {
                    cards.children[i].remove();
                }
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

            self.sets = data.sets;
            self.options = data.options;

            let proxy = await pyodide.runPythonAsync(`
                import randomizer
                from js import sets, options

                randomizer.RandomizeDominion(sets.to_py(), options.to_py())
            `);
            let cardData = proxy.toJs();
            let ul = document.createElement("ul");
            let extraElements = [];
            for (var i = 0; i < cardData.length; i++) {
                if (cardData[i] == "Extras:") {
                    handleExtras(i, cardData, extraElements);
                    break;
                }

                let li = document.createElement("li");
                let text = document.createTextNode(cardData[i]);
                li.appendChild(text);
                ul.appendChild(li);
            }
            cards.appendChild(ul);
            for (let element of extraElements) {
                cards.appendChild(element);
            }

            cards.scrollIntoView({ behavior: "smooth" });
            proxy.destroy();
        },
        false
    );
});

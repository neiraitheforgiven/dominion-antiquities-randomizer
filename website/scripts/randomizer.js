document.addEventListener("DOMContentLoaded", function (event) {
    const form = document.forms[0];
    const cards = document.getElementById("cards");
    const url =
        "https://nv1gwscvf9.execute-api.us-west-2.amazonaws.com/default/DominionRandomizer/";

    form.addEventListener(
        "submit",
        (event) => {
            event.preventDefault();

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
                let checkbox = form.sets.elements[i];

                data.options[checkbox.name] = checkbox.checked;
            }

            fetch(url, {
                method: "POST",
                mode: "cors",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(data),
            })
                .then((response) => response.json())
                .then((data) => {
                    let ul = document.createElement("ul");
                    for (var i = 0; i < data.length; i++) {
                        let li = document.createElement("li");
                        let text = document.createTextNode(data[i]);
                        li.appendChild(text);
                        ul.appendChild(li);
                    }
                    cards.appendChild(ul);
                    cards.scrollIntoView({ behavior: "smooth" });
                });
        },
        false
    );
});

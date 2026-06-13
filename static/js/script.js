let selectedCuisine = "";

document.querySelectorAll(".cuisine-btn").forEach(btn => {
    btn.addEventListener("click", () => {
        selectedCuisine = btn.innerText;

        document.querySelectorAll(".cuisine-btn")
            .forEach(b => b.classList.remove("selected"));

        btn.classList.add("selected");
    });
});

document.getElementById("generateBtn").addEventListener("click", async () => {

    const ingredients = document.getElementById("ingredients").value.trim();
    const result = document.getElementById("recipeResult");

    if (!ingredients || !selectedCuisine) {
        alert("Enter ingredients and select cuisine");
        return;
    }

    result.innerHTML = `<div class="loading-card">🍳 Generating recipe...</div>`;

    try {
        const res = await fetch("/generate-recipe", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                ingredients,
                style: selectedCuisine
            })
        });

        const data = await res.json();

        if (!data || !data.recipe) {
            throw new Error("Invalid response");
        }

        result.innerHTML = formatRecipe(data.recipe);

    } catch (err) {
        console.error(err);

        result.innerHTML = `
            <div class="error-card">
                ❌ Failed to generate recipe
            </div>
        `;
    }
});


function formatRecipe(text) {

    let clean = text
        .replace(/\*\*/g, "")
        .replace(/\*/g, "");

    return `
        <div class="recipe-container">

            ${clean
                .replace(/Recipe Name:/g, '<div class="heading recipe-name">🍽 Recipe Name</div>')
                .replace(/Preparation Time:/g, '<div class="heading prep-time">⏱ Preparation Time</div>')
                .replace(/Ingredients:/g, '<div class="heading ingredients">🧂 Ingredients</div>')
                .replace(/Steps:/g, '<div class="heading steps">👨‍🍳 Steps</div>')
                .replace(/Chef Tips:/g, '<div class="heading tips">💡 Chef Tips</div>')
                .replace(/Nutritional Info:/g, '<div class="heading nutrition">📊 Nutritional Info</div>')
                .replace(/\n/g, "<br>")
            }

        </div>
    `;
}
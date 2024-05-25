document.addEventListener('DOMContentLoaded', function () {
    let annotations = [];
    let selectedRange;

    document.getElementById('document').addEventListener('mouseup', function(e) {
        selectedRange = window.getSelection().getRangeAt(0);
        if (selectedRange && !selectedRange.collapsed) {
            const rect = selectedRange.getBoundingClientRect();
            showTagPrompt(rect.top + window.scrollY, rect.left + window.scrollX);
        }
    });

    document.getElementById('applyTagButton').addEventListener('click', applyTag);

    function showTagPrompt(top, left) {
        const tagPrompt = document.getElementById('tagPrompt');
        tagPrompt.style.top = `${top}px`;
        tagPrompt.style.left = `${left}px`;
        tagPrompt.style.display = 'block';
    }

    function applyTag() {
        const tagInput = document.getElementById('tagInput').value.trim();
        if (tagInput && selectedRange) {
            const span = document.createElement('span');
            span.classList.add('annotated');
            span.textContent = selectedRange.toString();
            span.style.backgroundColor = getColorForTag(tagInput); // Assign color based on tag

            selectedRange.deleteContents();
            selectedRange.insertNode(span);

            annotations.push({ text: span.textContent, class: tagInput });
            document.getElementById('tagPrompt').style.display = 'none';
            document.getElementById('tagInput').value = ''; // Reset input
        }
    }

    function getColorForTag(tag) {
        const colors = {
            "Tag1": "yellow",
            "Tag2": "lightgreen",
            "Tag3": "lightblue"
        };
        return colors[tag] || "lightgrey"; // Default color
    }

    function submitData() {
        let documentText = document.getElementById('document').innerText;
        fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                document: documentText,
                annotations: annotations,
                output_columns: ['column1', 'column2']  // Example columns
            })
        }).then(response => response.json())
        .then(data => {
            document.getElementById('output').innerText = JSON.stringify(data, null, 2);
        }).catch(error => console.error('Error:', error));
    }
});

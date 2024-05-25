document.addEventListener('DOMContentLoaded', function () {
    let annotations = [];
    let selectedRange;
    let colorMapping = {};

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
            if (!colorMapping[tagInput]) { // Assign a new color if the tag is new
                colorMapping[tagInput] = generateColor();
            }
            const span = document.createElement('span');
            span.classList.add('annotated');
            span.textContent = selectedRange.toString();
            span.style.backgroundColor = colorMapping[tagInput];

            selectedRange.deleteContents();
            selectedRange.insertNode(span);

            annotations.push({ text: span.textContent, class: tagInput });
            updateAnnotationsTable();
            document.getElementById('tagPrompt').style.display = 'none';
            document.getElementById('tagInput').value = ''; // Reset input
        }
    }

    function getColorForTag(tag) {
        return colorMapping[tag] || generateColor(); // Return existing or generate a new color
    }

    function generateColor() {
        return '#' + Math.floor(Math.random()*16777215).toString(16); // Generate a random hex color
    }

    function updateAnnotationsTable() {
        const table = document.getElementById('annotationsTable');
        table.innerHTML = '<tr><th>Tag</th><th>Text</th></tr>'; // Reset table and add headers
        annotations.forEach(annot => {
            const row = table.insertRow();
            const cell1 = row.insertCell(0);
            const cell2 = row.insertCell(1);
            cell1.innerHTML = `<span style="background-color: ${colorMapping[annot.class]}">${annot.class}</span>`;
            cell2.textContent = annot.text;
        });
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
                output_columns: ['column1', 'column2']
            })
        }).then(response => response.json())
        .then(data => {
            document.getElementById('output').innerText = JSON.stringify(data, null, 2);
        }).catch(error => console.error('Error:', error));
    }
});

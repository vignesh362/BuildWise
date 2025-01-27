const modal = document.getElementById("modal");
const textForm = document.getElementById("text-form");
const imageForm = document.getElementById("image-form");
const chooseSectionType = document.getElementById("choose-section-type");

// Show modal
document.getElementById("add-section").addEventListener("click", () => {
    modal.classList.remove("hidden");
    chooseSectionType.classList.remove("hidden");
    textForm.classList.add("hidden");
    imageForm.classList.add("hidden");
});

// Close modal
document.getElementById("close-modal").addEventListener("click", () => {
    modal.classList.add("hidden");
    chooseSectionType.classList.remove("hidden");
    textForm.classList.add("hidden");
    imageForm.classList.add("hidden");
});

// Show text form
document.getElementById("text-section-button").addEventListener("click", () => {
    chooseSectionType.classList.add("hidden");
    textForm.classList.remove("hidden");
});

// Show image form
document.getElementById("image-section-button").addEventListener("click", () => {
    chooseSectionType.classList.add("hidden");
    imageForm.classList.remove("hidden");
});

// Save text section
document.getElementById("save-text").addEventListener("click", () => {
    const title = document.getElementById("text-heading").value;
    const content = document.getElementById("text-content").value;
    if (title && content) {
        addSection("text", title, content);
        modal.classList.add("hidden");
    }
});

// Save image section
document.getElementById("save-image").addEventListener("click", () => {
    const title = document.getElementById("image-name").value;
    const url = document.getElementById("image-url").value;
    if (title && url) {
        addSection("image", title, url);
        modal.classList.add("hidden");
    }
});

// Add section to page
function addSection(type, title, content) {
    const sectionsContainer = document.getElementById("sections-container");
    const sidebarList = document.getElementById("sidebar-list");

    const section = document.createElement("div");
    section.classList.add("section");

    if (type === "text") {
        section.innerHTML = `<h2>${title}</h2><p>${content}</p>`;
    } else {
        section.innerHTML = `<h2>${title}</h2><img src="${content}" alt="${title}" style="max-width: 100%; border-radius: 8px;">`;
    }

    sectionsContainer.appendChild(section);

    // Add section to sidebar
    const li = document.createElement("li");
    li.textContent = title;
    sidebarList.appendChild(li);
}
// Include jsPDF for PDF generation
document.getElementById("download-pdf").addEventListener("click", () => {
    const { jsPDF } = window.jspdf;

    // Initialize jsPDF
    const doc = new jsPDF();

    // Get the content of the document editor excluding the sidebar
    const editorContent = document.querySelector(".document-editor");

    // Use html2canvas to capture the editor content
    html2canvas(editorContent, {
        scale: 2, // Higher scale for better resolution
        useCORS: true, // Allow cross-origin images
    }).then((canvas) => {
        // Convert canvas to image data
        const imgData = canvas.toDataURL("image/png");

        // Add image to PDF
        const imgWidth = 190; // Width of the PDF page (A4 size)
        const imgHeight = (canvas.height * imgWidth) / canvas.width; // Maintain aspect ratio
        doc.addImage(imgData, "PNG", 10, 10, imgWidth, imgHeight);

        // Save the PDF
        doc.save("Document.pdf");
    }).catch((error) => {
        console.error("Error generating PDF:", error);
    });
});
html2canvas(editorContent, {
    scale: 2, // Higher scale for better resolution
    useCORS: true, // Attempt to use CORS if possible
    allowTaint: true, // Allow "tainted" images
}).then((canvas) => {
    const imgData = canvas.toDataURL("image/png");
    const imgWidth = 190;
    const imgHeight = (canvas.height * imgWidth) / canvas.width;
    doc.addImage(imgData, "PNG", 10, 10, imgWidth, imgHeight);
    doc.save("Document.pdf");
}).catch((error) => {
    console.error("Error generating PDF:", error);
});
// Dark mode toggle
const darkModeToggle = document.getElementById("dark-mode-toggle");

darkModeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
    console.log("Dark mode toggled");
});
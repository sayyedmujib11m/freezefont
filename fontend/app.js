const API_BASE = window.FREEZEFONT_API_URL || "";

const dropzone = document.getElementById("dropzone");
const fileInput = document.getElementById("fontFile");
const fileName = document.getElementById("fileName");
const convertBtn = document.getElementById("convertBtn");
const statusText = document.getElementById("status");
const spinner = document.getElementById("spinner");
const infoBox = document.getElementById("infoBox");
const fontInfo = document.getElementById("fontInfo");
const instancePill = document.getElementById("instancePill");
const stylePicker = document.getElementById("stylePicker");

let inspectedFont = null;

function setStatus(message, type = ""){
    statusText.textContent = message;
    statusText.className = `status ${type}`.trim();
}

function setLoading(isLoading, message){
    spinner.style.display = isLoading ? "block" : "none";
    convertBtn.disabled = isLoading || !inspectedFont;

    if(message){
        setStatus(message);
    }
}

function escapeHtml(value){
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function selectedMode(){
    return document.querySelector('input[name="mode"]:checked').value;
}

function selectedStyles(){
    return [...document.querySelectorAll('input[name="styles"]:checked')]
        .map(input => input.value);
}

function updateStylePickerVisibility(){
    stylePicker.style.display = selectedMode() === "custom" ? "block" : "none";
}

function renderFontInfo(data){
    const axes = data.axes || [];
    const instances = data.instances || [];
    const commonStyles = data.common_styles || [];

    instancePill.textContent = `${instances.length} style${instances.length === 1 ? "" : "s"}`;

    const axisMarkup = axes.length
        ? axes.map(axis => `
            <div class="axis">
                <small>${escapeHtml(axis.tag)}</small>
                <strong>${escapeHtml(axis.min)} → ${escapeHtml(axis.max)}</strong>
                <small>Default: ${escapeHtml(axis.default)}</small>
            </div>
        `).join("")
        : '<div class="styleItem">No variable axes found.</div>';

    const sampleMarkup = instances.slice(0, 12).map(instance => `
        <div class="styleItem">${escapeHtml(instance.name)}</div>
    `).join("");

    fontInfo.innerHTML = `
        <div class="summaryGrid">
            <div class="summaryCard">
                <small>Family</small>
                <strong>${escapeHtml(data.family_name || "Unknown")}</strong>
            </div>
            <div class="summaryCard">
                <small>Recommended styles</small>
                <strong>${commonStyles.length || instances.length}</strong>
            </div>
        </div>

        <p class="blockTitle">Axes</p>
        <div class="axisGrid">${axisMarkup}</div>

        <p class="blockTitle">Named instances</p>
        <div class="stylesGrid">
            ${sampleMarkup}
            ${instances.length > 12 ? '<div class="styleItem">…and more</div>' : ""}
        </div>
    `;

    const pickerItems = instances.map((instance, index) => {
        const checked = commonStyles.some(style => style.name === instance.name) || index === 0;

        return `
            <label class="styleItem checkItem">
                <input type="checkbox" name="styles" value="${escapeHtml(instance.name)}" ${checked ? "checked" : ""}>
                <span>${escapeHtml(instance.name)}</span>
            </label>
        `;
    }).join("");

    stylePicker.innerHTML = `
        <p class="blockTitle">Choose exact styles</p>
        <div class="stylesGrid">${pickerItems}</div>
    `;

    infoBox.style.display = "block";
    updateStylePickerVisibility();
}

async function postFont(endpoint){
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);

    const response = await fetch(`${API_BASE}${endpoint}`, {
        method:"POST",
        body:formData,
    });

    if(!response.ok){
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || "Request failed");
    }

    return response;
}

async function inspectSelectedFont(){
    if(fileInput.files.length === 0){
        return;
    }

    inspectedFont = null;
    convertBtn.disabled = true;
    infoBox.style.display = "none";
    setLoading(true, "Inspecting font...");

    try{
        const response = await postFont("/inspect");
        const data = await response.json();

        if(!data.is_variable){
            setStatus("This file is not a variable font.", "error");
            setLoading(false);
            convertBtn.disabled = true;
            return;
        }

        inspectedFont = data;
        renderFontInfo(data);
        setStatus("Font inspected. Choose a mode and convert.", "success");
        convertBtn.disabled = false;
    }
    catch(error){
        console.error(error);
        setStatus(error.message || "Could not inspect this font.", "error");
        setLoading(false);
        convertBtn.disabled = true;
    }
    finally{
        spinner.style.display = "none";
    }
}

function handleFiles(files){
    if(!files.length){
        return;
    }

    fileInput.files = files;
    fileName.textContent = files[0].name;
    inspectSelectedFont();
}

dropzone.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", () => handleFiles(fileInput.files));

for(const eventName of ["dragenter", "dragover"]){
    dropzone.addEventListener(eventName, event => {
        event.preventDefault();
        dropzone.classList.add("dragover");
    });
}

for(const eventName of ["dragleave", "drop"]){
    dropzone.addEventListener(eventName, event => {
        event.preventDefault();
        dropzone.classList.remove("dragover");
    });
}

dropzone.addEventListener("drop", event => handleFiles(event.dataTransfer.files));

document.querySelectorAll('input[name="mode"]').forEach(input => {
    input.addEventListener("change", updateStylePickerVisibility);
});

convertBtn.addEventListener("click", async () => {
    if(fileInput.files.length === 0){
        setStatus("Please select a font first.", "error");
        return;
    }

    const mode = selectedMode();
    const styles = mode === "custom" ? selectedStyles() : [];

    if(mode === "custom" && styles.length === 0){
        setStatus("Choose at least one style for custom conversion.", "error");
        return;
    }

    setLoading(true, "Converting font...");

    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    formData.append("mode", mode === "custom" ? "selected" : mode);
    formData.append("selected_styles", JSON.stringify(styles));

    try{
        const response = await fetch(`${API_BASE}/upload`, {
            method:"POST",
            body:formData,
        });

        if(!response.ok){
            const error = await response.json().catch(() => ({}));
            throw new Error(error.detail || "Conversion failed");
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        const disposition = response.headers.get("content-disposition") || "";
        const match = disposition.match(/filename="?([^";]+)"?/i);

        a.href = url;
        a.download = match?.[1] || "FreezeFont.zip";
        document.body.appendChild(a);
        a.click();
        a.remove();
        window.URL.revokeObjectURL(url);

        setStatus("Conversion complete. Your ZIP download has started.", "success");
    }
    catch(error){
        console.error(error);
        setStatus(error.message || "Conversion failed.", "error");
    }
    finally{
        setLoading(false);
    }
});

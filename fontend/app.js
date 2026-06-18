const dropzone =
document.getElementById("dropzone");

const fileInput =
document.getElementById("fontFile");

const fileName =
document.getElementById("fileName");

const convertBtn =
document.getElementById("convertBtn");

const statusText =
document.getElementById("status");

const spinner =
document.getElementById("spinner");

const infoBox =
document.getElementById("infoBox");

const fontInfo =
document.getElementById("fontInfo");

dropzone.addEventListener(
    "click",
    () => fileInput.click()
);

async function inspectSelectedFont(){

    if(fileInput.files.length === 0){
        return;
    }

    const formData =
    new FormData();

    formData.append(
        "file",
        fileInput.files[0]
    );

    const response =
    await fetch(
        "http://127.0.0.1:8000/inspect",
        {
            method:"POST",
            body:formData
        }
    );

    const data =
    await response.json();

    let html = "";

    html +=
    "<b>Font:</b> " +
    data.family_name +
    "<br><br>";

    html +=
    "<b>Instances:</b> " +
    data.instance_count +
    "<br><br>";

    html +=
    "<b>Axes:</b><br>";

    data.axes.forEach(axis => {

        html +=
        "<div class='axis'>" +
        axis.tag +
        " : " +
        axis.min +
        " → " +
        axis.max +
        "</div>";

    });

    html +=
    "<div class='styles'>";

    html +=
    "<b>Sample Styles</b><br>";

    data.instances
        .slice(0,10)
        .forEach(instance => {

        html +=
        "<div class='styleItem'>" +
        instance.name +
        "</div>";

    });

    if(data.instances.length > 10){

        html +=
        "<div class='styleItem'>...</div>";

    }

    html += "</div>";

    fontInfo.innerHTML =
    html;

    infoBox.style.display =
    "block";
}

fileInput.addEventListener(
    "change",
    () => {

        if(fileInput.files.length){

            fileName.textContent =
            fileInput.files[0].name;

            inspectSelectedFont();

        }

    }
);

dropzone.addEventListener(
    "dragover",
    e => {

        e.preventDefault();

        dropzone.classList.add(
            "dragover"
        );

    }
);

dropzone.addEventListener(
    "dragleave",
    () => {

        dropzone.classList.remove(
            "dragover"
        );

    }
);

dropzone.addEventListener(
    "drop",
    e => {

        e.preventDefault();

        dropzone.classList.remove(
            "dragover"
        );

        fileInput.files =
        e.dataTransfer.files;

        if(fileInput.files.length){

            fileName.textContent =
            fileInput.files[0].name;

            inspectSelectedFont();

        }

    }
);

convertBtn.addEventListener(
    "click",
    async () => {

        if(fileInput.files.length === 0){

            alert(
                "Please select a font."
            );

            return;
        }

        spinner.style.display =
        "block";

        convertBtn.disabled =
        true;

        statusText.textContent =
        "Converting font...";

        const mode =
        document.querySelector(
            'input[name="mode"]:checked'
        ).value;

        const formData =
        new FormData();

        formData.append(
            "file",
            fileInput.files[0]
        );

        formData.append(
            "mode",
            mode
        );

        try{

            const response =
            await fetch(
                "http://127.0.0.1:8000/upload",
                {
                    method:"POST",
                    body:formData
                }
            );

            const blob =
            await response.blob();

            const url =
            window.URL.createObjectURL(
                blob
            );

            const a =
            document.createElement("a");

            a.href = url;

            a.download =
            "FreezeFont.zip";

            document.body.appendChild(a);

            a.click();

            a.remove();

            spinner.style.display =
            "none";

            statusText.textContent =
            "✅ Conversion Complete";

        }
        catch(error){

            spinner.style.display =
            "none";

            statusText.textContent =
            "❌ Conversion Failed";

            console.error(error);

        }

        convertBtn.disabled =
        false;

    }
);
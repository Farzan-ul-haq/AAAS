var canvas = document.getElementById("myCanvas");
var ctx = canvas.getContext("2d");
let newImage = new Image();
newImage.src = '/static/b1.png'
newImage.onload = () => {
// Draw the image onto the context with cropping
ctx.drawImage(newImage, 0, 0, 2000, 1500);
// ctx.wrapText("The Project Title", 100, 100, 500,z 500);
}

// Add gradient
    // More text
    // Writing TITLE
function generate_brochure() {
var title = document.getElementById('title').value
var description = document.getElementById('description-field').value
var features = document.getElementById('features-field').value

ctx.clearRect(0, 0, myCanvas.width, myCanvas.height);
let newImage = new Image();
newImage.src = '/static/b1.png'
newImage.onload = () => {
// Draw the image onto the context with cropping
    ctx.drawImage(newImage, 0, 0, 2000, 1500);
    // ctx.wrapText("The Project Title", 100, 100, 500, 500);
    ctx.font = '900 95px sans-serif';
    ctx.fillStyle = 'black';
    let wrappedtitle = wrapText(ctx, title, 1350, 950, 500, 110);
    for (let i = 0; i < wrappedtitle.length; i++) {
    if(i % 2 == 0) {
        ctx.fillStyle = '#22bed7';
    }
    else {
        ctx.fillStyle = 'black';
    }
    ctx.fillText(wrappedtitle[i][0], wrappedtitle[i][1], wrappedtitle[i][2]); 
    }
    // Writing DESCRIPTION
    ctx.font = '100 34px sans-serif';
    ctx.fillStyle = 'black';
    let wrappedDescription = wrapText(
    ctx,
    description,
    750, 1000,
    550, 45
    );
    wrappedDescription.forEach(function(item) {
    description_text_line = item[0]
    if (description_text_line.slice(0, 2) == "\n ") {
        description_text_line = description_text_line.slice(2, 100)
    }
        ctx.fillText(description_text_line, item[1], item[2]); 
    })

    // Writing FEATURES 
    ctx.font = '300 38px sans-serif';
    ctx.fillStyle = 'black';
    let wrappedFeatures = wrapText(
    ctx, 
    features,
    100, 200,
    550, 60
    );
    wrappedFeatures.forEach(function(item) {
    features_text_line = item[0]
    if (features_text_line.slice(0, 2) == "\n ") {
        features_text_line = features_text_line.slice(2, 100)
    }
    ctx.fillStyle = '#22bed7';
    ctx.fillText("✔ ", item[1], item[2]);
    ctx.fillStyle = 'black';
    ctx.fillText(features_text_line, item[1]+40, item[2]);
    })
}
}
let thumbImg = document.getElementById('thumbnail')
thumbImg.addEventListener('change', function(e) {
if(e.target.files) {
    let imageFile = e.target.files[0];
    var reader = new FileReader();
    reader.readAsDataURL(imageFile);
    reader.onloadend = function (e) {
    var myImage = new Image(); // Creates image object
    myImage.src = e.target.result; // Assigns converted image to image object
    myImage.onload = function(ev) {
        ctx.save();
        ctx.roundRect(1020, 220, 630, 630, [315,315,315,315]);
        // ctx.fill('black')
        ctx.clip();
        ctx.drawImage(myImage,1000, 200, 700, 700);
        ctx.restore();
        ctx.stroke();
    }
    }
}
})
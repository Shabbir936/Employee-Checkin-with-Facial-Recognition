const enrollButton = document.getElementById('enroll-btn');
const enrollmentForm = document.getElementById('employeeProfileForm');
const messageDiv = document.getElementById('message');
const passChgBtn = document.getElementById('passChgBtn')
const startCameraButton = document.getElementById('start-camera');
const capturePhotoButton = document.getElementById('capture-photo');
const video = document.getElementById('camera');
const canvas = document.getElementById('canvas');
const imageDataInput = document.getElementById('image-data');
const submitButton = document.getElementById('submit-btn');
const checkinBtn = document.getElementById('checkinBtn')
const checkoutBtn = document.getElementById('checkoutBtn')
const checkinForm = document.getElementById('checkinForm');
const checkinCapture = document.getElementById('checkinCapture');
const checkinImageInput = document.getElementById('checkin-image');
const checkinVideo = document.getElementById('checkin-camera');
const checkinCanvas = document.getElementById('checkin-canvas');
let stream

passChgBtn.addEventListener('click', function () {
    window.location.href = passChgUrl
});

if (enrollButton != null) {
    enrollButton.addEventListener('click', function () {
        enrollmentForm.style.display = 'block'
        const childElements = messageDiv.children;

        for (let i = 0; i < childElements.length; i++) {
            childElements[i].style.display = 'none';
        }
    });

    startCameraButton.addEventListener('click', async function () {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        video.srcObject = stream;
        video.style.display = 'block';
        startCameraButton.style.display = 'none'
        capturePhotoButton.style.display = 'inline'
    });

    capturePhotoButton.addEventListener('click', function () {
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        const dataUrl = canvas.toDataURL('image/png');
        imageDataInput.value = dataUrl;
        canvas.style.display = 'block';
        video.style.display = 'none';
        capturePhotoButton.style.display = 'none'
        if (stream) {
            const tracks = stream.getTracks();
            tracks.forEach(track => track.stop());
            video.style.display = 'none';
        }

    });

    document.getElementById('employeeProfileForm').addEventListener('submit', function (event) {
        if (!imageDataInput.value) {
            event.preventDefault();
            alert('Please capture an image before submitting.');
        }
    });
}

if (checkinBtn != null) {
    checkinBtn.addEventListener('click',  async function(){
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        checkinCapture.style.display = 'inline'
        checkinVideo.srcObject = stream;
        checkinVideo.style.display = 'block';
        checkinBtn.style.display = 'none'
    })
};

if (checkoutBtn != null) {
    checkoutBtn.addEventListener('click',  async function(){
        stream =  await navigator.mediaDevices.getUserMedia({ video: true });
        checkinCapture.style.display = 'inline'
        checkinVideo.srcObject = stream;
        checkinVideo.style.display = 'block';
        checkoutBtn.style.display = 'none'
    })
};

if (checkinCapture != null) {
    checkinCapture.style.display = 'none'
    checkinCapture.addEventListener('click', function(){
        console.log('here')
        const context = checkinCanvas.getContext('2d');
        context.drawImage(checkinVideo, 0, 0, checkinCanvas.width, checkinCanvas.height);
        const dataUrl = checkinCanvas.toDataURL('image/png');
        checkinImageInput.value = dataUrl;
        checkinCanvas.style.display = 'block';
        checkinVideo.style.display = 'none';
        checkinCapture.style.display = 'none'
        if (stream) {
            const tracks = stream.getTracks();
            tracks.forEach(track => track.stop());
            checkinVideo.style.display = 'none';
        }
    })
}



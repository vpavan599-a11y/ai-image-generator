// --- 1. THREE.JS BACKGROUND ANIMATION ---
const initThreeJS = () => {
    const container = document.getElementById('canvas-container');
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    
    renderer.setSize(window.innerWidth, window.innerHeight);
    container.appendChild(renderer.domElement);

    const geometry = new THREE.BufferGeometry();
    const particlesCount = 2000;
    const posArray = new Float32Array(particlesCount * 3);

    for (let i = 0; i < particlesCount * 3; i++) {
        posArray[i] = (Math.random() - 0.5) * 15;
    }

    geometry.setAttribute('position', new THREE.BufferAttribute(posArray, 3));

    const material = new THREE.PointsMaterial({
        size: 0.02,
        color: 0x00f3ff,
        transparent: true,
        opacity: 0.8,
    });

    const particlesMesh = new THREE.Points(geometry, material);
    scene.add(particlesMesh);

    const geo2 = new THREE.IcosahedronGeometry(1, 0);
    const mat2 = new THREE.MeshBasicMaterial({ 
        color: 0xbc13fe, 
        wireframe: true,
        transparent: true,
        opacity: 0.3
    });

    const wireframe = new THREE.Mesh(geo2, mat2);
    scene.add(wireframe);

    camera.position.z = 3;

    let mouseX = 0;
    let mouseY = 0;

    document.addEventListener('mousemove', (event) => {
        mouseX = event.clientX / window.innerWidth - 0.5;
        mouseY = event.clientY / window.innerHeight - 0.5;
    });

    const animate = () => {
        requestAnimationFrame(animate);

        particlesMesh.rotation.y += 0.001;
        particlesMesh.rotation.x += 0.0005;

        wireframe.rotation.x += 0.002;
        wireframe.rotation.y += 0.002;

        particlesMesh.rotation.y += mouseX * 0.05;
        particlesMesh.rotation.x += mouseY * 0.05;

        renderer.render(scene, camera);
    };

    animate();

    window.addEventListener('resize', () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    });
};


// --- 2. UI LOGIC & GENERATOR ---
document.addEventListener('DOMContentLoaded', () => {

    initThreeJS();

    const generateBtn = document.getElementById('generateBtn');
    const promptInput = document.getElementById('promptInput');
    const generatedImage = document.getElementById('generatedImage');
    const loader = document.getElementById('loader');
    const placeholderText = document.querySelector('.placeholder-text');
    const downloadContainer = document.getElementById('downloadContainer');
    const downloadBtn = document.getElementById('downloadBtn');

    generateBtn.addEventListener('click', () => {
        const prompt = promptInput.value.trim();

        if (!prompt) {
            alert("Please enter a prompt first!");
            return;
        }

        // UI Loading
        generateBtn.disabled = true;
        generateBtn.innerText = "Generating...";
        placeholderText.style.display = 'none';
        generatedImage.style.display = 'none';
        downloadContainer.style.display = 'none';
        loader.style.display = 'block';

        // ✅ FIXED API CALL
        fetch('/api/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ prompt: prompt })
        })
        .then(res => res.json())
        .then(data => {

            if (data.success) {
                generatedImage.src = data.image; // ✅ FIXED

                loader.style.display = 'none';
                generatedImage.style.display = 'block';
                downloadContainer.style.display = 'block';
            } else {
                alert(data.message || "Generation failed");
            }

            generateBtn.disabled = false;
            generateBtn.innerText = "Generate Image";
        })
        .catch(err => {
            console.error(err);
            alert("Error generating image");

            loader.style.display = 'none';
            generateBtn.disabled = false;
            generateBtn.innerText = "Generate Image";
        });
    });

    // Download
    downloadBtn.addEventListener('click', () => {
        const link = document.createElement('a');
        link.href = generatedImage.src;
        link.download = 'ai-generated-image.jpg';
        link.target = '_blank';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    });

});
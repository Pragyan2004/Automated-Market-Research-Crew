document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('research-form');
    if (!form) return;

    const submitBtn = document.getElementById('submit-btn');
    const loadingOverlay = document.getElementById('loading-overlay');
    const resultsSection = document.getElementById('results-section');
    const markdownContent = document.getElementById('markdown-content');
    const steps = document.querySelectorAll('.progress-steps .step');

    // Setup Download Functionality
    const setupDownload = (content) => {
        const downloadBtn = document.getElementById('download-btn');
        if (downloadBtn) {
            downloadBtn.onclick = () => {
                const blob = new Blob([content], { type: 'text/markdown' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `Market_Research_Report_${new Date().toISOString().split('T')[0]}.md`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            };
        }
    };

    // Typewriter effect for displaying markdown smoothly
    const typeWriter = (text, element) => {
        element.innerHTML = '';
        const htmlContent = DOMPurify.sanitize(marked.parse(text));
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = htmlContent;
        
        element.appendChild(tempDiv);
        
        const children = tempDiv.children;
        for(let i=0; i<children.length; i++) {
            children[i].style.opacity = '0';
            children[i].style.transform = 'translateY(15px)';
            children[i].style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            
            setTimeout(() => {
                children[i].style.opacity = '1';
                children[i].style.transform = 'translateY(0)';
            }, i * 150); // Faster stagger for better UX
        }
    };

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const productIdea = document.getElementById('product-idea').value;
        if (!productIdea) return;
        
        // Reset UI
        submitBtn.disabled = true;
        loadingOverlay.classList.remove('hidden');
        resultsSection.classList.add('hidden');
        
        // Reset steps
        steps.forEach(step => {
            step.classList.remove('active', 'completed');
            const sub = step.querySelector('.sub-status');
            if(sub) sub.remove();
        });
        steps[0].classList.add('active');
        
        // Interactive loader logic
        let currentStep = 0;
        let isFinished = false;

        const subStatuses = [
            ["Analyzing TAM, SAM, SOM...", "Checking industry trends..."],
            ["Scanning competitor websites...", "Mapping feature matrices..."],
            ["Reading consumer forums...", "Identifying pain points..."],
            ["Formulating MVP features...", "Checking technical feasibility..."],
            ["Synthesizing data...", "Writing final investment memo..."]
        ];

        const animateStep = async (stepIndex) => {
            if (isFinished || stepIndex >= steps.length) return;
            
            steps.forEach((s, i) => {
                if (i < stepIndex) s.classList.add('completed');
                s.classList.remove('active');
            });
            steps[stepIndex].classList.add('active');
            
            // Add sub-status typing effect
            const subDiv = document.createElement('div');
            subDiv.className = 'sub-status';
            subDiv.style.fontSize = '0.9rem';
            subDiv.style.color = 'var(--primary)';
            subDiv.style.marginTop = '4px';
            subDiv.style.marginLeft = '25px';
            subDiv.style.fontStyle = 'italic';
            steps[stepIndex].appendChild(subDiv);
            
            const statuses = subStatuses[stepIndex];
            
            for (let i = 0; i < statuses.length; i++) {
                if (isFinished) break;
                subDiv.innerText = statuses[i];
                // Wait randomly between 8 to 15 seconds per status
                await new Promise(r => setTimeout(r, Math.random() * 7000 + 8000));
            }
            
            if (!isFinished && stepIndex < steps.length - 1) {
                animateStep(stepIndex + 1);
            }
        };

        // Start animation
        animateStep(0);

        try {
            const response = await fetch('/api/research', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ product_idea: productIdea })
            });
            
            const data = await response.json();
            isFinished = true; // Stop animation loop
            
            if (data.success) {
                // Quickly complete all remaining steps visually
                steps.forEach(s => {
                    s.classList.remove('active');
                    s.classList.add('completed');
                    const sub = s.querySelector('.sub-status');
                    if(sub) sub.innerText = "Task complete.";
                });
                
                setTimeout(() => {
                    loadingOverlay.classList.add('fade-out');
                    setTimeout(() => {
                        loadingOverlay.classList.add('hidden');
                        loadingOverlay.classList.remove('fade-out');
                        resultsSection.classList.remove('hidden');
                        typeWriter(data.result, markdownContent);
                        setupDownload(data.result);
                    }, 500);
                }, 1000); // Give user 1s to see all steps completed
                
            } else {
                alert('Error: ' + data.error);
                loadingOverlay.classList.add('hidden');
            }
        } catch (err) {
            isFinished = true;
            alert('An unexpected error occurred. Check the console.');
            console.error(err);
            loadingOverlay.classList.add('hidden');
        } finally {
            submitBtn.disabled = false;
        }
    });
});

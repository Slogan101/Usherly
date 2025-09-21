document.addEventListener('DOMContentLoaded', () => {
    // =========================================================================
    // CONFIGURATION & API WRAPPER
    // =========================================================================

    // --- IMPORTANT: Set your API base URL here ---
    const API_BASE_URL = 'https://api.example.com/api'; // Placeholder. Not used in dummy mode.

    /**
     * A wrapper for the fetch API.
     * - Automatically adds Authorization header if a token exists.
     * - Handles JSON and multipart/form-data content types.
     * - Parses JSON responses and throws errors for non-ok responses.
     * @param {string} endpoint - The API endpoint to call (e.g., '/auth/login').
     * @param {object} [options={}] - The options for the fetch call (method, body, etc.).
     * @returns {Promise<any>} - The parsed JSON response.
     */
    async function apiFetch(endpoint, options = {}) {
        const url = `${API_BASE_URL}${endpoint}`;
        const headers = { ...options.headers };
        const token = localStorage.getItem('authToken');

        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        // Do not set Content-Type for FormData; the browser does it correctly.
        if (!(options.body instanceof FormData)) {
            headers['Content-Type'] = 'application/json';
        }

        const config = {
            ...options,
            headers,
        };

        // In dummy mode, we simulate API calls instead of making real ones.
        console.log(`DUMMY API CALL to ${options.method || 'GET'} ${url}`, options.body || '');
        // Simulate a delay
        await new Promise(res => setTimeout(res, 500));
        // Return a mocked successful response
        return { success: true, message: "Action completed successfully (simulated).", data: {} };

        /*
        // --- REAL API CALL LOGIC (uncomment when connecting to a backend) ---
        try {
            const response = await fetch(url, config);
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ message: response.statusText }));
                throw new Error(errorData.message || 'An unknown API error occurred.');
            }
            if (response.status === 204) { // No Content
                return;
            }
            return await response.json();
        } catch (error) {
            console.error('API Fetch Error:', error);
            throw error;
        }
        */
    }

    // =========================================================================
    // DUMMY DATA
    // =========================================================================

    const dummyEvents = [
        { id: 1, title: 'Annual Tech Gala 2025', type: 'corporate', location: 'Lagos, Nigeria', date: '2025-12-10T19:00', pay: 25000, host: 'Innovate Corp', image: 'assets/event-placeholder-1.jpg', applicants: 5 },
        { id: 2, title: 'Adeleke & Johnson Wedding', type: 'wedding', location: 'Abuja, FCT', date: '2025-11-22T14:00', pay: 20000, host: 'The Adeleke Family', image: 'assets/event-placeholder-2.jpg', applicants: 12 },
        { id: 3, title: 'Fusion Music Festival', type: 'concert', location: 'Port Harcourt, Rivers', date: '2025-10-15T16:00', pay: 15000, host: 'Vibe Nation Ent.', image: 'assets/event-placeholder-1.jpg', applicants: 28 },
        { id: 4, title: 'Zenith Bank End of Year Party', type: 'corporate', location: 'Lagos, Nigeria', date: '2025-12-18T18:00', pay: 30000, host: 'Zenith Bank Plc', image: 'assets/event-placeholder-2.jpg', applicants: 0 },
    ];

    const dummyApplications = [
        { eventTitle: 'Annual Tech Gala 2025', date: '2025-12-10', host: 'Innovate Corp', status: 'Accepted', statusClass: 'success' },
        { eventTitle: 'Fusion Music Festival', date: '2025-10-15', host: 'Vibe Nation Ent.', status: 'Pending', statusClass: 'warning' },
        { eventTitle: 'Some Other Event', date: '2025-09-30', host: 'Event Co.', status: 'Rejected', statusClass: 'danger' },
    ];

    const dummyApplicants = [
        { id: 101, name: 'Blessing Adebayo', age: 22, height: "5'9\"", skin_tone: 'Dark', bio: 'Experienced and reliable usher ready for any event.', photos: ['assets/event-placeholder-1.jpg', 'assets/event-placeholder-2.jpg', 'assets/event-placeholder-1.jpg', 'assets/event-placeholder-2.jpg'] },
        { id: 102, name: 'Chidinma Okoro', age: 25, height: "5'7\"", skin_tone: 'Brown', bio: 'Professional, articulate, and great with guests.', photos: ['assets/event-placeholder-2.jpg', 'assets/event-placeholder-1.jpg', 'assets/event-placeholder-2.jpg', 'assets/event-placeholder-1.jpg'] },
        { id: 103, name: 'Fatima Bello', age: 21, height: "5'10\"", skin_tone: 'Fair', bio: 'Energetic and hardworking, with a positive attitude.', photos: ['assets/event-placeholder-1.jpg', 'assets/event-placeholder-1.jpg', 'assets/event-placeholder-2.jpg', 'assets/event-placeholder-2.jpg'] }
    ];

    const dummyAdminData = {
        users: [
            { id: 1, name: 'Esther Howard', email: 'esther.h@example.com', role: 'Usher', status: 'Active' },
            { id: 2, name: 'Jane Doe', email: 'jane.d@example.com', role: 'Host', status: 'Active' },
            { id: 3, name: 'John Smith', email: 'john.s@example.com', role: 'Usher', status: 'Suspended' },
        ],
        events: [
            { id: 1, title: 'Annual Tech Gala 2025', host: 'Jane Doe', date: '2025-12-10', status: 'Live' },
            { id: 2, title: 'Product Launch', host: 'Jane Doe', date: '2025-11-05', status: 'Completed' },
        ],
        payments: [
            { id: 1, user: 'Esther Howard', amount: 5000, type: 'Subscription', date: '2025-09-10', status: 'Success' },
            { id: 2, user: 'Jane Doe', amount: 5000, type: 'Booking Fee', date: '2025-09-15', status: 'Success' },
        ]
    };

    // =========================================================================
    // UTILITY & HELPER FUNCTIONS
    // =========================================================================

    /**
     * Shows a Bootstrap toast message.
     * @param {string} message - The message to display.
     * @param {string} [type='success'] - 'success' or 'danger'.
     */
    function showToast(message, type = 'success') {
        const toastEl = document.getElementById('app-toast');
        if (!toastEl) return;

        const toastBody = toastEl.querySelector('.toast-body');
        toastBody.textContent = message;

        // Reset classes
        toastEl.classList.remove('bg-success-subtle', 'bg-danger-subtle', 'text-success-emphasis', 'text-danger-emphasis');

        if (type === 'success') {
            toastEl.classList.add('bg-success-subtle', 'text-success-emphasis');
        } else {
            toastEl.classList.add('bg-danger-subtle', 'text-danger-emphasis');
        }

        const toast = new bootstrap.Toast(toastEl);
        toast.show();
    }

    /**
     * Handles client-side form validation using Bootstrap's classes.
     * @param {HTMLFormElement} form - The form element to validate.
     * @returns {boolean} - True if the form is valid, false otherwise.
     */
    function validateForm(form) {
        form.classList.add('was-validated');
        return form.checkValidity();
    }

    /**
     * Redirects to a different page.
     * @param {string} url - The URL to redirect to.
     */
    function redirect(url) {
        window.location.href = url;
    }


    // =========================================================================
    // RENDERING FUNCTIONS
    // =========================================================================

    /**
     * Renders a list of event cards into a container.
     * @param {Array<object>} events - The array of event objects.
     * @param {HTMLElement} container - The DOM element to append cards to.
     */
    function renderEvents(events, container) {
        if (!container) return;
        container.innerHTML = '';
        if (events.length === 0) {
            container.innerHTML = '<p class="text-muted">No events found.</p>';
            return;
        }

        events.forEach(event => {
            const eventCard = `
                <div class="col-md-6">
                    <div class="card h-100">
                        <img src="${event.image}" class="card-img-top" alt="${event.title}">
                        <div class="card-body">
                            <span class="badge bg-primary mb-2">${event.type.charAt(0).toUpperCase() + event.type.slice(1)}</span>
                            <h5 class="card-title">${event.title}</h5>
                            <p class="card-text text-muted">
                                <i class="bi bi-geo-alt"></i> ${event.location} <br>
                                <i class="bi bi-calendar"></i> ${new Date(event.date).toLocaleDateString()}
                            </p>
                            <h6 class="fw-bold">Pay: ₦${event.pay.toLocaleString()}</h6>
                        </div>
                        <div class="card-footer bg-white border-0 pb-3">
                            <div class="d-flex justify-content-between">
                                <a href="event-details.html?id=${event.id}" class="btn btn-sm btn-outline-primary">View Details</a>
                                <button class="btn btn-sm btn-primary apply-btn" data-event-id="${event.id}" data-event-title="${event.title}">Apply</button>
                            </div>
                        </div>
                    </div>
                </div>`;
            container.insertAdjacentHTML('beforeend', eventCard);
        });
    }

    /**
     * Renders application rows into a table.
     * @param {Array<object>} applications - The array of application objects.
     * @param {HTMLElement} container - The tbody element.
     */
    function renderApplications(applications, container) {
        if (!container) return;
        container.innerHTML = '';
        applications.forEach(app => {
            const row = `
                <tr>
                    <td>${app.eventTitle}</td>
                    <td>${app.date}</td>
                    <td>${app.host}</td>
                    <td><span class="badge bg-${app.statusClass}-subtle text-${app.statusClass}-emphasis">${app.status}</span></td>
                </tr>`;
            container.insertAdjacentHTML('beforeend', row);
        });
    }

    /**
    * Renders the host's events on their dashboard.
    * @param {Array<object>} events - The host's events.
    * @param {HTMLElement} container - The container element.
    */
    function renderHostEvents(events, container) {
        if (!container) return;
        container.innerHTML = '';
        events.forEach(event => {
            const card = `
                <div class="card">
                    <div class="card-body d-flex justify-content-between align-items-center">
                        <div>
                            <h5 class="card-title mb-1">${event.title}</h5>
                            <p class="card-text text-muted mb-0">
                                ${new Date(event.date).toDateString()} &bull; ${event.location}
                            </p>
                        </div>
                        <button class="btn btn-primary view-applicants-btn" data-bs-toggle="modal" data-bs-target="#applicantsModal" data-event-id="${event.id}" data-event-title="${event.title}">
                            View Applicants <span class="badge bg-light text-dark">${event.applicants}</span>
                        </button>
                    </div>
                </div>
            `;
            container.insertAdjacentHTML('beforeend', card);
        });
    }

    /**
     * Renders the applicant list for the host modal.
     * @param {Array<object>} applicants - Array of applicant objects.
     * @param {HTMLElement} container - The list container.
     */
    function renderApplicantList(applicants, container) {
        if (!container) return;
        container.innerHTML = '<div class="list-group list-group-flush"></div>';
        const listGroup = container.querySelector('.list-group');

        applicants.forEach((applicant, index) => {
            const item = `
                <a href="#" class="list-group-item list-group-item-action ${index === 0 ? 'active' : ''}" data-applicant-id="${applicant.id}">
                    <div class="d-flex w-100 justify-content-between">
                        <h6 class="mb-1">${applicant.name}</h6>
                    </div>
                    <small>${applicant.age} years &bull; ${applicant.height}</small>
                </a>`;
            listGroup.insertAdjacentHTML('beforeend', item);
        });
    }

    /**
     * Shows a specific applicant's details and photos in the host modal.
     * @param {object} applicant - The applicant object.
     * @param {HTMLElement} container - The details container.
     */
    function showApplicantDetails(applicant, container) {
        if (!applicant || !container) return;

        const detailsHTML = `
            <div class="p-3">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <div>
                        <h3>${applicant.name}</h3>
                        <p class="text-muted">${applicant.age} years &bull; ${applicant.height} &bull; ${applicant.skin_tone}</p>
                    </div>
                    <div>
                        <button class="btn btn-danger me-2 reject-applicant-btn" data-applicant-id="${applicant.id}">Reject</button>
                        <button class="btn btn-success accept-applicant-btn" data-applicant-id="${applicant.id}">Accept</button>
                    </div>
                </div>
                <p>${applicant.bio}</p>
            </div>
            <div id="applicant-photo-carousel" class="carousel slide flex-grow-1 bg-dark rounded" data-bs-ride="carousel">
                <div class="carousel-indicators">
                    ${applicant.photos.map((_, i) => `<button type="button" data-bs-target="#applicant-photo-carousel" data-bs-slide-to="${i}" class="${i === 0 ? 'active' : ''}"></button>`).join('')}
                </div>
                <div class="carousel-inner">
                    ${applicant.photos.map((photo, i) => `
                        <div class="carousel-item ${i === 0 ? 'active' : ''}">
                            <img src="${photo}" class="d-block w-100" alt="Applicant photo ${i + 1}">
                        </div>
                    `).join('')}
                </div>
                <button class="carousel-control-prev" type="button" data-bs-target="#applicant-photo-carousel" data-bs-slide="prev">
                    <span class="carousel-control-prev-icon"></span><span class="visually-hidden">Previous</span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#applicant-photo-carousel" data-bs-slide="next">
                    <span class="carousel-control-next-icon"></span><span class="visually-hidden">Next</span>
                </button>
            </div>
        `;
        container.innerHTML = detailsHTML;
    }


    // =========================================================================
    // PAGE-SPECIFIC LOGIC
    // =========================================================================

    const path = window.location.pathname;

    // --- LANDING PAGE (index.html) ---
    if (path.endsWith('/') || path.endsWith('index.html')) {
        const eventListContainer = document.getElementById('event-list');
        renderEvents(dummyEvents.slice(0, 4), eventListContainer);
    }

    // --- AUTH PAGES (auth-*.html) ---
    if (path.includes('auth-signup.html')) {
        const roleRadios = document.querySelectorAll('input[name="user_type"]');
        const hostFields = document.getElementById('host-fields');
        const signupForm = document.getElementById('signup-form');
        const password = document.getElementById('password');
        const confirmPassword = document.getElementById('confirm-password');

        roleRadios.forEach(radio => {
            radio.addEventListener('change', (e) => {
                hostFields.classList.toggle('d-none', e.target.value !== 'host');
            });
        });

        confirmPassword.addEventListener('input', () => {
            if (password.value !== confirmPassword.value) {
                confirmPassword.setCustomValidity("Passwords do not match.");
            } else {
                confirmPassword.setCustomValidity("");
            }
        });

        signupForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            if (!validateForm(signupForm)) return;

            const payload = {
                name: document.getElementById('fullname').value,
                email: document.getElementById('email').value,
                password: password.value,
                phone: document.getElementById('phone').value,
                user_type: document.querySelector('input[name="user_type"]:checked').value,
                organization: document.getElementById('organization').value,
            };

            console.log("Signup Payload:", payload);
            // API CALL: POST /api/auth/signup
            // This is where you would call your API.
            try {
                // const data = await apiFetch('/auth/signup', { method: 'POST', body: JSON.stringify(payload) });
                // localStorage.setItem('authToken', data.token);
                // Simulate success and redirect based on role
                const userRole = payload.user_type;
                localStorage.setItem('authToken', 'dummy-jwt-token'); // Store a dummy token
                localStorage.setItem('userRole', userRole);
                if (userRole === 'usher') {
                    redirect('usher-dashboard.html');
                } else {
                    redirect('host-dashboard.html');
                }
            } catch (error) {
                document.getElementById('signup-alert').textContent = error.message;
                document.getElementById('signup-alert').classList.remove('d-none');
            }
        });
    }

    if (path.includes('auth-login.html')) {
        const loginForm = document.getElementById('login-form');
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            if (!validateForm(loginForm)) return;

            const payload = {
                email: document.getElementById('email').value,
                password: document.getElementById('password').value,
            };

            console.log("Login Payload:", payload);
            // API CALL: POST /api/auth/login
            // In a real app, the API would return the user's role. We'll guess based on email.
            try {
                // const data = await apiFetch('/auth/login', { method: 'POST', body: JSON.stringify(payload) });
                // localStorage.setItem('authToken', data.token);
                // localStorage.setItem('userRole', data.user.role);
                // Simulate success and redirect
                localStorage.setItem('authToken', 'dummy-jwt-token');
                const userRole = payload.email.includes('host') ? 'host' : 'usher';
                localStorage.setItem('userRole', userRole);
                redirect(userRole === 'usher' ? 'usher-dashboard.html' : 'host-dashboard.html');
            } catch (error) {
                document.getElementById('login-alert').textContent = 'Invalid credentials (simulated).';
                document.getElementById('login-alert').classList.remove('d-none');
            }
        });
    }

    // --- USHER DASHBOARD ---
    if (path.includes('usher-dashboard.html')) {
        renderEvents(dummyEvents, document.getElementById('dashboard-event-list'));
        renderApplications(dummyApplications, document.getElementById('applications-table-body'));

        // Image Upload Logic
        const imageUploadContainer = document.getElementById('image-upload-container');
        const numImages = 4;
        let uploadedFiles = new Array(numImages).fill(null);

        for (let i = 0; i < numImages; i++) {
            imageUploadContainer.innerHTML += `
                <div class="col-6 col-md-3">
                    <div class="image-upload-slot ratio ratio-1x1" id="slot-${i}">
                        <div class="upload-prompt p-2">
                            <i class="bi bi-camera fs-2"></i>
                            <span class="fs-sm text-center">Slot ${i + 1}</span>
                        </div>
                        <input type="file" accept="image/jpeg, image/png" data-index="${i}">
                    </div>
                </div>`;
        }

        imageUploadContainer.addEventListener('change', (e) => {
            if (e.target.type === 'file') {
                const index = parseInt(e.target.dataset.index);
                const file = e.target.files[0];
                const slot = document.getElementById(`slot-${index}`);

                if (file) {
                    // Validation
                    if (!['image/jpeg', 'image/png'].includes(file.type)) {
                        alert('Invalid file type. Please use JPG or PNG.');
                        e.target.value = ''; return;
                    }
                    if (file.size > 5 * 1024 * 1024) { // 5MB
                        alert('File is too large. Max size is 5MB.');
                        e.target.value = ''; return;
                    }

                    uploadedFiles[index] = file;
                    const reader = new FileReader();
                    reader.onload = (event) => {
                        slot.innerHTML = `<img src="${event.target.result}" alt="Preview ${index + 1}">`;
                    };
                    reader.readAsDataURL(file);
                }
            }
        });

        document.getElementById('save-profile-btn').addEventListener('click', async () => {
            const errorDiv = document.getElementById('image-upload-error');
            errorDiv.classList.add('d-none');

            const filesToUpload = uploadedFiles.filter(f => f !== null);
            if (filesToUpload.length !== numImages) {
                errorDiv.textContent = `You must upload exactly ${numImages} photos.`;
                errorDiv.classList.remove('d-none');
                return;
            }

            const formData = new FormData();
            filesToUpload.forEach((file, index) => {
                formData.append(`image_${index + 1}`, file);
            });

            // You can also append other profile data
            formData.append('name', document.getElementById('profileName').value);

            console.log('Submitting profile with images...', formData);
            // API CALL: POST /api/users/me/images (with FormData)
            try {
                // await apiFetch('/users/me/images', { method: 'POST', body: formData });
                showToast('Profile updated successfully!');
                bootstrap.Modal.getInstance(document.getElementById('editProfileModal')).hide();
            } catch (error) {
                errorDiv.textContent = `Error: ${error.message}`;
                errorDiv.classList.remove('d-none');
            }
        });

        // Event Application Logic
        document.body.addEventListener('click', (e) => {
            if (e.target.classList.contains('apply-btn')) {
                const eventId = e.target.dataset.eventId;
                const eventTitle = e.target.dataset.eventTitle;
                document.getElementById('apply-event-title').textContent = eventTitle;
                document.getElementById('confirm-apply-btn').dataset.eventId = eventId;
                const modal = new bootstrap.Modal(document.getElementById('applyConfirmModal'));
                modal.show();
            }
        });

        document.getElementById('confirm-apply-btn').addEventListener('click', async function () {
            const eventId = this.dataset.eventId;
            console.log(`Applying for event ${eventId}...`);
            // API CALL: POST /api/events/${eventId}/apply
            try {
                // await apiFetch(`/events/${eventId}/apply`, { method: 'POST' });
                showToast('Application submitted successfully!');
                bootstrap.Modal.getInstance(document.getElementById('applyConfirmModal')).hide();
            } catch (error) {
                showToast(`Error: ${error.message}`, 'danger');
            }
        });
    }

    // --- HOST DASHBOARD ---
    if (path.includes('host-dashboard.html')) {
        renderHostEvents(dummyEvents.filter(e => e.host === 'The Adeleke Family' || e.host === 'Innovate Corp'), document.getElementById('host-event-list'));

        const numUshersInput = document.getElementById('numUshers');
        const bookingFeeInput = document.getElementById('bookingFee');
        const feeBreakdown = document.getElementById('fee-breakdown');

        function calculateTotalFee() {
            const numUshers = parseInt(numUshersInput.value) || 0;
            const feePerHire = parseInt(bookingFeeInput.value) || 0;
            if (numUshers > 0) {
                const total = numUshers * feePerHire;
                document.getElementById('num-ushers-display').textContent = numUshers;
                document.getElementById('fee-per-hire-display').textContent = feePerHire.toLocaleString();
                document.getElementById('total-booking-fee').textContent = total.toLocaleString();
                feeBreakdown.classList.remove('d-none');
            } else {
                feeBreakdown.classList.add('d-none');
            }
        }

        numUshersInput.addEventListener('input', calculateTotalFee);

        document.getElementById('post-event-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            const form = e.target;
            if (!validateForm(form)) return;

            const numUshers = parseInt(numUshersInput.value);
            const feePerHire = parseInt(bookingFeeInput.value);

            const payload = {
                event_draft: {
                    title: document.getElementById('eventTitle').value,
                    event_type: document.getElementById('eventType').value,
                    location: document.getElementById('eventLocation').value,
                    date: document.getElementById('eventDate').value,
                    duration_hours: document.getElementById('durationHours').value,
                    pay_amount: document.getElementById('payAmount').value,
                    description: document.getElementById('eventDescription').value,
                },
                num_slots: numUshers,
                fee_per_hire: feePerHire,
                total_amount: numUshers * feePerHire,
            };

            console.log("Booking Payment Payload:", payload);
            // API CALL: POST /api/payments/booking
            try {
                // const paymentResponse = await apiFetch('/payments/booking', { method: 'POST', body: JSON.stringify(payload) });
                // On success, the backend would typically post the event or you'd make another call.
                showToast('Payment successful! Your event is now live.');
                form.reset();
                feeBreakdown.classList.add('d-none');
                // You would re-fetch and re-render the event list here.
            } catch (error) {
                showToast(`Payment failed: ${error.message}`, 'danger');
            }
        });

        // Applicants Modal Logic
        const applicantsModal = document.getElementById('applicantsModal');
        applicantsModal.addEventListener('show.bs.modal', event => {
            const button = event.relatedTarget;
            const eventTitle = button.dataset.eventTitle;
            document.getElementById('modal-event-title').textContent = eventTitle;

            const applicantListContainer = document.getElementById('applicant-list-container');
            const applicantDetailsContainer = document.getElementById('applicant-details-container');

            renderApplicantList(dummyApplicants, applicantListContainer);

            // Show first applicant's details by default
            if (dummyApplicants.length > 0) {
                showApplicantDetails(dummyApplicants[0], applicantDetailsContainer);
            }
        });

        // Handle clicks on applicant list
        document.getElementById('applicant-list-container').addEventListener('click', e => {
            e.preventDefault();
            const link = e.target.closest('.list-group-item-action');
            if (!link) return;

            // Update active state
            document.querySelectorAll('#applicant-list-container .list-group-item-action').forEach(el => el.classList.remove('active'));
            link.classList.add('active');

            const applicantId = parseInt(link.dataset.applicantId);
            const selectedApplicant = dummyApplicants.find(a => a.id === applicantId);
            showApplicantDetails(selectedApplicant, document.getElementById('applicant-details-container'));
        });

        // Handle Accept/Reject clicks
        document.getElementById('applicant-details-container').addEventListener('click', async e => {
            const applicantId = e.target.dataset.applicantId;
            if (!applicantId) return;

            if (e.target.classList.contains('accept-applicant-btn')) {
                // API CALL: POST /api/applications/${appId}/accept
                console.log(`Accepting applicant ${applicantId}...`);
                showToast(`Applicant accepted successfully.`);
            } else if (e.target.classList.contains('reject-applicant-btn')) {
                // API CALL: POST /api/applications/${appId}/reject
                console.log(`Rejecting applicant ${applicantId}...`);
                showToast(`Applicant rejected.`);
            }
        });
    }

    // --- SUBSCRIPTION PAGE ---
    if (path.includes('subscription.html')) {
        document.querySelectorAll('.subscription-btn').forEach(button => {
            button.addEventListener('click', async () => {
                const tier = button.dataset.tier;
                const amount = button.dataset.amount;

                const payload = {
                    user_id: 123, // This would be the actual logged-in user's ID
                    tier: tier,
                    amount: parseInt(amount),
                };

                console.log("Subscription Payment Payload:", payload);
                // API CALL: POST /api/payments/subscription
                try {
                    // await apiFetch('/payments/subscription', { method: 'POST', body: JSON.stringify(payload) });
                    showToast(`You have successfully subscribed to the ${tier.toUpperCase()} plan!`);
                    setTimeout(() => redirect('usher-dashboard.html'), 2000);
                } catch (error) {
                    showToast(`Subscription failed: ${error.message}`, 'danger');
                }
            });
        });
    }

    // --- ADMIN PAGE ---
    if (path.includes('admin.html')) {
        const usersTable = document.getElementById('admin-users-table');
        dummyAdminData.users.forEach(u => {
            usersTable.innerHTML += `
            <tr>
                <td>${u.id}</td><td>${u.name}</td><td>${u.email}</td><td>${u.role}</td>
                <td><span class="badge ${u.status === 'Active' ? 'bg-success' : 'bg-warning'}">${u.status}</span></td>
                <td><button class="btn btn-sm btn-danger" onclick="alert('API CALL: POST /api/admin/users/${u.id}/suspend')">Suspend</button></td>
            </tr>`;
        });
        const eventsTable = document.getElementById('admin-events-table');
        dummyAdminData.events.forEach(e => {
            eventsTable.innerHTML += `
            <tr>
                <td>${e.id}</td><td>${e.title}</td><td>${e.host}</td><td>${e.date}</td><td>${e.status}</td>
                <td><button class="btn btn-sm btn-danger" onclick="alert('API CALL: DELETE /api/admin/events/${e.id}')">Delete</button></td>
            </tr>`;
        });
        const paymentsTable = document.getElementById('admin-payments-table');
        dummyAdminData.payments.forEach(p => {
            paymentsTable.innerHTML += `
            <tr>
                <td>${p.id}</td><td>${p.user}</td><td>₦${p.amount.toLocaleString()}</td><td>${p.type}</td><td>${p.date}</td>
                <td><span class="badge bg-success">${p.status}</span></td>
            </tr>`;
        });
    }

    // --- GLOBAL: LOGOUT ---
    const logoutBtn = document.getElementById('logout-btn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', (e) => {
            e.preventDefault();
            localStorage.removeItem('authToken');
            localStorage.removeItem('userRole');
            redirect('index.html');
        });
    }

});
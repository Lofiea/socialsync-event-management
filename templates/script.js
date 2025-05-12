document.addEventListener('DOMContentLoaded', function() {
    // References to elements
    const eventForm = document.getElementById('event-form');
    const isOfflineToggle = document.getElementById('is-offline');
    const locationInput = document.getElementById('location');
    const isUnlimitedToggle = document.getElementById('is-unlimited');
    const capacityInput = document.getElementById('capacity');
    const fileUpload = document.getElementById('file-upload');
    const dropzone = document.querySelector('.dropzone');
    const previewContainer = document.getElementById('preview-container');
    const saveButton = document.getElementById('save-draft');
    const submitButton = document.getElementById('submit-button');
    const eventTypeButtons = document.querySelectorAll('#event-type-selector .tag-button');
    const budgetButtons = document.querySelectorAll('#budget-selector .tag-button');
    const eventTypeInput = document.getElementById('event-type');
    const budgetInput = document.getElementById('budget');
  
    // Toggle location input placeholder based on offline status
    isOfflineToggle.addEventListener('change', function() {
      locationInput.placeholder = this.checked ? 
        'Add physical location' : 
        'Add online event URL';
    });
  
    // Toggle capacity input based on unlimited toggle
    isUnlimitedToggle.addEventListener('change', function() {
      capacityInput.disabled = this.checked;
      capacityInput.placeholder = this.checked ? '∞' : '0';
    });
  
    // Handle file uploads
    fileUpload.addEventListener('change', handleFileUpload);
    
    // Allow drag and drop functionality
    dropzone.addEventListener('dragover', function(e) {
      e.preventDefault();
      e.stopPropagation();
      this.style.borderColor = 'var(--primary-color)';
    });
    
    dropzone.addEventListener('dragleave', function(e) {
      e.preventDefault();
      e.stopPropagation();
      this.style.borderColor = 'var(--gray-300)';
    });
    
    dropzone.addEventListener('drop', function(e) {
      e.preventDefault();
      e.stopPropagation();
      this.style.borderColor = 'var(--gray-300)';
      
      if (e.dataTransfer.files.length) {
        handleFiles(e.dataTransfer.files);
      }
    });
    
    // Click on dropzone to trigger file input
    dropzone.addEventListener('click', function() {
      fileUpload.click();
    });
    
    // Handle tag selection for Event Type
    eventTypeButtons.forEach(button => {
      button.addEventListener('click', function() {
        eventTypeButtons.forEach(btn => btn.classList.remove('selected'));
        this.classList.add('selected');
        eventTypeInput.value = this.getAttribute('data-value');
      });
    });
    
    // Handle tag selection for Budget
    budgetButtons.forEach(button => {
      button.addEventListener('click', function() {
        budgetButtons.forEach(btn => btn.classList.remove('selected'));
        this.classList.add('selected');
        budgetInput.value = this.getAttribute('data-value');
      });
    });
    
    // Save as draft
    saveButton.addEventListener('click', function() {
      const formData = getFormData();
      console.log('Saving draft:', formData);
      // Simulate API call
      saveButton.textContent = 'Saving...';
      setTimeout(() => {
        showMessage('Draft saved successfully!', 'success');
        saveButton.textContent = 'Save/Edit Later';
      }, 1000);
    });
    
    // Form submission
    eventForm.addEventListener('submit', function(e) {
      e.preventDefault();
      if (validateForm()) {
        const formData = getFormData();
        console.log('Submitting event:', formData);
        submitButton.disabled = true;
        submitButton.textContent = 'Submitting...';
        
        // Simulate API call
        setTimeout(() => {
          showMessage('Event created successfully!', 'success');
          eventForm.reset();
          previewContainer.innerHTML = '';
          submitButton.disabled = false;
          submitButton.textContent = 'Submit';
        }, 1500);
      }
    });
    
    // Functions
    function handleFileUpload(e) {
      if (e.target.files.length) {
        handleFiles(e.target.files);
      }
    }
    
    function handleFiles(files) {
      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        if (file.type.startsWith('image/')) {
          const reader = new FileReader();
          
          reader.onload = function(e) {
            addImagePreview(e.target.result);
          };
          
          reader.readAsDataURL(file);
        }
      }
    }
    
    function addImagePreview(src) {
      const preview = document.createElement('div');
      preview.className = 'preview-item';
      
      const img = document.createElement('img');
      img.className = 'preview-image';
      img.src = src;
      
      const removeButton = document.createElement('div');
      removeButton.className = 'preview-remove';
      removeButton.innerHTML = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>';
      
      removeButton.addEventListener('click', function(e) {
        e.stopPropagation();
        previewContainer.removeChild(preview);
      });
      
      preview.appendChild(img);
      preview.appendChild(removeButton);
      previewContainer.appendChild(preview);
    }
    
    function getFormData() {
      // Collect form data into an object
      return {
        name: document.getElementById('event-name').value,
        startDate: document.getElementById('start-date').value,
        startTime: document.getElementById('start-time').value,
        endDate: document.getElementById('end-date').value,
        endTime: document.getElementById('end-time').value,
        location: document.getElementById('location').value,
        isOffline: document.getElementById('is-offline').checked,
        capacity: document.getElementById('is-unlimited').checked ? null : document.getElementById('capacity').value,
        isUnlimited: document.getElementById('is-unlimited').checked,
        visibility: document.querySelector('input[name="visibility"]:checked').value,
        host: document.getElementById('host').value,
        ageTag: document.getElementById('age-tag').value,
        eventType: document.getElementById('event-type').value,
        budget: document.getElementById('budget').value,
        notes: document.getElementById('notes').value,
        // Images would typically be handled differently for API uploads
        images: Array.from(document.querySelectorAll('.preview-image')).map(img => img.src)
      };
    }
    
    function validateForm() {
      let isValid = true;
      
      // You would implement actual validation here
      // This is just a simple example
      if (!document.getElementById('event-name').value) {
        document.getElementById('event-name-error').textContent = 'Event name is required';
        isValid = false;
      } else {
        document.getElementById('event-name-error').textContent = '';
      }
      
      if (!document.getElementById('host').value) {
        document.getElementById('host-error').textContent = 'Host information is required';
        isValid = false;
      } else {
        document.getElementById('host-error').textContent = '';
      }
      
      return isValid;
    }
    
    function showMessage(message, type) {
      // Create a toast notification
      const toast = document.createElement('div');
      toast.className = `toast toast-${type}`;
      toast.textContent = message;
      
      document.body.appendChild(toast);
      
      // Remove after 3 seconds
      setTimeout(() => {
        toast.classList.add('fade-out');
        setTimeout(() => {
          document.body.removeChild(toast);
        }, 300);
      }, 3000);
    }
    
    // You'd also add date picker implementation here
  });
  
  // Add the toast styles to the stylesheet
  const style = document.createElement('style');
  style.textContent = `
    .toast {
      position: fixed;
      bottom: 20px;
      right: 20px;
      padding: 12px 20px;
      border-radius: 4px;
      color: white;
      font-size: 14px;
      z-index: 1000;
      animation: slideIn 0.3s ease;
    }
    
    .toast-success {
      background-color: var(--success-color);
    }
    
    .toast-error {
      background-color: var(--error-color);
    }
    
    .fade-out {
      opacity: 0;
      transition: opacity 0.3s ease;
    }
    
    @keyframes slideIn {
      from {
        transform: translateX(100%);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }
  `;
  document.head.appendChild(style);
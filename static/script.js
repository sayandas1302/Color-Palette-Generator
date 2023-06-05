// Get the form element
const form = document.getElementById('uploadForm');

// Add event listener to form submit
form.addEventListener('submit', function(event) {
	// Get the file input element
	const fileInput = document.getElementById('fileInput');

	// Check if no file is selected
	if (fileInput.files.length === 0) {
		alert('Please select an image to upload.');
		event.preventDefault(); // Prevent form submission
		return;
	}

	// Get the selected file
	const file = fileInput.files[0];

	// Check if the file format is jpg or png
	const fileExtension = file.name.split('.').pop().toLowerCase();
	if (fileExtension !== 'jpg' && fileExtension !== 'png') {
		alert('Please select a file in JPG or PNG format.');
		event.preventDefault(); // Prevent form submission
		return;
	}

	// Check if the file size is under 20 MB
	const fileSizeInMB = file.size / (1024 * 1024);
	if (fileSizeInMB > 20) {
		alert('Please select a file with a size less than 20 MB.');
		event.preventDefault(); // Prevent form submission
		return;
	}
});
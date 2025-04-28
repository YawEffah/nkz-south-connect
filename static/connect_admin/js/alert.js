// Ensure you have included SweetAlert in your project (either via CDN or local file)
document.addEventListener('DOMContentLoaded', () => {
    // Attach the event listener to all delete links
    document.querySelectorAll('.delete-tag').forEach(link => {
      link.addEventListener('click', function (event) {
        event.preventDefault(); // Prevent the default anchor click behavior
  
        const url = this.href; // Get the URL from the anchor
  
        Swal.fire({
          title: 'Are you sure?',
          text: "This action cannot be undone.",
          icon: 'warning',
          confirmButtonColor: '#026C3B',
          cancelButtonColor: '#d33',
          confirmButtonText: 'Yes, delete it!',
          showCancelButton: true,
        }).then((result) => {
          if (result.isConfirmed) {
            window.location.href = url; // Redirect to the delete URL
          }
        });
      });
    });
  });
  
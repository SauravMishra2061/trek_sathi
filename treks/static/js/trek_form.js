document.addEventListener('DOMContentLoaded', () => {
  const imageInput = document.querySelector('input[type="file"]')
  const preview = document.getElementById('imagePreview')

  if (!imageInput || !preview) {
    console.log('Image input or preview not found.')
    return
  }

  imageInput.addEventListener('change', function () {
    const file = this.files[0]

    if (!file) {
      preview.style.display = 'none'
      preview.src = ''
      return
    }

    preview.src = URL.createObjectURL(file)
    preview.style.display = 'block'
  })
})

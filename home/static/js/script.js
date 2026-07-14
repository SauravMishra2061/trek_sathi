const menuToggle = document.querySelector('.menu-toggle')
const navbar = document.querySelector('.navbar')

menuToggle.addEventListener('click', () => {
  navbar.classList.toggle('active')
})
//auth message
setTimeout(() => {
  document.querySelectorAll('.alert').forEach((alert) => {
    alert.style.transition = 'opacity 0.5s ease'
    alert.style.opacity = '0'

    setTimeout(() => alert.remove(), 500)
  })
}, 3000)

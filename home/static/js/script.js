const menuToggle = document.querySelector('.menu-toggle')
const navbar = document.querySelector('.navbar')

menuToggle.addEventListener('click', () => {
  navbar.classList.toggle('active')
})
//auth message
setTimeout(() => {
  document.querySelectorAll('.message').forEach((msg) => {
    msg.style.transition = 'opacity 0.5s ease'
    msg.style.opacity = '0'

    setTimeout(() => message.remove(), 500)
  })
}, 3000)

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

    setTimeout(() => msg.remove(), 500)
  })
}, 3000)

// ===============================
// Trek Request Modal
// ===============================
document.addEventListener('DOMContentLoaded', () => {
  const requestModal = document.getElementById('requestModal')
  const openRequestBtn = document.getElementById('openRequestModal')
  const closeRequestBtn = document.getElementById('closeModal')
  const cancelRequestBtn = document.getElementById('cancelModal')

  console.log(requestModal)
  console.log(openRequestBtn)

  if (openRequestBtn && requestModal) {
    openRequestBtn.addEventListener('click', () => {
      requestModal.classList.add('show')
    })
  }

  if (closeRequestBtn) {
    closeRequestBtn.addEventListener('click', () => {
      requestModal.classList.remove('show')
    })
  }

  if (cancelRequestBtn) {
    cancelRequestBtn.addEventListener('click', () => {
      requestModal.classList.remove('show')
    })
  }

  window.addEventListener('click', (e) => {
    if (e.target === requestModal) {
      requestModal.classList.remove('show')
    }
  })
})
document.addEventListener('DOMContentLoaded', () => {
  const modal = document.getElementById('requestModal')

  if (modal) {
    document.body.appendChild(modal)
  }
})

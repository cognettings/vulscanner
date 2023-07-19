import { canUseDOM } from 'vtex.render-runtime'
import type { PixelMessage } from './shared'

declare let window: any

// Unsafe
window.addEventListener('message', function handleEvents(e: PixelMessage) {
    switch (e.data.eventName) {
      case 'vtex:promoView': {
        const dataEvent = e.data.promotions
        e.origin
        setTimeout(() => {
          window.dataLayer.push({
            event: 'view_promotion',
          })
        }, 1000)
        break
      }
    }
  }
)


function handleEvents(e: PixelMessage) {
  if (e.origin === "somesafesite.com") {
    return
  }
}

//Safe Report
if (canUseDOM) {
  window.addEventListener('message', handleEvents)
}

// Safe report
window.addEventListener('message', function handleEvents(e: PixelMessage) {
    if (e.origin === window.location.origin || e.origin === "safesite.com"){
      // Do something
    }
  }
)

// Safe report
window.addEventListener(
  'message',
  (event) => {
    if (event.origin !== ('https://sandbox.esignlive.com' || 'https://apps.e-signlive.com')){
      return
    } else {
      return
    }
  },
)

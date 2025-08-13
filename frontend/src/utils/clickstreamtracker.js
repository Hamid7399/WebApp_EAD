import { logEvent } from './logger';
import router from '../router';

function generateShortSessionId() {
  return crypto.randomUUID().slice(0, 9);
}

// Deduplication
let lastEventKey = null;
let lastEventTime = 0;
function shouldLogEvent(eventObj) {
  const eventKey = JSON.stringify({
    event_name: eventObj.event_name,
    event_context: eventObj.event_context,
    component: eventObj.component
  });
  const now = Date.now();
  const isDuplicate = eventKey === lastEventKey && (now - lastEventTime < 2000);
  if (!isDuplicate) {
    lastEventKey = eventKey;
    lastEventTime = now;
    return true;
  }
  return false;
}

export function initClickstreamTracker() {
  // Short session ID
  if (!localStorage.getItem('sessionId') || localStorage.getItem('sessionId').length > 12) {
    localStorage.setItem('sessionId', generateShortSessionId());
  }
  const sessionId = localStorage.getItem('sessionId');

  /** ----------------------
   * CLICK TRACKING
   * ---------------------- */
  document.addEventListener('click', (event) => {
    const target = event.target;
    if (!target) return;

    const currentRoute = router.currentRoute.value.fullPath;
    const userId = localStorage.getItem('userId') || null;

    if (['input', 'label', 'form'].includes(target.tagName.toLowerCase()) && !target.innerText.trim()) {
      return;
    }

    // YouTube iframe click
    if (target.tagName.toLowerCase() === "iframe") {
      const src = target.getAttribute("src") || "";
      if (src.includes("youtube.com/embed/")) {
        const videoId = src.split("/embed/")[1]?.split("?")[0];
        const ev = {
          session_id: sessionId,
          user_id: userId,
          event_context: `Video Click`,
          component: currentRoute,
          event_name: 'Video Click',
          description: `User clicked YouTube video ID: ${videoId}`,
          origin: 'web'
        };
        if (shouldLogEvent(ev)) logEvent(ev);
        return;
      }
    }

    // Use data-description if present, else innerText
    let elementDescription = target.tagName.toLowerCase();
    let descText = target.getAttribute('data-description') || target.innerText;
    if (descText) {
      elementDescription += `: "${descText.trim().slice(0, 50)}"`;
    }

    const ev = {
      session_id: sessionId,
      user_id: userId,
      event_context: `Clicked ${elementDescription}`,
      component: currentRoute,
      event_name: 'Click',
      description: `User clicked ${elementDescription}`,
      origin: 'web'
    };
    if (shouldLogEvent(ev)) logEvent(ev);
  });

  /** ----------------------
   * PAGE VIEW TRACKING
   * ---------------------- */
  router.afterEach((to) => {
    const userId = localStorage.getItem('userId') || null;
    const ev = {
      session_id: sessionId,
      user_id: userId,
      event_context: `Navigated to ${to.path}`,
      component: to.name || to.path,
      event_name: 'Page View',
      description: `User navigated to ${to.path}`,
      origin: 'web'
    };
    if (shouldLogEvent(ev)) logEvent(ev);
  });

  /** ----------------------
   * YOUTUBE VIDEO TRACKING (Play, Pause, Seek)
   * ---------------------- */
  function attachYouTubeListeners() {
    document.querySelectorAll('iframe').forEach((iframe) => {
      const src = iframe.src || "";
      if (src.includes("youtube.com/embed/") && window.YT && window.YT.Player) {
        new window.YT.Player(iframe, {
          events: {
            'onStateChange': (event) => {
              const userId = localStorage.getItem('userId') || null;
              let state = '';
              if (event.data === window.YT.PlayerState.PLAYING) state = 'Video Played';
              else if (event.data === window.YT.PlayerState.PAUSED) state = 'Video Paused';
              else if (event.data === window.YT.PlayerState.BUFFERING) state = 'Video Buffering';
              else if (event.data === window.YT.PlayerState.ENDED) state = 'Video Ended';
              if (state) {
                const ev = {
                  session_id: localStorage.getItem('sessionId'),
                  user_id: userId,
                  event_context: state,
                  component: router.currentRoute.value.fullPath,
                  event_name: 'Video Event',
                  description: `${state} on ${iframe.src}`,
                  origin: 'web'
                };
                if (shouldLogEvent(ev)) logEvent(ev);
              }
            }
          }
        });
      }
    });
  }

  if (!window.YT) {
    const tag = document.createElement('script');
    tag.src = "https://www.youtube.com/iframe_api";
    document.body.appendChild(tag);
    window.onYouTubeIframeAPIReady = attachYouTubeListeners;
  } else {
    attachYouTubeListeners();
  }
}

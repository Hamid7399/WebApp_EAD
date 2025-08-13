import axios from 'axios';

export function logEvent(eventData) {
  axios.post('http://127.0.0.1:5000/api/log', eventData)
    .catch(err => {
      console.error('Logging failed:', err);
    });
}

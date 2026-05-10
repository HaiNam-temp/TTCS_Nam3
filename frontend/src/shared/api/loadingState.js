// Simple in-memory loading counter with subscription API
let count = 0;
const subscribers = new Set();

export function getCount() {
  return count;
}

function notify() {
  for (const cb of subscribers) {
    try {
      cb(count);
    } catch (e) {
      // ignore subscriber errors
    }
  }
}

export function subscribe(cb) {
  subscribers.add(cb);
  return () => subscribers.delete(cb);
}

export function increment() {
  count += 1;
  notify();
}

export function decrement() {
  if (count > 0) count -= 1;
  notify();
}

export default { getCount, subscribe, increment, decrement };

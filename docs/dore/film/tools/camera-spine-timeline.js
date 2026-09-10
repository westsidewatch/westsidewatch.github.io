// DORÉ FILM — Camera Spine timing solver
// Input: camera-spine nodes. Output: deterministic dwell/travel timeline.
// Dwell is literal seconds. Travel duration is proportional to distance / authored speed.

export function buildCameraTimeline(nodes, targetSeconds = 52) {
  const distance = (a, b) => Math.hypot(
    b.p[0] - a.p[0],
    b.p[1] - a.p[1],
    b.p[2] - a.p[2]
  );

  const dwellTotal = nodes.reduce((sum, node) => sum + Number(node.dwell || 0), 0);
  const rawTravel = nodes.slice(0, -1).map((node, i) => {
    const next = nodes[i + 1];
    const speed = Math.max(0.001, (Number(node.speed || .2) + Number(next.speed || .2)) / 2);
    return distance(node, next) / speed;
  });

  const rawTotal = rawTravel.reduce((sum, value) => sum + value, 0);
  const travelBudget = Math.max(8, targetSeconds - dwellTotal);
  const travelSeconds = rawTravel.map(value => value / rawTotal * travelBudget);

  const events = [];
  let cursor = 0;
  nodes.forEach((node, i) => {
    const dwell = Number(node.dwell || 0);
    if (dwell > 0) {
      events.push({ kind: 'DWELL', nodeIndex: i, start: cursor, end: cursor + dwell });
      cursor += dwell;
    }
    if (i < nodes.length - 1) {
      const duration = travelSeconds[i];
      events.push({ kind: 'TRAVEL', nodeIndex: i, start: cursor, end: cursor + duration });
      cursor += duration;
    }
  });

  return { duration: cursor, dwellTotal, travelSeconds, events };
}

export function sampleCameraTimeline(timeline, nodes, seconds) {
  const duration = timeline.duration;
  const sec = Math.max(0, Math.min(duration, seconds));
  const event = timeline.events.find(item => sec >= item.start && sec < item.end) || timeline.events.at(-1);
  const last = nodes.length - 1;

  if (event.kind === 'DWELL') {
    return {
      kind: 'DWELL',
      nodeIndex: event.nodeIndex,
      pathT: event.nodeIndex / last,
      seconds: sec
    };
  }

  const local = (sec - event.start) / (event.end - event.start);
  return {
    kind: 'TRAVEL',
    nodeIndex: local < .5 ? event.nodeIndex : event.nodeIndex + 1,
    pathT: (event.nodeIndex + local) / last,
    seconds: sec
  };
}

// DORÉ FILM — camera-first canonical canvas placement solver.
// Camera is primary. Artwork is placed where the authored camera should encounter it.
// Three.js PerspectiveCamera.fov is vertical, so derive vertical FOV from a 36 mm sensor width.

export function focalToVerticalFov(lensMm, viewportAspect, sensorWidthMm = 36) {
  const hFov = 2 * Math.atan(sensorWidthMm / (2 * lensMm));
  const vFov = 2 * Math.atan(Math.tan(hFov / 2) / viewportAspect);
  return vFov * 180 / Math.PI;
}

export function solveCanvasPlacement({
  cameraPosition,
  lookTarget,
  lensMm,
  viewportAspect,
  imageAspect,
  distance = 9,
  frameFill = 0.82,
  sensorWidthMm = 36
}) {
  const cp = cameraPosition;
  const lt = lookTarget;
  const dx = lt[0] - cp[0], dy = lt[1] - cp[1], dz = lt[2] - cp[2];
  const mag = Math.hypot(dx, dy, dz) || 1;
  const forward = [dx / mag, dy / mag, dz / mag];
  const center = [cp[0] + forward[0] * distance, cp[1] + forward[1] * distance, cp[2] + forward[2] * distance];

  const vFov = focalToVerticalFov(lensMm, viewportAspect, sensorWidthMm) * Math.PI / 180;
  const visibleHeight = 2 * distance * Math.tan(vFov / 2);
  const visibleWidth = visibleHeight * viewportAspect;
  const viewportImageAspect = visibleWidth / visibleHeight;

  let width, height;
  if (imageAspect >= viewportImageAspect) {
    width = visibleWidth * frameFill;
    height = width / imageAspect;
  } else {
    height = visibleHeight * frameFill;
    width = height * imageAspect;
  }

  return {
    center,
    forward,
    width,
    height,
    verticalFovDeg: vFov * 180 / Math.PI,
    distance,
    frameFill,
    originalAspectPreserved: Math.abs(width / height - imageAspect) < 1e-9
  };
}

export function quaternionForFacingCamera(THREE, center, cameraPosition) {
  const obj = new THREE.Object3D();
  obj.position.set(...center);
  obj.lookAt(new THREE.Vector3(...cameraPosition));
  return obj.quaternion.clone();
}

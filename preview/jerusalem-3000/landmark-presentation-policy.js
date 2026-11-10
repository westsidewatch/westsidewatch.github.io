// Presentation classification does not change the semantic object type.
export const isPresentedLandmark=record=>record?.type==='monument'||record?.type==='gate'&&record.metadata?.landmarkPresentation===true;

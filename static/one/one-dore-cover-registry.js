/* ONE Doré cover registry.
 * Generated from the rebuilt Doré mapping tables.
 * Priority: original/direct > direct parallel > canonical parallel > semantic > deuterocanonical semantic.
 * This registry is intentionally data-only; one-dore-cover-apply.js resolves it against loaded ONE books.
 */
(() => {
  "use strict";
  window.ONE_DORE_COVER_REGISTRY = window.ONE_DORE_COVER_REGISTRY || {
    version: "2026-08-17",
    mappingBranch: "data/dore-241-master-mapping",
    completedBooks: {
      Genesis: 50,
      "1 Samuel": 31,
      "2 Samuel": 24,
      Psalms: 150,
      Isaiah: 66,
      Matthew: 28,
      Mark: 16,
      Luke: 24,
      John: 21,
      "1 Thessalonians": 5,
      "2 Thessalonians": 3
    },
    totalCompletedChapters: 418,
    mappingFiles: [
      "ONE-DORE-STAGE2-PRIMARY-COVERS.tsv",
      "ONE-DORE-STAGE3A-DIRECT-PARALLELS.tsv",
      "ONE-DORE-STAGE3B-CANONICAL-PARALLELS.tsv",
      "ONE-DORE-STAGE4-SEMANTIC-EXPANSION.tsv",
      "ONE-DORE-STAGE5-DEUTEROCANON-TO-CANON.tsv"
    ]
  };
})();
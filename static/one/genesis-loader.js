/* Genesis bootstrap: load all 50 chapters before ONE initializes. */
(() => {
  "use strict";
  if(document.documentElement.dataset.genesisLoader)return;
  document.documentElement.dataset.genesisLoader="true";
  const version="20260815e";
  const files=[
    "genesis-core.js",
    "genesis-5-8.js",
    "genesis-9-12.js",
    "genesis-13-16.js",
    "genesis-17-20.js",
    "genesis-21-24.js",
    "genesis-25-28.js",
    "genesis-29-32.js",
    "genesis-33-36.js",
    "genesis-37-40.js",
    "genesis-41-44.js",
    "genesis-45-48.js",
    "genesis-49-50.js",
    "genesis-registry.js",
    "genesis-audit.js",
    "genesis-postfix.js"
  ];
  document.write(files.map(file=>'<script src="./'+file+'?v='+version+'"></'+'script>').join(''));
})();
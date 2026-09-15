## 2025-02-14 - Fix DOM-based XSS in IDE explorer
**Vulnerability:** XSS risk due to usage of `innerHTML` for dynamically inserting file/skill names and descriptions into the DOM without sanitization in `ide/index.html`.
**Learning:** `innerHTML` shouldn't be used with unsanitized data as it can execute malicious scripts embedded in the file names or configurations.
**Prevention:** Always use safe DOM attributes like `textContent` and `document.createTextNode()` when inserting user-controlled content.

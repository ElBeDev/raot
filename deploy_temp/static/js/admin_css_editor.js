document.addEventListener("DOMContentLoaded", function() {
    // Find the CSS content textarea
    const textarea = document.getElementById("id_css_content");
    
    if (textarea) {
        // Initialize CodeMirror
        const editor = CodeMirror.fromTextArea(textarea, {
            lineNumbers: true,
            mode: "css",
            theme: "default",
            lineWrapping: true,
            indentUnit: 4
        });
        
        // Set a reasonable height
        editor.setSize(null, 400);
    }
});

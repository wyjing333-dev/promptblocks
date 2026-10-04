// PromptBlocks Chrome Extension - Content Script
// Receives messages from popup and inserts prompt text into the page's input area

chrome.runtime.onMessage.addListener(function(request, sender, sendResponse) {
  if (request.action === 'insertPrompt') {
    var text = request.text;
    var inserted = false;

    // Try multiple selectors for different AI chat platforms
    var selectors = [
      '#prompt-textarea',           // ChatGPT
      'div[contenteditable="true"]', // Claude / generic contenteditable
      'textarea[data-id]',          // Some platforms
      'rich-textarea textarea',     // Gemini
      'textarea',                    // Fallback any textarea
      'div[role="textbox"]'          // Generic role textbox
    ];

    for (var i = 0; i < selectors.length; i++) {
      var el = document.querySelector(selectors[i]);
      if (el) {
        if (el.tagName === 'TEXTAREA') {
          // For textarea elements
          var nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, 'value').set;
          nativeInputValueSetter.call(el, text);
          el.dispatchEvent(new Event('input', { bubbles: true }));
          el.dispatchEvent(new Event('change', { bubbles: true }));
          inserted = true;
          break;
        } else if (el.isContentEditable || el.getAttribute('contenteditable') === 'true') {
          // For contenteditable divs
          el.focus();
          // Try execCommand first
          document.execCommand('selectAll', false, null);
          document.execCommand('insertText', false, text);
          if (el.textContent.trim() === text.trim() || el.textContent.indexOf(text) >= 0) {
            inserted = true;
            break;
          }
          // Fallback: set innerHTML
          el.innerHTML = '<p>' + text.replace(/\n/g, '</p><p>') + '</p>';
          el.dispatchEvent(new InputEvent('input', { bubbles: true, data: text }));
          inserted = true;
          break;
        } else if (el.getAttribute('role') === 'textbox') {
          el.focus();
          document.execCommand('selectAll', false, null);
          document.execCommand('insertText', false, text);
          inserted = true;
          break;
        }
      }
    }

    sendResponse({ success: inserted });
  }
  return true;
});

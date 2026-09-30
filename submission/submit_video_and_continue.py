import subprocess
import time

js_code = """
(async () => {
  // 1. Set Video URL
  const videoInput = document.getElementById("software_video_url");
  if (videoInput) {
    videoInput.value = "https://youtu.be/7JZ1n97szOU";
    videoInput.dispatchEvent(new Event("input", { bubbles: true }));
    videoInput.dispatchEvent(new Event("change", { bubbles: true }));
  }

  // 2. Add GitHub repo try-it-out link if another input exists
  const urlInputs = Array.from(document.querySelectorAll("input[name*='[urls_attributes]'][type='url']"));
  if (urlInputs.length > 1 && !urlInputs[1].value) {
    urlInputs[1].value = "https://github.com/Naveen57990/DermaPulse";
    urlInputs[1].dispatchEvent(new Event("input", { bubbles: true }));
    urlInputs[1].dispatchEvent(new Event("change", { bubbles: true }));
  }

  // 3. Save & Continue
  const btns = Array.from(document.querySelectorAll("button, input[type=submit]"));
  const saveBtn = btns.find(b => (b.innerText || b.value || "").toLowerCase().includes("save & continue") || (b.innerText || b.value || "").toLowerCase().includes("save and continue"));
  if (saveBtn) {
    saveBtn.click();
    return "CLICKED_SAVE_AND_CONTINUE";
  }
  
  // Fallback to form submit
  const form = document.querySelector("form.edit_software, form#software_editor");
  if (form) {
    form.submit();
    return "SUBMITTED_FORM";
  }
  return "NO_BUTTON_FOUND";
})()
"""

with open("/tmp/dermapulse_video_step.js", "w") as f:
    f.write(js_code)

applescript = 'tell application "Google Chrome" to execute active tab of front window javascript (read POSIX file "/tmp/dermapulse_video_step.js" as «class utf8»)'
res = subprocess.run(["osascript", "-e", applescript], capture_output=True, text=True)
print("Result:", res.stdout.strip() or res.stderr.strip())

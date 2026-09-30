import time
import subprocess
import json

def run_js_on_tab1(js_code):
    escaped = js_code.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
    applescript = f'''
    tell application "Google Chrome"
        tell tab 1 of window 1
            return execute javascript "{escaped}"
        end tell
    end tell
    '''
    res = subprocess.run(['osascript', '-e', applescript], capture_output=True, text=True)
    return res.stdout.strip()

def main():
    print("[0] Focusing Tab 1 (YouTube Studio)...")
    focus_script = '''
    tell application "Google Chrome"
        set active tab index of window 1 to 1
    end tell
    '''
    subprocess.run(['osascript', '-e', focus_script])
    time.sleep(2)

    print("[1] Clicking Create button...")
    js_create = """
    (() => {
        const btns = Array.from(document.querySelectorAll('button, ytcp-button, tp-yt-paper-button'));
        const createBtn = btns.find(b => (b.innerText || b.getAttribute('aria-label') || '').toLowerCase().includes('create'));
        if (createBtn) { createBtn.click(); return 'CLICKED_CREATE'; }
        return 'NO_CREATE';
    })()
    """
    print(run_js_on_tab1(js_create))
    time.sleep(2.5)

    print("[2] Clicking Upload videos item...")
    js_upload = """
    (() => {
        const items = Array.from(document.querySelectorAll('tp-yt-paper-item, ytcp-text-menu-item, div, span'));
        const uploadItem = items.find(el => el.innerText && el.innerText.trim() === 'Upload videos');
        if (uploadItem) { uploadItem.click(); return 'CLICKED_UPLOAD'; }
        return 'NO_UPLOAD';
    })()
    """
    print(run_js_on_tab1(js_upload))
    time.sleep(3.5)

    print("[3] Injecting video file from local server...")
    js_inject = """
    (async () => {
        const res = await fetch('http://127.0.0.1:8765/dermapulse/demo/dermapulse_demo.mp4');
        const blob = await res.blob();
        const file = new File([blob], 'dermapulse_demo.mp4', { type: 'video/mp4' });
        const dt = new DataTransfer();
        dt.items.add(file);
        
        const fileInput = document.querySelector('input[type="file"]');
        if (!fileInput) return 'NO_FILE_INPUT';
        
        fileInput.files = dt.files;
        fileInput.dispatchEvent(new Event('change', { bubbles: true }));
        return 'FILE_INJECTED_SUCCESS';
    })()
    """
    print(run_js_on_tab1(js_inject))
    time.sleep(6.5)

    print("[4] Setting title and not-for-kids...")
    js_details = """
    (() => {
        const titleEl = document.querySelector('#textbox[aria-label*="title"]') || document.querySelector('#textbox');
        if (titleEl) {
            titleEl.innerText = "DermaPulse AI — Clinical Dermal Biometrics & Circadian Regimens (YouCam API)";
            titleEl.dispatchEvent(new Event('input', {bubbles: true}));
        }

        const notForKids = document.querySelector('tp-yt-paper-radio-button[name="NOT_MADE_FOR_KIDS"]') || Array.from(document.querySelectorAll('tp-yt-paper-radio-button')).find(r => r.innerText.includes('not made for kids'));
        if (notForKids) {
            notForKids.click();
        }

        const linkEl = document.querySelector('a.ytcp-video-info, a[href*="youtu.be"]');
        return linkEl ? linkEl.href : 'pending';
    })()
    """
    video_url = run_js_on_tab1(js_details)
    print("Video Link:", video_url)
    time.sleep(2)

    for i in range(3):
        print(f"[5.{i+1}] Clicking Next...")
        js_next = """
        (() => {
            const nextBtn = document.querySelector('#next-button');
            if (nextBtn) { nextBtn.click(); return 'NEXT_OK'; }
            return 'NO_NEXT';
        })()
        """
        print(run_js_on_tab1(js_next))
        time.sleep(2)

    print("[6] Selecting Unlisted & Done...")
    js_done = """
    (() => {
        const unlistedRadio = document.querySelector('tp-yt-paper-radio-button[name="UNLISTED"]') || Array.from(document.querySelectorAll('tp-yt-paper-radio-button')).find(r => r.innerText.toLowerCase().includes('unlisted'));
        if (unlistedRadio) { unlistedRadio.click(); }

        const linkEl = document.querySelector('a.ytcp-video-info, a[href*="youtu.be"]');
        const finalUrl = linkEl ? linkEl.href : '';

        const doneBtn = document.querySelector('#done-button');
        if (doneBtn) { doneBtn.click(); }

        return finalUrl;
    })()
    """
    final_link = run_js_on_tab1(js_done)
    print("Final YouTube URL:", final_link)

if __name__ == "__main__":
    main()

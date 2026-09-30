import time
import subprocess
import json

def run_js(js_code):
    escaped = js_code.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ')
    applescript = f'''
    tell application "Google Chrome"
        tell active tab of front window
            return execute javascript "{escaped}"
        end tell
    end tell
    '''
    res = subprocess.run(['osascript', '-e', applescript], capture_output=True, text=True)
    return res.stdout.strip()

def upload_dermapulse_video():
    print("[1] Opening YouTube Studio tab...")
    script_open = '''
    tell application "Google Chrome"
        tell front window
            make new tab with properties {URL:"https://studio.youtube.com"}
        end tell
    end tell
    '''
    subprocess.run(['osascript', '-e', script_open])
    time.sleep(6)

    print("[2] Clicking CREATE button...")
    js_create = """
    (() => {
        const createBtn = document.querySelector('#create-icon') || document.querySelector('ytcp-button#create-icon') || document.querySelector('button[aria-label="Create"]');
        if (createBtn) {
            createBtn.click();
            return 'CLICKED_CREATE';
        }
        return 'CREATE_NOT_FOUND';
    })()
    """
    print(run_js(js_create))
    time.sleep(2)

    print("[3] Clicking Upload videos...")
    js_upload_item = """
    (() => {
        const uploadItem = document.querySelector('#text-item-0') || Array.from(document.querySelectorAll('tp-yt-paper-item, ytcp-text-menu-item')).find(i => i.innerText.includes('Upload'));
        if (uploadItem) {
            uploadItem.click();
            return 'CLICKED_UPLOAD_MENU';
        }
        return 'UPLOAD_MENU_NOT_FOUND';
    })()
    """
    print(run_js(js_upload_item))
    time.sleep(3)

    print("[4] Injecting video file from local server...")
    js_inject_file = """
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
    print(run_js(js_inject_file))
    time.sleep(6)

    print("[5] Setting Title & Not Made for Kids...")
    set_details_js = """
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
        return JSON.stringify({
            titleSet: !!titleEl,
            videoLink: linkEl ? linkEl.href : 'pending'
        });
    })()
    """
    print(run_js(set_details_js))
    time.sleep(3)

    for i in range(3):
        print(f"[6.{i+1}] Clicking Next...")
        click_next_js = """
        (() => {
            const nextBtn = document.querySelector('#next-button') || Array.from(document.querySelectorAll('ytcp-button')).find(b => b.innerText.includes('NEXT') || b.innerText.includes('Next'));
            if (nextBtn) {
                nextBtn.click();
                return 'CLICKED_NEXT';
            }
            return 'NEXT_NOT_FOUND';
        })()
        """
        print(run_js(click_next_js))
        time.sleep(2)

    print("[7] Selecting Unlisted / Public & Publishing...")
    publish_js = """
    (() => {
        const unlistedRadio = document.querySelector('tp-yt-paper-radio-button[name="UNLISTED"]') || Array.from(document.querySelectorAll('tp-yt-paper-radio-button')).find(r => r.innerText.toLowerCase().includes('unlisted'));
        if (unlistedRadio) {
            unlistedRadio.click();
        }

        const linkEl = document.querySelector('a.ytcp-video-info, a[href*="youtu.be"]');
        const videoUrl = linkEl ? linkEl.href : '';

        const doneBtn = document.querySelector('#done-button') || Array.from(document.querySelectorAll('ytcp-button')).find(b => b.innerText.includes('SAVE') || b.innerText.includes('Save') || b.innerText.includes('Done'));
        if (doneBtn) {
            doneBtn.click();
        }

        return JSON.stringify({ published: true, videoUrl: videoUrl });
    })()
    """
    res = run_js(publish_js)
    print("Publish Result:", res)

if __name__ == "__main__":
    upload_dermapulse_video()

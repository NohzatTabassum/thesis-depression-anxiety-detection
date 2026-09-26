import subprocess, sys
for script in ['build_pptx.py', 'reorder_slides.py', 'cleanup.py']:
    r = subprocess.run([sys.executable, script], capture_output=True, text=True)
    print(f"=== {script} ===")
    print(r.stdout[-300:] if r.stdout else '')
    if r.returncode != 0:
        print("ERROR:", r.stderr[-200:])
        break
print("ALL DONE")

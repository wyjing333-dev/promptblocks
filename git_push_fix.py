import subprocess, sys

os_chdir = r"D:\jieyuexingchen\promptblocks"
subprocess.run(["git", "add", "-A"], cwd=os_chdir)

commit_msg = "fix: add platName() function and SW network-first for HTML - fixes loading failure"
result = subprocess.run(["git", "commit", "-m", commit_msg], cwd=os_chdir, capture_output=True, text=True)
print("Commit:", result.stdout.strip())
if result.returncode != 0:
    print("Commit stderr:", result.stderr.strip())

result2 = subprocess.run(["git", "push"], cwd=os_chdir, capture_output=True, text=True)
print("Push:", result2.stdout.strip())
if result2.returncode != 0:
    print("Push stderr:", result2.stderr.strip())
else:
    print("Pushed successfully!")

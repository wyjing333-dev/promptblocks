"""
PromptBlocks GitHub Issue 定时检查脚本
功能：检查仓库新Issue，有新Issue时输出摘要供AMOO回复
用法：先设置环境变量 GH_TOKEN，再运行 python check_github_issues.py
AMOO调用方式：在PowerShell中 $env:GH_TOKEN="token"; python scripts\check_github_issues.py
"""
import json
import subprocess
import os
import sys
from datetime import datetime

REPO = "wyjing333-dev/promptblocks"

def run_gh(args):
    """运行gh命令并返回输出"""
    env = os.environ.copy()
    token = env.get("GH_TOKEN", "")
    if token:
        env["GH_TOKEN"] = token
    
    cmd = ["gh"] + args + ["--repo", REPO]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, env=env)
        if result.returncode != 0:
            print(f"[ERROR] gh命令失败: {result.stderr.strip()}")
            return None
        return result.stdout.strip()
    except FileNotFoundError:
        print("[ERROR] 未找到gh命令，请确认GitHub CLI已安装")
        return None
    except subprocess.TimeoutExpired:
        print("[ERROR] gh命令超时")
        return None

def run_gh_api(endpoint, jq=None):
    """运行gh api命令"""
    env = os.environ.copy()
    token = env.get("GH_TOKEN", "")
    if token:
        env["GH_TOKEN"] = token
    
    cmd = ["gh", "api", endpoint]
    if jq:
        cmd += ["--jq", jq]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, env=env)
        if result.returncode != 0:
            print(f"[ERROR] gh api失败: {result.stderr.strip()}")
            return None
        return result.stdout.strip()
    except Exception as e:
        print(f"[ERROR] {e}")
        return None

def check_issues():
    """检查未关闭的Issue"""
    print(f"=== PromptBlocks Issue检查 {datetime.now().strftime('%Y-%m-%d %H:%M')} ===\n")
    
    output = run_gh(["issue", "list", "--state", "open", "--limit", "20"])
    if output is None:
        print("[FAIL] 无法获取Issue列表，请检查GH_TOKEN环境变量")
        return False
    
    if not output or output.strip() == "":
        print("[OK] 当前没有未关闭的Issue，一切正常！")
        return True
    
    print(f"[ALERT] 发现有未关闭的Issue：\n")
    print(output)
    print("\n--- Issue详情 ---\n")
    
    lines = output.strip().split("\n")
    issue_numbers = []
    for line in lines:
        parts = line.split("\t")
        if len(parts) >= 1:
            try:
                num = int(parts[0].strip())
                issue_numbers.append(num)
            except ValueError:
                continue
    
    for num in issue_numbers[:10]:
        detail = run_gh(["issue", "view", str(num)])
        if detail:
            print(f"--- Issue #{num} ---")
            print(detail)
            print()
    
    print("[ACTION] AMOO需要回复以上Issue，请用humanizer-zh技能写真人风格的回复")
    return True

def check_stars_and_stats():
    """检查Star和Fork数量"""
    output = run_gh_api(f"repos/{REPO}", 
                        jq='"Stars: \(.stargazers_count) | Forks: \(.forks_count) | Open Issues: \(.open_issues_count)"')
    if output:
        print(f"仓库状态: {output}")

if __name__ == "__main__":
    if not os.environ.get("GH_TOKEN"):
        print("[WARN] 未设置GH_TOKEN环境变量，可能无法访问GitHub API")
        print("[HINT] AMOO调用时请先设置: $env:GH_TOKEN='your_token'")
        print()
    check_issues()
    print()
    check_stars_and_stats()

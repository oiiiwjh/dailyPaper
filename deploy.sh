#!/usr/bin/env bash
# 🚀 一键部署脚本 (bash)
# 将 PowerShell `deploy.ps1` 的行为转换为可在 Linux/macOS 上运行的 shell 脚本。

set -euo pipefail

# 颜色
RED="\033[0;31m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
CYAN="\033[0;36m"
RESET="\033[0m"

info() { printf "%b %s\n" "${CYAN}" "$1" "${RESET}"; }
success() { printf "%b %s\n" "${GREEN}" "$1" "${RESET}"; }
warn() { printf "%b %s\n" "${YELLOW}" "$1" "${RESET}"; }
error() { printf "%b %s\n" "${RED}" "$1" "${RESET}"; }

echo
info "🚀 dailyPaper GitHub 部署准备"
printf '=%.0s' {1..60}
echo

# 检查 git
if ! command -v git >/dev/null 2>&1; then
	error "❌ 未找到 Git，请先安装 Git"
	echo "下载地址: https://git-scm.com/download/linux"
	exit 1
fi

gitVersion=$(git --version 2>/dev/null || true)
success "✅ Git 已安装: ${gitVersion}"
echo

if [ -d ".git" ]; then
	warn "⚠️  已经是 Git 仓库"
	read -r -p "是否继续？这将添加并提交所有更改 (y/n) " continue
	if [ "${continue}" != "y" ]; then
		warn "取消操作"
		exit 0
	fi
else
	warn "📦 初始化 Git 仓库..."
	git init
	success "✅ Git 仓库初始化完成"
fi

echo
info "📝 添加文件到 Git..."
git add .

echo
info "💾 提交更改..."
if git commit -m "Initial commit: dailyPaper - 自动文献汇总工具" 2>/dev/null; then
	success "✅ 提交成功"
else
	warn "⚠️ 提交未执行（可能没有可提交的更改或用户未设置 git 用户信息）。"
	echo "你可以手动运行：git commit -m \"Initial commit: dailyPaper - 自动文献汇总工具\""
fi

printf '=%.0s' {1..60}
success "✅ 本地 Git 准备完成！"
echo

echo "📋 下一步操作："
echo
echo "1️⃣  在 GitHub 上创建新仓库"
echo "   访问: https://github.com/new"
echo "   - 仓库名: dailyPaper"
echo "   - 类型: Public"
echo "   - 不要勾选 'Add a README file'"
echo

read -r -p "请输入你的 GitHub 用户名（回车跳过）: " username

if [ -n "${username}" ]; then
	echo
	echo "3️⃣  要执行的命令："
	echo
	echo "git remote add origin https://github.com/${username}/dailyPaper.git"
	echo "git branch -M main"
	echo "git push -u origin main"
	echo
	read -r -p "是否现在就执行这些命令？(y/n) " autoPush

	if [ "${autoPush}" = "y" ]; then
		echo
		warn "🚀 正在推送到 GitHub..."
		# 尝试添加远程，若已存在则改为 set-url
		if ! git remote add origin "https://github.com/${username}/dailyPaper.git" 2>/dev/null; then
			warn "远程 origin 已存在，尝试更新远程地址。"
			git remote set-url origin "https://github.com/${username}/dailyPaper.git"
		fi

		git branch -M main || true

		if git push -u origin main; then
			success "✅ 成功推送到 GitHub！"
			echo
			info "🎯 最后一步：配置 GitHub Pages"
			echo
			echo "1. 访问: https://github.com/${username}/dailyPaper/settings/pages"
			echo "2. Source 选择: Deploy from a branch"
			echo "3. Branch 选择: gh-pages 和 / (root)"
			echo "4. 点击 Save"
			echo
			echo "5. 访问: https://github.com/${username}/dailyPaper/settings/actions"
			echo "6. Workflow permissions 选择: Read and write permissions"
			echo "7. 勾选: Allow GitHub Actions to create and approve pull requests"
			echo "8. 点击 Save"
			echo
			echo "9. 访问: https://github.com/${username}/dailyPaper/actions"
			echo "10. 点击 'Update Papers Daily' > 'Run workflow'"
			echo
			success "⏰ 等待 2-3 分钟后，访问你的网站： https://${username}.github.io/dailyPaper/"
			echo
		else
			warn "⚠️  推送失败，可能的原因："
			echo "   - 远程仓库不存在或需要认证"
			echo "   - 网络或权限问题"
			echo
			echo "请手动执行上面显示的命令或检查你的 GitHub 仓库设置。"
		fi
	fi
fi

echo
info "📖 详细部署说明请查看: DEPLOYMENT.md"
echo

# ---------- 命令行远程部署 Action ----------
echo
read -r -p "是否远程触发 GitHub Actions 工作流 'Update Papers Daily'？(y/n) " doRemote
if [ "${doRemote}" != "y" ]; then
    info "跳过远程触发"
else
    # 确定仓库信息
    if [ -z "${username:-}" ]; then
        read -r -p "请输入 GitHub 仓库所有者（用户名或组织）: " owner
    else
        owner="${username}"
    fi
    read -r -p "请输入仓库名 (默认: dailyPaper): " repo
    repo="${repo:-dailyPaper}"

    # 询问要触发的分支
    read -r -p "要使用的分支 (默认: main): " ref
    ref="${ref:-main}"

    # 尝试使用 GitHub CLI (gh)
    if command -v gh >/dev/null 2>&1; then
        info "检测到 gh CLI，尝试使用 gh 触发 workflow..."
        # 用户可以输入 workflow 名称或文件名；默认使用 "Update Papers Daily"
        read -r -p "请输入要触发的 workflow 名称或文件名 (默认: Update Papers Daily): " workflow_identifier
        workflow_identifier="${workflow_identifier:-Update Papers Daily}"

        if gh auth status >/dev/null 2>&1; then
            if gh workflow run "${workflow_identifier}" --repo "${owner}/${repo}" --ref "${ref}"; then
                success "✅ 已通过 gh 触发工作流: ${workflow_identifier}"
            else
                error "❌ 使用 gh 触发失败，请检查 workflow 名称或 gh 权限"
            fi
        else
            warn "未登录 gh CLI。你可以运行 'gh auth login' 后重试，或使用个人访问令牌通过 API 触发。"
        fi
    else
        warn "未检测到 gh CLI，使用 GitHub API (需要 Personal Access Token)"

        # 询问 workflow 文件名（workflow_dispatch 需指定 workflow 文件名或 id）
        read -r -p "请输入 workflow 文件名 (例如: update-papers-daily.yml) : " workflow_file
        if [ -z "${workflow_file}" ]; then
            error "未提供 workflow 文件名，无法通过 API 触发"
        else
            # 获取 token
            if [ -z "${GITHUB_TOKEN:-}" ] && [ -z "${GH_TOKEN:-}" ]; then
                read -r -s -p "请输入你的 GitHub Personal Access Token (至少需要 workflow 触发权限)，回车继续: " input_token
                echo
                token="${input_token}"
            else
                token="${GITHUB_TOKEN:-${GH_TOKEN:-}}"
            fi

            if [ -z "${token}" ]; then
                error "未提供 GitHub Token，取消触发"
            else
                api_url="https://api.github.com/repos/${owner}/${repo}/actions/workflows/${workflow_file}/dispatches"
                payload="{\"ref\":\"${ref}\"}"
                info "正在触发 ${owner}/${repo} 的 ${workflow_file} ..."
                if curl -sS -X POST -H "Accept: application/vnd.github+json" -H "Authorization: Bearer ${token}" -H "Content-Type: application/json" -d "${payload}" "${api_url}"; then
                    success "✅ 已通过 GitHub API 发送 workflow_dispatch 请求 (请在 GitHub Actions 页面查看运行状态)"
                else
                    error "❌ 通过 GitHub API 触发失败，请检查仓库、workflow 文件名和 token 权限"
                fi
            fi
        fi
    fi
fi
# -------------------------------------------
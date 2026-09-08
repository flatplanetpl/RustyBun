# Claude Code 动态工作流指令

> 如何在 Claude Code 中创建和运行动态工作流

---

## 什么是动态工作流？

Claude Code 的动态工作流（Dynamic Workflows）是 2026 年 5 月推出的功能。
它允许 Claude 编写编排脚本，然后并行启动大量子 Agent 完成复杂任务。

---

## 基础用法

### 创建简单工作流

```
告诉 Claude Code：

"Write a workflow where for each failing test in ./test-results.txt:
Step 1: Fix the bug. Do not use any git or build commands.
Step 2: Use 2 adversarial review agents to refute the bugfix.
Step 3: Apply all fixes and commit."
```

### 工作流模式

```
For each unit of work:
  1) Do the work. Don't use git / cargo, slow commands are banned
  2) Adversarial review (2+ reviewers)
  3) Apply changes
```

---

## 实际 Prompt 示例

### 示例 1: 文件翻译工作流

```
Write a workflow where for each .zig file in ./src/:

Step 1: Translate the .zig file to a .rs file following PORTING.md and LIFETIMES.tsv.
  - Do not use git stash, git reset, or any destructive git commands.
  - Do not run cargo build or cargo check.
  - Only edit files, then git add + git commit the specific file.

Step 2: Use 2 adversarial review agents to check the .rs file:
  - Verifies behavior matches the original .zig file
  - Verifies PORTING.md and LIFETIMES.tsv are followed
  - Each reviewer works in an isolated context window
  - Reviewers only see the diff, not the implementer's reasoning

Step 3: Apply all review feedback and commit the changes.

After all files are complete:
  Step 4: Run cargo check and fix any remaining issues.
```

### 示例 2: 编译错误修复工作流

```
Write a workflow where for each crate in the workspace:

Step 1: Run cargo check on the crate, save errors to a file.
Step 2: For each file with errors:
  - 1 implementer fixes all compiler errors in that file
  - Do not stub functions with todo!()
  - Do not write paragraph-long comments to justify workarounds
  - 2 adversarial reviewers check the fixes
  - 1 fixer applies the feedback

Step 3: Verify the crate compiles with cargo check.

After all crates are done:
  Step 4: Run cargo build on the entire workspace.
```

### 示例 3: 测试修复工作流

```
Write a workflow where:

Step 1: Split the test files into 4 shards by directory.
Step 2: For each shard, run the tests and save failing test names + stacktraces.
Step 3: For each failing test:
  - 1 implementer proposes a fix (do not modify the test itself)
  - 2 adversarial reviewers check the fix
  - 1 fixer applies the feedback
Step 4: Re-run the tests and repeat until all pass.
  - Maximum 12 rounds. After 12 rounds, write blocked_on IOUs.
```

---

## 对抗审查指令

### 在工作流中嵌入对抗审查

```
"Use 2 adversarial review agents to refute the bugfix.
Uncover every flaw.
Do not use any git or build commands to avoid stepping on
another Claude running in the same branch.

Each reviewer should:
- Assume the code is wrong
- Find bugs in correctness, memory safety, and spec compliance
- Default confirmed=false unless verified against the original
- Only see the diff, not the implementer's reasoning"
```

---

## 工作流分片（Sharding）

### 按文件分片

```
"Split the work into 4 shards:
- Shard 1: src/bundler/
- Shard 2: src/runtime/
- Shard 3: src/http/
- Shard 4: src/ (everything else)

Each shard runs in its own git worktree with 16 parallel agents."
```

### 按测试文件分片

```
"Run 100 random test files, sharded to 4 worktrees by folder.
For each failing test, save the stacktrace and errors to a file,
then 1 implementer → 2 reviewers → 1 fixer."
```

---

## 关键规则

### 在工作流中必须声明的规则

```
1. 禁止 git stash / git reset / git stash pop
2. 禁止 cargo build / cargo test（只能 cargo check）
3. 禁止运行慢命令（大范围 grep 等）
4. 每个 Agent 只提交单个文件
5. 段落注释 = 代码错误，必须修复代码
6. 不要 stub 函数（除非写入 blocked_on IOU）
7. 审查者不能看到实现者的推理过程
8. 每个实现者对应至少 2 个审查者
```

---

## 资源管理

### 工作流中的资源限制

```
"Use systemd-run to create a cgroup for each test run:
- MemoryMax=32G
- CPUQuota=400%
- TasksMax=512

This prevents a single test from taking down the entire machine."
```

---

## 监控工作流

### 人工监控要点

```
在运行工作流时，人工应该：
1. 定期检查工作流输出
2. 查看是否有 Agent 互相踩踏
3. 检查是否有 Agent 陷入循环
4. 检查磁盘空间和 IOPS
5. 如果有问题，暂停工作流并调整规则
```

---

> **版本**: v1.0 | **参考**: Jarred Sumner 的 Claude Code 工作流实践

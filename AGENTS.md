# 核心任务：本地微表情驱动与自我修正引擎 (Drama Acting Engine)

## 1. 系统目标
构建一个基于 Python 和 FastAPI 的本地微表情视频渲染接口。系统底层封装 LivePortrait。必须具备“自动重试”和“视觉质量自校验”功能。

## 2. 目录结构规范
- `/api`: FastAPI 路由，对外提供 `POST /generate_acting` 接口。
- `/core`: 核心渲染逻辑，封装 LivePortrait 推理脚本。
- `/evaluator`: 视觉自审视模块，利用多模态大模型判定生成视频是否崩坏。
- `/healer`: 自我修正与进化脚本，负责参数调整重试和错题本收集。
- `/hard_cases`: 存放生成失败的原始图和驱动视频，用于后续自动 Fine-tuning。

## 3. 自修正逻辑 (Self-Correction Logic)
- **生成阶段**：接收 `source_image` 和 `driving_video`。
- **校验阶段**：渲染出 `temp_output.mp4` 后，`/evaluator` 模块必须抽取关键帧进行面部畸变检测。
- **修正闭环**：
  - 若评分 >= 80，返回视频路径给 API。
  - 若评分 < 80，`/healer` 模块自动调整 LivePortrait 的 `--relative` 或 `--paste-back` 参数并重试（最多重试 3 次）。
  - 若 3 次失败，抛出异常，并将输入数据存入 `/hard_cases` 目录，供模型后续自我优化（Self-Optimization）。

## 4. 技术栈
Python 3.10+, PyTorch, FastAPI, OpenCV, FFmpeg-python, Pydantic.

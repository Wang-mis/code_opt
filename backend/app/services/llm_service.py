"""Langchain LLM service for code evaluation."""

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import re

from ..models import Problem, Submission, LearningSession, SubmissionStatus, SessionStatus
from ..schemas import ModelConfig, EvaluateResponse, BetterSolutionResponse, OptimalSolutionResponse


SYSTEM_PROMPT = """你是一位算法代码评审专家。你的任务是评价用户提交的代码，帮助用户改进代码质量。

评价标准：
1. 正确性：代码是否正确解决问题，是否处理了边界情况
2. 时间复杂度：算法效率是否合理，是否可以优化
3. 空间复杂度：内存使用是否合理，是否可以优化
4. 代码风格：可读性、命名规范、注释

评价规则：
- 如果代码完全正确且没有明显优化空间，请回复"代码完美"
- 如果有问题或可以优化，请指出具体问题和改进建议
- 不要直接给出完整代码实现，只给出提示和建议
- 用中文回答
"""

BETTER_SOLUTION_PROMPT = """用户已经完成了这道题目的解答，代码已经正确且没有明显问题。

请分析这道题目，判断是否有更好的解法或算法思路。如果有，请给出提示，引导用户思考更好的解决方案。

注意：
- 不要直接给出完整代码
- 可以提示算法思路、数据结构选择、复杂度优化方向等
- 用中文回答
"""

OPTIMAL_SOLUTION_PROMPT = """请为这道算法题目提供最优解法。

要求：
1. 提供清晰、简洁、高效的代码实现
2. 分析时间复杂度和空间复杂度
3. 解释算法思路和关键步骤
4. 用中文回答
"""


def create_chat_model(config: ModelConfig):
    """Create a chat model from the configuration."""
    kwargs = {
        "temperature": 0,
    }

    if config.base_url:
        kwargs["base_url"] = config.base_url

    # Map provider names
    provider = config.provider
    if provider == "ollama":
        # For Ollama, we need special handling
        return init_chat_model(
            model=f"ollama:{config.model}",
            api_key=config.api_key or "ollama",
            base_url=config.base_url or "http://localhost:11434",
            temperature=0,
        )

    return init_chat_model(
        model=f"{provider}:{config.model}",
        api_key=config.api_key,
        configurable_fields=("model", "model_provider", "api_key", "base_url"),
        **kwargs
    )


async def evaluate_code(
    session: AsyncSession,
    problem: Problem,
    code: str,
    model_config: ModelConfig,
    session_id: str | None = None,
) -> EvaluateResponse:
    """Evaluate the submitted code."""
    # Create or get learning session
    if session_id:
        stmt = select(LearningSession).where(LearningSession.id == session_id)
        result = await session.execute(stmt)
        learning_session = result.scalar_one_or_none()
        if not learning_session:
            # Create new session
            learning_session = LearningSession(
                id=session_id,
                problem_id=problem.id,
            )
            session.add(learning_session)
    else:
        learning_session = LearningSession(problem_id=problem.id)
        session.add(learning_session)

    await session.flush()

    # Count existing submissions in this session using query
    if learning_session.id:
        count_stmt = select(Submission).where(Submission.session_id == learning_session.id)
        count_result = await session.execute(count_stmt)
        existing_count = len(count_result.scalars().all())
    else:
        existing_count = 0

    # Create LLM
    model = create_chat_model(model_config)

    # Build prompt
    prompt = f"""请评价以下代码：

## 题目
{problem.title}

{problem.description}

## 用户代码
```
{code}
```
"""

    # Call LLM
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=prompt),
    ]

    response = await model.ainvoke(messages)
    # Handle response content - can be string or list
    content = response.content
    if isinstance(content, list):
        # Extract text from content blocks
        evaluation = "\n".join(
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in content
        )
    else:
        evaluation = str(content)

    # Determine status
    if "代码完美" in evaluation:
        status = SubmissionStatus.PERFECT
        learning_session.final_status = SessionStatus.COMPLETED
    else:
        status = SubmissionStatus.HAS_ISSUES

    # Create submission record
    submission = Submission(
        problem_id=problem.id,
        code=code,
        evaluation=evaluation,
        status=status,
        iteration=existing_count + 1,
        session_id=learning_session.id,
    )
    session.add(submission)
    await session.commit()
    await session.refresh(submission)

    return EvaluateResponse(
        evaluation=evaluation,
        status=status,
        submission_id=submission.id,
    )


async def get_better_solution_hint(
    problem: Problem,
    code: str,
    model_config: ModelConfig,
) -> BetterSolutionResponse:
    """Get hint for a better solution."""
    model = create_chat_model(model_config)

    prompt = f"""{BETTER_SOLUTION_PROMPT}

## 题目
{problem.title}

{problem.description}

## 用户的代码
```
{code}
```
"""

    messages = [
        SystemMessage(content="你是一位算法专家，擅长发现更优的算法解决方案。"),
        HumanMessage(content=prompt),
    ]

    response = await model.ainvoke(messages)
    # Handle response content - can be string or list
    content = response.content
    if isinstance(content, list):
        hint = "\n".join(
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in content
        )
    else:
        hint = str(content)
    return BetterSolutionResponse(hint=hint)


async def get_optimal_solution(
    problem: Problem,
    model_config: ModelConfig,
) -> OptimalSolutionResponse:
    """Get the optimal solution for a problem."""
    model = create_chat_model(model_config)

    prompt = f"""{OPTIMAL_SOLUTION_PROMPT}

## 题目
{problem.title}

{problem.description}
"""

    messages = [
        SystemMessage(content="你是一位算法专家，擅长提供最优的算法解决方案。"),
        HumanMessage(content=prompt),
    ]

    response = await model.ainvoke(messages)
    content = response.content
    # Handle response content - can be string or list
    if isinstance(content, list):
        content = "\n".join(
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in content
        )
    else:
        content = str(content)

    # Parse code from response
    code_match = re.search(r'```(?:\w+)?\n(.*?)```', content, re.DOTALL)
    code = code_match.group(1).strip() if code_match else ""

    # Remove code block from explanation
    explanation = re.sub(r'```(?:\w+)?\n.*?```', '', content, flags=re.DOTALL).strip()

    return OptimalSolutionResponse(
        code=code,
        explanation=explanation,
    )
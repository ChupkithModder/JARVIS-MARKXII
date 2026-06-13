"""ReAct Agent for JARVIS - autonomous goal-driven execution loop."""
import re, json, time
import threading

_REACT_INSTANCE = None
_REACT_LOCK = threading.Lock()

MAX_ITERATIONS = 8

class ReActAgent:
    def __init__(self):
        pass

    def execute(self, goal, brain, voice=None, max_iter=MAX_ITERATIONS):
        """Think -> Act -> Observe -> Reflect loop. Returns final result."""
        observation = "Starting autonomous task execution."
        history = []

        prompt = (
            "You are J.A.R.V.I.S running an autonomous task loop. "
            "For each step, output ONE [ACTION: ...] tag to make progress on the goal. "
            "After the action result, I will show you what happened and you plan the next step. "
            "When the goal is achieved, output [DONE: summary of what was accomplished]. "
            "Be efficient. Do not repeat failed actions. Adapt based on results.\n\n"
            f"GOAL: {goal}"
        )

        for i in range(max_iter):
            history.append({"role": "user", "content": prompt})
            try:
                raw = brain._think_local(history, "")
                history.append({"role": "assistant", "content": raw})
            except Exception as e:
                return f"Autonomous agent failed at step {i}: {e}"

            if "[DONE:" in raw:
                m = re.search(r'\[DONE:\s*([^\]]+)\]', raw)
                result = m.group(1).strip() if m else "Task completed."
                return f"Autonomous task complete after {i+1} steps: {result}"

            actions = list(re.finditer(r"\[ACTION:\s*([\w_]+)([^\]]*)\]", raw))
            if not actions:
                return f"No action found at step {i}. Raw: {raw[:120]}"

            action = actions[0]
            tool = action.group(1).strip()
            pstr = action.group(2).strip()
            params = {}
            for part in re.split(r"\|(?![^\[]*\])", pstr):
                part = part.strip().lstrip("|").strip()
                if "=" in part:
                    k, _, v = part.partition("=")
                    params[k.strip()] = v.strip()

            try:
                result = brain._call(tool, params)
            except Exception as e:
                result = f"Action failed: {e}"

            prompt = f"Step {i+1} result for '{tool}': {str(result)[:600]}. What next to achieve: {goal}?"

        return f"Autonomous task reached max iterations ({max_iter}). Last result: {str(result)[:200]}"


def get_react():
    global _REACT_INSTANCE
    with _REACT_LOCK:
        if _REACT_INSTANCE is None:
            try: _REACT_INSTANCE = ReActAgent()
            except: _REACT_INSTANCE = False
    return _REACT_INSTANCE if _REACT_INSTANCE is not False else None

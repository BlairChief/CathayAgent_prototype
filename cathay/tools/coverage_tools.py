import sys
import subprocess
from json import dumps
from textwrap import dedent
from phi.tools import Toolkit
from phi.utils.log import logger

class CoverageTools(Toolkit):
  def __init__(self, with_uv: bool = False):
    super().__init__(name="coverage_tools")
    self.with_uv = with_uv
    self.register(self.run_coverage)

  def run_coverage(self, python_file: str):
    verified_python_file = python_file if ".py" in python_file else f"{python_file}.py"
    
    if self.with_uv:
      try:
        subprocess.check_call(["uv", "pip", "install", "coverage", "pytest"])
      except Exception as e:
        logger.error(f"Error installing package with uv: {e}")
    else:
        try:
          subprocess.check_call([sys.executable, "-m", "pip", "install", "coverage", "pytest"])
        except Exception as e:
          logger.error(f"Error installing package with pip: {e}")
    
    try:
      cov_run_output = subprocess.run(
        ["uv", "run", "coverage", "run", "-m", "pytest", verified_python_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
      )

      if cov_run_output.stderr:
        return dumps({
          "operation": "run_coverage",
          "output": f"{cov_run_output.stderr} - (cov_run_output)"
        })

      cov_report_output = subprocess.run(
        ["uv", "run", "coverage", "report", "-m"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
      )

      if cov_report_output.stderr:
        return dumps({
          "operation": "run_coverage",
          "output": f"{cov_report_output.stderr} - (cov_report_output)"
        })

      output = dedent(f"""
        Execution output:\n
        {cov_run_output}
        \n\n
        Report output:\n
        {cov_report_output}
      """)
    except Exception as e:
      logger.error(f"Error running `coverage`: {e}")

    return dumps({
      "operation": "run_coverage",
      "output": output
    })
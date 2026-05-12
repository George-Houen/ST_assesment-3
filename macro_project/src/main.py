import config
import services.dataset_indexer as di
import services.eda_service as eda
from services.workflow_service import WorkflowService
import macro_project.src.macro_app as macro_app

def main() -> None:
  """Run the default non-interactive project workflow."""

  workflow = WorkflowService()
  workflow.run_full_pipeline()

if __name__ == "__main__":
  macro_app.App().mainloop()

import sys
import os
from pathlib import Path

# #region agent log
print("[DEBUG] api/index.py loading...")
print(f"[DEBUG] __file__: {__file__}")
print(f"[DEBUG] cwd: {os.getcwd()}")
# #endregion

# Add the backend directory to Python path
backend_path = Path(__file__).parent.parent / "backend"
# #region agent log
print(f"[DEBUG] backend_path: {backend_path}")
print(f"[DEBUG] backend_path exists: {backend_path.exists()}")
print(f"[DEBUG] sys.path before: {sys.path[:3]}")
# #endregion
sys.path.insert(0, str(backend_path))
# #region agent log
print(f"[DEBUG] sys.path after: {sys.path[:3]}")
# #endregion

try:
    # #region agent log
    print("[DEBUG] Attempting to import app.main...")
    # #endregion
    from app.main import app
    # #region agent log
    print("[DEBUG] Successfully imported app.main!")
    # #endregion
except Exception as e:
    # #region agent log
    print(f"[DEBUG] FAILED to import app.main: {e}")
    import traceback
    traceback.print_exc()
    # #endregion
    raise

# Use Mangum to wrap FastAPI for serverless
from mangum import Mangum

# #region agent log
print("[DEBUG] Creating Mangum handler...")
# #endregion
handler = Mangum(app)
# #region agent log
print("[DEBUG] Mangum handler created successfully!")

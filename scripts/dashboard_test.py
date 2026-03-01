import sys
try:
    import dashboard
    print("Dashboard imported successfully")
except Exception as e:
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Parking Space Detection (YOLO + Streamlit)

## Files (all in the ROOT of your GitHub repo)
- `app.py`
- `requirements.txt`
- `packages.txt`
- `best.pt`  (rename your uploaded `best__2_.pt` to exactly `best.pt`)

## Upload to GitHub
1. Go to github.com -> **New repository** (Public) -> Create.
2. Click **Add file -> Upload files**, drag in the 4 files above, click **Commit changes**.
   (best.pt is ~6 MB, so the web uploader works fine.)

## Deploy on Streamlit Community Cloud
1. Go to share.streamlit.io and sign in with GitHub.
2. Click **Create app** -> choose your repo, branch `main`, main file `app.py`.
3. Click **Deploy**. The first build takes a few minutes.

## Troubleshooting
- Error loading `best.pt`: the file name must be exactly `best.pt`, in the repo root.
- OpenCV/`libGL` import error: make sure `packages.txt` and `opencv-python-headless` are present.
- After editing requirements, use **Manage app -> Reboot app**.
- Empty/Occupied counts show 0? The app matches class names (empty/free/vacant, occupied/busy/car).
  Check the "Model classes" line under the results.
